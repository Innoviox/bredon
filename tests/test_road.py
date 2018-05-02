from model import *

TEST_SIZE = 4

def exec_road(threat, size):
    """
    Threat types:
    1) column or row (straight) e.g. "a", "1"
    2) bent "{start}{start_dir}{bend-position}{new_dir}..." e.g.
        - c1+2<b+
    """

    b = Board(size)
    if len(threat) == 1:
        if threat in ascii_lowercase:
            return exec_road(threat + "1+", size)
        return exec_road("a" + threat + ">", size)
    else:
        srow, col, direction, *road = threat
        row, col = tile_to_coords(srow + col)

        sq = b.get(row, col)
        sqs = [coords_to_tile(sq.x, sq.y)]
        for bend, nd in zip(road[::2], road[1::2]):
            cond = True
            while cond:
                if direction in UP + DOWN:
                    cond = sq.x < int(bend) - 1
                else:
                    cond = sq.y < ascii_lowercase.index(bend)
                if not cond:
                    direction = nd
                sq = b.get(*sq.next(direction, size))
                sqs.append(coords_to_tile(sq.x, sq.y))

        while True:
            nsq = b.get(*sq.next(direction, size))
            if (nsq.x, nsq.y) == (sq.x, sq.y):
                break
            sq = nsq
            sqs.append(coords_to_tile(sq.x, sq.y))
        return sqs


def test_straight_roads():
    def _test(c, z2):
        b = Board(TEST_SIZE)
        ms = ""
        for m in zip(c if len(c) == TEST_SIZE else c * TEST_SIZE, z2):
            b.force_str(''.join(m), Colors.WHITE)
            ms += ''.join(m) + " "
            if len(ms.split()) < TEST_SIZE:
                try:
                    assert b.road() == False
                    print(ms, "worked!")
                except:
                    print(ms, "did not work")
                    print(b)
                    print(b.road())
                    input()
        try:
            assert b.road() == Colors.WHITE
            print(ms, "worked!")
        except:
            print(ms, "did not work")
            print(b)
            print(b.road())
            input()

    for c in "abcd":
        _test(c, "1234")
    for d in "1234":
         _test("abcd", d * TEST_SIZE)

test_straight_roads()