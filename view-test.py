from view import *
from controller import *

g = ViewGame(size=4, white_type=(AI, 3), black_type=(AI, 3)) # black_type=HUMAN)
g.run()