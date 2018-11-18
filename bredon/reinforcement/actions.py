from bredon.model import *
from rl.core import Space as RlSpace
import random

class Action:
    def __init__(self, move, player):
        self.move = move
        try:
            self.color = player.color
        except:
            self.color = player

    def __repr__(self):
        return str(self.color) + ":" + str(self.move)

    @staticmethod
    def of(s):
        c, m = s.split(":")
        return Action(Move.of(m), Colors.of(c))

class Actions(RlSpace):
    def __init__(self, env, player):
        self.env = env
        self.player = player

    def sample(self, seed=None):
        return random.choice(self.get_valid())

    def contains(self, x):
        return str(x) in self.get_valid_str()

    def get_valid(self):
        return list(self.env.get_actions(self.player))

    def get_valid_str(self):
        return list(map(str, self.get_valid()))

    def get_rand_idx(self):
        return self.get_valid_str().index(str(self.sample()))

    def get_at_idx(self, n):
        return self.get_valid_str()[n]