from __future__ import annotations

import re

from mcp_humorizer.humor import humorous_rewrite


def _count_sentences(text: str) -> int:
    # Count sentences by splitting on ., !, ? and filtering empties
    parts = re.split(r"[.!?]+", text)
    return sum(1 for p in parts if p.strip())


def test_humor_preserves_fact_and_is_punchy():
    summary = "The economy shrank by 2% last quarter"
    out = humorous_rewrite(summary, style="light")

    # Fact should be present verbatim (first sentence echoes the input with punctuation)
    assert summary in out

    # Output should be short-form (2–4 sentences)
    n = _count_sentences(out)
    assert 2 <= n <= 4

    # Number/percent punchline should appear for numeric inputs (light style default)
    assert "shrinking faster" in out.lower()


def test_humor_money_trigger_light_style():
    summary = "The budget was cut by $5 million for next year"
    out = humorous_rewrite(summary, style="light")

    # Fact preserved
    assert summary in out

    # Money quip for default/light style
    assert "Wallets are doing cardio" in out


def test_humor_generic_trigger_deadpan():
    summary = "Scientists discovered a new exoplanet nearby"
    out = humorous_rewrite(summary, style="deadpan")

    # Fact preserved
    assert summary in out

    # Deadpan specific lines likely present
    assert "In other news, water is still wet." in out or "We remain cautiously unimpressed." in out

    # Sentence count still constrained
    n = _count_sentences(out)
    assert 2 <= n <= 4
