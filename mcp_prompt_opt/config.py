from __future__ import annotations

import os
from typing import Literal, Optional

from dotenv import load_dotenv
load_dotenv(override=False)

from pydantic import BaseModel, Field
Provider = Literal["openai", "anthropic", "none"]

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
    model_name: Optional[str] = Field(default=None)

    timeout: float = Field(default=30.0)
    max_output_tokens: int = Field(default=400)
    temperature: float = Field(default=0.7)
    seed: Optional[int] = Field(default=None)

    @classmethod
    def from_env(cls) -> "Settings":
        provider = os.getenv("MODEL_PROVIDER", "none").strip().lower()
        if provider not in ("openai", "anthropic", "none"):
            provider = "none"

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
            model_provider=provider, 
            api_key=api_key,
            humor_style=humor_style,  
            model_name=model_name,
            timeout=timeout,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            seed=seed,
        )