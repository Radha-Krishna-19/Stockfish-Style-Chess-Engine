import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from move_generation import (
    generate_white_pawn_moves,
    generate_white_knight_moves,
    generate_white_bishop_moves,
    generate_white_rook_moves,
    generate_white_queen_moves,
    generate_white_king_moves,
    generate_black_pawn_moves,
    generate_black_knight_moves,
    generate_black_bishop_moves,
    generate_black_rook_moves,
    generate_black_queen_moves,
    generate_black_king_moves,
    generate_white_pawn_moves_with_promotion,
    generate_white_castling_moves,
    generate_white_pawn_en_passant,
    generate_black_pawn_moves_with_promotion,
    generate_black_castling_moves,
    generate_black_pawn_en_passant,
)

standard_board = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R']
]


def test_white_pawn_moves_standard():
    moves = generate_white_pawn_moves(standard_board)
    expected = [((6, c), (5, c)) for c in range(8)] + [((6, c), (4, c)) for c in range(8)]
    assert sorted(moves) == sorted(expected)

def test_white_knight_moves_standard():
    moves = generate_white_knight_moves(standard_board)
    expected = [((7, 1), (5, 0)), ((7, 1), (5, 2)), ((7, 6), (5, 5)), ((7, 6), (5, 7))]
    assert sorted(moves) == sorted(expected)

def test_white_bishop_moves_standard():
    moves = generate_white_bishop_moves(standard_board)
    # Initially blocked by pawns, no moves possible
    assert moves == []

def test_white_rook_moves_standard():
    moves = generate_white_rook_moves(standard_board)
    assert moves == []

def test_white_queen_moves_standard():
    moves = generate_white_queen_moves(standard_board)
    assert moves == []

def test_white_king_moves_standard():
    moves = generate_white_king_moves(standard_board)
    assert moves == []

def test_black_pawn_moves_standard():
    moves = generate_black_pawn_moves(standard_board)
    expected = [((1, c), (2, c)) for c in range(8)] + [((1, c), (3, c)) for c in range(8)]
    assert sorted(moves) == sorted(expected)

def test_black_knight_moves_standard():
    moves = generate_black_knight_moves(standard_board)
    expected = [((0, 1), (2, 0)), ((0, 1), (2, 2)), ((0, 6), (2, 5)), ((0, 6), (2, 7))]
    assert sorted(moves) == sorted(expected)

def test_black_bishop_moves_standard():
    moves = generate_black_bishop_moves(standard_board)
    assert moves == []

def test_black_rook_moves_standard():
    moves = generate_black_rook_moves(standard_board)
    assert moves == []

def test_black_queen_moves_standard():
    moves = generate_black_queen_moves(standard_board)
    assert moves == []

def test_black_king_moves_standard():
    moves = generate_black_king_moves(standard_board)
    assert moves == []

def test_white_pawn_promotion():
    board = [['.' for _ in range(8)] for __ in range(8)]
    board[1][0] = 'P'
    moves = generate_white_pawn_moves_with_promotion(board)
    expected = [
        ((1, 0), (0, 0), 'Q'),
        ((1, 0), (0, 0), 'R'),
        ((1, 0), (0, 0), 'B'),
        ((1, 0), (0, 0), 'N'),
    ]
    for move in expected:
        assert move in moves
    # Ensure no normal move without promotion on last rank
    assert not any(move == ((1, 0), (0, 0)) for move in moves)

def test_black_pawn_promotion():
    board = [['.' for _ in range(8)] for __ in range(8)]
    board[6][0] = 'p'
    moves = generate_black_pawn_moves_with_promotion(board)
    expected = [
        ((6, 0), (7, 0), 'q'),
        ((6, 0), (7, 0), 'r'),
        ((6, 0), (7, 0), 'b'),
        ((6, 0), (7, 0), 'n'),
    ]
    for move in expected:
        assert move in moves
    assert not any(move == ((6, 0), (7, 0)) for move in moves)

def test_white_castling_moves():
    board = [['.' for _ in range(8)] for __ in range(8)]
    board[7][4] = 'K'
    board[7][0] = 'R'
    board[7][7] = 'R'
    rights = {'K': True, 'Q': True}
    moves = generate_white_castling_moves(board, rights)
    expected = [((7, 4), (7, 6)), ((7, 4), (7, 2))]
    assert sorted(moves) == sorted(expected)

def test_black_castling_moves():
    board = [['.' for _ in range(8)] for __ in range(8)]
    board[0][4] = 'k'
    board[0][0] = 'r'
    board[0][7] = 'r'
    rights = {'k': True, 'q': True}
    moves = generate_black_castling_moves(board, rights)
    expected = [((0, 4), (0, 6)), ((0, 4), (0, 2))]
    assert sorted(moves) == sorted(expected)

def test_white_en_passant():
    board = [['.' for _ in range(8)] for __ in range(8)]
    board[3][3] = 'P'
    en_passant_target = (2, 4)
    moves = generate_white_pawn_en_passant(board, en_passant_target)
    expected = [((3, 3), (2, 4))]
    assert moves == expected

def test_black_en_passant():
    board = [['.' for _ in range(8)] for __ in range(8)]
    board[4][3] = 'p'
    en_passant_target = (5, 4)
    moves = generate_black_pawn_en_passant(board, en_passant_target)
    expected = [((4, 3), (5, 4))]
    assert moves == expected
