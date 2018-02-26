from model import *

# board = load_moves_from_file("games/sarras vs takkybot 18.1.27 14.15.ptn")
# print(board)
board = Board(5, 5)  # load_moves_from_file("You vs You 18.1.29 20.43.ptn")
board.force(board.parse_move(Move(col='a', row=5), BLACK))
board.force(board.parse_move(Move(col='e', row=5), WHITE))


ai = MinimaxAI(board, WHITE)
p = Player(board, BLACK)

while 1:
    while 1:
        ai_move = ai.pick_move()
        print(ai_move)
        try:
            ai.do(ai_move)
            break
        except ValueError as e:
            print("Error:", e)

    # board.force(board.parse_move(ai_move, ai.curr_player))
    # ai.switch_player()
    print(board)
    # my_move = board.parse_move()
    # while not board.valid(my_move):
    #     my_move = board.parse_move(input("Enter move: "), BLACK)
    while 1:
        try:
            p.do(str_to_move(input("Enter move: ")))
            break
        except Exception as e:
            print("Error:", e)
    print(board)
