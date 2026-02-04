"""
Constants used throughout the chess game.
Phase 1: Core constants
"""

# Board dimensions
ROWS = 8
COLS = 8

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

# Piece types
PIECE_TYPES = {
    'p': 'pawn',
    'n': 'knight',
    'b': 'bishop',
    'r': 'rook',
    'q': 'queen',
    'k': 'king'
}

# UI Constants (Phase 3)
WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE_SQUARE = (240, 217, 181)
BLACK_SQUARE = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)
SELECT_COLOR = (246, 246, 130)
VALID_MOVE_COLOR = (100, 200, 100, 120)  # Semi-transparent green

# UI Element Sizes
VALID_MOVE_DOT_RADIUS = 15  # Small dot for empty squares
VALID_MOVE_RING_RADIUS = 35  # Larger ring for capture moves
STATUS_PADDING = 10
STATUS_HEIGHT = 30
STATUS_WIDTH_BASE = 250

# Unicode chess symbols
PIECE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}
