from __future__ import annotations

from mcp_humorizer import Settings, comedicize_text


def test_engine_fallback_when_provider_none_numeric_light():
    # When provider is 'none', engine should use deterministic fallback
    settings = Settings(model_provider="none", humor_style="light")
    summary = "The economy shrank by 2% last quarter"
    out = comedicize_text(summary, settings)

    # Fact should be present; output should include numeric quip for light style
    assert summary in out
    assert "shrinking faster" in out.lower()
    assert 0 < len(out.strip())


def test_engine_fallback_on_openai_missing_api_key():
    # Provider set to openai but no API key => engine must gracefully fall back
    settings = Settings(model_provider="openai", api_key=None, humor_style="light", model_name="gpt-4o-mini")
    summary = "Unemployment rose by 1.2% according to the latest report"
    out = comedicize_text(summary, settings)

    # Should not raise; should still include fallback content
    assert summary in out
    assert "shrinking faster" in out.lower() or "budget" in out.lower()
    assert 0 < len(out.strip())


def test_engine_fallback_respects_style_deadpan():
    # Ensure style influences fallback phrasing
    settings = Settings(model_provider="none", humor_style="deadpan")
    summary = "Scientists discovered a new exoplanet nearby"
    out = comedicize_text(summary, settings)

    assert summary in out
    # Deadpan specific phrasing appears in fallback variants
    assert ("we remain cautiously unimpressed" in out.lower()) or ("in other news, water is still wet" in out.lower())
