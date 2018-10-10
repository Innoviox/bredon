import gym
from model import *
import random

class TakEnv(gym.Env):
    metadata = {'render.modes': ['ansi']}

    def __init__(self, size=5, player_class=Player):
        self.size = size
        self.board = Board(size=size)
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