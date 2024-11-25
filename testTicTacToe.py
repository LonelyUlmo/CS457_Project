import TicTacToe

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
game = TicTacToe.TicTacToe(TicTacToe.Role.SERVER)
board = game.board
# Print initial board
game.printBoard()

moves = [
    ("B2", "X", "X"),
    ("A1", "O", "O"),
    ("A2", "X", "X"),
    ("A3", "O", "O"),
    ("C2", "X", "X"),
    ("C1", "O", "O")
]
print(game.liveGame)
for move in moves:
    # print(move)
    game.takeTurn(move[0], move[1], move[2])
    # game.printBoard()
    # print(game.turn)

print(game.liveGame)