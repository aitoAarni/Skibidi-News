import re
import os, json, math, random, asyncio, uuid, time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple, Optional
from _client import client as _client


PROMPT_JUDGE_SYSTEM_PROMPT = open("judge_prompt.txt").read()
MODEL = os.getenv("MODEL_NAME") or "gpt-4o-mini"
if not MODEL:
    raise ValueError("MODEL_NAME not set.")

@dataclass
class PromptPack:
    prompt_id: str
    safety_profile: str
    style: str
    angle: str
    structure: str
    devices: List[str]
    word_cap: int
    receipts_target: int
    writer_system: str
    writer_user_template: str
    few_shots: List[Dict[str, str]] | None = None
    decode_prefs: Dict[str, Any] | None = None
    audit: Dict[str, Any] | None = None
    eval_checks: List[str] | None = None
    elo: float = 1000.0
    wins: int = 0
    losses: int = 0


@dataclass
class InputItem:
    prompt: str
    summary: str


@dataclass
class MatchResult:
    a_id: str
    b_id: str
    winner_id: str
    confidence: float
    input_idx: int


@dataclass
class Generation:
    pack_id: str
    text: str
    meta: Dict[str, Any]


def fill_user_template(pack: PromptPack, item: InputItem) -> str:
    return pack.writer_user_template.replace("{{prompt}}", item.prompt).replace(
        "{{summary}}", item.summary
    )


def shortlist(packs: List[PromptPack], survivors: int) -> List[PromptPack]:
    return sorted(packs, key=lambda p: p.elo, reverse=True)[:survivors]


def k_factor(elo: float) -> float:
    if elo < 1200:
        return 40.0
    if elo < 1500:
        return 24.0
    if elo < 1800:
        return 16.0
    return 12.0


def elo_update(a: PromptPack, b: PromptPack, winner_id: str, conf: float = 0.7):
    if not a.elo:
        Ra = 1000.0
    else:
        Ra = a.elo

    if not b.elo:
        Rb = 1000.0
    else:
        Rb = b.elo

    if not b.wins:
        b.wins = 0

    if not b.losses:
        b.losses = 0

    if not a.wins:
        a.wins = 0

    if not a.losses:
        a.losses = 0

    Ea = 1.0 / (1.0 + 10 ** ((Rb - Ra) / 400))
    Eb = 1.0 / (1.0 + 10 ** ((Ra - Rb) / 400))
    Ka, Kb = k_factor(Ra), k_factor(Rb)
    Sa, Sb = (1.0, 0.0) if winner_id == a.prompt_id else (0.0, 1.0)
    w = max(0.0, min(1.0, (conf - 0.5) / 0.5))
    a.elo = Ra + Ka * w * (Sa - Ea)
    b.elo = Rb + Kb * w * (Sb - Eb)
    if winner_id == a.prompt_id:
        a.wins += 1
        b.losses += 1
    else:
        b.wins += 1
        a.losses += 1


def mutate(pack: PromptPack, p: float = 0.25) -> PromptPack:
    new = PromptPack(**asdict(pack))
    new.prompt_id = f"{pack.prompt_id}-m{str(uuid.uuid4())[:4]}"
    if random.random() < p and new.decode_prefs:
        new.decode_prefs["temperature"] = round(
            min(
                1.2,
                max(
                    0.2,
                    (new.decode_prefs.get("temperature"))
                    + random.choice([-0.2, -0.1, 0.1, 0.2]),
                ),
            ),
            2,
        )
    if random.random() < p:
        new.word_cap = random.choice([60, 140, new.word_cap])

    if random.random() < p:
        alt = [
            "Setup→Turn→Tag",
            "Rule of Three",
            "Angle–Example–Zinger",
            "Thesis→3 Receipts→Kicker",
        ]
        alt.remove(new.structure) if new.structure in alt else None
        new.structure = random.choice(alt)

    new.elo = max(
        900.0, new.elo - 50.0
    )

    new.wins = new.losses = 0
    return new


async def call_writer(pack: PromptPack, item: InputItem) -> Generation:
    user = fill_user_template(pack, item)
    print(user)
    messages = [{"role": "system", "content": pack.writer_system}]
    if pack.few_shots:
        for ex in pack.few_shots:
            messages.append({"role": "user", "content": f"SUMMARY: {ex['summary']}"})
            messages.append({"role": "assistant", "content": ex["output"]})

    messages.append({"role": "user",
        "content": user
        })

    dp = pack.decode_prefs or {}
    temperature = float(dp.get("temperature", 0.6))
    top_p = float(dp.get("top_p", 0.9))
    try:
        if _client:
            resp = await _client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=1200,
            )
            text = (resp.choices[0].message.content or "").strip()
        else:
            text = "Stub: elevator silence meets weather report. (parody)"

    except Exception as e:
        text = f"Stub due to error: {e}"

    return Generation(
        pack_id=pack.prompt_id,
        text=text,
        meta={"temperature": temperature, "top_p": top_p},
    )


