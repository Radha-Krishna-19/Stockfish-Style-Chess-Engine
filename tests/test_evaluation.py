import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from main import advanced_evaluate, engine_move

def test_evaluation_simple():
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
    score = advanced_evaluate(board, state)
    assert isinstance(score, (int, float))

def test_engine_move_returns_move():
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
    move = engine_move(board, state, max_time=0.1)
    assert move is not None
