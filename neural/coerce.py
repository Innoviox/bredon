import pickle
from model import *

def gen_classes(size):
    for c in cols[:size]:
        for r in range(1, size + 1):
            for s in stones:
                yield s + c + str(r)
            for t in range(1, size + 1):
                for ms in sums(t):
                    for d in dirs:
                        yield str(t) + c + str(r) + d + ''.join(map(str, ms))

def board_to_vector(b):
    #TODO: Board to vector
    ...

def move_to_vector(m):
    #TODO: Move to vector
    ...

def load_features(fn):
    print("Reading:", fn)
    boards, moves = [], []
    for b, m in load_moves_from_file(fn):
        boards.append(board_to_vector(b))
        moves.append(move_to_vector(m))
    return boards, moves


def handle_features(fn):
    boards, moves = load_features(fn)
    moves = moves[1:]
    boards = boards[:-1]
    return boards, moves

def create_feature_sets_and_labels(file, test_size = 0.1):
    features = list(zip(*handle_features(file)))
    random.shuffle(features)
    features = np.array(features)

    testing_size = int(test_size*len(features))

    train_x = list(features[:,0][:-testing_size])
    train_y = list(features[:,1][:-testing_size])
    test_x = list(features[:,0][-testing_size:])
    test_y = list(features[:,1][-testing_size:])

    return train_x,train_y,test_x,test_y
