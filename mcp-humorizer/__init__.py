"""
mcp_summarizedText_ComedicText

MCP Server – Summarized Text → Comedic Text
- Receives summarized news text and transforms it into comedic text.
- Pluggable LLM providers (OpenAI, Anthropic) with an offline deterministic fallback.
- Exposes MCP tools via FastMCP:
    - comedicize(id: str, summarized_text: str) -> {"id": str, "comedic_text": str}
    - health() -> basic server status info
"""

from __future__ import annotations

__all__ = [
    "__version__",
    "comedicize_text",
    "Settings",
    "HumorStyle",
    "Provider",
    "build_system_prompt",
]

__version__ = "0.1.0"

from .engine import comedicize_text
from .config import Settings, HumorStyle, Provider, build_system_prompt
