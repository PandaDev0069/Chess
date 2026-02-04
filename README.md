# Chess Game - Phase-Based Architecture

A fully functional chess game built with Python and Pygame, following clean architecture principles with complete separation of game logic and UI.

## Features

✅ **All Chess Rules Implemented**
- Complete piece movement (Pawn, Knight, Bishop, Rook, Queen, King)
- Check and checkmate detection
- Stalemate detection
- Castling (kingside and queenside)
- En passant capture
- Pawn promotion
- Move validation (prevents exposing king to check)

✅ **Professional UI/UX**
- Valid moves highlighting (green circles)
- Selected piece highlighting
- Check indicator (red border)
- Turn indicator
- Game status display (checkmate/stalemate)

✅ **Clean Architecture**
- Core logic independent of pygame
- Fully testable without UI
- Modular, maintainable code
- Phase-based development approach

## Setup

### Windows
```powershell
# Create venv (Python 3.12 recommended for pygame)
py -3.12 -m venv .venv

# Activate venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Run game
python main.py

# Run tests (no pygame required)
python test_core_logic.py
```

### Linux/Mac
```bash
# Create venv
python3 -m venv .venv

# Activate venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run game
python main.py

# Run tests
python test_core_logic.py
```

## Architecture

This project follows a **phase-based architecture** as outlined in DESIGN.md:

### Phase 1: Core Chess Logic (No pygame)
Pure Python chess logic - fully testable without UI.

**Modules:**
- `core/board.py` - Board representation and operations
- `core/game_state.py` - Game state and turn management
- `core/pieces/` - Individual piece movement rules
  - `pawn.py`, `knight.py`, `king.py`, `sliding.py` (bishop/rook/queen)

### Phase 2: Game Rules & Constraints
Advanced chess rules and move validation.

**Modules:**
- `core/rules/check.py` - Check detection and square attacks
- `core/rules/legality.py` - Move validation, checkmate, stalemate
- `core/rules/special.py` - Castling, en passant, pawn promotion

### Phase 3: Pygame Visualization
Rendering the game state visually.

**Modules:**
- `ui/renderer/board_renderer.py` - Chess board drawing
- `ui/renderer/piece_renderer.py` - Piece rendering (Unicode symbols)
- `ui/renderer/highlight_renderer.py` - Highlights and status display

### Phase 4: Player Interaction
Mouse input and user interaction.

**Modules:**
- `ui/input/input_handler.py` - Mouse clicks, piece selection, move execution

### Phase 5: Game Polish
Status indicators, highlights, visual feedback (integrated in Phase 3 & 4).

### Supporting Modules
- `utils/constants.py` - All game constants (colors, sizes, board setup)
- `main.py` - Thin orchestration layer (< 100 lines)

## File Structure

```text
chess_game/
│
├── main.py                    # Main entry point (~100 lines)
├── DESIGN.md                  # Architecture documentation
├── test_core_logic.py         # Core logic tests (no pygame)
│
├── core/                      # Phase 1 & 2: Pure game logic
│   ├── board.py              # Board representation
│   ├── game_state.py         # Game state management
│   │
│   ├── pieces/               # Piece movement rules
│   │   ├── pawn.py
│   │   ├── knight.py
│   │   ├── king.py
│   │   └── sliding.py        # Bishop, Rook, Queen
│   │
│   └── rules/                # Game rules engine
│       ├── check.py          # Check detection
│       ├── legality.py       # Move validation
│       └── special.py        # Castling, en passant, promotion
│
├── ui/                        # Phase 3 & 4: Pygame UI
│   ├── renderer/
│   │   ├── board_renderer.py
│   │   ├── piece_renderer.py
│   │   └── highlight_renderer.py
│   │
│   └── input/
│       └── input_handler.py
│
├── utils/
│   └── constants.py          # All constants
│
└── assets/
    └── images/               # (Future: piece sprites)
```

## Design Principles

1. **Separation of Concerns**
   - Game logic knows nothing about pygame
   - UI only asks logic for validity, never decides it

2. **Testability**
   - Core logic fully testable without UI
   - Run `test_core_logic.py` to verify

3. **Modularity**
   - Each module has a single responsibility
   - Easy to extend or modify

4. **Clean Code**
   - Well-documented
   - Type hints where helpful
   - Descriptive names

## How It Works

```python
# main.py is just orchestration:

# 1. Create game state (Phase 1 & 2)
game_state = GameState()
input_handler = InputHandler(game_state)

# 2. Game loop
while running:
    # Handle input (Phase 4)
    input_handler.handle_click(mouse_pos)
    
    # Render (Phase 3)
    draw_board(screen)
    draw_pieces(screen, game_state.board, font)
    draw_status_indicator(screen, game_state)
```

The UI **never** decides if a move is legal - it always asks the core logic.

## Testing

```bash
# Test core logic (no pygame required)
python test_core_logic.py

# All tests verify:
# ✓ Board operations
# ✓ Piece movements
# ✓ Game state management
# ✓ Check detection
# ✓ Move legality
# ✓ Special moves
```

## Future Enhancements (Phase 6)

- [ ] Move history and undo/redo
- [ ] Save/load games (PGN format)
- [ ] Game timer/clock
- [ ] AI opponent (minimax algorithm)
- [ ] Move animations
- [ ] Sound effects
- [ ] Online multiplayer

## Credits

Built following best practices in software architecture and game development.
- Clean separation between game logic and presentation
- Test-driven development approach
- Modular design for maintainability
