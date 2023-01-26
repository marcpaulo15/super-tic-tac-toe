
class TicTacToeBasicBoard:
    # Parent class for TicTacToeBoard and SuperTicTacToeBoard
    # TODO: try to merge everything into this class:
    # board_type="local" or "global" to set the element_class and distance_pct

    def __init__(self):
        self.board = None
        self.tl = None
        self.width = None

    def __getattr__(self, name="winner"):
        # dynamic attribute, depends on board
        board = [e.winner for e in self.board]
        for player in (1, 2):
            winner_comb = [player]*3
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

        return 0

    def __getitem__(self, idx):
        # index directly on board attribute
        return self.board[idx]  # local_board or cell
