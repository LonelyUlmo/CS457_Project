# The Othello class is to represent the game-state and functionality of an Othello game.
# This class is to be used for both libserver.py and libclient.py

from enum import Enum

# Identify if the Othello object is for servers of clients
class Role(Enum):
    SERVER = "server"
    CLIENT = "client"

class Othello:
    def __init__(self, role) :
        self.role = role # role is a Role(Enum): { SERVER, CLIENT }
        self.players = {}
        self.__init_board()

    def _init_board(self):
        self.board = {f"{col}{row}": "empty" for row in range(1, 9) for col in "ABCDEFGH"}
        self.board["D4"], self.board["E5"] = "white"
        self.board["D5"], self.board["E4"] = "black"

    # Returns a copy of the board state
    def getBoardState(self):
        return self.board.copy()
    
    def setBoardTile(self, tile, value):
        if self.role == Role.CLIENT : # Is this where I want to check authorization?
            print("[Othello.setBoardTile()] Must be a server")
            return
        self.board[tile] = value
        # implement functionality to: flip tiles, check valid move