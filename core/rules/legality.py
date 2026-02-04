"""
Chess Rules Engine - Move Legality

Validates whether moves are legal according to chess rules.
Ensures moves don't expose the king to check and handles checkmate/stalemate detection.
"""

from core.rules.check import would_be_in_check, would_be_in_check_en_passant, is_in_check
from core.pieces import pawn


def is_legal_move(game_state, from_row, from_col, to_row, to_col):
    """
    Check if a move is legal (piece can move there AND doesn't expose king).
    
    Args:
        game_state: GameState object
        from_row, from_col: Starting position
        to_row, to_col: Ending position
    
    Returns:
        Boolean indicating if move is legal
    """
    piece = game_state.board.get_piece(from_row, from_col)
    if piece == ' ':
        return False
    
    color = game_state.board.get_piece_color(from_row, from_col)
    
    # Check if it's this player's turn
    if color != game_state.current_turn:
        return False
    
    # Get possible moves for this piece
    possible_moves = game_state.get_possible_moves(from_row, from_col)
    
    # Check for en passant
    if piece.lower() == 'p':
        if pawn.can_en_passant(game_state.board, from_row, from_col, 
                               to_row, to_col, game_state.en_passant_target):
            if (to_row, to_col) not in possible_moves:
                possible_moves.append((to_row, to_col))
    
    # Check if destination is in possible moves
    if (to_row, to_col) not in possible_moves:
        return False
    
    # Check if move would expose own king to check
    if would_be_in_check(game_state.board, from_row, from_col, to_row, to_col, color):
        return False
    
    return True


def get_all_legal_moves(game_state, row, col):
    """
    Get all legal moves for a piece (including check validation).
    
    Returns:
        List of (to_row, to_col) tuples
    """
    possible_moves = game_state.get_possible_moves(row, col)
    legal_moves = []
    
    color = game_state.board.get_piece_color(row, col)
    if not color:
        return []
    
    for to_row, to_col in possible_moves:
        if not would_be_in_check(game_state.board, row, col, to_row, to_col, color):
            legal_moves.append((to_row, to_col))
    
    # Add en passant if applicable
    piece = game_state.board.get_piece(row, col)
    if piece.lower() == 'p' and game_state.en_passant_target:
        to_row, to_col = game_state.en_passant_target
        if pawn.can_en_passant(game_state.board, row, col, to_row, to_col, 
                               game_state.en_passant_target):
            if not would_be_in_check_en_passant(game_state.board, row, col, to_row, to_col, color):
                legal_moves.append((to_row, to_col))
    
    return legal_moves


def has_any_legal_moves(game_state, color):
    """Check if the given color has any legal moves."""
    pieces = game_state.board.get_all_pieces(color)
    
    for row, col, piece in pieces:
        if len(get_all_legal_moves(game_state, row, col)) > 0:
            return True
    
    return False


def is_checkmate(game_state, color):
    """Check if the given color is in checkmate."""
    return is_in_check(game_state.board, color) and not has_any_legal_moves(game_state, color)


def is_stalemate(game_state, color):
    """Check if the given color is in stalemate."""
    return not is_in_check(game_state.board, color) and not has_any_legal_moves(game_state, color)
