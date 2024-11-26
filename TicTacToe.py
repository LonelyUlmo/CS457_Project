
from enum import Enum
import logging

class Role(Enum):
    SERVER = "server"
    CLIENT = "client"

class TicTacToe:
    def __init__(self, role, logger) :
        self.role = role # role is a Role(Enum): { SERVER, CLIENT }
        self.logger = logger
        self.players = {}
        self.ROWs = range(1, 4)
        self.COLs = "ABC"
        self._init_board()
        self.turn = "X"
        self.liveGame = True
        self.logger.info(f"Initializations completed.")

    def _init_board(self):
        self.board = {f"{col}{row}": "-" for row in self.ROWs for col in self.COLs}
        self.logger.info(f"Board initialized.")

    def _checkWinConditions(self, team):
        # Check rows
        for row in self.ROWs:
            if all(self.board[f"{col}{row}"] == team for col in self.COLs):
                return True
        # Check columns
        for col in self.COLs:
            if all(self.board[f"{col}{row}"] == team for row in self.ROWs):
                return True
        # Check diagonals
        if self.board["A1"] == team and self.board["B2"] == team and self.board["C3"] == team:
            return True
        if self.board["C1"] == team and self.board["B2"] == team and self.board["A3"] == team:
            return True
        return False

    def _endTurn(self, team):
        # Check for win conditions
        if self._checkWinConditions(team):
            self.liveGame = False
            # print(f"{team} wins!")
            self.logger.info(f"{team} wins!")
            return
        # Check for deadlock
        if all(value != "-" for value in self.board.values()):
            self.liveGame = False
            # print("Deadlock, there is no winner. Game over.")
            self.logger.info("Deadlock, there is no winner. Game over.")
            return
        # If not, iterate turn to next player.
        self.turn = "O" if self.turn == "X" else "X"
        self.logger.info(f"Turn is passed to {self.turn}.")

    def getBoardState(self):
        self.logger.info(f"getBoardState() is called.")
        return self.board.copy()
    
    def takeTurn(self, tile, value, team):
        # Check if game is stil live.
        if not self.liveGame:
            # print("The game is over. No more turns.")
            self.logger.info("The game is over. No more turns.")
            return
        # Check if move is valid
        if self.turn != team:
            # print("Invalid move. Not this player's turn.")
            self.logger.info("Invalid move. Not this player's turn.")
            return
        if tile not in {"A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"}:
            # print("Invalid move. That tile is not valid.")
            self.logger.info("Invalid move. That tile is not valid.")
            return
        if self.board[tile] != "-":
            # print("Invalid move. That tile is not blank.")
            self.logger.info("Invalid move. That tile is not blank.")
            return
        # Take turn
        self.board[tile] = value
        self.logger.info(f"{team} takes turn and marks {tile}.")
        self._endTurn(team)
    
    def printBoard(self):
        print("      " + "     ".join(col for col in self.COLs))
        for row in self.ROWs:
            print(f"{row} | " + "".join(f"{self.board[f'{col}{row}']:^6}" for col in self.COLs))
        print()

    def isLive(self):
        self.logger.info(f"isLive() is called.")
        return self.liveGame