# mcp_prompt_opt/server.py
from __future__ import annotations
import os, json, asyncio, uuid
from typing import List, Dict, Any, Optional
from dataclasses import asdict
import logging

from mcp.server.fastmcp import FastMCP

from _prompt_factory import ask_prompt_generator, Request
from _optimizer import PromptPack, InputItem, tournament

logger = logging.getLogger("mcp-prompt-opt")
logging.basicConfig(level=logging.INFO)

app = FastMCP("mcp-prompt-opt")

LIBRARY_PATH = os.getenv("PROMPT_LIBRARY", "variants.json")
LEADERBOARD_PATH = os.getenv("PROMPT_LEADERBOARD", "opt_logs/leaderboard_final.json")
FAST_ITERATIONS = int(os.getenv("FAST_ITERATIONS", "1"))
FAST_SAMPLES = int(os.getenv("FAST_SAMPLES_PER_INPUT", "2"))
FAST_PAIRINGS = int(os.getenv("FAST_PAIRINGS", "1"))
FAST_SURVIVORS = int(os.getenv("FAST_SURVIVORS", "8"))
FAST_MUTANTS = int(os.getenv("FAST_MUTANTS_PER_SURVIVOR", "1"))


# ---------------- util ----------------
def _load_variants(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []

    txt = open(path).read().strip()
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
    out = []

    for line in txt.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except:
            continue
    return out


def _load_leaderboard(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        return json.load(open(path))
    except Exception:
        return []


def _packs_from_json(arr: List[Dict[str, Any]]) -> List[PromptPack]:
    out = []
    for p in arr:
        keep = {
            k: p.get(k)
            for k in [
                "prompt_id",
                "safety_profile",
                "style",
                "angle",
                "structure",
                "devices",
                "word_cap",
                "receipts_target",
                "writer_system",
                "writer_user_template",
                "few_shots",
                "decode_prefs",
                "audit",
                "eval_checks",
                "elo",
                "wins",
                "losses",
            ]
        }

        keep["prompt_id"] = keep["prompt_id"] or f"pp-{str(uuid.uuid4())[:8]}"
        keep["elo"] = keep.get("elo", 1000.0)
        keep["wins"] = keep.get("wins", 0)
        keep["losses"] = keep.get("losses", 0)
        out.append(PromptPack(**keep))
    return out


def _best_ready(packs: List[PromptPack]) -> Optional[PromptPack]:
    candidates = [p for p in packs if (p.wins + p.losses) >= 12]
    if not candidates:
        candidates = packs
    if not candidates:
        return None
    return sorted(candidates, key=lambda x: (x.elo, x.wins - x.losses), reverse=True)[0]


def _default_inputs() -> List[InputItem]:
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
            summary="Team joins video call; half are on mute; someone echoes; slide deck doesn’t load; meeting runs long.",
        ),
        InputItem(
            prompt="Joke about gym resolutions in January.",
            summary="Crowded gym in January; everyone signs up; by March, machines are empty except one guy filming squats.",
        ),
        InputItem(
            prompt="Short roast about corporate jargon.",
            summary="CEO email full of phrases like 'synergy', 'leverage', 'circle back'; employees roll eyes.",
        ),
        InputItem(
            prompt="Funny caption about procrastination.",
            summary="Deadline looms; person cleans desk, alphabetizes pens, watches 3 tutorials on productivity instead of working.",
        ),
        InputItem(
            prompt="Observational gag on airline boarding.",
            summary="Passengers crowd gate before boarding group; overhead bins fill; middle seat panic ensues.",
        ),
        InputItem(
            prompt="Satirical take on diet trends.",
            summary="New diet bans carbs, then fruit, then fun; influencer posts confusing meal plan.",
        ),
        InputItem(
            prompt="Witty remark on smart home devices.",
            summary="Smart fridge suggests expired kale smoothie; speaker mishears 'play jazz' as 'order 6 pizzas'.",
        ),
        InputItem(
            prompt="Comedic take on group projects.",
            summary="Group of 5; 1 does all the work; 2 argue about font; 2 vanish until submission.",
        ),
    ]


