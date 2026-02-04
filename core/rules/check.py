"""
Chess Rules Engine - Check Detection

Implements check detection logic.
Determines when a king is in check or if squares are under attack.
"""

from core.pieces import pawn, knight, king
from core.pieces.sliding import get_bishop_moves, get_rook_moves, get_queen_moves
from utils.constants import ROWS, COLS


def is_square_attacked(board, row, col, by_color):
    """
    Check if a square is attacked by any piece of the given color.
    
    Args:
        board: Board object
        row, col: Square to check
        by_color: 'white' or 'black' - attacking color
    
    Returns:
        Boolean indicating if square is under attack
    """
    # Check all pieces of the attacking color
    for r in range(ROWS):
        for c in range(COLS):
            piece = board.get_piece(r, c)
            if piece == ' ':
                continue
            
            piece_color = board.get_piece_color(r, c)
            if piece_color != by_color:
                continue
            
            # For pawns, check attack squares (different from movement)
            if piece.lower() == 'p':
                direction = -1 if by_color == 'white' else 1
                for col_offset in [-1, 1]:
                    attack_row = r + direction
                    attack_col = c + col_offset
                    if attack_row == row and attack_col == col:
                        return True
            else:
                # For other pieces, check if target square is in their moves
                moves = get_piece_moves(board, r, c, piece_color, piece.lower())
                if (row, col) in moves:
                    return True
    
    return False


def get_piece_moves(board, row, col, color, piece_type):
    """Helper to get moves for any piece type."""
    if piece_type == 'n':
        return knight.get_knight_moves(board, row, col, color)
    elif piece_type == 'b':
        return get_bishop_moves(board, row, col, color)
    elif piece_type == 'r':
        return get_rook_moves(board, row, col, color)
    elif piece_type == 'q':
        return get_queen_moves(board, row, col, color)
    elif piece_type == 'k':
        return king.get_king_moves(board, row, col, color)
    elif piece_type == 'p':
        return pawn.get_pawn_moves(board, row, col, color)
    return []


def is_in_check(board, color):
    """
    Check if the king of the given color is in check.
    
    Args:
        board: Board object
        color: 'white' or 'black'
    
    Returns:
        Boolean indicating if king is in check
    """
    king_pos = board.find_king(color)
    if not king_pos:
        return False
    
    opponent_color = 'black' if color == 'white' else 'white'
    return is_square_attacked(board, king_pos[0], king_pos[1], opponent_color)


def would_be_in_check(board, from_row, from_col, to_row, to_col, color):
    """
    Check if making a move would result in check.
    Used to validate if a move is legal.
    
    Args:
        board: Board object
        from_row, from_col: Starting position
        to_row, to_col: Ending position
        color: Color of the moving player
    
    Returns:
        Boolean indicating if move would result in check
    """
    # Make a copy and simulate the move
    board_copy = board.copy()
    board_copy.move_piece(from_row, from_col, to_row, to_col)
    
    # Check if king is in check after the move
    return is_in_check(board_copy, color)


def would_be_in_check_en_passant(board, from_row, from_col, to_row, to_col, color):
    """
    Check if en passant move would result in check.
    Special handling for en passant since captured pawn is on different square.
    
    Args:
        board: Board object
        from_row, from_col: Starting position of capturing pawn
        to_row, to_col: Ending position (where pawn moves)
        color: Color of the moving player
    
    Returns:
        Boolean indicating if move would result in check
    """
    # Make a copy and simulate the en passant move
    board_copy = board.copy()
    board_copy.move_piece(from_row, from_col, to_row, to_col)
    
    # Remove the captured pawn (on the same row as the moving pawn, but at to_col)
    board_copy.set_piece(from_row, to_col, ' ')
    
    # Check if king is in check after the move
    return is_in_check(board_copy, color)
