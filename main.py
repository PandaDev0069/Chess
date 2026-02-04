"""
Chess Game - Main Entry Point

This chess game follows a phase-based architecture:
- Phase 1: Core chess logic (board, pieces, game state)
- Phase 2: Game rules (check, checkmate, move validation)
- Phase 3: Pygame visualization (rendering)
- Phase 4: Player interaction (input handling)
- Phase 5: Game polish (status indicators, highlights)

All core logic is independent of pygame and fully testable.
UI only asks logic for validity - never decides legality itself.
"""

import pygame
import sys

# Core game logic (Phase 1 & 2)
from core.game_state import GameState

# UI rendering (Phase 3)
from ui.renderer.board_renderer import draw_board
from ui.renderer.piece_renderer import draw_pieces
from ui.renderer.highlight_renderer import draw_selected_square, draw_valid_moves, draw_status_indicator

# Input handling (Phase 4)
from ui.input.input_handler import InputHandler

# Constants
from utils.constants import WIDTH, HEIGHT


def main():
    """Main game loop."""
    # Initialize Pygame
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game - Phase-Based Architecture")
    
    # Create game state and input handler
    game_state = GameState()
    input_handler = InputHandler(game_state)
    
    # Create font for pieces
    piece_font = pygame.font.SysFont('Arial', 60)
    
    # Game clock
    clock = pygame.time.Clock()
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_handler.handle_click(pygame.mouse.get_pos())
                # Check for game over after move
                input_handler.check_game_over()
        
        # Render everything
        
        # Phase 3: Draw board
        draw_board(screen)
        
        # Phase 4: Draw selected square highlight
        if input_handler.selected_pos:
            row, col = input_handler.selected_pos
            draw_selected_square(screen, row, col)
        
        # Phase 4: Draw valid move highlights
        if input_handler.valid_moves:
            draw_valid_moves(screen, input_handler.valid_moves, game_state.board)
        
        # Phase 3: Draw pieces
        draw_pieces(screen, game_state.board, piece_font)
        
        # Phase 5: Draw status indicator
        draw_status_indicator(screen, game_state)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
