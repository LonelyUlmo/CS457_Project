import othello

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
game = othello.Othello(othello.Role.SERVER)
board = game.board
# Print initial board
# game.printBoard()

moves = [
    ("E3", "W", "white"),
    ("F3", "B", "black"),
    ("F3", "W", "white"),
    ("C5", "W", "white")
]

for move in moves:
    # print(game.turn)
    print(move)
    game.takeTurn(move[0], move[1], move[2])
    game.printBoard()
    print(game.turn)
