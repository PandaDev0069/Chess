"""
Phase 1: Core Chess Logic - Pawn Movement
Pure logic for pawn movement rules (no game state, no pygame).
"""

from utils.constants import ROWS, COLS


def get_pawn_moves(board, from_row, from_col, color):
    """
    Get all possible pawn moves (without considering check).
    
    Args:
        board: Board object
        from_row, from_col: Starting position
        color: 'white' or 'black'
    
    Returns:
        List of (to_row, to_col) tuples
    """
    moves = []
    direction = -1 if color == 'white' else 1
    start_row = 6 if color == 'white' else 1
    
    # Forward one square
    new_row = from_row + direction
    if 0 <= new_row < ROWS and board.is_empty(new_row, from_col):
        moves.append((new_row, from_col))
        
        # Forward two squares from starting position
        if from_row == start_row:
            new_row2 = from_row + 2 * direction
            if board.is_empty(new_row2, from_col):
                moves.append((new_row2, from_col))
    
    # Diagonal captures
    for col_offset in [-1, 1]:
        new_col = from_col + col_offset
        new_row = from_row + direction
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            target_piece = board.get_piece(new_row, new_col)
            if target_piece != ' ':
                target_color = board.get_piece_color(new_row, new_col)
                if target_color != color:
                    moves.append((new_row, new_col))
    
    return moves


def can_en_passant(board, from_row, from_col, to_row, to_col, en_passant_target):
    """
    Check if en passant capture is possible.
    
    Args:
        en_passant_target: (row, col) where en passant is possible, or None
    """
    if en_passant_target is None:
        return False
    return (to_row, to_col) == en_passant_target


def is_promotion_move(to_row, color):
    """Check if pawn move results in promotion."""
    if color == 'white':
        return to_row == 0
    else:
        return to_row == 7
