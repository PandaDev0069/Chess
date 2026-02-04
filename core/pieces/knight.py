"""
Phase 1: Core Chess Logic - Knight Movement
Pure logic for knight movement rules.
"""

from utils.constants import ROWS, COLS


def get_knight_moves(board, from_row, from_col, color):
    """
    Get all possible knight moves (L-shaped: 2+1 or 1+2).
    
    Args:
        board: Board object
        from_row, from_col: Starting position
        color: 'white' or 'black'
    
    Returns:
        List of (to_row, to_col) tuples
    """
    moves = []
    
    # All 8 possible L-shaped moves
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    for row_offset, col_offset in knight_moves:
        new_row = from_row + row_offset
        new_col = from_col + col_offset
        
        # Check if in bounds
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            target_color = board.get_piece_color(new_row, new_col)
            # Can move if empty or opponent's piece
            if target_color != color:
                moves.append((new_row, new_col))
    
    return moves
