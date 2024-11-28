import TicTacToe
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler("temp.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
game = TicTacToe.TicTacToe(TicTacToe.Role.SERVER, logger)
# Print initial board
game.printBoard()

moves = [
    ("B2", "X"),
    ("A1", "O"),
    ("A2", "X"),
    ("A3", "O"),
    ("C2", "X"),
    ("C1", "O")
]
for move in moves:
    game.takeTurn(move[0], move[1])
    
print(game.getPrintableBoard())

handlers = logger.handlers[:]
for handler in handlers:
    handler.close()
    logger.removeHandler(handler)

logging.shutdown()