"""
Chess Piece Movement - King

Implements movement rules for the king piece.
Handles standard one-square moves in any direction.
"""

from utils.constants import ROWS, COLS


def get_king_moves(board, from_row, from_col, color):
    """
    Get all possible king moves (one square in any direction).
    Does not include castling - that's handled separately.
    
    Args:
        board: Board object
        from_row, from_col: Starting position
        color: 'white' or 'black'
    
    Returns:
        List of (to_row, to_col) tuples
    """
    moves = []
    
    # All 8 adjacent squares
    for row_offset in [-1, 0, 1]:
        for col_offset in [-1, 0, 1]:
            if row_offset == 0 and col_offset == 0:
                continue  # Skip current position
            
            new_row = from_row + row_offset
            new_col = from_col + col_offset
            
            # Check if in bounds
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                target_color = board.get_piece_color(new_row, new_col)
                # Can move if empty or opponent's piece
                if target_color != color:
                    moves.append((new_row, new_col))
    
    return moves
