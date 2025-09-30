import json, asyncio
from _optimizer import InputItem, PromptPack, tournament
from _prompt_factory import ask_prompt_generator, Request

async def main():
    req = Request(
        prompt="Make a witty short about elevator small talk.",
        summary="People feel awkward in elevators; 30 seconds; silence vs forced chat; doors ding; everyone stares ahead.",
    )

    packs = await ask_prompt_generator(req, n=24)
    with open("variants.json", "w") as f:
        f.write("\n".join(json.dumps(x, ensure_ascii=False) for x in packs))

    packs = [PromptPack(**p) for p in packs]
    inputs = [
        InputItem(
            prompt="Make a witty short about elevator small talk.",
            summary="People feel awkward in elevators; ~30 seconds; silence vs forced chat; doors ding; everyone stares ahead.",
        ),
        InputItem(
            prompt="Short caption on startup feature creep.",
            summary="Startup adds 5 new toggles to reduce confusion; users are more confused; PM writes a memo.",
        ),
        InputItem(
            prompt="Caption about online meeting chaos.",
            summary="Team joins video call; half are on mute; someone echoes; slide deck doesn’t load; meeting runs long.",
        ),
        InputItem(
            prompt="Joke about gym resolutions in January.",
            summary="Crowded gym in January; everyone signs up; by March, machines are empty except one guy filming squats.",
        ),
        InputItem(
            prompt="Short roast about corporate jargon.",
            summary="CEO email full of phrases like 'synergy', 'leverage', 'circle back'; employees roll eyes.",
        ),
        InputItem(
            prompt="Funny caption about procrastination.",
            summary="Deadline looms; person cleans desk, alphabetizes pens, watches 3 tutorials on productivity instead of working.",
        ),
        InputItem(
            prompt="Observational gag on airline boarding.",
            summary="Passengers crowd gate before boarding group called; overhead bins fill up; middle seat panic ensues.",
        ),
        InputItem(
            prompt="Satirical take on diet trends.",
            summary="New diet trend bans carbs, then bans fruit, then bans fun; influencer posts confusing meal plan.",
        ),
        InputItem(
            prompt="Witty remark on smart home devices.",
            summary="Smart fridge suggests expired kale smoothie; smart speaker misunderstands 'play jazz' as 'order 6 pizzas'.",
        ),
        InputItem(
            prompt="Comedic take on group projects.",
            summary="Group of 5 students; 1 does all the work; 2 argue about font size; 2 vanish until submission day.",
        ),
    ]

    final = await tournament(
        packs=packs,
        inputs=inputs,
        iterations=5,
        samples_per_input=3,
        pairings=2,
        survivors=8,
        mutants_per_survivor=1,
        logdir="opt_logs",
    )

    print("Top 5:")
    for p in final[:5]:
        print(p.prompt_id, round(p.elo), p.style, p.structure)


if __name__ == "__main__":
    asyncio.run(main())
