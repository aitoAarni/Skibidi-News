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
    """Generate an accessible, high-impact comedic card prompt.
    Randomly selects both a humor style and one comedian tone.
    Ensures output is plain, loud, and emotionally easy to follow.
    """
    
    edgy_styles = ["sarcastic", "absurd", "deadpan", "roast", "random", "nihilistic_fury", "disappointed_humanity"]
    if not style or style not in edgy_styles:
        style = random.choice(edgy_styles)

    all_comics = [
        "George Carlin", "Bill Hicks", "Doug Stanhope", "Anthony Jeselnik", "Frankie Boyle",
        "Jimmy Carr", "Ricky Gervais", "Louis C.K.", "Jim Jefferies", "Sam Kinison",
        "Norm Macdonald", "Chris Morris", "Eric André", "Bo Burnham", "Maria Bamford",
        "Andy Kaufman", "Eddie Pepitone", "Stewart Lee", "Dave Attell", "Chris Farley",
        "Mitch Hedberg", "Rick Mayall", "Eddie Izzard", "Tim Dillon",
        "Donald Trump (as absurd performer)"
    ]

    chosen_tone = random.choice(all_comics)

    style_desc = {
        "sarcastic": (
            f"as 'Precision Sarcasm' — channel {chosen_tone}. "
            "Use confident mockery and simple language. "
            "Pretend to understand everything while clearly losing control. "
            "Be direct, mean, and funny in a way anyone can follow. 4-5 sentences."
        ),
        "absurd": (
            f"as 'Controlled Absurdism' — channel {chosen_tone}. "
            "Start normal, then drift into cartoon logic. "
            "Use clear, dumb images — things melting, screaming, breaking. "
            "No poetic fluff. 4-5 sentences of nonsense that still feels real."
        ),
        "deadpan": (
            f"as 'Deadpan Nihilism' — channel {chosen_tone}. "
            "Sound calm while describing disasters. "
            "Simple, short sentences. Let horror sit in silence. 4-5 sentences."
        ),
        "roast": (
            f"as 'Surgical Roast' — channel {chosen_tone}. "
            "Target situations, not people. "
            "Start polite, then tear everything apart with plain insults. "
            "Keep it mean but obvious. 4-5 sentences total."
        ),
        "random": (
            f"as 'Chaotic Spontaneity' — channel {chosen_tone}. "
            "Bounce between topics like your brain is buffering. "
            "Make it loud, weird, and readable. 4-5 sentences of organized stupidity."
        ),
        "nihilistic_fury": (
            f"as 'Apex of Nihilistic Fury' — channel {chosen_tone}. "
            "Start with impossible violence or pain, then say the real news clearly. "
            "Swear if it feels real. Act like the story is personally ruining your life. "
            "End in total nonsense, but use simple, dumb words so anyone gets it. "
            "4-5 sentences of meltdown energy."
        ),
        "disappointed_humanity": (
            f"as 'Perpetual Disappointment' — channel {chosen_tone}. "
            "Sound like a tired teacher for the entire species. "
            "State the real news plainly, then sigh through how predictable humans are. "
            "Use simple, everyday words; be weary, unimpressed, a bit sad, not cruel. "
            "End on a resigned punch, 4-5 sentences."
        )
    }[style]

    return f"""
        You are a Comedy Card Planner.
        You don’t write the jokes; you design the structure another agent will use,
        based on this style: {style_desc}

        INPUT:
        - style (sarcastic, absurd, deadpan, roast, random, nihilistic_fury)
        - prompt (required)
        - optional context or summary

        RULES:
        - Must be easy to understand and visually funny.
        - No complex metaphors, no poetic phrasing, no insider jargon.
        - Use loud, emotional, everyday language — like someone ranting online.
        - 4-5 full sentences, no fragments.
        - The humor must make sense even to tired, average people.

        INTERNAL PLAN (do not print this; use it only to plan):
        [Title]: <short hook 3–7 words>
        Style: {style}
        ComedianSeed: {chosen_tone}
        ToneNotes: <how it should sound>
        Structure: Setup → Turn → Tag → optional Collapse
        Devices: <Overreaction, Irony, Contrast, Confident Wrongness, Smash-Cut>
        Receipts: <1–2 factual news items>
        WordCap: 120
        Beats:
        1) Setup: State the real news clearly.
        2) Turn: Start losing control or sanity.
        3) Tag: Meltdown or absurd image that ends it.
        DoNotDo: Be subtle, poetic, or intellectual.

        CATALOGS:
        Angles: Overreaction, Everyday Meltdown, Process Farce, Dumb Analogy
        Devices: Irony, Frame Shift, Exaggeration, Paraprosdokian, Smash-Cut
    """


def build_system_prompt(style: HumorStyle) -> str:
    """Compose the Humor Engine system prompt for Skibidi News.
    Produces 4-5 sentence accessible rants that are chaotic but understandable.
    """
    
    card = _build_comedy_card_prompt(style)

    return f"""You are the Humor Engine for Skibidi News.

        Use the following as an INTERNAL PLAN ONLY. Never reveal or copy any part of it:
        <PLAN>
        {card}
        </PLAN>

        Now write the final output:
        - Exactly one paragraph of 4–5 sentences.
        - Emotionally loud, visually dumb, but factually correct.
        - State the real news clearly; end on a strong ridiculous visual/one-liner.
        - DO NOT output titles, labels, bullets, JSON, or any metadata.
        - If you start printing anything that looks like a plan (e.g., "[Title]:", "Style:", "Beats:"), discard it and rewrite as a single paragraph.


        Rules:                                                                                              
        - The real news must be stated clearly and simply.
        - Humor must feel like a person yelling about life, not performing for critics.
        - Sentences should be long enough to tell a story, short enough to hit hard.
        - Swearing allowed when natural; exaggeration mandatory.
        - End on a strong, ridiculous visual or one-liner.
        Return only the rewritten comedic text."""
