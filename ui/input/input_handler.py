"""
Chess UI - Input Handler

Handles user input and player interactions.
Processes mouse clicks and delegates to game logic for move validation.
"""

from utils.constants import SQUARE_SIZE, ROWS, COLS
from core.rules.legality import get_all_legal_moves, is_checkmate, is_stalemate
from core.rules.check import is_in_check
from core.rules.special import can_castle, execute_castle, execute_en_passant, promote_pawn
from core.pieces.pawn import can_en_passant


class InputHandler:
    """Handles user input for chess game."""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.selected_pos = None
        self.valid_moves = []
    
    def handle_click(self, pos):
        """
        Handle mouse click on the board.
        
        Args:
            pos: (x, y) mouse position
        
        Returns:
            Boolean indicating if board state changed
        """
        if self.game_state.game_over:
            return False  # No more moves after game over
        
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        if not (0 <= row < ROWS and 0 <= col < COLS):
            return False
        
        # If no piece selected, try to select one
        if self.selected_pos is None:
            return self._try_select_piece(row, col)
        else:
            # Try to move selected piece
            return self._try_move_piece(row, col)
    
    def _try_select_piece(self, row, col):
        """Try to select a piece at the given position."""
        piece = self.game_state.board.get_piece(row, col)
        
        if piece == ' ':
            return False
        
        # Check if piece belongs to current player
        if self.game_state.is_current_player_piece(row, col):
            self.selected_pos = (row, col)
            # Calculate valid moves for this piece
            self.valid_moves = get_all_legal_moves(self.game_state, row, col)
            
            # Add castling if applicable
            if piece.lower() == 'k':
                self._add_castling_moves(row, col)
            
            return True
        
        return False
    
    def _try_move_piece(self, to_row, to_col):
        """Try to move the selected piece to the target position."""
        from_row, from_col = self.selected_pos
        piece = self.game_state.board.get_piece(from_row, from_col)
        
        # Check if clicked on another own piece (switch selection)
        if self.game_state.is_current_player_piece(to_row, to_col):
            self.selected_pos = (to_row, to_col)
            self.valid_moves = get_all_legal_moves(self.game_state, to_row, to_col)
            
            # Add castling if applicable for newly selected piece
            new_piece = self.game_state.board.get_piece(to_row, to_col)
            if new_piece.lower() == 'k':
                self._add_castling_moves(to_row, to_col)
            
            return True
        
        # Check if move is valid
        if (to_row, to_col) not in self.valid_moves:
            # Deselect
            self.selected_pos = None
            self.valid_moves = []
            return False
        
        # Execute the move
        self._execute_move(from_row, from_col, to_row, to_col, piece)
        
        # Clear selection
        self.selected_pos = None
        self.valid_moves = []
        
        return True
    
    def _execute_move(self, from_row, from_col, to_row, to_col, piece):
        """Execute a move and update game state."""
        # Check for special moves
        
        # Castling
        if piece.lower() == 'k' and abs(to_col - from_col) == 2:
            execute_castle(self.game_state, from_row, from_col, to_col)
        # En passant
        elif piece.lower() == 'p' and can_en_passant(
            self.game_state.board, from_row, from_col,
            to_row, to_col, self.game_state.en_passant_target
        ):
            execute_en_passant(self.game_state, from_row, from_col, to_row, to_col)
        # Normal move
        else:
            self.game_state.board.move_piece(from_row, from_col, to_row, to_col)
        
        # Update en passant target
        self.game_state.update_en_passant(piece, from_row, to_row, from_col)
        
        # Handle pawn promotion
        promote_pawn(self.game_state, to_row, to_col)
        
        # Track piece movements (for castling)
        self.game_state.track_piece_move(piece, from_row, from_col)
        
        # Update check status
        self._update_game_status()
        
        # Switch turn
        self.game_state.switch_turn()
    
    def _update_game_status(self):
        """Update check, checkmate, and stalemate status."""
        opponent = 'black' if self.game_state.current_turn == 'white' else 'white'
        
        # Check for check
        self.game_state.check_status = None
        if is_in_check(self.game_state.board, opponent):
            self.game_state.check_status = opponent
        
        # Check for checkmate or stalemate (after turn switches)
        # We'll check this after the turn switch in the main game loop
    
    def _add_castling_moves(self, row, col):
        """Add castling moves to valid moves if applicable."""
        # Kingside castling
        if can_castle(self.game_state, row, col, 6):
            self.valid_moves.append((row, 6))
        
        # Queenside castling
        if can_castle(self.game_state, row, col, 2):
            self.valid_moves.append((row, 2))
    
    def check_game_over(self):
        """Check if the game is over and update game state."""
        if is_checkmate(self.game_state, self.game_state.current_turn):
            self.game_state.game_over = True
            winner_color = 'Black' if self.game_state.current_turn == 'white' else 'White'
            self.game_state.winner = winner_color
            return True
        elif is_stalemate(self.game_state, self.game_state.current_turn):
            self.game_state.game_over = True
            self.game_state.winner = 'Draw (Stalemate)'
            return True
        return False
