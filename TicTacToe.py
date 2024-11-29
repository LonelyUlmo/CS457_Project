
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
            response = f"{team} wins! Game over."
            self.logger.info(response) # TODO: send to clients
            return response
        # Check for deadlock
        if all(value != "-" for value in self.board.values()):
            self.liveGame = False
            response = "Deadlock, there is no winner. Game over."
            self.logger.info(response) # TODO: send to clients
            return response
        # If not, iterate turn to next player.
        self.turn = "O" if self.turn == "X" else "X"
        response = f"Turn is passed to {self.turn}."
        self.logger.info(response) # TODO: send to clients
        return response
    
    def takeTurn(self, tile, team):
        # Check if game is stil live.
        if not self.liveGame:
            response = "The game is over. No more turns."
            self.logger.info(response)
            return response
        # Check if move is valid
        if self.turn != team:
            response = f"Player {team} tried to go out of turn. It is {self.turn}'s turn."
            # response = "Invalid move. Not this player's turn."
            self.logger.info(response)
            return response
        if tile not in {"A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"}:
            response = f"Invalid move by player {team}. {tile} is not a valid tile."
            self.logger.info(response)
            return response
        if self.board[tile] != "-":
            response = f"Invalid move by {team}. {tile} is not blank."
            self.logger.info(response)
            return response
        # Take turn
        self.board[tile] = team
        response = f"{team} takes their turn and marks {tile}."
        self.logger.info(response)
        return response + "\n" + self._endTurn(team)
    
    def getPrintableBoard(self):
        board_output = ""
        board_output += "      " + "     ".join(col for col in self.COLs) + "\n"
        for row in self.ROWs:
            board_output += f"{row} | " + "".join(f"{self.board[f'{col}{row}']:^6}" for col in self.COLs) + "\n"
        # Return the final string
        return board_output

    def isLive(self):
        self.logger.info(f"isLive() is called.")
        return self.liveGame