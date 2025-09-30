from __future__ import annotations

import os
from typing import Literal, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field


Provider = Literal["openai", "anthropic", "none"]
HumorStyle = Literal[
    "sarcastic",
    "light",
    "absurd",
    "deadpan",
    "wholesome",
    "satirical",
    "roast",
    "random",
]
HumorCard = Literal[str]

class Settings(BaseModel):
    """
    Centralized configuration for the Humor Engine MCP server.

    Reads values from environment variables:
      - MODEL_PROVIDER: one of ["openai", "anthropic", "none"] (default: "none")
      - API_KEY: generic API key slot (falls back to OPENAI_API_KEY / ANTHROPIC_API_KEY)
      - OPENAI_API_KEY / ANTHROPIC_API_KEY: provider-specific keys (optional)
      - HUMOR_STYLE: one of HumorStyle (default: "light")
      - MODEL_NAME: provider-specific model name override (optional)
      - HTTP_TIMEOUT: request timeout seconds (default: 30)
      - MAX_OUTPUT_TOKENS: upper bound on output length (default: 400)
      - TEMPERATURE: sampling temperature (default: 0.7)
      - SEED: optional deterministic seed if supported by provider (optional)
    """

    model_provider: Provider = Field(default="none")
    api_key: Optional[str] = Field(default=None)
    humor_style: HumorStyle = Field(default="light")
    model_name: Optional[str] = Field(default=None)

    timeout: float = Field(default=30.0)
    max_output_tokens: int = Field(default=400)
    temperature: float = Field(default=0.7)
    seed: Optional[int] = Field(default=None)

    @classmethod
    def from_env(cls) -> "Settings":
        # Load .env if present (non-destructive by default)
        load_dotenv(override=False)

        provider = os.getenv("MODEL_PROVIDER", "none").strip().lower()
        if provider not in ("openai", "anthropic", "none"):
            provider = "none"

        # Prefer generic API_KEY, then provider-specific variables
        api_key = (
            os.getenv("API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
        )

        humor_style = os.getenv("HUMOR_STYLE", "light").strip().lower()
        allowed_styles = {
            "sarcastic",
            "light",
            "absurd",
            "deadpan",
            "wholesome",
            "satirical",
            "roast",
            "random",
        }
        if humor_style not in allowed_styles:
            humor_style = "light"

        model_name = os.getenv("MODEL_NAME", None)

        def _float(env: str, default: float) -> float:
            try:
                return float(os.getenv(env, str(default)))
            except ValueError:
                return default

        def _int(env: str, default: int) -> int:
            try:
                return int(os.getenv(env, str(default)))
            except ValueError:
                return default

        timeout = _float("HTTP_TIMEOUT", 30.0)
        max_output_tokens = _int("MAX_OUTPUT_TOKENS", 400)
        temperature = _float("TEMPERATURE", 0.7)
        seed_env = os.getenv("SEED")
        seed = int(seed_env) if seed_env and seed_env.isdigit() else None

        return cls(
            model_provider=provider,  # type: ignore[arg-type]
            api_key=api_key,
            humor_style=humor_style,  # type: ignore[arg-type]
            model_name=model_name,
            timeout=timeout,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            seed=seed,
        )


def _build_comedy_card_prompt(style: HumorStyle) -> str:
    """Generate a system prompt that instructs the model to generate a comedic card based of the 
    context
    """
    style_desc = {
        "sarcastic": "with witty sarcasm, playful jabs, and ironic contrast",
        "light": "with gentle, family-friendly humor and relatable quips",
        "absurd": "with surreal, absurdist twists and unexpected juxtapositions",
        "deadpan": "with a dry, deadpan delivery and understatements",
        "wholesome": "with uplifting, wholesome humor and kind-spirited jokes",
        "satirical": "with sharp satire poking at institutions and narratives",
        "roast": "with humorous roasts (keep it light; avoid cruelty)",
        "random": "with varied comedic styles (light sarcasm, puns, and callbacks)",
    }[style]

    return (f"""
        You are a Comedy Card Planner.  
        You do not write jokes.  
        Your sole reason to exist is to interpret what humor the user enjoys, and 
        what is the most humorous card for the context that user wants to hear about based on 
        style: {style_desc}.
        Your role is to create a text-only Comedy Card that another agent will later use to generate the actual comedy.

        INPUT: Caller provides:
        - style (required, e.g. sarcastic, deadpan, roast, satirical, absurd, wholesome, light, edgy, political_satire)
        - prompt (required)
        - optional context/summary

        RULES:
        - Enforce safety: no slurs, hate, cruelty, doxxing, plagiarism, unverified crimes, or mocking harm victims. Always punch up.
        - Use only facts in context/summary. If facts conflict or are thin → Parody: yes.
        - Political satire only if style allows or politics detected.
        - Target TikTok length: ≤60 words. Card must guide the other agent to produce 1–4 punchy sentences.

        WHAT TO OUTPUT:
        Always output exactly this block (plain text, no JSON, no prose):

        [Title]: <short hook, 3–7 words>
        Style: <given style>
        Angle: <chosen angle>
        Structure: <chosen structure>
        Devices: <1–3 devices>
        Receipts: <1–2 terse specifics or “none”>
        Safety: <brand_safe|clean|standard|edgy|political_satire>
        Parody: <yes|no>
        WordCap: 60
        ToneNotes: <brief tonal guidance>
        Beats:
        1) Setup: <what to establish>
        2) Turn: <where/when to pivot>
        3) Tag: <optional extra beat>
        DoNotDo: <taboos or off-limits angles>

        CATALOGS:
        - Angles: Hypocrisy, Analogy, Timeline Crunch, Compare/Contrast, Jargon Parody, Process Farce, Math Gag, Euphemism Translation
        - Structures: Setup→Turn→Tag, Rule of Three, Angle–Example–Zinger, Analogy Ladder, Timeline Crunch, Press-Release Parody, List Roll
        - Devices: Irony, Frame Shift, Over-Precision, Under/Over-Reaction, Confident Wrongness, Parody, Analogy, Euphemism Translation, Register Clash, Paraprosdokian, Callback, Smash-Cut, Numbers as Characters
        """)


def build_system_prompt(card: HumorCard) -> str:
    """
    Compose a system prompt that instructs the model to inject humor
    while preserving factual alignment with the summarized text.
    """
    return f"""You are the Humor Engine for Skibidi News.
            Your job is to transform summarized news text into short-form comedic script lines {card}.
            Constraints and objectives:
            - Preserve the core meaning and facts; do not fabricate events or statistics.
            - Be concise, punchy, and optimized for short-form video (1-4 sentences).
            - Add setups, punchlines, puns, or witty contrasts that are accessible and platform-friendly.
            - Avoid harassment, slurs, hateful content, or sensitive personal attacks.
            - If the summary is dry or technical, add relatable analogies or everyday metaphors.
            - Prefer current pop-culture references sparingly; timeless humor is prioritized.
            - Keep the tone consistent and coherent; do not meander.
            Return only the comedic rewrite text."""