import chess
from move_generation import generate_all_moves
from move_application import apply_move
from copy import deepcopy
import time

# Piece-square tables reward or penalize pieces based on their positional placement on the board.
pawn_table = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

knight_table = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

bishop_table = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

rook_table = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]

queen_table = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

king_table = [
    [20, 30, 10, 0, 0, 10, 30, 20],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30]
]

piece_values = {
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
    'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000,
    '.': 0
}

center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
center_bonus_value = 50

transposition_table = {}

def board_hash(board, state):
    """Create a hashable key representing board and side to move for transposition table."""
    board_str = ''.join(''.join(row) for row in board) + state['side_to_move']
    return hash(board_str)

def get_piece_square_value(piece, r, c):
    """Return positional value of piece on board square from tables."""
    is_white = piece.isupper()
    row = r if is_white else 7 - r  # Mirror for black
    col = c
    if piece.upper() == 'P':
        val = pawn_table[row][col]
    elif piece.upper() == 'N':
        val = knight_table[row][col]
    elif piece.upper() == 'B':
        val = bishop_table[row][col]
    elif piece.upper() == 'R':
        val = rook_table[row][col]
    elif piece.upper() == 'Q':
        val = queen_table[row][col]
    elif piece.upper() == 'K':
        val = king_table[row][col]
    else:
        val = 0
    return val if is_white else -val

def find_king(board, side):
    """Find the row, col of the king of specified side."""
    king_char = 'K' if side == 'white' else 'k'
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_char:
                return r, c
    return None

