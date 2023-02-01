from typing import Tuple


class TicTacToeBasicBoard:
    """
    TicTacToeBasicBoard Implements the basic functionalities that both Local
        and global boards share in the Super Tic-Tac-Toe game. This class is
        intended to be used as a Parent Class for TicTacToeBoard and
        SuperTicTacToeBoard classes.

    TicTacToeBasicBoard Attributes
        width      - board's shape is a {width}x{width} square
        topleft    - coordinates of the top-left corner of the board

    TicTacToeBasicBoard Methods
        winner     - check if there is a winner on the current board
    """

    def __init__(self, topleft: Tuple[float, float], width: int) -> None:
        """
        Inits a TicTacToeBasicBoard instance at a given location with a given
        width

        :param topleft: coordinates of the top-left corner of the board
        :param width: length of the square defining the board's shape
        """

        self.board = None
        self.topleft = topleft
        self.width = width

    def winner(self):
        """
        Check if there is a winner or game is draw based on the current board
        :return: -1 if the game is a draw, 0 if the game is running,
            1 if player1 has won, 2 if player2 has won
        """

        board = [e.winner() for e in self.board]
        for player in (1, 2):
            winner_comb = [player] * 3
            # check winner by rows
            for i in range(0, 9, 3):
                row = [board[i], board[i+1], board[i+2]]
                if row == winner_comb:
                    return player
            # check winner by columns
            for j in range(3):
                col = [board[j], board[j+3], board[j+6]]
                if col == winner_comb:
                    return player
            # check winner by diagonals
            asc_diag = [board[0], board[4], board[8]]
            if asc_diag == winner_comb:
                return player
            desc_diag = [board[6], board[4], board[2]]
            if desc_diag == winner_comb:
                return player

        # if there is no winner, check if the game is a draw
        num_filled_cells = 0
        for cell_state in board:
            num_filled_cells += int(cell_state > 0)

        # if num_filled_cells is 9, there aren't legal moves to play: game draw
        return -1 if num_filled_cells == 9 else 0

    def __getitem__(self, idx):
        """
        Allows to index directly on the board attribute
        :param idx: cell or local board index
        :return: a cell if indexing a local board,
            a local board if indexing a global board
        """
        return self.board[idx]
