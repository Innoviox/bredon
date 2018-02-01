from model.board import Board, WHITE, BLACK, load_moves_from_file as lmff
from model.ai import RandomAI, LookAhead1AI
from model.player import Player

board = Board(5, 5)  # load_moves_from_file("You vs You 18.1.29 20.43.ptn")
board.force(board.parse_move("a5", BLACK))
board.force(board.parse_move("e5", WHITE))


ai = LookAhead1AI(board, WHITE)
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
    p.do(input("Enter move: "))
    print(board)
