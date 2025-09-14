import sys
import os
from copy import deepcopy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from move_application import apply_move, undo_move

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

    move = ((6,4), (4,4))  # e2 to e4
    new_board, new_state = apply_move(board, move, state)

    assert new_board[4][4] == 'P'
    assert new_board[6][4] == '.'
    assert new_state['side_to_move'] == 'black'
    assert new_state['en_passant'] == (5, 4)

def test_apply_pawn_promotion():
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[1][0] = 'P'
    state = {
        'castling_rights': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': None,
        'side_to_move': 'white'
    }

    move = ((1, 0), (0, 0), 'Q')  # Promote to queen
    new_board, new_state = apply_move(board, move, state)

    assert new_board[0][0] == 'Q'
    assert new_board[1][0] == '.'
    assert new_state['side_to_move'] == 'black'

def test_apply_castling():
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[7][4] = 'K'
    board[7][7] = 'R'
    state = {
        'castling_rights': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': None,
        'side_to_move': 'white'
    }

    move = ((7, 4), (7, 6))  # White kingside castling
    new_board, new_state = apply_move(board, move, state)

    assert new_board[7][6] == 'K'
    assert new_board[7][5] == 'R'
    assert new_board[7][7] == '.'
    assert new_board[7][4] == '.'
    assert not new_state['castling_rights']['K']
    assert not new_state['castling_rights']['Q']
    assert new_state['side_to_move'] == 'black'

def test_apply_en_passant():
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'P'  # White pawn at d5
    board[3][4] = 'p'  # Black pawn at e5 (to be captured en passant)
    state = {
        'castling_rights': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': (2, 4),
        'side_to_move': 'white'
    }

    move = ((3, 3), (2, 4))  # White captures en passant
    new_board, new_state = apply_move(board, move, state)

    assert new_board[2][4] == 'P'
    assert new_board[3][3] == '.'
    assert new_board[3][4] == '.'

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
    move = ((6, 4), (4, 4))  # e2 to e4
    new_board, new_state = apply_move(board, move, state)
    undo_board, undo_state = deepcopy(prev_board), deepcopy(prev_state)

    assert undo_board == prev_board
    assert undo_state == prev_state