async def _quick_opt(
    packs: List[PromptPack],
    inputs: List[InputItem],
    gen_more: bool,
    seed_prompt: str,
    seed_summary: str,
    n_new: int = 8,
) -> List[PromptPack]:
    """Optionally generate a few challengers, then run a short tournament."""
    base = [*packs]

    if gen_more:
        req = Request(prompt=seed_prompt, summary=seed_summary)
        new = await ask_prompt_generator(req, n=n_new)
        base.extend(_packs_from_json(new))

    final = await tournament(
        packs=base,
        inputs=inputs,
        iterations=FAST_ITERATIONS,
        samples_per_input=FAST_SAMPLES,
        pairings=FAST_PAIRINGS,
        survivors=FAST_SURVIVORS,
        mutants_per_survivor=FAST_MUTANTS,
        logdir="opt_logs",
    )

    return final


@app.tool()
def health() -> Dict[str, Any]:
    """Basic health + library stats."""
    lib = _packs_from_json(_load_variants(LIBRARY_PATH))
    lb = _packs_from_json(_load_leaderboard(LEADERBOARD_PATH))
    total = len(lib) or len(lb)
    return {"name": "mcp-prompt-opt", "library_prompts": total, "status": "ok"}


@app.tool()
def best_prompt(
    prompt: str, summary: str, allow_quick_opt: bool = True
) -> Dict[str, Any]:
    """
    Fast path: return the best available prompt pack for (prompt, summary).
    If allow_quick_opt=True and no confident winner exists, run a tiny optimize pass.
    Returns: {"prompt_pack": {...}, "note": str}
    """
    raw = _load_leaderboard(LEADERBOARD_PATH)
    if not raw:
        raw = _load_variants(LIBRARY_PATH)
    packs = _packs_from_json(raw)

    if not packs:
        return {
            "error": "No prompt library found. Generate variants first (variants.json or leaderboard)."
        }

    champ = _best_ready(packs)
    if champ and (champ.wins + champ.losses) >= 15 and champ.elo >= 1050:
        return {"prompt_pack": asdict(champ), "note": "selected_from_library"}

    if not allow_quick_opt:
        return {
            "prompt_pack": asdict(champ),
            "note": "selected_from_library_low_confidence",
        }

    inputs = _default_inputs()
    final_packs = asyncio.run(
        _quick_opt(
            packs,
            inputs,
            gen_more=True,
            seed_prompt=prompt,
            seed_summary=summary,
            n_new=6,
        )
    )
    best = final_packs[0]
    return {"prompt_pack": asdict(best), "note": "quick_optimized"}


@app.tool()
def optimize(
    prompt: str,
    summary: str,
    n_new: int = 12,
    iterations: int = 2,
    samples_per_input: int = 2,
    pairings: int = 1,
) -> Dict[str, Any]:
    """
    On-demand quick optimization for this (prompt, summary).
    Generates n_new challengers and runs a compact tournament over a small input set.
    Returns best prompt pack + lightweight leaderboard.
    """
    base_raw = _load_leaderboard(LEADERBOARD_PATH)
    if not base_raw:
        base_raw = _load_variants(LIBRARY_PATH)
    packs = _packs_from_json(base_raw)

    req = Request(prompt=prompt, summary=summary)
    new = asyncio.run(ask_prompt_generator(req, n=n_new))
    packs.extend(_packs_from_json(new))

    inputs = _default_inputs()
    final = asyncio.run(
        tournament(
            packs=packs,
            inputs=inputs,
            iterations=iterations,
            samples_per_input=samples_per_input,
            pairings=pairings,
            survivors=max(8, min(16, len(packs) // 2)),
            mutants_per_survivor=1,
            logdir="opt_logs",
        )
    )

    best = final[0]
    board = [
        {"prompt_id": p.prompt_id, "elo": p.elo, "wins": p.wins, "losses": p.losses}
        for p in final[:10]
    ]
    return {"best": asdict(best), "leaderboard_top10": board}


def main():
    app.run()


if __name__ == "__main__":
    main()
