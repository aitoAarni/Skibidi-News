from __future__ import annotations
from typing import Dict, Any, Optional
import logging
import os

from wan_deploy_vast import (
    list_offers,
    pick_cheapest_h200,
    create_instance,
    wait_instance_ready,
    wait_port_and_health,
    run_remote_inference,
    destroy_instance,
    DOCKER_IMAGE_DEFAULT,
)

LOG = logging.getLogger("mcp-audio-to-video")
logging.basicConfig(level=logging.INFO)

# Defaults (can be overridden by env)
CONTAINER_PORT = int(os.getenv("CONTAINER_PORT", "7861"))
DEFAULT_TEMPLATE_HASH = os.getenv("TEMPLATE_HASH", "")


def health() -> Dict[str, Any]:
    """Basic health check."""
    return {"status": "ok", "service": "mcp-audio-to-video"}


def run_inference_vast(
    prompt: str = "A cat playing piano",
    image: str = DOCKER_IMAGE_DEFAULT,
    template_hash: Optional[str] = DEFAULT_TEMPLATE_HASH,
    keep: bool = False,
) -> Dict[str, Any]:
    """
    Deploy WAN2S2V on Vast.ai and run inference with provided audio.
    - Picks cheapest verified H200
    - Creates from template if provided, else falls back to image
    - Resolves external port mapped to container 7861/tcp
    - Waits for /health before sending work
    """
    instance_id = None
    try:
        offers = list_offers()
        offer = pick_cheapest_h200(offers)
        if not offer:
            raise RuntimeError("No H200 offers available")

        instance_id = create_instance(
            offer.id,
            template_hash=template_hash or None,
            image=image if not template_hash else None,
        )

        inst = wait_instance_ready(instance_id)
        ip = inst.get("public_ipaddr")
        if not ip:
            raise RuntimeError("Instance has no public_ipaddr")

        # Find external port for 7861/tcp and wait for /health
        ext_port = wait_port_and_health(ip, inst, CONTAINER_PORT)
        public_url = f"http://{ip}:{ext_port}"
        LOG.info(f"🌐 API available at: {public_url}")

        output_json = run_remote_inference(ip, ext_port, prompt)
        return {
            "success": True,
            "instance_id": instance_id,
            "endpoint": public_url,
            "output": output_json,
            "kept_running": keep,
        }

    except Exception as e:
        LOG.exception("Inference failed")
        return {"success": False, "error": str(e), "instance_id": instance_id}
    finally:
        if instance_id and not keep:
            try:
                destroy_instance(instance_id)
            except Exception as e:
                LOG.warning("Failed to destroy instance %s: %s", instance_id, e)
