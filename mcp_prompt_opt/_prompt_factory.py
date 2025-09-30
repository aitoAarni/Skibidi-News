import os, json, uuid, asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

load_dotenv()
from agents import Agent, OpenAIChatCompletionsModel, Runner

from mcp_prompt_opt._client import client

MODEL = os.getenv("MODEL_NAME") or "gpt-4o-mini"
if not MODEL:
    raise ValueError("MODEL_NAME not set.")

PROMPT_GENERATOR_SYSTEM_PROMPT = open("meta_system.txt").read()

@dataclass
class Request:
    prompt: str
    summary: str


REQUIRED_FIELDS = {
    "safety_profile", "style", "angle", "structure", "devices",
    "word_cap", "receipts_target", "writer_system", "writer_user_template"
}


def _ensure_id(obj: Dict[str, Any]) -> Dict[str, Any]:
    obj.setdefault("prompt_id", str(uuid.uuid4())[:8])
    return obj


def _valid_pack(obj: Dict[str, Any]) -> bool:
    return isinstance(obj, dict) and REQUIRED_FIELDS.issubset(set(obj.keys()))


def _fallback_pack() -> Dict[str, Any]:
    return {
        "prompt_id": "local-fallback",
        "safety_profile": "standard",
        "style": "satirical",
        "angle": "Compare/Contrast",
        "structure": "Setup→Turn→Tag",
        "devices": ["Irony"],
        "word_cap": 60,
        "receipts_target": 2,
        "writer_system": (
            "You are a concise comedy writer. Preserve supplied facts; do not invent. "
            "Think internally; do not show reasoning. Output 1–4 sentences, clear setup and punch. "
            "If facts conflict, switch to (parody)."
        ),
        "writer_user_template": (
            "PROMPT: {{prompt}}\nSUMMARY: {{summary}}\n"
            "TASK: Write a short caption (≤60 words) using Setup→Turn→Tag. "
            "Include up to 2 brief receipts only from SUMMARY. Output plain text only."
        ),
        "few_shots": [],
        "decode_prefs": {"temperature": 0.6, "top_p": 0.9, "presence_penalty": 0.0, "frequency_penalty": 0.2, "n": 1, "stop": []},
        "audit": {"mode": "real_news", "numbers_policy": "normalize; no invention", "attribution_policy": "omit unless asked", "failover": "contradictions → (parody)"},
        "eval_checks": ["Fidelity","Form","Safety","Device fit","Receipts"]
    }


async def _request_one_variant(agent: Agent, req: Request, max_tokens=1200, temperature=0.6, retries=2, idx: int = 0) -> Dict[str, Any]:
    """
    One independent Prompt-Generator call → ONE JSON object (a prompt pack).
    Retries with exponential backoff.
    """
    user_msg = (
        f"[PROMPT]\n{req.prompt}\n[/PROMPT]\n"
        f"[SUMMARY]\n{req.summary}\n[/SUMMARY]\n"
        f"Produce exactly 1 optimized prompt pack for the *Writer model*. "
        f"Return EXACTLY ONE JSON object (no extra text, no code fences). "
        f"The object MUST include fields: {sorted(REQUIRED_FIELDS)}."
    )
    messages = [
        {"role": "system", "content": PROMPT_GENERATOR_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    delay = 1.5
    for attempt in range(retries + 1):
        try:
            resp = await Runner.run(agent, messages)
            text = (getattr(resp, "final_output", "") or "").strip()
            if text.startswith("```"):
                first = text.find("{")
                last  = text.rfind("}")
                if first != -1 and last != -1:
                    text = text[first:last+1]

            obj = json.loads(text)
            if not isinstance(obj, dict):
                raise ValueError("Response is not a JSON object")
            if not _valid_pack(obj):
                raise ValueError(f"Missing required fields; got keys={list(obj.keys())}")
            return _ensure_id(obj)

        except Exception as e:
            if attempt >= retries:
                fb = _fallback_pack()
                fb["prompt_id"] = f"fallback-{idx}"
                return fb
            await asyncio.sleep(delay)
            delay *= 2


async def ask_prompt_generator(
    req: Request,
    n: int = 5,
    max_tokens: int = 1200,
    temperature: float = 0.6,
    retries: int = 2,
) -> List[dict]:
    """
    Launch N independent generation calls concurrently.
    """
    agent = Agent(
        name="prompt_generator",
        instructions=PROMPT_GENERATOR_SYSTEM_PROMPT,
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    tasks = [
        _request_one_variant(agent, req, max_tokens=max_tokens, temperature=temperature, retries=retries, idx=i)
        for i in range(n)
    ]
    results = await asyncio.gather(*tasks)
    seen: set[Tuple] = set()
    uniq: List[Dict[str, Any]] = []
    for r in results:
        sig = (r.get("style"), r.get("angle"), r.get("structure"), r.get("word_cap"))
        if sig in seen:
            # tweak id to keep uniqueness visible
            r = dict(r)
            r["prompt_id"] = r["prompt_id"] + "-dup"
        else:
            seen.add(sig)
        uniq.append(r)
    return uniq


async def main():
    req = Request(
        prompt="Make a witty short about elevator small talk.",
        summary="People feel awkward in elevators; 30 seconds; silence vs forced chat; doors ding; everyone stares ahead.",
    )

    packs = await ask_prompt_generator(req, n=16)
    with open("variants.json", "w") as f:
        f.write("\n".join(json.dumps(x, ensure_ascii=False) for x in packs))

if __name__ == "__main__":
    asyncio.run(main())
