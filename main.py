import pygame
import sys

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
        
    def is_white_piece(self, piece):
        return piece.isupper()
    
    def is_black_piece(self, piece):
        return piece.islower()
    
    def get_piece_at(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Basic move validation for each piece type
        
        Note: This validates piece movement rules but does NOT check for:
        - Check/checkmate conditions
        - Moves that would put own king in check
        - Castling, en passant, or promotion
        """
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
                if target != ' ':
                    if self.current_turn == 'white' and self.is_black_piece(target):
                        return True
                    if self.current_turn == 'black' and self.is_white_piece(target):
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
        
        # King movement
        if piece == 'k':
            return abs(row_diff) <= 1 and abs(col_diff) <= 1
        
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
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move piece if valid"""
        if self.is_valid_move(from_row, from_col, to_row, to_col):
            self.board[to_row][to_col] = self.board[from_row][from_col]
            self.board[from_row][from_col] = ' '
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            return True
        return False
    
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
        """Show whose turn it is"""
        indicator_font = pygame.font.SysFont('Arial', 24)
        turn_text = f"Turn: {self.current_turn.capitalize()}"
        text = indicator_font.render(turn_text, True, (255, 255, 255))
        # Draw a small background rectangle
        bg_rect = pygame.Rect(10, 10, 150, 30)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), bg_rect, 2)
        self.screen.blit(text, (15, 15))
    
    def handle_click(self, pos):
        """Handle mouse click on the board"""
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
            else:
                # Try to move the selected piece
                if self.move_piece(self.selected_pos[0], self.selected_pos[1], row, col):
                    self.selected_piece = None
                    self.selected_pos = None
                else:
                    # If click on own piece, select it instead
                    if piece != ' ' and \
                       ((self.current_turn == 'white' and self.is_white_piece(piece)) or \
                        (self.current_turn == 'black' and self.is_black_piece(piece))):
                        self.selected_piece = piece
                        self.selected_pos = (row, col)
                    else:
                        # Deselect if invalid move
                        self.selected_piece = None
                        self.selected_pos = None
    
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