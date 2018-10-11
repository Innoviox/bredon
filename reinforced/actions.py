from model import *

class Action:
    def __init__(self, move, player):
        self.move = move
        try:
            self.color = player.color
        except:
            self.color = player

    def __repr__(self):
        return str(self.color) + ":<" + str(self.move) + ">"

    @staticmethod
    def of(s):
        c, m = s.split(":")
        m = m[1:-1]
        return Action(Move.of(m), Colors.of(c))