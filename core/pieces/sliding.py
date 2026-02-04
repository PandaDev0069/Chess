"""
Phase 1: Core Chess Logic - Sliding Pieces (Bishop, Rook, Queen)
Shared logic for pieces that move in straight lines.
"""

from utils.constants import ROWS, COLS


def get_sliding_moves(board, from_row, from_col, color, directions):
    """
    Generic function for sliding pieces (bishop, rook, queen).
    
    Args:
        board: Board object
        from_row, from_col: Starting position
        color: 'white' or 'black'
        directions: List of (row_step, col_step) tuples
    
    Returns:
        List of (to_row, to_col) tuples
    """
    moves = []
    
    for row_step, col_step in directions:
        current_row = from_row + row_step
        current_col = from_col + col_step
        
        while 0 <= current_row < ROWS and 0 <= current_col < COLS:
            target_color = board.get_piece_color(current_row, current_col)
            
            if target_color is None:
                # Empty square - can move here
                moves.append((current_row, current_col))
            elif target_color != color:
                # Opponent's piece - can capture
                moves.append((current_row, current_col))
                break  # Can't move further
            else:
                # Own piece - blocked
                break
            
            current_row += row_step
            current_col += col_step
    
    return moves


def get_bishop_moves(board, from_row, from_col, color):
    """Get all possible bishop moves (diagonal)."""
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return get_sliding_moves(board, from_row, from_col, color, directions)


def get_rook_moves(board, from_row, from_col, color):
    """Get all possible rook moves (horizontal/vertical)."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return get_sliding_moves(board, from_row, from_col, color, directions)


def get_queen_moves(board, from_row, from_col, color):
    """Get all possible queen moves (bishop + rook)."""
    directions = [
        (-1, -1), (-1, 1), (1, -1), (1, 1),  # Diagonal
        (-1, 0), (1, 0), (0, -1), (0, 1)      # Straight
    ]
    return get_sliding_moves(board, from_row, from_col, color, directions)
