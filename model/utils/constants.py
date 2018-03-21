COLORS = ("black", "white")
BLACK, WHITE = COLORS
COLORS_REV = tuple(reversed(COLORS))
EMPTY = ' '
MARKS = '?!'

DIRS = '+-<>'
UP, DOWN, LEFT, RIGHT = DIRS
STONES = 'FCS'
FLAT, CAP, STAND = STONES

TILE_SIZE = 40
SQUARE_SIZE = 75
ANIM_STEPS = 30
OFFSET_STEP = 3
PAD_STEP = 5

SIZES = {
    3: [10, 0],
    4: [15, 0],
    5: [21, 1],
    6: [30, 1],
    7: [40, 2],
    8: [50, 2]
}
