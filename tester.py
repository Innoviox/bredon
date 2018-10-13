from reinforcement import *

env = TakEnv()
actions = Actions(env)

env.add_player(make_agent(env, Colors.WHITE))
env.add_player(make_agent(env, Colors.BLACK))
for i in range(20):
    for p in env.players:
        act = actions.sample(p)
        print(act)
        env.step(act)
        env.render("human")
        input()