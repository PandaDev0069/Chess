"""
Chess Board Representation

Provides the chess board data structure and basic operations.
Manages board state, piece positioning, and board queries.
Pure Python implementation with no UI dependencies.
"""

from utils.constants import ROWS, COLS, INITIAL_BOARD


class Board:
    """Represents the chess board state."""
    
    def __init__(self):
        """Initialize board with starting position."""
        self.board = [row[:] for row in INITIAL_BOARD]  # Deep copy
    
    def get_piece(self, row, col):
        """Get piece at given position."""
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None
    
    def set_piece(self, row, col, piece):
        """Set piece at given position."""
        if 0 <= row < ROWS and 0 <= col < COLS:
            self.board[row][col] = piece
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move piece from one position to another (no validation)."""
        piece = self.get_piece(from_row, from_col)
        self.set_piece(to_row, to_col, piece)
        self.set_piece(from_row, from_col, ' ')
        return piece
    
    def is_empty(self, row, col):
        """Check if square is empty."""
        return self.get_piece(row, col) == ' '
    
    def is_white_piece(self, piece):
        """Check if piece belongs to white."""
        return piece.isupper() if piece else False
    
    def is_black_piece(self, piece):
        """Check if piece belongs to black."""
        return piece.islower() if piece else False
    
    def get_piece_color(self, row, col):
        """Get color of piece at position ('white', 'black', or None)."""
        piece = self.get_piece(row, col)
        if piece == ' ':
            return None
        return 'white' if self.is_white_piece(piece) else 'black'
    
    def find_king(self, color):
        """Find the position of the king for given color."""
        king = 'K' if color == 'white' else 'k'
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == king:
                    return (row, col)
        return None
    
    def get_all_pieces(self, color):
        """Get all pieces of a given color."""
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != ' ':
                    if (color == 'white' and self.is_white_piece(piece)) or \
                       (color == 'black' and self.is_black_piece(piece)):
                        pieces.append((row, col, piece))
        return pieces
    
    def copy(self):
        """Create a deep copy of the board."""
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        return new_board
    
    def __str__(self):
        """String representation for debugging."""
        result = "  a b c d e f g h\n"
        for i, row in enumerate(self.board):
            result += f"{8-i} {' '.join(row)} {8-i}\n"
        result += "  a b c d e f g h"
        return result
