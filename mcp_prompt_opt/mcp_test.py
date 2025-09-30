from mcp_server import health, optimize, best_prompt

print(health())

best = best_prompt(
    prompt="Make a witty short about elevators",
    summary="Awkward silence, 30s, doors ding",
    allow_quick_opt=True
)
print(best)

opt = optimize(
    prompt="Short caption on startup feature creep",
    summary="Startup adds 5 toggles to reduce confusion; users are more confused; PM writes memo.",
    n_new=8,       
    iterations=1,
    samples_per_input=2,
    pairings=1
)
print(opt)
