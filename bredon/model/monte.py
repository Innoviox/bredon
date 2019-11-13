from mcts import mcts
from .utils import *

class State(Board):
    def __init__(self, players=None, current_player=Colors.BLACK, turn=1, *args, **kwargs):
        super(Board, self).__init__(self, *args, **kwargs)
        self.current_player = current_player
        self.turn = turn
        self.players = players if players else {i: Player(self, i) for i in Colors}

    # MCTS Protocol Implementation
    def getPossibleActions(self):
        p = self.cp
        return self.generate_all_moves(self.turn, p.color, p.caps)

    def takeAction(self, action):
        return self.copy().step_current(action)

    def isTerminal(self):
        return bool(self.winner(self.players))

    def getReward(self):
        w = self.winner(self.players)
        if w == self.current_player:
            return 1
        elif w:
            return -1
        return 0

    # Helper Methods
    @property
    def cp(self):
        return self.players[self.current_player]

    def copy(self):
        return State(players=self.players, current_player=self.current_player, turn=self.turn, size=self.size, board=self.copy_board())

    def step_current(self, action):
       p = self.cp
       p._do(action, p.color)
       return self

    def step(self, action, color):
        self.players[color]._do(action, color)
        self.current_player.flip()