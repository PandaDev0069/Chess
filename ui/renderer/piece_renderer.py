"""
Chess UI - Piece Renderer

Renders chess pieces on the board using Unicode symbols.
Displays pieces with appropriate colors for visual distinction.
"""

from utils.constants import ROWS, COLS, SQUARE_SIZE, PIECE_SYMBOLS


def draw_pieces(screen, board, font):
    """
    Draw all pieces on the board using Unicode symbols.
    
    Args:
        screen: Pygame screen surface
        board: Board object
        font: Pygame font for rendering pieces
    """
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece(row, col)
            if piece != ' ':
                # Get Unicode symbol for piece
                symbol = PIECE_SYMBOLS.get(piece, piece)
                
                # White pieces rendered in black for contrast, black pieces in white
                is_white = board.is_white_piece(piece)
                color = (0, 0, 0) if is_white else (255, 255, 255)
                
                # Render text
                text = font.render(symbol, True, color)
                text_rect = text.get_rect(
                    center=(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2
                    )
                )
                screen.blit(text, text_rect)
