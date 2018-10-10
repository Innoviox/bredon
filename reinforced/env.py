import gym
from model import *
import random

class TakEnv(gym.Env):
    metadata = {'render.modes': ['ansi']}

    def __init__(self, size=5, player_class=Player, board=None):
        self.size = size
        self.board = Board(size=size, board=board)
        self.player_class = player_class
        self.players = [player_class(self.board, Colors.WHITE), player_class(self.board, Colors.BLACK)]
        self.turn, self.move = 1, 1

    def get_actions(self, player):
        return self.board.generate_valid_moves(self.turn, player.color, player.caps)

    def _step_turn(self):
        self.move = self.move % 2 + 1
        if self.move == 1:
            self.turn += 1

    def step(self, action):
        move = self.board.parse_move(action.move, action.color)
        if isinstance(move, PseudoBoard) and move.bool:
            self.board.force(move)
            self._step_turn()
            return (self.board.board,
                    self.board.evaluate(action.color),
                    self.board.winner(self.players),
                    {} # TODO: implement info
                    )
        else:
            raise ValueError("Illegal Move")

    def reset(self):
        self.board = Board(size=self.size)

    def render(self, mode='ansi'):
        if mode == 'ansi':
            return str(self.board)

    def close(self):
        self.board = None

    def seed(self, seed=None):
        random.seed(seed)
        return [seed]

class HypoEnv(TakEnv):
    def __init__(self, **kwargs):
        TakEnv.__init__(self, **kwargs)
        self.old_state = self.board.copy()
        
    def step(self, action):
        ret = super().step(action)
        self.old_state = self.board.copy()
        return ret
        
    def hypostep(self, action):
        return super().step(action)
    
    def unstep(self):
        self.state = self.old_state.copy()

def hypoenv(env: TakEnv):
    return HypoEnv(size=env.size, player_class=env.player_class, board=env.board.board)
