# This Othello class is to represent the game-state and functionality of an Othello game.
# This class is to be used for both servers and clients.

from enum import Enum

# Identify if the Othello object is for servers of clients
class Role(Enum):
    SERVER = "server"
    CLIENT = "client"

class Othello:
    def __init__(self, role) :
        self.role = role # role is a Role(Enum): { SERVER, CLIENT }
        self.players = {}
        self._init_board()
        self.turn = "white"

    def _init_board(self):
        self.board = {f"{col}{row}": "-" for row in range(1, 9) for col in "ABCDEFGH"}
        self.board["D4"] = "W"
        self.board["E5"] = "W"
        self.board["D5"] = "B"
        self.board["E4"] = "B"

    def _endTurn(self):
        if self.turn == "white":
            self.turn = "black"
        else: 
            self.turn = "white"

    def _opositeColor(self, color):
        if color != "W" and color != "B":
            print("[Othello._opositeColor()] Method incorrectly called. Expects \"W\" or \"B\".")
            return -1
        return "B" if color == "W" else "W"

    def getBoardState(self):
        return self.board.copy()
    
    def takeTurn(self, tile, value, player):
    # def takeTurn(self, tile, value):
        if self.turn != player:
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

    def _updateInDirection(self, tile, col_diff, row_diff, color):
        # check if tile is right color
        if self.board[tile] == "-":
            return 0
        if self.board[tile] == color:
            return 1 # Return 1 to update all the tiles before this one! All the way back to the recursive source
        # get coordinates of next neighbor
        # (chr(ord(col) - 1)
        next_col = chr(ord(tile[0]) + col_diff)
        next_row = int(tile[1]) + row_diff
        neighbor = f"{next_col}{next_row}"
        # recursive call on next neighbor
        flipCount = self._updateInDirection(neighbor, col_diff, row_diff, color)
        if flipCount == 0:
            return 0
        self.board[tile] = color
        return flipCount + 1

    def getNeighborOppositeTiles(self, tile, color):
        col = tile[0]
        row = int(tile[1])
        # Possible neighbors with directions
        neighbors = [
            ((chr(ord(col) + col_offset), row + row_offset), (col_offset, row_offset))
            for col_offset in [-1, 0, 1]
            for row_offset in [-1, 0, 1]
            if not (col_offset == 0 and row_offset == 0) ]
        # Filter valid neighbors with directions
        valid_neighbors = {
            (f"{c}{r}", neighbor) 
            for ((c, r), neighbor) in neighbors 
            if 'A' <= c <= 'H' and 1 <= r <= 8 and self.board[f"{c}{r}"] == self._opositeColor(color) }
        return valid_neighbors

    # for updating client's board
    def updateBoard(self, board):
        self.board = board

    def printBoard(self):
        print("      " + "     ".join(col for col in "ABCDEFGH"))
        for row in range(1, 9):  # Rows from 1 to 8 for a game-like display
            print(f"{row} | " + "".join(f"{self.board[f'{col}{row}']:^6}" for col in "ABCDEFGH"))
        print()