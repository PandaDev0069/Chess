import pygame
import sys
import copy

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
SELECT = (246, 246, 130)
VALID_MOVE = (100, 200, 100, 120)  # Semi-transparent green for valid moves

# Piece representation: uppercase = white, lowercase = black
# K/k = King, Q/q = Queen, R/r = Rook, B/b = Bishop, N/n = Knight, P/p = Pawn
INITIAL_BOARD = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.board = [row[:] for row in INITIAL_BOARD]  # Deep copy
        self.selected_piece = None
        self.selected_pos = None
        self.current_turn = 'white'  # white starts
        self.font = pygame.font.SysFont('Arial', 60)
        self.valid_moves = []  # Store valid moves for selected piece
        self.game_over = False
        self.winner = None
        self.check_status = None  # 'white' or 'black' if in check
        
        # Track if pieces have moved (for castling)
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_left_moved = False
        self.white_rook_right_moved = False
        self.black_rook_left_moved = False
        self.black_rook_right_moved = False
        
        # Track en passant
        self.en_passant_target = None  # (row, col) where en passant capture is possible
        
        # Move history for undo/game records
        self.move_history = []
        
    def is_white_piece(self, piece):
        return piece.isupper()
    
    def is_black_piece(self, piece):
        return piece.islower()
    
    def find_king(self, color):
        """Find the position of the king for the given color"""
        king = 'K' if color == 'white' else 'k'
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == king:
                    return (row, col)
        return None
    
    def is_square_attacked(self, row, col, by_color):
        """Check if a square is attacked by any piece of the given color"""
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece == ' ':
                    continue
                    
                # Check if piece belongs to attacking color
                if (by_color == 'white' and self.is_white_piece(piece)) or \
                   (by_color == 'black' and self.is_black_piece(piece)):
                    # Temporarily switch turn to check if this piece can attack the square
                    saved_turn = self.current_turn
                    self.current_turn = by_color
                    
                    # For pawn, we need special handling as it attacks differently than it moves
                    if piece.lower() == 'p':
                        direction = -1 if by_color == 'white' else 1
                        row_diff = row - r
                        col_diff = abs(col - c)
                        if row_diff == direction and col_diff == 1:
                            self.current_turn = saved_turn
                            return True
                    elif self.is_valid_move_basic(r, c, row, col):
                        self.current_turn = saved_turn
                        return True
                    
                    self.current_turn = saved_turn
        return False
    
    def is_in_check(self, color):
        """Check if the king of the given color is in check"""
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        
        opponent_color = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(king_pos[0], king_pos[1], opponent_color)
    
    def would_be_in_check(self, from_row, from_col, to_row, to_col, color):
        """Check if making a move would result in check"""
        # Make a copy of the board and simulate the move
        original_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = ' '
        
        in_check = self.is_in_check(color)
        
        # Undo the move
        self.board[from_row][from_col] = self.board[to_row][to_col]
        self.board[to_row][to_col] = original_piece
        
        return in_check
    
    def is_valid_move_basic(self, from_row, from_col, to_row, to_col):
        """Basic move validation without check considerations"""
        piece = self.board[from_row][from_col].lower()
        target = self.board[to_row][to_col]
        
        # Can't move to the same square
        if from_row == to_row and from_col == to_col:
            return False
        
        # Can't capture own piece
        if self.current_turn == 'white' and self.is_white_piece(target):
            return False
        if self.current_turn == 'black' and self.is_black_piece(target):
            return False
        
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        
        # Pawn movement
        if piece == 'p':
            direction = -1 if self.current_turn == 'white' else 1
            # Move forward
            if col_diff == 0:
                if row_diff == direction and target == ' ':
                    return True
                # Initial two-square move
                start_row = 6 if self.current_turn == 'white' else 1
                if from_row == start_row and row_diff == 2 * direction and target == ' ':
                    if self.board[from_row + direction][from_col] == ' ':
                        return True
            # Capture diagonally
            elif abs(col_diff) == 1 and row_diff == direction:
                # Normal capture
                if target != ' ':
                    if self.current_turn == 'white' and self.is_black_piece(target):
                        return True
                    if self.current_turn == 'black' and self.is_white_piece(target):
                        return True
                # En passant
                elif self.en_passant_target == (to_row, to_col):
                    return True
            return False
        
        # Knight movement
        if piece == 'n':
            return (abs(row_diff) == 2 and abs(col_diff) == 1) or (abs(row_diff) == 1 and abs(col_diff) == 2)
        
        # Bishop movement
        if piece == 'b':
            if abs(row_diff) != abs(col_diff):
                return False
            return self.is_path_clear(from_row, from_col, to_row, to_col)
        
        # Rook movement
        if piece == 'r':
            if row_diff != 0 and col_diff != 0:
                return False
            return self.is_path_clear(from_row, from_col, to_row, to_col)
        
        # Queen movement (combination of rook and bishop)
        if piece == 'q':
            if row_diff == 0 or col_diff == 0 or abs(row_diff) == abs(col_diff):
                return self.is_path_clear(from_row, from_col, to_row, to_col)
            return False
        
        # King movement (regular and castling)
        if piece == 'k':
            # Regular king move (one square)
            if abs(row_diff) <= 1 and abs(col_diff) <= 1:
                return True
            
            # Castling
            if row_diff == 0 and abs(col_diff) == 2:
                return self.can_castle(from_row, from_col, to_col)
            
            return False
        
        return False
    
    def can_castle(self, king_row, king_col, target_col):
        """Check if castling is valid"""
        # King must not have moved
        if self.current_turn == 'white' and self.white_king_moved:
            return False
        if self.current_turn == 'black' and self.black_king_moved:
            return False
        
        # King must not be in check
        if self.is_in_check(self.current_turn):
            return False
        
        # Determine castling side
        if target_col > king_col:  # Kingside castling
            rook_col = 7
            if self.current_turn == 'white' and self.white_rook_right_moved:
                return False
            if self.current_turn == 'black' and self.black_rook_right_moved:
                return False
            
            # Check if path is clear
            for col in range(king_col + 1, rook_col):
                if self.board[king_row][col] != ' ':
                    return False
                # King cannot pass through check
                if self.is_square_attacked(king_row, col, 'black' if self.current_turn == 'white' else 'white'):
                    return False
        else:  # Queenside castling
            rook_col = 0
            if self.current_turn == 'white' and self.white_rook_left_moved:
                return False
            if self.current_turn == 'black' and self.black_rook_left_moved:
                return False
            
            # Check if path is clear
            for col in range(rook_col + 1, king_col):
                if self.board[king_row][col] != ' ':
                    return False
            # King cannot pass through check (only check king's path, not rook's)
            for col in range(min(king_col, target_col), max(king_col, target_col) + 1):
                if col != king_col and self.is_square_attacked(king_row, col, 'black' if self.current_turn == 'white' else 'white'):
                    return False
        
        # Check if rook is in correct position
        rook = 'R' if self.current_turn == 'white' else 'r'
        if self.board[king_row][rook_col] != rook:
            return False
        
        return True
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Full move validation including check rules"""
        if not self.is_valid_move_basic(from_row, from_col, to_row, to_col):
            return False
        
        # Move cannot put own king in check
        if self.would_be_in_check(from_row, from_col, to_row, to_col, self.current_turn):
            return False
        
        return True
    
    def get_all_valid_moves(self, from_row, from_col):
        """Get all valid moves for a piece at the given position"""
        valid_moves = []
        piece = self.board[from_row][from_col]
        
        if piece == ' ':
            return valid_moves
        
        # Check all possible destination squares
        for to_row in range(ROWS):
            for to_col in range(COLS):
                if self.is_valid_move(from_row, from_col, to_row, to_col):
                    valid_moves.append((to_row, to_col))
        
        return valid_moves
    
    def has_any_valid_moves(self, color):
        """Check if the given color has any valid moves"""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece == ' ':
                    continue
                
                if (color == 'white' and self.is_white_piece(piece)) or \
                   (color == 'black' and self.is_black_piece(piece)):
                    # Save current turn
                    saved_turn = self.current_turn
                    self.current_turn = color
                    
                    if len(self.get_all_valid_moves(row, col)) > 0:
                        self.current_turn = saved_turn
                        return True
                    
                    self.current_turn = saved_turn
        
        return False
    
    def check_game_over(self):
        """Check if the game is over (checkmate or stalemate)"""
        if not self.has_any_valid_moves(self.current_turn):
            if self.is_in_check(self.current_turn):
                # Checkmate
                self.game_over = True
                self.winner = 'Black' if self.current_turn == 'white' else 'White'
                return True
            else:
                # Stalemate
                self.game_over = True
                self.winner = 'Draw (Stalemate)'
                return True
        return False
    
    def is_path_clear(self, from_row, from_col, to_row, to_col):
        """Check if path is clear for sliding pieces (rook, bishop, queen)"""
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        current_row = from_row + row_step
        current_col = from_col + col_step
        
        while current_row != to_row or current_col != to_col:
            if self.board[current_row][current_col] != ' ':
                return False
            current_row += row_step
            current_col += col_step
        
        return True
    
    def promote_pawn(self, row, col):
        """Promote pawn to queen (simplified - always queen)"""
        piece = self.board[row][col]
        if piece.lower() == 'p':
            # Check if pawn reached the end
            if (piece == 'P' and row == 0) or (piece == 'p' and row == 7):
                # Promote to queen
                self.board[row][col] = 'Q' if piece == 'P' else 'q'
                return True
        return False
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move piece if valid"""
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False
        
        piece = self.board[from_row][from_col]
        captured_piece = self.board[to_row][to_col]
        
        # Handle castling
        if piece.lower() == 'k' and abs(to_col - from_col) == 2:
            # Move the king
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = ' '
            
            # Move the rook
            if to_col > from_col:  # Kingside
                self.board[from_row][5] = self.board[from_row][7]
                self.board[from_row][7] = ' '
            else:  # Queenside
                self.board[from_row][3] = self.board[from_row][0]
                self.board[from_row][0] = ' '
        # Handle en passant
        elif piece.lower() == 'p' and self.en_passant_target == (to_row, to_col):
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = ' '
            # Remove the captured pawn
            capture_row = from_row
            self.board[capture_row][to_col] = ' '
        # Normal move
        else:
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = ' '
        
        # Update en passant target
        self.en_passant_target = None
        if piece.lower() == 'p' and abs(to_row - from_row) == 2:
            # Pawn moved two squares, set en passant target
            self.en_passant_target = ((from_row + to_row) // 2, from_col)
        
        # Handle pawn promotion
        self.promote_pawn(to_row, to_col)
        
        # Track piece movements for castling
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
        
        # Update check status
        self.check_status = None
        opponent = 'black' if self.current_turn == 'white' else 'white'
        if self.is_in_check(opponent):
            self.check_status = opponent
        
        # Switch turn
        self.current_turn = opponent
        
        # Check for game over
        self.check_game_over()
        
        return True
    
    def draw_board(self):
        """Draw the chess board"""
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                
                # Highlight selected square
                if self.selected_pos and self.selected_pos == (row, col):
                    color = SELECT
                
                pygame.draw.rect(self.screen, color, 
                               (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        # Highlight valid moves
        if self.selected_pos and self.valid_moves:
            for move_row, move_col in self.valid_moves:
                # Draw a semi-transparent circle for valid moves
                surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                center = (SQUARE_SIZE // 2, SQUARE_SIZE // 2)
                radius = 15 if self.board[move_row][move_col] == ' ' else 35
                pygame.draw.circle(surface, VALID_MOVE, center, radius)
                self.screen.blit(surface, (move_col * SQUARE_SIZE, move_row * SQUARE_SIZE))
    
    def draw_pieces(self):
        """Draw pieces on the board"""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != ' ':
                    # Use Unicode chess symbols
                    symbols = {
                        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
                        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
                    }
                    symbol = symbols.get(piece, piece)
                    # White pieces rendered in black for contrast, black pieces in white
                    text = self.font.render(symbol, True, (0, 0, 0) if self.is_white_piece(piece) else (255, 255, 255))
                    text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                                      row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    self.screen.blit(text, text_rect)
    
    def draw_turn_indicator(self):
        """Show whose turn it is and game status"""
        indicator_font = pygame.font.SysFont('Arial', 24)
        
        if self.game_over:
            if 'Draw' in str(self.winner):
                status_text = f"{self.winner}"
            else:
                status_text = f"Checkmate! {self.winner} wins!"
        elif self.check_status:
            status_text = f"Check! Turn: {self.current_turn.capitalize()}"
        else:
            status_text = f"Turn: {self.current_turn.capitalize()}"
        
        text = indicator_font.render(status_text, True, (255, 255, 255))
        # Draw a background rectangle
        bg_rect = pygame.Rect(10, 10, max(250, text.get_width() + 20), 30)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
        
        # Highlight in red if in check
        if self.check_status or self.game_over:
            pygame.draw.rect(self.screen, (200, 0, 0), bg_rect, 3)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), bg_rect, 2)
        
        self.screen.blit(text, (15, 15))
    
    def handle_click(self, pos):
        """Handle mouse click on the board"""
        if self.game_over:
            return  # No more moves after game over
        
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        if 0 <= row < ROWS and 0 <= col < COLS:
            piece = self.board[row][col]
            
            # If no piece selected, select piece of current player
            if self.selected_piece is None:
                if piece != ' ':
                    if (self.current_turn == 'white' and self.is_white_piece(piece)) or \
                       (self.current_turn == 'black' and self.is_black_piece(piece)):
                        self.selected_piece = piece
                        self.selected_pos = (row, col)
                        # Calculate valid moves for this piece
                        self.valid_moves = self.get_all_valid_moves(row, col)
            else:
                # Try to move the selected piece
                if self.move_piece(self.selected_pos[0], self.selected_pos[1], row, col):
                    self.selected_piece = None
                    self.selected_pos = None
                    self.valid_moves = []
                else:
                    # If click on own piece, select it instead
                    if piece != ' ' and \
                       ((self.current_turn == 'white' and self.is_white_piece(piece)) or \
                        (self.current_turn == 'black' and self.is_black_piece(piece))):
                        self.selected_piece = piece
                        self.selected_pos = (row, col)
                        # Calculate valid moves for this piece
                        self.valid_moves = self.get_all_valid_moves(row, col)
                    else:
                        # Deselect if invalid move
                        self.selected_piece = None
                        self.selected_pos = None
                        self.valid_moves = []
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
            
            # Draw everything
            self.draw_board()
            self.draw_pieces()
            self.draw_turn_indicator()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    game = ChessGame()
    game.run()

if __name__ == "__main__":
    main()