def is_attacked(board, r, c, attacker_side):
    """
    Check if square (r,c) is attacked by any piece of attacker_side.
    Uses all standard chess attack vectors.
    """
    directions = {
        'N': [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)],
        'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        'R': [(-1, 0), (1, 0), (0, -1), (0, 1)],
        'Q': [(-1, -1), (-1, 1), (1, -1), (1, 1),
              (-1, 0), (1, 0), (0, -1), (0, 1)],
        'K': [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]
    }

    enemy_pawns = ['p'] if attacker_side == 'black' else ['P']
    enemy_knights = ['n'] if attacker_side == 'black' else ['N']
    enemy_bishops = ['b'] if attacker_side == 'black' else ['B']
    enemy_rooks = ['r'] if attacker_side == 'black' else ['R']
    enemy_queens = ['q'] if attacker_side == 'black' else ['Q']
    enemy_king = ['k'] if attacker_side == 'black' else ['K']

    def on_board(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    # Pawn attacks diagonally forward
    pawn_dir = 1 if attacker_side == 'white' else -1
    for dc in [-1, 1]:
        nr, nc = r + pawn_dir, c + dc
        if on_board(nr, nc) and board[nr][nc] in enemy_pawns:
            return True

    # Knight attacks
    for dr, dc in directions['N']:
        nr, nc = r + dr, c + dc
        if on_board(nr, nc) and board[nr][nc] in enemy_knights:
            return True

    # Bishop/queen diagonal attacks
    for dr, dc in directions['B']:
        nr, nc = r + dr, c + dc
        while on_board(nr, nc):
            sq = board[nr][nc]
            if sq != '.':
                if sq in enemy_bishops or sq in enemy_queens:
                    return True
                break
            nr += dr
            nc += dc

    # Rook/queen orthogonal attacks
    for dr, dc in directions['R']:
        nr, nc = r + dr, c + dc
        while on_board(nr, nc):
            sq = board[nr][nc]
            if sq != '.':
                if sq in enemy_rooks or sq in enemy_queens:
                    return True
                break
            nr += dr
            nc += dc

    # King attacks (adjacent squares)
    for dr, dc in directions['K']:
        nr, nc = r + dr, c + dc
        if on_board(nr, nc) and board[nr][nc] in enemy_king:
            return True

    return False

def is_in_check(board, state, side):
    """
    Return True if side's king is in check; False otherwise.
    Uses is_attacked helper.
    """
    king_pos = find_king(board, side)
    if king_pos is None:
        # If king is missing from the board, treat it as in check (illegal)
        return True
    r, c = king_pos
    attacker_side = 'black' if side == 'white' else 'white'
    return is_attacked(board, r, c, attacker_side)

def mobility_score(board, state, side):
    """Heuristic score based on number of legal moves for side to move."""
    moves = generate_all_moves(board, state)
    count = sum(1 for m in moves if state['side_to_move'] == side)
    return count * 10

def king_safety(board, side):
    """Penalty for opponent pieces attacking squares around king."""
    king_pos = find_king(board, side)
    if king_pos is None:
        return -100000 if side == 'white' else 100000
    kr, kc = king_pos
    danger_squares = [(kr + dr, kc + dc) for dr in range(-1, 2) for dc in range(-1, 2)
                      if 0 <= kr + dr < 8 and 0 <= kc + dc < 8]
    danger_count = 0
    opponent_side = 'black' if side == 'white' else 'white'
    for r, c in danger_squares:
        sq = board[r][c]
        if sq != '.' and ((opponent_side == 'white' and sq.isupper()) or (opponent_side == 'black' and sq.islower())):
            danger_count += 1
    return -50 * danger_count if side == 'white' else 50 * danger_count

def advanced_evaluate(board, state):
    """Combined evaluation: material, piece-square tables, center, mobility, king safety."""
    score = 0
    side = state['side_to_move']
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            score += piece_values.get(piece, 0)
            score += get_piece_square_value(piece, r, c)

    for r, c in center_squares:
        sq = board[r][c]
        if side == 'white':
            if sq.isupper():
                score += center_bonus_value
            elif sq.islower():
                score -= center_bonus_value
        else:
            if sq.islower():
                score += center_bonus_value
            elif sq.isupper():
                score -= center_bonus_value

    score += mobility_score(board, state, side)
    score += king_safety(board, side)
    return score

def is_capture_move(board, move):
    """Returns True if move is a capture."""
    from_sq, to_sq = move[0], move[1]
    return board[to_sq[0]][to_sq[1]] != '.'

def quiescence_search(board, state, alpha, beta, side_to_move):
    """
    Extend search to only capture moves when depth reaches zero to reduce horizon effect.
    """
    stand_pat = advanced_evaluate(board, state)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    moves = [m for m in generate_all_moves(board, state) if is_capture_move(board, m)]

    for move in moves:
        nb, ns = apply_move(board, move, state)
        score = -quiescence_search(nb, ns, -beta, -alpha, 'black' if side_to_move == 'white' else 'white')
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def move_ordering(board, moves):
    """
    Simple move ordering to improve alpha-beta pruning efficiency: captures first.
    """
    def move_value(move):
        from_sq, to_sq = move[0], move[1]
        target = board[to_sq[0]][to_sq[1]]
        return 1 if target != '.' else 0
    return sorted(moves, key=move_value, reverse=True)

def alphabeta(board, state, depth, alpha, beta, maximizing, generate_moves_fn, apply_move_fn):
    """
    Alpha-beta pruning minimax search with transposition table and quiescence search at leaf nodes.
    """
    key = board_hash(board, state)
    if key in transposition_table and transposition_table[key]['depth'] >= depth:
        return transposition_table[key]['value'], transposition_table[key]['best_move']

    if depth == 0:
        return quiescence_search(board, state, alpha, beta, state['side_to_move']), None

    moves = generate_moves_fn(board, state)
    moves = move_ordering(board, moves)
    if not moves:
        if is_in_check(board, state, state['side_to_move']):
            # Checkmate
            return (-100000 if maximizing else 100000), None
        else:
            # Stalemate
            return 0, None

    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            nb, ns = apply_move_fn(board, move, state)
            eval_score, _ = alphabeta(nb, ns, depth - 1, alpha, beta, False, generate_moves_fn, apply_move_fn)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        transposition_table[key] = {'value': max_eval, 'best_move': best_move, 'depth': depth}
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            nb, ns = apply_move_fn(board, move, state)
            eval_score, _ = alphabeta(nb, ns, depth - 1, alpha, beta, True, generate_moves_fn, apply_move_fn)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        transposition_table[key] = {'value': min_eval, 'best_move': best_move, 'depth': depth}
        return min_eval, best_move

def iterative_deepening_search(board, state, max_time=1.0):
    """
    Iterative deepening search with time limit.
    Gradually increases depth until time expires.
    """
    start_time = time.time()
    depth = 1
    best_move = None
    while True:
        if time.time() - start_time > max_time:
            break
        score, move = alphabeta(board, state, depth, float('-inf'), float('inf'),
                               maximizing=(state['side_to_move'] == 'white'),
                               generate_moves_fn=generate_all_moves,
                               apply_move_fn=apply_move)
        if move is not None:
            best_move = move
        depth += 1
    return best_move

def engine_move(board, state, max_time=1.0):
    """Interface for getting engine move within time limit."""
    return iterative_deepening_search(board, state, max_time)

def board_to_fen(board, state):
    fen_rows = []
    for row in board:
        empty_count = 0
        fen_row = ""
        for cell in row:
            if cell == '.':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    fen_position = '/'.join(fen_rows)
    cr = state.get('castling_rights', {})
    cr_str = ""
    cr_str += 'K' if cr.get('K', False) else ''
    cr_str += 'Q' if cr.get('Q', False) else ''
    cr_str += 'k' if cr.get('k', False) else ''
    cr_str += 'q' if cr.get('q', False) else ''
    if cr_str == "":
        cr_str = '-'
    ep = state.get('en_passant', None)
    if ep:
        row, col = ep
        ep_str = chr(ord('a') + col) + str(8 - row)
    else:
        ep_str = '-'
    stm = 'w' if state.get('side_to_move', 'white') == 'white' else 'b'
    halfmove_clock = '0'
    fullmove_number = '1'
    return f"{fen_position} {stm} {cr_str} {ep_str} {halfmove_clock} {fullmove_number}"

def san_to_move(board, state, san):
    fen = board_to_fen(board, state)
    board_obj = chess.Board(fen)
    try:
        move = board_obj.parse_san(san)
    except ValueError:
        raise ValueError(f"Invalid SAN: {san}")
    from_sq = move.from_square
    to_sq = move.to_square
    promotion = move.promotion
    from_row = 7 - chess.square_rank(from_sq)
    from_col = chess.square_file(from_sq)
    to_row = 7 - chess.square_rank(to_sq)
    to_col = chess.square_file(to_sq)
    if promotion:
        promo_piece = chess.piece_symbol(promotion).upper()
        return ((from_row, from_col), (to_row, to_col), promo_piece)
    return ((from_row, from_col), (to_row, to_col))

def print_board(board):
    print("  a b c d e f g h")
    for i, row in enumerate(board):
        print(8 - i, ' '.join(row))
    print()

def play_game():
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
    user_side = None
    while True:
        side_input = input("Choose your side (white/black): ").strip().lower()
        if side_input in ['white', 'black']:
            user_side = side_input
            break
        else:
            print("Invalid input, please enter 'white' or 'black'")

    while True:
        print_board(board)
        if state['side_to_move'] == user_side:
            san = input("Your move (SAN): ")
            try:
                move = san_to_move(board, state, san.strip())
            except Exception as e:
                print("Invalid move:", e)
                continue
            board, state = apply_move(board, move, state)
        else:
            print("AI thinking...")
            best = engine_move(board, state, max_time=1.0)
            if best is None:
                print("Game over!")
                break
            board, state = apply_move(board, best, state)
            print(f"AI plays: {best}")

if __name__ == '__main__':
    play_game()
