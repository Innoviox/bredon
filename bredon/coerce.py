import pickle
from .model import *
import numpy as np

def board_to_vector(ptn: PTN):
    m, s, c = ptn.to_moves()
    board = Board.from_moves(m, 8, c, s)
    b = [0] * 512
    for i, row in enumerate(board.board):
        for j, sq in enumerate(row):
            for k, tile in enumerate(sq.tiles[-8:]):
                idx = k + j * 8 + i * 64
                i = STONES.index(tile.stone) + 1
                if tile.color == Colors.WHITE:
                    i += 3
                b[idx] = i
    return b




def move_to_vector(m: Move):
    '''
    Converts a move to a vector of 1s and 0s.

    The 1s and 0s are in the following format:
    First 8 slots: if the person is moving tiles, how many
    Next 8 slots: what column
    Next 8 slots: what row
    Next 64 slots: how much the player is moving
    Last 4 slots: what direction
    ---
    Total: 80 slots
    :param m:
    :return:
    '''
    v = [0] * 84
    i = -1
    for k in [m.total, m.get_col_n(), m.row, *m.moves]:
        v[int(k) + i] = 1
        i += 8
    if m.direction:
        v[-DIRS.index(m.direction)-1] = 1
    return v


def vector_to_move(v):
    m = Move()
    print(v)
    m.total = v.index(1) + 1
    m.col = ascii_lowercase[v.index(1, 7) - 7]
    m.row = v.index(1, 15) - 15
    for i in range(23, 79, 8):
        if 1 in v[i:i+8]:
            m.moves.append(v[i:i+8].index(1))
    try:
        m.direction = DIRS[3 - (v.index(1, 80) - 80)]
    except ValueError:
        # move is a placement
        pass
    return m

def load_features(fn):
    print("Reading:", fn)
    boards, moves = [], []
    ptn = PTN()
    for m in load_moves_from_file(fn):
        ptn.append(m)
        boards.append(board_to_vector(ptn))
        moves.append(move_to_vector(m))
    return boards, moves


def handle_features(fn):
    boards, moves = load_features(fn)
    moves = moves[1:]
    boards = boards[:-1]
    return boards, moves


def create_feature_sets_and_labels(files, test_size=0.1):
    features = []
    for file in files:
        features.extend(zip(*handle_features(file)))
    random.shuffle(features)
    features = np.array(features)

    testing_size = int(test_size*len(features))

    train_x = list(features[:, 0][:-testing_size])
    train_y = list(features[:, 1][:-testing_size])
    test_x = list(features[:, 0][-testing_size:])
    test_y = list(features[:, 1][-testing_size:])

    return train_x, train_y, test_x, test_y


if __name__ == '__main__':
    move = Move.of('a1')
    print(vector_to_move(move_to_vector(move)))

    move = Move.of('8b4+2213')
    print(vector_to_move(move_to_vector(move)))

    move = Move.of('2b4>2')
    print(vector_to_move(move_to_vector(move)))


    #files = []
    #train_x, train_y, test_x, test_y = create_feature_sets_and_labels(files)
    #with open('note_features.pickle', 'wb') as f:
    #    pickle.dump([train_x, train_y, test_x, test_y], f)
