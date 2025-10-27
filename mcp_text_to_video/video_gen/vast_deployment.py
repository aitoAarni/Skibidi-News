#!/usr/bin/env python3
"""
Vast.ai lifecycle + WAN2S2V deployment/inference
- Picks a cheap H200 offer
- Creates instance from TEMPLATE_HASH (preferred) or DOCKER_IMAGE_DEFAULT fallback
- Fetches external port mapped to 7861/tcp
- Waits for /health to be OK
- Can POST your audio to /s2v
"""

import os
import sys
import time
import json
import logging
import subprocess
import argparse
import re
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
LOG = logging.getLogger("vast-wan")

VAST_API_KEY = os.getenv("VAST_API_KEY")
BASE_URL = os.getenv("VAST_BASE_URL", "https://console.vast.ai/api/v0")
DOCKER_IMAGE_DEFAULT = os.getenv(
    "DOCKER_IMAGE_DEFAULT", "ghcr.io/astranero/wan2s2v:latest"
)
TEMPLATE_HASH = os.getenv("TEMPLATE_HASH", "")  # <-- fixed typo here
CONTAINER_PORT = int(os.getenv("CONTAINER_PORT", "7861"))
HEALTH_PATH = os.getenv("HEALTH_PATH", "/health")
HEALTH_TIMEOUT = int(os.getenv("HEALTH_TIMEOUT", "900"))

if not VAST_API_KEY:
    sys.exit("Please set VAST_API_KEY in environment (or .env)")

CURL_BASE = [
    "curl",
    "-4",
    "--silent",
    "--show-error",
    "--fail",
    "--connect-timeout",
    "20",
    "--header",
    f"Authorization: Bearer {VAST_API_KEY}",
    "--header",
    "Content-Type: application/json",
]

