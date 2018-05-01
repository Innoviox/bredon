from model import *

TEST_SIZE = 4

def exec_road(threat, size):
    """
    Threat types:
    1) column or row (straight) e.g. "a", "1"
    2) bent "{start}{bend-position}{new_dir}..." e.g.
        - c1+2<b+
    """

    b = Board(size)
    if len(threat) == 1:
        # straight threat
        pass
    else:
        srow, col, direction, *road = threat
        row, col = tile_to_coords(srow + col)

        bends, new_dirs = [], []
        while road:
            bends.append(road.pop(0))
            new_dirs.append(road.pop(0))

        sq = b.get(row, col)
        for bend, nd in zip(bends, new_dirs):
            print(direction, sq, bend, nd, sq.x, sq.y)
            if direction in UP + DOWN:
                cond = sq.x < int(bend) #ascii_lowercase.index(bend)
            else:
                cond = sq.y < int(bend)
            if cond:
                sq = b.get(*sq.next(direction, size))
            else:
                direction = nd
            print(cond, sq)


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