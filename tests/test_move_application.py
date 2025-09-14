import sys
import os
from copy import deepcopy

# Add project root directory to sys.path to allow imports from the root folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from move_application import apply_move, undo_move

# Test applying a simple pawn move e2 to e4 and validate board/state update
def test_apply_simple_move():
    board = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ]
    state = {
        'castling_rights': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': None,
        'side_to_move': 'white'
    }
    move = ((6,4), (4,4))  # White pawn from e2 to e4
    new_board, new_state = apply_move(board, move, state)

    # Check pawn moved correctly
    assert new_board[4][4] == 'P'
    assert new_board[6][4] == '.'
    # Side to move changed
    assert new_state['side_to_move'] == 'black'
    # En passant square correctly set (square behind pawn)
    assert new_state['en_passant'] == (5,4)

# Test applying pawn promotion move with all promotion types
def test_apply_pawn_promotion():
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[1][0] = 'P'  # White pawn ready to promote
    state = {
        'castling_rights': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': None,
        'side_to_move': 'white'
    }
    move = ((1,0), (0,0), 'Q')  # Promote to queen
    new_board, new_state = apply_move(board, move, state)

    # Pawn replaced by promoted piece
    assert new_board[0][0] == 'Q'
    assert new_board[1][0] == '.'
    # Side to move changed after promotion
    assert new_state['side_to_move'] == 'black'

# Test applying kingside castling move, and verify rook moves
def test_apply_castling():
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[7][4] = 'K'
    board[7][7] = 'R'
    state = {
        'castling_rights': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': None,
        'side_to_move': 'white'
    }
    move = ((7,4), (7,6))  # White kingside castle
    new_board, new_state = apply_move(board, move, state)

    # King moved correctly
    assert new_board[7][6] == 'K'
    # Rook moved correctly to square between old and new king position
    assert new_board[7][5] == 'R'
    # Original rook and king squares are empty
    assert new_board[7][7] == '.'
    assert new_board[7][4] == '.'
    # Castling rights lost after king move
    assert new_state['castling_rights']['K'] is False
    assert new_state['castling_rights']['Q'] is False
    # Side to move changes after castling
    assert new_state['side_to_move'] == 'black'

# Test applying en passant capture move and verify captured pawn is removed
def test_apply_en_passant():
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'P'  # White pawn on d5
    board[3][4] = 'p'  # Black pawn on e5 (to be captured en passant)
    state = {
        'castling_rights': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': (2, 4),  # e6 square en passant target
        'side_to_move': 'white'
    }
    move = ((3, 3), (2, 4))  # White pawn captures en passant

    new_board, new_state = apply_move(board, move, state)
    # Check white pawn moved diagonally
    assert new_board[2][4] == 'P'
    # Original white pawn square emptied
    assert new_board[3][3] == '.'
    # Captured black pawn is removed from board
    assert new_board[3][4] == '.'

# Test undoing a move restores previous board and state exactly
def test_undo_move():
    board = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ]
    state = {
        'castling_rights': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': None,
        'side_to_move': 'white'
    }

    prev_board = deepcopy(board)
    prev_state = deepcopy(state)

    move = ((6,4), (4,4))  # e2 to e4
    new_board, new_state = apply_move(board, move, state)
    undo_board, undo_state = undo_move(prev_board, prev_state)

    # Undo restores original board and state
    assert undo_board == prev_board
    assert undo_state == prev_state
