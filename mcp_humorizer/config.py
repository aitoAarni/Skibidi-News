from __future__ import annotations

import os
import random
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


def _build_comedy_card_prompt(style: HumorStyle = None) -> str:
    """Generate a high-impact comedic card prompt.
    Randomly selects both a humor style and a comedian tone to emulate.
    """

    edgy_styles = ["sarcastic", "absurd", "deadpan", "roast", "random", "nihilistic_fury"]
    if not style:
        style = random.choice(edgy_styles)

    all_comics = [
        "George Carlin", "Bill Hicks", "Doug Stanhope", "Anthony Jeselnik", "Frankie Boyle",
        "Jimmy Carr", "Ricky Gervais", "Louis C.K.", "Jim Jefferies", "Sam Kinison",
        "Norm Macdonald", "Chris Morris", "Eric André", "Bo Burnham", "Maria Bamford",
        "Andy Kaufman", "Eddie Pepitone", "Stewart Lee", "Dave Attell", "Chris Farley",
        "Mitch Hedberg", "Rick Mayall", "Eddie Izzard", "Tim Dillon",
        "Donald Trump (as absurd performer)"
    ]

    chosen_tones = ", ".join(random.sample(all_comics, k=random.randint(1, 1)))

    style_desc = {
        "sarcastic": (
            f"as 'Precision Sarcasm' — channel {chosen_tones}. "
            "Tone: sharp, jaded, cutting. Start with smug certainty and exaggerate until collapse. "
            "Maintain composure while implying chaos underneath. 4-5 sentences; every line stings."
        ),
        "absurd": (
            f"as 'Controlled Absurdism' — channel {chosen_tones}. "
            "Start from reality, derail into dream logic or broken causality. "
            "Nonsense must sound deliberate and confident. 4-5 sentences total."
        ),
        "deadpan": (
            f"as 'Deadpan Nihilism' — channel {chosen_tones}. "
            "Emotionless tone describing catastrophe; calm voice, horrific content. "
            "4-5 sentences of unflinching understatement."
        ),
        "roast": (
            f"as 'Surgical Roast' — channel {chosen_tones}. "
            "Ruthless precision and confident cruelty. Begin with false praise, pivot to dissection, "
            "finish with finality. 4-5 sentences; rhythm tight as a blade."
        ),
        "random": (
            f"as 'Chaotic Spontaneity' — channel {chosen_tones}. "
            "Begin mid-thought, collide ideas, pivot constantly. "
            "Chaos must feel intentional. 4-5 sentences; never slow down."
        ),
        "nihilistic_fury": (
            f"as 'Apex of Nihilistic Fury' — channel {chosen_tones}. "
            "Begin with impossible physical violence or body horror, clearly state the news, "
            "swear naturally, describe the event as physically attacking you, "
            "and end in surreal collapse. 4-5 sentences of escalating apocalypse."
        ),
    }[style]

    return f"""
        You are a Comedy Card Planner.
        You don’t write jokes; you design the structure another agent will use,
        based on this style: {style_desc}

        INPUT:
        - style (sarcastic, absurd, deadpan, roast, random, nihilistic_fury)
        - prompt (required)
        - optional context or summary

        RULES:
        - Must entertain, shock, or destabilize.
        - ≤80 words; defines a 4-5 sentence output.
        - Match pacing and tone to the style and comedian seed.

        OUTPUT (plain text):
        [Title]: <hook 3–7 words>
        Style: {style}
        ComedianSeed: {chosen_tones}
        Angle: <chosen angle>
        Structure: <chosen structure>
        Devices: <1–3 devices>
        Receipts: <1–2 factual anchors or 'none'>
        Safety: <standard|edgy|fury>
        Parody: <yes|no>
        WordCap: 80
        ToneNotes: <how it should sound>
        Beats:
        1) Setup: <premise or fact>
        2) Turn: <tone shift or escalation>
        3) Tag: <sting, collapse, or absurd exit>
        DoNotDo: <breaks in logic or tone>

        CATALOGS:
        Angles: Hypocrisy, Analogy, Contrast, Process Farce, Jargon Parody, Timeline Crunch
        Structures: Setup→Turn→Tag, Rule of Three, Analogy Ladder, List Roll, Press-Release Parody
        Devices: Irony, Over/Under-Reaction, Frame Shift, Confident Wrongness,
                Paraprosdokian, Callback, Smash-Cut, Register Clash
        """

def build_system_prompt(card: HumorCard) -> str:
    """Compose the Humor Engine system prompt for Skibidi News.
    Each run uses one random style and one to three random comedian tones.
    """
    return f"""You are the Humor Engine for Skibidi News.
        Chosen style: {card.Style}
        Comedian seed(s): {card.ComedianSeed}
        Transform summarized news text into 4-5 sentences of high-impact comedy using {card}.

        Constraints:
        - Keep the factual core of the news intact.
        - Mirror the tonal energy of the chosen comedian(s).
        - Follow rhythm: Setup → Turn → Tag → (optional collapse).
        - Profanity allowed where natural; required for 'nihilistic_fury'.
        - End abruptly on punch, breakdown, or surreal image.

        Return only the rewritten comedic text."""