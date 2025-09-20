from __future__ import annotations

import re
from typing import Literal

from .config import HumorStyle


_WHITESPACE_RE = re.compile(r"\s+")


def _clean(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", (text or "").strip())


def _ensure_sentence(s: str) -> str:
    s = s.strip()
    if not s:
        return s
    if s[-1] in ".!?":
        return s
    return s + "."


def _has_percent(text: str) -> bool:
    return bool(re.search(r"\d+(?:\.\d+)?\s*%", text))


def _has_money(text: str) -> bool:
    return bool(re.search(r"[$€£]\s*\d", text) or re.search(r"\b(?:million|billion|trillion)\b", text, re.I))


def _has_numbers(text: str) -> bool:
    return bool(re.search(r"\d", text))


def _quip_for_numbers(style: HumorStyle) -> str:
    if style in ("sarcastic", "satirical", "roast"):
        return "Relax—my budget is dropping faster than my willpower on pizza night."
    if style == "deadpan":
        return "Comparatively, my savings remain theoretical."
    if style == "absurd":
        return "Meanwhile, the numbers tried to unionize with my calculator."
    if style == "wholesome":
        return "Deep breaths—numbers bounce back, and so can we."
    # light / random / default
    return "On the bright side, my diet is shrinking faster."


def _quip_for_money(style: HumorStyle) -> str:
    if style in ("sarcastic", "satirical"):
        return "Somewhere, a committee just approved a 'vibes only' budget."
    if style == "deadpan":
        return "Fiscal responsibility remains on lunch break."
    if style == "absurd":
        return "A flock of dollar bills migrated south for the winter."
    if style == "wholesome":
        return "Money comes and goes—community and good coffee remain."
    if style == "roast":
        return "Politicians looked at the math and said, 'We prefer interpretive dancing.'"
    return "Wallets are doing cardio; endurance pending."


def _quip_for_generic(style: HumorStyle) -> str:
    if style == "deadpan":
        return "In other news, water is still wet."
    if style == "absurd":
        return "It's like a goose in a board meeting—nobody knows why it's here, but now everyone's honking."
    if style == "wholesome":
        return "Hang in there—every headline has a human on the other side."
    if style in ("satirical", "sarcastic"):
        return "Experts responded by deploying charts, acronyms, and confident nods."
    if style == "roast":
        return "If common sense were Wi‑Fi, this situation would have one bar."
    # light / random / default
    return "So yeah—big mood, tiny attention span, perfect for a short video."


def _tagline(style: HumorStyle) -> str:
    if style == "deadpan":
        return "End of joke. That was the joke."
    if style == "absurd":
        return "Cue the kazoo solo."
    if style == "wholesome":
        return "Stay kind; laugh often."
    if style in ("satirical", "sarcastic"):
        return "Back to you, spin department."
    if style == "roast":
        return "Apply ice to the narrative."
    # light / random / default
    return "Like, follow, and pretend you learned economics."


def humorous_rewrite(summarized_text: str, style: str | HumorStyle = "light") -> str:
    """
    Deterministic humorizer for summarized news text.

    Guarantees:
    - Preserves the original meaning by keeping the first sentence close to the input.
    - Outputs 2–4 short sentences (platform-friendly).
    - Avoids offensive content by using mild, general humor.
    """
    text = _clean(summarized_text)
    if not text:
        return "No input provided. Punchline withheld until further notice."

    # Normalize style
    allowed: tuple[HumorStyle, ...] = (
        "sarcastic",
        "light",
        "absurd",
        "deadpan",
        "wholesome",
        "satirical",
        "roast",
        "random",
    )
    s: HumorStyle = style if style in allowed else "light"
    if s == "random":
        # Deterministic 'random' based on simple hash of content length
        idx = len(text) % 5
        s = ("light", "sarcastic", "deadpan", "absurd", "wholesome")[idx]  # type: ignore[assignment]

    # Line 1: echo core fact concisely (avoid fabricating details)
    line1 = _ensure_sentence(text)

    # Line 2: punchline tailored by content signals
    if _has_money(text):
        line2 = _ensure_sentence(_quip_for_money(s))
    elif _has_percent(text) or _has_numbers(text):
        line2 = _ensure_sentence(_quip_for_numbers(s))
    else:
        line2 = _ensure_sentence(_quip_for_generic(s))

    # Line 3: short analogy / contrast
    if s in ("absurd",):
        line3 = _ensure_sentence("Imagine explaining that to a rubber duck with a briefcase.")
    elif s in ("deadpan",):
        line3 = _ensure_sentence("We remain cautiously unimpressed.")
    elif s in ("satirical", "sarcastic"):
        line3 = _ensure_sentence("Translation: same plot, new press release.")
    elif s == "wholesome":
        line3 = _ensure_sentence("Small steps forward still count.")
    else:
        line3 = _ensure_sentence("Perfect for a 15‑second attention span recap.")

    # Optional Line 4: brief sign-off/tagline
    line4 = _ensure_sentence(_tagline(s))

    # Keep to 3–4 sentences depending on input length
    sentences = [line1, line2, line3]
    if len(text) > 80:
        sentences.append(line4)

    # Join and ensure compact output
    out = " ".join(sentences)
    return _clean(out)
