"""
Chess UI - Highlight Renderer

Renders visual highlights for selected pieces and valid moves.
Displays game status including turn, check, and checkmate indicators.
"""

import pygame
from utils.constants import (
    SQUARE_SIZE, SELECT_COLOR, VALID_MOVE_COLOR,
    VALID_MOVE_DOT_RADIUS, VALID_MOVE_RING_RADIUS,
    STATUS_PADDING, STATUS_HEIGHT, STATUS_WIDTH_BASE
)


def draw_selected_square(screen, row, col):
    """
    Draw highlight for selected square.
    
    Args:
        screen: Pygame screen surface
        row, col: Position of selected square
    """
    pygame.draw.rect(
        screen,
        SELECT_COLOR,
        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    )


def draw_valid_moves(screen, valid_moves, board):
    """
    Draw circles/rings on valid move squares.
    
    Args:
        screen: Pygame screen surface
        valid_moves: List of (row, col) tuples
        board: Board object (to check if square is empty)
    """
    for move_row, move_col in valid_moves:
        # Create semi-transparent surface
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        center = (SQUARE_SIZE // 2, SQUARE_SIZE // 2)
        
        # Small dot for empty squares, larger ring for captures
        is_empty = board.is_empty(move_row, move_col)
        radius = VALID_MOVE_DOT_RADIUS if is_empty else VALID_MOVE_RING_RADIUS
        
        pygame.draw.circle(surface, VALID_MOVE_COLOR, center, radius)
        screen.blit(surface, (move_col * SQUARE_SIZE, move_row * SQUARE_SIZE))


def draw_status_indicator(screen, game_state):
    """
    Draw game status (turn, check, checkmate, etc.).
    
    Args:
        screen: Pygame screen surface
        game_state: GameState object
    """
    font = pygame.font.SysFont('Arial', 24)
    
    # Determine status text
    if game_state.game_over:
        if 'Draw' in str(game_state.winner):
            status_text = f"{game_state.winner}"
        else:
            status_text = f"Checkmate! {game_state.winner} wins!"
    elif game_state.check_status:
        status_text = f"Check! Turn: {game_state.current_turn.capitalize()}"
    else:
        status_text = f"Turn: {game_state.current_turn.capitalize()}"
    
    text = font.render(status_text, True, (255, 255, 255))
    
    # Draw background rectangle
    bg_rect = pygame.Rect(
        STATUS_PADDING,
        STATUS_PADDING,
        max(STATUS_WIDTH_BASE, text.get_width() + 20),
        STATUS_HEIGHT
    )
    pygame.draw.rect(screen, (0, 0, 0), bg_rect)
    
    # Red border if in check or game over
    if game_state.check_status or game_state.game_over:
        pygame.draw.rect(screen, (200, 0, 0), bg_rect, 3)
    else:
        pygame.draw.rect(screen, (100, 100, 100), bg_rect, 2)
    
    screen.blit(text, (STATUS_PADDING + 5, STATUS_PADDING + 5))
