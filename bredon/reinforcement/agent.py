from .env import *
from ..model import *
from random import sample
from tqdm import *
from rl.agents.dqn import DQNAgent


class TakAgent(Player, DQNAgent):
    def __init__(self, **kwargs):
        self.env = kwargs.pop("env")
        Player.__init__(self, **kwargs)