os.environ.update(
    {k: "" for k in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy")}
)
os.environ.update({"NO_PROXY": "*", "no_proxy": "*"})


@dataclass
class Offer:
    id: int
    dph: float
    gpu_name: str
    vram_gib: float
    verified: bool


def run_curl(args: List[str]) -> str:
    res = subprocess.run(CURL_BASE + args, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip() or res.stdout.strip())
    return res.stdout.strip()


def curl_json(args: List[str]) -> Any:
    out = run_curl(args)
    return json.loads(out or "{}")


def list_offers() -> List[Offer]:
    LOG.info("Fetching verified on-demand offers via /search/asks ...")
    query = {
        "select_cols": ["*"],
        "q": {
            "verified": {"eq": True},
            "rentable": {"eq": True},
            "external": {"eq": False},
            "rented": {"eq": False},
            "order": [["dph_total", "asc"]],
            "type": "on-demand",
            "limit": 50,
        },
    }
    data = curl_json(
        ["--request", "PUT", "--data", json.dumps(query), f"{BASE_URL}/search/asks/"]
    )
    offers = []
    for b in data.get("offers", []):
        offers.append(
            Offer(
                id=int(b["id"]),
                dph=float(b.get("dph_total", 0)),
                gpu_name=str(b.get("gpu_name", "")).upper(),
                vram_gib=float(b.get("gpu_total_ram", b.get("gpu_ram", 0))),
                verified=bool(b.get("verified", True)),
            )
        )
    LOG.info("Found %d verified offers", len(offers))
    return offers


def pick_cheapest_h200(offers: List[Offer]) -> Optional[Offer]:
    cands = [o for o in offers if "H200" in o.gpu_name and o.vram_gib >= 138]
    return min(cands, key=lambda o: o.dph) if cands else None


def create_instance(
    offer_id: int,
    template_hash: Optional[str] = None,
    disk_gb: int = 120,
    image: Optional[str] = None,
) -> int:
    """
    Preferred: pass template_hash (or set env TEMPLATE_HASH)
    Fallback: specify image and minimal runtime config
    """
    template_hash = template_hash or TEMPLATE_HASH
    if template_hash:
        payload = {
            "template_hash_id": template_hash,
            "disk": disk_gb,
            "target_state": "running",
            "label": "wan2s2v-h200",
        }
    else:
        img = image or DOCKER_IMAGE_DEFAULT
        payload = {
            "image": img,
            "disk": disk_gb,
            "target_state": "running",
            "label": "wan2s2v-h200",
            "ports": {f"{CONTAINER_PORT}/tcp": CONTAINER_PORT},
        }

    data = curl_json(
        [
            "--request",
            "PUT",
            "--data",
            json.dumps(payload),
            f"{BASE_URL}/asks/{offer_id}/",
        ]
    )
    if not data.get("success"):
        raise RuntimeError(f"Failed to create instance: {data}")
    new_id = data.get("new_contract")
    LOG.info("Created instance %s", new_id)
    return new_id


def get_instance(instance_id: int) -> Dict[str, Any]:
    data = curl_json(["--get", f"{BASE_URL}/instances/{instance_id}/"])
    return data.get("instances", data)


def parse_external_port(
    inst: Dict[str, Any], internal: int, proto: str = "tcp"
) -> Optional[int]:
    """
    Try common shapes Vast uses to represent port mappings.
    """
    ports = inst.get("ports")
    if isinstance(ports, dict):
        key = f"{internal}/{proto}"
        if key in ports:
            try:
                return int(ports[key])
            except Exception:
                pass

    for key in ("port_mapping", "port_map", "ports_list", "port_list"):
        lst = inst.get(key)
        if isinstance(lst, list):
            for p in lst:
                try:
                    if (
                        int(p.get("internal")) == internal
                        and str(p.get("proto", "tcp")).lower() == proto
                    ):
                        ext = (
                            p.get("external")
                            or p.get("external_port")
                            or p.get("public")
                        )
                        if ext is not None:
                            return int(ext)
                except Exception:
                    continue

    for key in ("ip_port_info", "public_ports", "port_status"):
        s = inst.get(key)
        if isinstance(s, str):
            m = re.search(r"(?P<ext>\d+)\s*->\s*%d/%s" % (internal, proto), s)
            if m:
                return int(m.group("ext"))

    return None


def wait_instance_ready(instance_id: int, timeout: int = 900) -> Dict[str, Any]:
    LOG.info("Waiting for instance #%s to become 'running' with IP...", instance_id)
    t0 = time.time()
    while True:
        inst = get_instance(instance_id)
        state = inst.get("actual_status") or inst.get("cur_state")
        ip = inst.get("public_ipaddr")
        if state == "running" and ip:
            LOG.info("Instance running at %s", ip)
            return inst
        if time.time() - t0 > timeout:
            raise TimeoutError("Timeout waiting for instance to be ready")
        time.sleep(4)


def wait_port_and_health(
    ip: str, inst: Dict[str, Any], internal_port: int, timeout: int = HEALTH_TIMEOUT
) -> int:
    """
    Wait until Vast publishes an external port mapping for internal_port, then poll /health.
    Returns the external port number.
    """
    LOG.info("Waiting for external port mapping for %d/tcp ...", internal_port)
    t0 = time.time()
    ext_port: Optional[int] = None

    while True:
        ext_port = parse_external_port(inst, internal_port)
        if ext_port:
            LOG.info("Mapped %d/tcp -> %d", internal_port, ext_port)
            break
        if time.time() - t0 > timeout:
            raise TimeoutError("Timeout waiting for external port mapping")
        time.sleep(3)
        inst = get_instance(int(inst.get("id") or inst.get("contract_id") or 0))

    LOG.info("Probing http://%s:%d%s ...", ip, ext_port, HEALTH_PATH)
    t1 = time.time()
    while True:
        try:
            with urllib.request.urlopen(
                f"http://{ip}:{ext_port}{HEALTH_PATH}", timeout=5
            ) as resp:
                if resp.status == 200:
                    LOG.info("Health OK")
                    return ext_port
        except urllib.error.URLError:
            pass

        if time.time() - t1 > timeout:
            raise TimeoutError("Timeout waiting for /health to become ready")
        time.sleep(2)


def destroy_instance(instance_id: int):
    try:
        run_curl(["--request", "DELETE", f"{BASE_URL}/instances/{instance_id}/"])
        LOG.info("Instance #%s destroyed", instance_id)
    except Exception as e:
        LOG.warning("Destroy failed: %s", e)


def run_remote_inference(ip: str, port: int, prompt: str) -> str:
    cmd = [
        "curl",
        "-sS",
        "-X",
        "POST",
        f"http://{ip}:{port}/s2v",
        "-F",
        f"prompt={prompt}",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr or res.stdout)
    return res.stdout.strip()


# ---------- CLI ----------
def cli():
    ap = argparse.ArgumentParser(description="Run WAN2S2V on Vast.ai")
    ap.add_argument("--prompt", required=True, help="Text prompt")
    ap.add_argument(
        "--template-hash", default=TEMPLATE_HASH, help="Vast template hash to use"
    )
    ap.add_argument(
        "--image",
        default=DOCKER_IMAGE_DEFAULT,
        help="Fallback image if no template is provided",
    )
    ap.add_argument(
        "--keep", action="store_true", help="Keep instance running after inference"
    )
    args = ap.parse_args()

    instance_id = None
    try:
        offers = list_offers()
        offer = pick_cheapest_h200(offers)
        if not offer:
            raise RuntimeError("No rentable H200 offers found")

        instance_id = create_instance(
            offer.id, template_hash=args.template_hash, image=args.image
        )
        inst = wait_instance_ready(instance_id)
        ip = inst.get("public_ipaddr")
        ext_port = wait_port_and_health(ip, inst, CONTAINER_PORT)

        LOG.info("Public endpoint: http://%s:%d", ip, ext_port)
        LOG.info("Try: curl -sS http://%s:%d/health", ip, ext_port)

        out = run_remote_inference(ip, ext_port, args.prompt)
        print(out)

    finally:
        if instance_id and not args.keep:
            destroy_instance(instance_id)


if __name__ == "__main__":
    cli()
