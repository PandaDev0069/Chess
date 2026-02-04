"""
Phase 2: Game Rules - Special Moves
Castling, en passant, and pawn promotion logic.
"""

from core.rules.check import is_in_check, is_square_attacked


def can_castle(game_state, from_row, from_col, to_col):
    """
    Check if castling is valid.
    
    Args:
        game_state: GameState object
        from_row, from_col: King position
        to_col: Target column (2 for queenside, 6 for kingside)
    
    Returns:
        Boolean indicating if castling is valid
    """
    color = game_state.current_turn
    
    # King must not have moved
    if color == 'white' and game_state.white_king_moved:
        return False
    if color == 'black' and game_state.black_king_moved:
        return False
    
    # King must not be in check
    if is_in_check(game_state.board, color):
        return False
    
    # Determine castling side
    if to_col > from_col:  # Kingside castling
        rook_col = 7
        if color == 'white' and game_state.white_rook_right_moved:
            return False
        if color == 'black' and game_state.black_rook_right_moved:
            return False
        
        # Check if path is clear and not through check
        for col in range(from_col + 1, rook_col):
            if not game_state.board.is_empty(from_row, col):
                return False
            # King cannot pass through check
            opponent = 'black' if color == 'white' else 'white'
            if is_square_attacked(game_state.board, from_row, col, opponent):
                return False
    else:  # Queenside castling
        rook_col = 0
        if color == 'white' and game_state.white_rook_left_moved:
            return False
        if color == 'black' and game_state.black_rook_left_moved:
            return False
        
        # Check if path is clear
        for col in range(rook_col + 1, from_col):
            if not game_state.board.is_empty(from_row, col):
                return False
        
        # King cannot pass through check (check king's path only)
        for col in range(min(from_col, to_col), max(from_col, to_col) + 1):
            if col != from_col:
                opponent = 'black' if color == 'white' else 'white'
                if is_square_attacked(game_state.board, from_row, col, opponent):
                    return False
    
    # Check if rook is in correct position
    rook = 'R' if color == 'white' else 'r'
    if game_state.board.get_piece(from_row, rook_col) != rook:
        return False
    
    return True


def execute_castle(game_state, from_row, from_col, to_col):
    """
    Execute castling move.
    
    Moves both king and rook to their castled positions.
    """
    # Move the king
    piece = game_state.board.get_piece(from_row, from_col)
    game_state.board.set_piece(from_row, to_col, piece)
    game_state.board.set_piece(from_row, from_col, ' ')
    
    # Move the rook
    if to_col > from_col:  # Kingside
        rook = game_state.board.get_piece(from_row, 7)
        game_state.board.set_piece(from_row, 5, rook)
        game_state.board.set_piece(from_row, 7, ' ')
    else:  # Queenside
        rook = game_state.board.get_piece(from_row, 0)
        game_state.board.set_piece(from_row, 3, rook)
        game_state.board.set_piece(from_row, 0, ' ')


def execute_en_passant(game_state, from_row, from_col, to_row, to_col):
    """
    Execute en passant capture.
    
    Moves pawn and removes captured pawn.
    """
    piece = game_state.board.get_piece(from_row, from_col)
    game_state.board.set_piece(to_row, to_col, piece)
    game_state.board.set_piece(from_row, from_col, ' ')
    
    # Remove the captured pawn (on the same row as the moving pawn)
    game_state.board.set_piece(from_row, to_col, ' ')


def promote_pawn(game_state, row, col):
    """
    Promote pawn to queen (simplified - always queen).
    
    Returns:
        Boolean indicating if promotion occurred
    """
    piece = game_state.board.get_piece(row, col)
    if piece.lower() == 'p':
        # Check if pawn reached the end
        if (piece == 'P' and row == 0) or (piece == 'p' and row == 7):
            # Promote to queen
            new_piece = 'Q' if piece == 'P' else 'q'
            game_state.board.set_piece(row, col, new_piece)
            return True
    return False
