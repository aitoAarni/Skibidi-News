## 3.10

Humorizer broken.  
YouTube auth figured out.  
News fetching by category.  
More backend and frontend stuff.

## 27.10

Tried making unfunny AI funny, to no avail.  
Tried using shady GPUs for video gen, to no avail.  
Frontend and backend progressing though. :>

## 20.10

Experimented with video stuff.

My journey through the Realm of Image Generation has ended in ruin. The treasury
of credits—gone. The gods—silent. The errors—multiplying.

wan2.2’s documentation reads like an ancient spellbook missing half its pages.
I’ve already cast ten dollars into the void, and still the daemon of “dependency
conflict” laughs in my terminal.

Until the School bestows divine funding upon us, I shall sheathe my keyboard and
await the next prophecy of pip install.

Refactored deployment setup.

## 13.10

Integration: everything up and running.

## 6.10

🎤 “So, this week in skibidi chaos…”

We started fixing dependencies for news_aggr — because apparently, “latest
version” means “hope you like debugging for sport.” Then we tried connecting it
to the router agent, which went about as smoothly as teaching a cat to do
calculus.

Meanwhile, the text to speech was out here like, “Hey, remember Docker?” — yeah,
we fixed that too. It only took seventeen rebuilds, one existential crisis, and
a prayer to the DevOps gods.

Then came audio splicing — because every text to speech model ever has the
reading endurance of a toddler. “Oh, you want me to read more than 500
characters? That’s cute.” So now we’re basically audio surgeons — slicing and
stitching words together like, 🎧 “Next up — your daily dose of AI mumble rap!”

After that, we built a frontend with React and Tailwind, which means we spent
half the day arguing about spacing and pretending we know how Tailwind’s flex
classes actually work. Centering a div? Still a mythical art form.

And then we updated the docs, which is code for “future us will never understand
this, but let’s pretend we’re being responsible.”

Finally, the grand finale: “Integrate router agent with all servers.”
Translation? “Let’s make every system talk to every other system until they all
start asking, ‘Wait… who am I?’”

So yeah — team productivity: chaotic good. System stability: hanging by a
thread.

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

Built a Humor Engine MCP server that transforms summarized news text into
comedic short-form content.

Exposed two MCP tools:

comedicize(id, summarized_text) → returns comedic rewrite.

health() → returns server status and config.

Pluggable LLM backends (OpenAI, Anthropic) via environment config Deterministic
offline fallback humorizer (no API key required) CLI interface for local runs
and testing Configurable parameters: humor style, provider, temperature, max
tokens, seed, etc. Ready for integration with MCP clients
