"""
Chess Game State Management

Manages overall game state including turn system, move tracking, and game flow.
Coordinates between board state and game rules.
"""

from core.board import Board
from core.pieces import pawn, knight, king
from core.pieces.sliding import get_bishop_moves, get_rook_moves, get_queen_moves


class GameState:
    """Manages chess game state and turn system."""
    
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'  # white starts
        self.game_over = False
        self.winner = None
        self.check_status = None  # 'white' or 'black' if in check
        
        # Track piece movements for castling
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_left_moved = False
        self.white_rook_right_moved = False
        self.black_rook_left_moved = False
        self.black_rook_right_moved = False
        
        # Track en passant
        self.en_passant_target = None  # (row, col) where en passant capture is possible
    
    def get_possible_moves(self, row, col):
        """
        Get all possible moves for a piece (basic movement, no check validation yet).
        
        Returns:
            List of (to_row, to_col) tuples
        """
        piece = self.board.get_piece(row, col)
        if piece == ' ':
            return []
        
        color = self.board.get_piece_color(row, col)
        piece_type = piece.lower()
        
        if piece_type == 'p':
            return pawn.get_pawn_moves(self.board, row, col, color)
        elif piece_type == 'n':
            return knight.get_knight_moves(self.board, row, col, color)
        elif piece_type == 'b':
            return get_bishop_moves(self.board, row, col, color)
        elif piece_type == 'r':
            return get_rook_moves(self.board, row, col, color)
        elif piece_type == 'q':
            return get_queen_moves(self.board, row, col, color)
        elif piece_type == 'k':
            return king.get_king_moves(self.board, row, col, color)
        
        return []
    
    def switch_turn(self):
        """Switch to the other player's turn."""
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
    
    def is_current_player_piece(self, row, col):
        """Check if piece at position belongs to current player."""
        color = self.board.get_piece_color(row, col)
        return color == self.current_turn
    
    def track_piece_move(self, piece, from_row, from_col):
        """Track if special pieces have moved (for castling)."""
        if piece == 'K':
            self.white_king_moved = True
        elif piece == 'k':
            self.black_king_moved = True
        elif piece == 'R':
            if from_row == 7 and from_col == 0:
                self.white_rook_left_moved = True
            elif from_row == 7 and from_col == 7:
                self.white_rook_right_moved = True
        elif piece == 'r':
            if from_row == 0 and from_col == 0:
                self.black_rook_left_moved = True
            elif from_row == 0 and from_col == 7:
                self.black_rook_right_moved = True
    
    def update_en_passant(self, piece, from_row, to_row, from_col):
        """Update en passant target after a move."""
        self.en_passant_target = None
        if piece.lower() == 'p' and abs(to_row - from_row) == 2:
            # Pawn moved two squares, set en passant target
            self.en_passant_target = ((from_row + to_row) // 2, from_col)
