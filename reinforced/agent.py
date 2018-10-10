from .env import *
from model import *
from random import sample


class TakAgent(Player):
    ...

env = TakEnv(player_class=TakAgent)
agents = env.players


env.reset()

