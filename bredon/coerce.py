import pickle
from model import *
import numpy as np
import os

def board_to_vector(board: Board):
    b = [0] * 512
    for i, row in enumerate(board.board):
        for j, sq in enumerate(row):
            for k, tile in enumerate(sq.tiles[-8:]):
                idx = k + j * 8 + i * 64
                i = STONES.index(tile.stone) + 1
                if tile.color == Colors.WHITE:
                    i += 3
                b[idx] = i
    return np.array(b)




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
    return np.array(v)


def vector_to_move(v):
    m = Move()
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

def non_normal_vtm(v):
    max_idx = lambda l: l.index(max(l))
    total = v[:8]
    col = v[8:16]
    row = v[16:24]
    moves = v[24:-4]
    moves = [moves[i:i+8] for i in range(0, len(moves), 8)]
    dire = v[-4:]

    m = Move()
    m.total = max_idx(total)
    m.col = ascii_lowercase[max_idx(col)]
    m.row = max_idx(row)
    for i in moves:
        m.moves.append(max_idx(i))
    m.direction = DIRS[3 - max_idx(dire)]

    return m


def color_iterator():
    yield Colors.BLACK
    yield Colors.WHITE
    while 1:
        yield Colors.WHITE
        yield Colors.BLACK

def load_features(fn):
    print("Reading:", fn)
    boards, moves = [], []
    # ptn = PTN()
    for b, m in load_moves_from_file(fn):
        # print(b, m)
        # print(m)
        # ptn.append(m)
        # b.force_move(m, next(c))
        try:
            boards.append(board_to_vector(b))
            moves.append(move_to_vector(str_to_move(m)))
        except Exception as e:
            print(e)
            # input()

    return boards, moves


def handle_features(fn):
    boards, moves = load_features(fn)
    moves = moves[1:]
    boards = boards[:-1]
    return boards, moves


def create_feature_sets_and_labels(files, test_size=0.1):
    features = []
    try:
        for file in files:
            features.extend(zip(*handle_features(file)))
    except KeyboardInterrupt:
        print("reading terminated")
    except:
        print("reading terminated b/c suck :)")
    random.shuffle(features)
    features = np.array(features)

    testing_size = int(test_size*len(features))

    train_x = np.array(list(features[:, 0][:-testing_size]))
    train_y = np.array(list(features[:, 1][:-testing_size]))
    test_x = np.array(list(features[:, 0][-testing_size:]))
    test_y = np.array(list(features[:, 1][-testing_size:]))

    return train_x, train_y, test_x, test_y


if __name__ == '__main__':
    os.chdir("/Volumes/External Hard Drive/tak_games/")
    files = os.listdir()
    train_x, train_y, test_x, test_y = create_feature_sets_and_labels(files)
    with open('../tak.pickle', 'wb') as f:
        pickle.dump([train_x, train_y, test_x, test_y], f)
        print("dumped")
