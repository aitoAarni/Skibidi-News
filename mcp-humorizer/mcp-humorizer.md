# MCP Server – Summarized Text → Comedic Text

## Overview

This MCP server receives **summarized news text** and transforms it into **comedic text**, maintaining the original meaning while injecting humor, satire, and punchlines. It acts as the **Humor Engine** of *Skibidi News*, bridging factual news with digestible entertainment.

## Responsibilities

1. **Input:** Summarized text (from News Aggregation service).
2. **Processing:**

   * Parse and analyze text context.
   * Apply comedic prompt templates and humor strategies.
   * Optimize for short, punchy delivery (suited for TikTok/short-form content).
3. **Output:** Comedic text (ready for transcript → audio or transcript → video stages).

## API Contract

* **Input:**

  ```json
  {
    "id": "uuid",
    "summarized_text": "The economy shrank by 2% last quarter."
  }
  ```

* **Output:**

  ```json
  {
    "id": "uuid",
    "comedic_text": "The economy shrank by 2%. Don’t worry, my diet is shrinking faster!"
  }
  ```

## Connection with Router Agent

* Registered as an MCP Server (`mcp_summarizedText_ComedicText`).
* Communicates with Router Agent to receive jobs and return results.
* AI model (LLM) can be swapped easily thanks to containerization.

## Deployment

* **Containerized (Docker):** Enables independent deployment and scalability.
* **Configurable AI backend:** OpenAI, Anthropic, or custom humor-tuned models.
* **Environment variables:**
  * `MODEL_PROVIDER`
  * `API_KEY`
  * `HUMOR_STYLE` (sarcastic, light, absurd, etc.)

## Example Flow

1. Router Agent receives summarized text.
2. Passes payload to MCP server.
3. Server applies humor transformation.
4. Comedic text is returned to Router Agent.

## Notes

* Humor should be **short-form, punchy, and platform-ready**.
* Ensure output remains tied to actual summarized content (not fake news).
* Comedic “flavor” can be adjusted via system prompt or config.
