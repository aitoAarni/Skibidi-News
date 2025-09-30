from __future__ import annotations
import os, json, asyncio
from dataclasses import asdict
from typing import List
from _optimizer import PromptPack, InputItem, tournament
from _prompt_factory import ask_prompt_generator, Request

TARGET_ELO = float(os.getenv("TARGET_ELO", "1500"))
TARGET_WINS = int(os.getenv("TARGET_WINS", "20"))
LIBRARY_PATH = os.getenv("LIBRARY_PATH", "variants.json")
LEADERBOARD_PATH = os.getenv("LEADERBOARD_PATH", "opt_logs/leaderboard_final.json")

import json, uuid
from typing import List, Dict, Any

def load_json_or_ndjson(path: str) -> List[Dict[str, Any]]:
    try:
        txt = open(path, "r", encoding="utf-8").read().strip()
    except FileNotFoundError:
        return []
    if not txt:
        return []

    try:
        obj = json.loads(txt)
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            return [obj]
    except Exception:
        pass

    out: List[Dict[str, Any]] = []
    for ln in txt.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except Exception:
            # ignore bad lines
            continue
    return out

def ensure_prompt_pack_defaults(p: Dict[str, Any]) -> Dict[str, Any]:
    p = dict(p)
    p.setdefault("prompt_id", f"pp-{str(uuid.uuid4())[:8]}")
    p.setdefault("safety_profile", "standard")
    p.setdefault("style", "satirical")
    p.setdefault("angle", "Compare/Contrast")
    p.setdefault("structure", "Setup→Turn→Tag")
    p.setdefault("devices", ["Irony"])
    p.setdefault("word_cap", 60)
    p.setdefault("receipts_target", 2)
    p.setdefault("writer_system",
        "You are a concise comedy writer. Preserve supplied facts; do not invent. "
        "Think internally; do not show reasoning. Output 1–4 sentences, clear setup and punch. "
        "If facts conflict, switch to (parody)."
    )
    p.setdefault("writer_user_template",
        "PROMPT: {{prompt}}\nSUMMARY: {{summary}}\n"
        "TASK: Write a short caption (≤60 words) using Setup→Turn→Tag. "
        "Include up to 2 brief receipts only from SUMMARY. Output plain text only."
    )
    p.setdefault("few_shots", [])
    dp = p.get("decode_prefs") or {}
    dp.setdefault("temperature", 0.6)
    dp.setdefault("top_p", 0.9)
    p["decode_prefs"] = dp
    p["elo"] = float(p.get("elo") or 1000.0)
    p["wins"] = int(p.get("wins") or 0)
    p["losses"] = int(p.get("losses") or 0)
    return p


def _packs_from_dicts(items: List[dict]) -> List[PromptPack]:
    return [PromptPack(**ensure_prompt_pack_defaults(p)) for p in items]

async def bootstrap_if_needed() -> List[PromptPack]:
    items = load_json_or_ndjson(LIBRARY_PATH)
    if items:
        return _packs_from_dicts(items)
    req = Request(
        prompt="Make a witty short about elevator small talk.",
        summary="People feel awkward in elevators; ~30 seconds; silence vs forced chat; doors ding; everyone stares ahead.",
    )
    fresh = await ask_prompt_generator(req, n=12)
    packs = _packs_from_dicts(fresh)

    os.makedirs(os.path.dirname(LIBRARY_PATH) or ".", exist_ok=True)
    with open(LIBRARY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(json.dumps(asdict(p), ensure_ascii=False) for p in packs))
    return packs

def _inputs() -> List[InputItem]:
    return [
        InputItem(
            prompt="Make a witty short about elevator small talk.",
            summary="People feel awkward in elevators; ~30 seconds; silence vs forced chat; doors ding; everyone stares ahead.",
        ),
        InputItem(
            prompt="Short caption on startup feature creep.",
            summary="Startup adds 5 new toggles to reduce confusion; users are more confused; PM writes a memo.",
        ),
        InputItem(
            prompt="Caption about online meeting chaos.",
            summary="Team joins call; half on mute; someone echoes; deck won’t load; meeting runs long.",
        ),
        InputItem(
            prompt="Joke about gym resolutions in January.",
            summary="Crowded gym in Jan; by March it’s empty except one guy filming squats.",
        ),
        InputItem(
            prompt="Short roast about corporate jargon.",
            summary="CEO email: 'synergy', 'leverage', 'circle back'; employees roll eyes.",
        ),
    ]

async def overnight_run():
    packs = await bootstrap_if_needed()
    inputs = _inputs()

    round_no = 0
    while True:
        round_no += 1
        print(f"=== Round {round_no} ===")

        packs = await tournament(
            packs=packs,
            inputs=inputs,
            iterations=3,
            samples_per_input=3,
            pairings=2,
            survivors=8,
            mutants_per_survivor=1,
            logdir="opt_logs",
        )

        os.makedirs(os.path.dirname(LIBRARY_PATH) or ".", exist_ok=True)
        os.makedirs(os.path.dirname(LEADERBOARD_PATH) or ".", exist_ok=True)
        with open(LIBRARY_PATH, "w", encoding="utf-8") as f:
            json.dump([asdict(p) for p in packs], f, ensure_ascii=False, indent=2)
        with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
            json.dump([asdict(p) for p in packs], f, ensure_ascii=False, indent=2)

        best = packs[0]
        print(f"Top: {best.prompt_id} elo={best.elo:.1f} wins={best.wins} losses={best.losses}")

        if best.elo >= TARGET_ELO and best.wins >= TARGET_WINS:
            print("🎉 Target reached. Stopping.")
            break

if __name__ == "__main__":
    asyncio.run(overnight_run())
