import TicTacToe
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler("server.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
game = TicTacToe.TicTacToe(TicTacToe.Role.SERVER, logger)
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

handlers = logger.handlers[:]
for handler in handlers:
    handler.close()
    logger.removeHandler(handler)

logging.shutdown()