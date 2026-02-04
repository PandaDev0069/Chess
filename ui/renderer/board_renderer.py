"""
Phase 3: Pygame Visualization - Board Renderer
Draws the chess board.
"""

import pygame
from utils.constants import (
    ROWS, COLS, SQUARE_SIZE,
    WHITE_SQUARE, BLACK_SQUARE
)


def draw_board(screen):
    """
    Draw the chess board (8x8 grid with alternating colors).
    
    Args:
        screen: Pygame screen surface
    """
    for row in range(ROWS):
        for col in range(COLS):
            # Alternate colors
            color = WHITE_SQUARE if (row + col) % 2 == 0 else BLACK_SQUARE
            
            pygame.draw.rect(
                screen,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
