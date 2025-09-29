from __future__ import annotations

import logging
from typing import Optional

from .config import Settings, build_system_prompt

# Providers are optional; imports are inside functions to avoid import errors
# if users don't install all SDKs.
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GenerationError(Exception):
    pass


def _generate_with_openai(
    summarized_text: str, settings: Settings, system_prompt: str
) -> str:
    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:  # pragma: no cover
        raise GenerationError(f"OpenAI SDK import failed: {e}")

    if not settings.api_key:
        raise GenerationError("OpenAI requires an API key (API_KEY or OPENAI_API_KEY).")

    client = OpenAI(api_key=settings.api_key)

    model = settings.model_name or "gpt-4o-mini"
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Summarized news text:\n\n{summarized_text}\n\nRewrite as comedic text.",
                },
            ],
            temperature=settings.temperature,
            max_tokens=settings.max_output_tokens,
        )
        text = completion.choices[0].message.content or ""
        if not text.strip():
            raise GenerationError("OpenAI returned empty content.")
        return text.strip()
    except Exception as e:
        raise GenerationError(f"OpenAI generation failed: {e}")


def _generate_with_anthropic(
    summarized_text: str, settings: Settings, system_prompt: str
) -> str:
    try:
        import anthropic  # type: ignore
    except Exception as e:  # pragma: no cover
        raise GenerationError(f"Anthropic SDK import failed: {e}")

    if not settings.api_key:
        raise GenerationError("Anthropic requires an API key (API_KEY or ANTHROPIC_API_KEY).")

    client = anthropic.Anthropic(api_key=settings.api_key)
    model = settings.model_name or "claude-3-5-sonnet-latest"

    try:
        msg = client.messages.create(
            model=model,
            max_output_tokens=settings.max_output_tokens,
            temperature=settings.temperature,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarized news text:\n\n{summarized_text}\n\nRewrite as comedic text.",
                }
            ],
        )
        # msg.content is a list of blocks; join text parts
        parts = []
        for block in getattr(msg, "content", []) or []:
            text = getattr(block, "text", None)
            if text:
                parts.append(text)
        text = "\n".join(parts).strip()
        if not text:
            raise GenerationError("Anthropic returned empty content.")
        return text
    except Exception as e:
        raise GenerationError(f"Anthropic generation failed: {e}")


def _humor_fallback(summarized_text: str, style: str) -> str:
    """
    Lightweight, deterministic humorizer to ensure offline functionality.
    Produces short, punchy lines while preserving meaning.
    """
    from .humor import humorous_rewrite

    return humorous_rewrite(summarized_text, style)


def _card_fallback(style: str) -> str:
    """
    Lightweight, deterministic humour card to ensure offline functionality.
    """
    return """
        [Title]: Cached Punchline
        Style: absurd
        Angle: Process Farce
        Structure: Setup→Turn→Tag
        Devices: Confident Wrongness; Analogy
        Receipts: none
        Safety: brand_safe
        Parody: yes
        WordCap: 60
        ToneNotes: light, timeless, self-referential
        Beats:
        1) Setup: Announce a “lightweight, deterministic humor module.”
        2) Turn: Compare it to comedy that runs even in airplane mode.
        3) Tag: “All jokes pre-downloaded for your convenience.”
        DoNotDo: No politics, no identities, no tragedy references.
        """


def comedicize_text(summarized_text: str, settings: Settings) -> str:
    """
    Main entry point for generating comedic text with graceful fallback.
    """
    summarized_text = (summarized_text or "").strip()
    if not summarized_text:
        return "No input provided. Punchline withheld until further notice."

    provider = settings.model_provider
    if provider == "openai":
        try:
            comedy_card = _generate_with_openai(build_system_prompt(settings.humor_style))
        except GenerationError as e:
            logger.warning("OpenAI failed, using humor fallback: %s", e)
            comedy_card = _card_fallback()
    elif provider == "anthropic":        
        try:
            comedy_card = _generate_with_anthropic(build_system_prompt(settings.humor_style))
        except GenerationError as e:
            logger.warning("OpenAI failed, using humor fallback: %s", e)
            comedy_card = _card_fallback()
    else:
        # No provider configured; use local humorous card
        return _card_fallback(summarized_text, settings.humor_style)

    system_prompt = build_system_prompt(comedy_card)

    provider = settings.model_provider
    if provider == "openai":
        try:
            return _generate_with_openai(summarized_text, settings, system_prompt)
        except GenerationError as e:
            logger.warning("OpenAI failed, using humor fallback: %s", e)
            return _humor_fallback(summarized_text, settings.humor_style)
    elif provider == "anthropic":
        try:
            return _generate_with_anthropic(summarized_text, settings, system_prompt)
        except GenerationError as e:
            logger.warning("Anthropic failed, using humor fallback: %s", e)
            return _humor_fallback(summarized_text, settings.humor_style)
    else:
        # No provider configured; use local humorous rewrite
        return _humor_fallback(summarized_text, settings.humor_style)
