from move_generation import generate_all_moves
from move_application import apply_move
from copy import deepcopy

def simple_evaluate(board):
    """
    Simple material evaluation: positive for white, negative for black.
    """
    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0,
        '.': 0
    }
    return sum(piece_values.get(piece, 0) for row in board for piece in row)

def minimax(board, state, depth, maximizing_player, generate_moves_fn, apply_move_fn):
    """
    Simple minimax search to a fixed depth. Returns best score, best move.
    No alpha-beta pruning.
    """
    if depth == 0:
        return simple_evaluate(board), None

    moves = generate_moves_fn(board, state)
    if not moves:
        return simple_evaluate(board), None
    
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board, new_state = apply_move_fn(board, move, state)
            eval_score, _ = minimax(new_board, new_state, depth - 1, False, generate_moves_fn, apply_move_fn)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board, new_state = apply_move_fn(board, move, state)
            eval_score, _ = minimax(new_board, new_state, depth - 1, True, generate_moves_fn, apply_move_fn)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

def engine_move(board, state, depth=2):
    """
    Find and return the best move for current side, using minimax.
    """
    score, move = minimax(
        board, state, depth,
        maximizing_player=(state['side_to_move']=='white'),
        generate_moves_fn=generate_all_moves,
        apply_move_fn=apply_move
    )
    return move

if __name__ == '__main__':
    # Example initial board and state
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

    # Compute engine move
    best = engine_move(board, state, depth=2)
    print("Engine selects move:", best)
