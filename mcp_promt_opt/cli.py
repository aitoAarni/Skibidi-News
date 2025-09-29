from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from .config import Settings
from .engine import optimize


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Local CLI to transform summarized news text into comedic text."
    )
    parser.add_argument(
        "--id",
        default="local-test",
        help="Job identifier (default: local-test)",
    )
    parser.add_argument(
        "-t",
        "--text",
        help="Summarized text input. If omitted, the CLI reads from stdin.",
    )
    parser.add_argument(
        "--style",
        choices=["sarcastic", "light", "absurd", "deadpan", "wholesome", "satirical", "roast", "random"],
        help="Override humor style for this run.",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "none"],
        help="Override model provider for this run.",
    )
    parser.add_argument(
        "--api-key",
        help="Override API key for this run.",
    )
    parser.add_argument(
        "--model-name",
        help="Override model name for this run (e.g., gpt-4o-mini, claude-3-5-sonnet-latest).",
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        help="Override max output tokens for this run.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Override sampling temperature for this run.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.text is not None:
        summarized_text = args.text
    else:
        summarized_text = sys.stdin.read()

    settings = Settings.from_env()

    updates: Dict[str, Any] = {}
    if args.style:
        updates["humor_style"] = args.style
    if args.provider:
        updates["model_provider"] = args.provider
    if args.api_key:
        updates["api_key"] = args.api_key
    if args.model_name:
        updates["model_name"] = args.model_name
    if args.max_output_tokens is not None:
        updates["max_output_tokens"] = args.max_output_tokens
    if args.temperature is not None:
        updates["temperature"] = args.temperature

    if updates:
        settings = settings.model_copy(update=updates)

    optimized_prompt = optimize(summarized_text, settings)
    output = {
        "id": args.id,
        "optimized_prompt": optimized_prompt,
    }
    print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