async def call_judge(
    judge_system: str, 
    a_text: str,
    b_text: str, 
    summary: str
) -> Tuple[str, float]:
    user = (
        f"SUMMARY:\n{summary}\n\nA:\n{a_text}\n\nB:\n{b_text}\n\nReturn strictly JSON."
    )
    try:
        if _client:
            resp = await _client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": judge_system},
                    {"role": "user", "content": user},
                ],
                temperature=0.0,
                max_tokens=60,
                response_format={"type": "json_object"},
            )
            raw = (resp.choices[0].message.content or "").strip()
        else:
            raw = json.dumps(
                {
                    "winner": "A" if len(a_text) >= len(b_text) else "B",
                    "confidence": 0.6,
                }
            )

        obj = json.loads(raw)
        return obj.get("winner", "A"), float(obj.get("confidence", 0.6))
    except Exception:
        return ("A" if len(a_text) < len(b_text) else "B"), 0.55


async def tournament(
    packs: List[PromptPack],
    inputs: List[InputItem],
    iterations: int = 3,
    samples_per_input: int = 2,
    pairings: int = 1,
    survivors: int = 6,
    mutants_per_survivor: int = 1,
    logdir: str = "opt_logs",
):
    os.makedirs(logdir, exist_ok=True)
    judge_system = PROMPT_JUDGE_SYSTEM_PROMPT

    for it in range(iterations):
        round_log = []
        gens: Dict[Tuple[int, str], Generation] = {}
        for i, item in enumerate(inputs):
            chosen = random.sample(packs, min(samples_per_input, len(packs)))
            results = await asyncio.gather(*[call_writer(p, item) for p in chosen])
            for g in results:
                gens[(i, g.pack_id)] = g

        matches: List[MatchResult] = []
        for i, item in enumerate(inputs):
            cand = [p for p in packs if (i, p.prompt_id) in gens]
            if len(cand) < 2:
                continue
            for _ in range(pairings):
                a, b = random.sample(cand, 2)
                ga, gb = gens[(i, a.prompt_id)], gens[(i, b.prompt_id)]
                winner, conf = await call_judge(
                    judge_system, ga.text, gb.text, item.summary
                )
                win_id = a.prompt_id if winner == "A" else b.prompt_id
                matches.append(
                    MatchResult(
                        a_id=a.prompt_id,
                        b_id=b.prompt_id,
                        winner_id=win_id,
                        confidence=conf,
                        input_idx=i,
                    )
                )
                elo_update(a, b, win_id, conf)
                round_log.append(
                    {
                        "iter": it,
                        "input_idx": i,
                        "a": {"id": a.prompt_id, "elo": a.elo, "text": ga.text},
                        "b": {"id": b.prompt_id, "elo": b.elo, "text": gb.text},
                        "winner": winner,
                        "confidence": conf,
                    }
                )

        packs = shortlist(packs, survivors)
        new_mutants = []
        for p in packs:
            for _ in range(mutants_per_survivor):
                new_mutants.append(mutate(p))
        packs.extend(new_mutants)

        with open(os.path.join(logdir, f"round_{it}.jsonl"), "w") as f:
            for row in round_log:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        with open(os.path.join(logdir, f"leaderboard_iter_{it}.json"), "w") as f:
            f.write(
                json.dumps(
                    [
                        asdict(p)
                        for p in sorted(packs, key=lambda x: x.elo, reverse=True)
                    ],
                    ensure_ascii=False,
                    indent=2,
                )
            )

    final = sorted(packs, key=lambda p: p.elo, reverse=True)
    with open(os.path.join(logdir, "leaderboard_final.json"), "w") as f:
        f.write(json.dumps([asdict(p) for p in final], ensure_ascii=False, indent=2))
    return final



def _coerce_pack_defaults(p: PromptPack) -> PromptPack:
    if p.elo is None or not isinstance(p.elo, (int, float)):
        p.elo = 1000.0
    if p.wins is None or not isinstance(p.wins, int):
        p.wins = 0
    if p.losses is None or not isinstance(p.losses, int):
        p.losses = 0
    if p.decode_prefs is None:
        p.decode_prefs = {"temperature": 0.6, "top_p": 0.9}
    else:
        p.decode_prefs.setdefault("temperature", 0.6)
        p.decode_prefs.setdefault("top_p", 0.9)
    return p



async def main():
    packs_raw = json.load(open("variants.json"))
    packs = [_coerce_pack_defaults(PromptPack(**p)) for p in packs_raw]

    inputs = [
        InputItem(
            prompt="Make a witty short about elevator small talk.",
            summary="People feel awkward in elevators; ~30 seconds; silence vs forced chat; doors ding; everyone stares ahead.",
        ),
        InputItem(
            prompt="Short caption on startup feature creep.",
            summary="Startup adds 5 new toggles to reduce confusion; users are more confused; PM writes a memo.",
        ),
    ]

    final = await tournament(
        packs=packs,
        inputs=inputs,
        iterations=3,
        samples_per_input=2,
        pairings=1,
        survivors=8,
        mutants_per_survivor=1,
        logdir="opt_logs",
    )

    print("Top 5:")
    for p in final[:5]:
        print(p.prompt_id, round(p.elo), p.style, p.structure)


if __name__ == "__main__":
    asyncio.run(main())
