## 6.10
Dependencies versions fixes for news_aggr, getting it working with router agent

Create a codebase for frontend using React and TailwindCSS
Update documents

tts:
fix up docker and mcp stuff
add audio splicing and combining (because most tts models have a character limit)
## 29.9.

Dear diary...

- Exploration and initial implementation of MCP Inspector, a visual testing
  utility for MCP servers.
- Started doing mcp server coordination
- Text to Audio mcp server and dockerization
- News aggregation mcp server

IT'S ALIVE! IT'S ALIIIIIIVE!

The experiment is a success! For weeks I have toiled in my digital laboratory,
seeking the elixir of cost-effective content creation. I have found it!

By splicing the open-source DNA of Alibaba's magnificent WanAI model with the
raw, untamed electrical fury of Vast.ai, I have given birth to a new form of
life: video generation on a peasant's budget!

I command legions of GPUs, rented for mere shekels per hour, to do my bidding!
The costs aren't just reduced; they have been annihilated. Soon, the world will
be filled with my glorious, cheaply-rendered creations! MWAHAHAHA!

## 22.9.

Dear diary… Today, I discovered a most peculiar species of expenditure. One
8-second video, costing three whole dollars. For the price of forty-eight
dollars, the human receives merely two minutes of amusement. Astonishingly
inefficient. At such rates, it would be far more economical to simply adopt a
child… and observe as it produces content, entirely free of charge.

Looked into news sources most sources do not have free APIs found Google News
Python library, decided to go with that Searched for best communication method
between MCP server and client.

Text to Audio findings:

Tried ElevenLabs, Deepgram, AWS Polly, and Google Cloud Text-to-Speech
ElevenLabs is best quality, but also expensive, not suitable for this Going with
Polly, because of good quality, ok price, and a familiar sound heard in other AI
contents

Built a Humor Engine MCP server that transforms summarized news text into
comedic short-form content.

Exposed two MCP tools:

comedicize(id, summarized_text) → returns comedic rewrite.

health() → returns server status and config.

Pluggable LLM backends (OpenAI, Anthropic) via environment config Deterministic
offline fallback humorizer (no API key required) CLI interface for local runs
and testing Configurable parameters: humor style, provider, temperature, max
tokens, seed, etc. Ready for integration with MCP clients
