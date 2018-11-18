import gym
from bredon.model import *
from .actions import *
import random
from bredon.view import *
import numpy as np
from rl.core import Env as RlEnv


class TakEnv(gym.Env, RlEnv):
    metadata = {'render.modes': ['ansi', 'human']}

    def __init__(self, size=5, players=None, board=None):
        self.size = size
        self.board = Board(size=size, board=board)
        self.players = players if players else []
        self.turn, self.move = 1, 1
        self.done = False
        self.vg = None

    def get_actions(self, player):
        return map(lambda i: Action(i, player), self.board.generate_valid_moves(self.turn, player.color, player.caps))

    def _step_turn(self):
        self.move = self.move % 2 + 1
        if self.move == 1:
            self.turn += 1

    def step(self, action):
        move = self.board.parse_move(action.move, action.color)
        # print(action)
        if isinstance(move, PseudoBoard) and move.bool:
            self.board.force(move)
        else:
            for m in move:
                if isinstance(move, PseudoBoard) and move.bool:
                    self.board.force(m)
                else:
                    return (self.get_state(), 0, False, {})

        self._step_turn()
        s, r, d, i = (self.get_state(),
                      self.board.evaluate(action.color),
                      self.board.winner(self.players),
                      {}  # TODO: implement info
                      )
        if d:
            self.done = True
        return s, r, d, i

    def get_state(self):
        arr = []
        for row in self.board.board:
            k = []
            for c in map(str, row):
                i = 0
                if len(c) > 6:
                    stone = c[6]
                    color = Colors.WHITE if c[0] == 'W' else Colors.BLACK
                    i = STONES.index(stone) + 1
                    if color == Colors.WHITE:
                        i += 3
                k.append(i)
            arr.append(k)
        return np.array(arr)

    def reset(self):
        self.board = Board(size=self.size)
        return self.get_state()

    def render(self, mode='ansi'):
        if True or mode == 'ansi':
            print(str(self.board))
        elif mode == 'human':
            if not self.vg:
                self.vg = ViewGame(size=self.board.size,
                                   board=self.board, white=HUMAN, black=HUMAN)
            else:
                self.vg._init_gui(board=self.board)
                self.vg.viz()

    def close(self):
        self.board = None

    def seed(self, seed=None):
        random.seed(seed)
        return [seed]

    def add_player(self, p: Player):
        self.players.append(p)

    def make_agent(self, color, class_, **kwargs):
        p = class_(env=self, color=color, board=self.board, **kwargs)
        self.add_player(p)
        return p


class ActTakEnv(TakEnv):
    def __init__(self, player, **kwargs):
        TakEnv.__init__(self, **kwargs)
        self.actions = Actions(self, player)
        self.players = [player]

    def step(self, n):
        action = Action.of(self.actions.get_at_idx(n))
        move = self.board.parse_move(action.move, action.color)
        # print(action)
        if isinstance(move, PseudoBoard) and move.bool:
            self.board.force(move)
        else:
            for m in move:
                if isinstance(move, PseudoBoard) and move.bool:
                    self.board.force(m)
                else:
                    return (self.get_state(), 0, False, {})

        self._step_turn()
        s, r, d, i = (self.get_state(),
                      self.board.evaluate(action.color),
                      self.board.winner(self.players),
                      {}  # TODO: implement info
                      )
        if d:
            self.done = True
        return s, r, d, i


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
        self.board = self.old_state.copy()


def hypoenv(env: TakEnv):
    return HypoEnv(size=env.size, players=env.players, board=env.board.board)
