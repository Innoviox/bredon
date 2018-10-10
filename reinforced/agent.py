from .env import *
from model import *
from random import sample


class TakAgent(Player):
    pass

class HypoTakAgent(TakAgent):
    def __init__(self, **kwargs):
        self.depth = kwargs.pop("depth")
        self.env = kwargs.pop("env")
        TakAgent.__init__(self, **kwargs)
       
    def solve(self):
        self.rewards = {i: 0 for i in self.env.get_actions(self)}
        return self._solve(self.depth, hypoenv(self.env))
    
    def _solve(self, depth, env):
        if depth == 0: return
        actions = env.get_actions(self)
        for a in actions:
            s, r, d, i = env.hypostep(a)
            results[a] += r
            self._solve(depth - 1, env)
            env.unstep()
            
    
env = TakEnv(player_class=HypoTakAgent)
agents = env.players


env.reset()

