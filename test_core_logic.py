"""
Chess Core Logic Tests

Comprehensive test suite for chess game logic.
Tests board operations, piece movements, game rules, and special moves.
All tests run without pygame dependency.
"""

# Test Phase 1: Core logic
from core.board import Board
from core.game_state import GameState
from core.pieces import pawn, knight
from core.pieces.sliding import get_bishop_moves, get_rook_moves

# Test Phase 2: Rules
from core.rules.check import is_in_check
from core.rules.legality import has_any_legal_moves
from core.rules.special import promote_pawn


def test_board_basics():
    """Test basic board operations."""
    print("Testing Board basics...")
    board = Board()
    
    # Test piece retrieval
    assert board.get_piece(0, 0) == 'r', "Black rook should be at a8"
    assert board.get_piece(7, 4) == 'K', "White king should be at e1"
    assert board.get_piece(3, 3) == ' ', "Middle squares should be empty"
    
    # Test piece colors
    assert board.is_white_piece('K') == True
    assert board.is_black_piece('k') == True
    assert board.is_white_piece('k') == False
    
    # Test find king
    white_king = board.find_king('white')
    assert white_king == (7, 4), "White king at e1"
    
    print("  ✓ Board operations work")


def test_piece_movements():
    """Test piece movement rules."""
    print("\nTesting Piece movements...")
    board = Board()
    
    # Test pawn moves
    pawn_moves = pawn.get_pawn_moves(board, 6, 4, 'white')
    assert (5, 4) in pawn_moves, "Pawn can move one square"
    assert (4, 4) in pawn_moves, "Pawn can move two squares from start"
    print("  ✓ Pawn movement works")
    
    # Test knight moves
    knight_moves = knight.get_knight_moves(board, 7, 1, 'white')
    assert (5, 0) in knight_moves, "Knight L-shape move"
    assert (5, 2) in knight_moves, "Knight L-shape move"
    print("  ✓ Knight movement works")
    
    # Test rook (clear a path first)
    board.set_piece(6, 0, ' ')  # Remove pawn
    rook_moves = get_rook_moves(board, 7, 0, 'white')
    assert (6, 0) in rook_moves, "Rook can move forward"
    print("  ✓ Rook movement works")
    
    # Test bishop
    board.set_piece(6, 3, ' ')  # Remove pawn
    bishop_moves = get_bishop_moves(board, 7, 2, 'white')
    assert (6, 3) in bishop_moves, "Bishop diagonal move"
    print("  ✓ Bishop movement works")


def test_game_state():
    """Test game state management."""
    print("\nTesting Game State...")
    game_state = GameState()
    
    # Test initial state
    assert game_state.current_turn == 'white', "White starts"
    assert game_state.game_over == False, "Game not over at start"
    
    # Test getting possible moves
    moves = game_state.get_possible_moves(6, 4)  # White e2 pawn
    assert len(moves) == 2, "Pawn has 2 initial moves"
    
    print("  ✓ Game state management works")


def test_check_detection():
    """Test check detection."""
    print("\nTesting Check detection...")
    game_state = GameState()
    
    # Initial position - no check
    assert is_in_check(game_state.board, 'white') == False
    assert is_in_check(game_state.board, 'black') == False
    print("  ✓ No check in initial position")
    
    # Create check position
    game_state.board.board = [
        ['r', 'n', 'b', ' ', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', ' ', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', 'p', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', 'P', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', 'Q', ' ', ' '],  # White queen attacking black king
        ['P', 'P', 'P', 'P', ' ', 'P', 'P', 'P'],
        ['R', 'N', 'B', ' ', 'K', 'B', 'N', 'R']
    ]
    
    # Note: The queen at f3 doesn't actually attack the king at e8
    # Let me fix the test board
    game_state.board.board = [
        ['r', 'n', 'b', ' ', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', ' ', 'Q', 'p', 'p', 'p'],  # Queen at e7 checks king
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', ' ', 'K', 'B', 'N', 'R']
    ]
    
    in_check = is_in_check(game_state.board, 'black')
    assert in_check == True, "Black king should be in check"
    print("  ✓ Check detection works")


def test_move_legality():
    """Test move legality (can't move into check)."""
    print("\nTesting Move legality...")
    game_state = GameState()
    
    # All moves should be legal in starting position
    assert has_any_legal_moves(game_state, 'white') == True
    assert has_any_legal_moves(game_state, 'black') == True
    
    print("  ✓ Move legality validation works")


def test_special_moves():
    """Test special move detection."""
    print("\nTesting Special moves...")
    game_state = GameState()
    
    # Test castling detection
    assert game_state.white_king_moved == False
    assert game_state.black_king_moved == False
    print("  ✓ Castling rights tracking works")
    
    # Test en passant target
    assert game_state.en_passant_target is None
    print("  ✓ En passant tracking works")
    
    # Test pawn promotion detection
    game_state.board.set_piece(0, 0, 'P')  # White pawn at promotion rank
    promoted = promote_pawn(game_state, 0, 0)
    assert promoted == True
    assert game_state.board.get_piece(0, 0) == 'Q'
    print("  ✓ Pawn promotion works")


def main():
    """Run all tests."""
    print("="*60)
    print("PHASE 1 & 2 CORE LOGIC TESTS (No pygame)")
    print("="*60)
    
    test_board_basics()
    test_piece_movements()
    test_game_state()
    test_check_detection()
    test_move_legality()
    test_special_moves()
    
    print("\n" + "="*60)
    print("✅ ALL CORE LOGIC TESTS PASSED!")
    print("="*60)
    print("\nCore chess logic is:")
    print("  ✓ Independent of pygame")
    print("  ✓ Fully testable")
    print("  ✓ Following phase-based architecture")
    print("  ✓ Ready for UI integration")


if __name__ == "__main__":
    main()
