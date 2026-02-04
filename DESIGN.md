# Chess Game Design Document

## Phase 0 - Design Decisions

### Chess Rules Summary

#### Basic Movement
- **Pawn**: Moves forward 1 square (2 on first move), captures diagonally
- **Knight**: L-shape (2+1 or 1+2 squares)
- **Bishop**: Diagonal movement, any distance
- **Rook**: Horizontal/vertical movement, any distance
- **Queen**: Combination of bishop and rook movement
- **King**: One square in any direction

#### Special Rules
- **Check**: King is under attack
- **Checkmate**: King in check with no legal moves
- **Stalemate**: Not in check but no legal moves (draw)
- **Castling**: King and rook special move (conditions: neither moved, path clear, not through check)
- **En Passant**: Special pawn capture after opponent's 2-square pawn advance
- **Pawn Promotion**: Pawn reaching end rank becomes queen (or other piece)

### Data Representation

#### Square Representation
- **Format**: `(row, col)` tuple
- **Indexing**: 0-based, row 0 = top (black pieces), row 7 = bottom (white pieces)
- **Example**: `(0, 0)` = a8 (black's queenside rook), `(7, 4)` = e1 (white king)

#### Piece Representation
- **Type**: Single character
  - Uppercase = White pieces (`K`, `Q`, `R`, `B`, `N`, `P`)
  - Lowercase = Black pieces (`k`, `q`, `r`, `b`, `n`, `p`)
  - Space `' '` = Empty square
- **Position**: Stored in board 2D array at `board[row][col]`
- **State**: Tracked separately (e.g., has piece moved for castling)

#### Board Representation
- **Structure**: 8x8 2D list/array
- **Access**: `board[row][col]` returns piece character or `' '`
- **Initial State**: Standard chess starting position

### Architecture Principles

1. **Separation of Concerns**
   - Core logic independent of UI
   - Pure functions for move validation
   - State mutations clearly defined

2. **Testability**
   - All core logic testable without pygame
   - Mock-free unit tests possible

3. **Modularity**
   - Each piece type in separate module
   - Rules engine separate from game state
   - Rendering separate from game logic

## Implementation Phases

### Phase 1: Core Chess Logic
Pure Python, no pygame dependencies. All game rules as functions and classes.

### Phase 2: Game Rules & Constraints
Check detection, move validation, endgame conditions.

### Phase 3: Pygame Visualization
Drawing board and pieces, visual state reflection.

### Phase 4: Player Interaction
Mouse input, move selection, UI feedback.

### Phase 5: Game Polish
Status indicators, highlights, animations.

### Phase 6: Extensions
Optional features: undo, save/load, AI, timers.
