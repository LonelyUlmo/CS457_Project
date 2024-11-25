
from enum import Enum

class Role(Enum):
    SERVER = "server"
    CLIENT = "client"

class TicTacToe:
    def __init__(self, role) :
        self.role = role # role is a Role(Enum): { SERVER, CLIENT }
        self.players = {}
        self._init_board()
        self.turn = "X"

    def _init_board(self):
        self.board = {f"{col}{row}": " " for row in range(1, 3) for col in "ABC"}

    def _endTurn(self):
        if self.turn == "X":
            self.turn = "O"
        elif self.turn == "O": 
            self.turn = "X"

    def _opositeTeam(self, team):
        if team != "X" and team != "O":
            print("[Othello._opositeTeam()] Method incorrectly called. Expects \"X\" or \"O\".")
            return -1
        return "B" if team == "W" else "W"

    def getBoardState(self):
        return self.board.copy()
    
    def takeTurn(self, tile, value, team):
    # def takeTurn(self, tile, value):
        if self.turn != team:
            print("Invalid move. Not this player's turn.")
            return
        if self.board[tile] != "-":
            print("Invalid move. That tile is not blank.")
            return
        # implement functionality to: flip tiles, check valid move
        wasValidMove = self.tryMove(tile, value) > 0
        if wasValidMove:
            self._endTurn()
        else:
            print("Invalid move. You must select a tile that will sandwich opponent's tiles.")

    def tryMove(self, tile, value):
        neighbors = self.getNeighborOppositeTiles(tile, value)
        flipCount = 0
        for neighbor in neighbors:
            flipCount = 1 + self._updateInDirection(neighbor[0], neighbor[1][0], neighbor[1][1], value)
        if flipCount > 1:
            self.board[tile] = value
        return flipCount