import chess
from move_generation import generate_all_moves
from move_application import apply_move
from copy import deepcopy

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

def find_king(board, side):
    king_char = 'K' if side == 'white' else 'k'
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_char:
                return r, c
    return None

def is_attacked(board, r, c, attacker_side):
    directions = {
        'N': [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)],
        'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        'R': [(-1, 0), (1, 0), (0, -1), (0, 1)],
        'Q': [(-1, -1), (-1, 1), (1, -1), (1, 1),
              (-1, 0), (1, 0), (0, -1), (0, 1)],
        'K': [(-1, -1), (-1, 0), (-1, 1),
              (0, -1), (0, 1),
              (1, -1), (1, 0), (1, 1)]
    }
    enemy_pawns = ['p'] if attacker_side == 'black' else ['P']
    enemy_knights = ['n'] if attacker_side == 'black' else ['N']
    enemy_bishops = ['b'] if attacker_side == 'black' else ['B']
    enemy_rooks = ['r'] if attacker_side == 'black' else ['R']
    enemy_queen = ['q'] if attacker_side == 'black' else ['Q']
    enemy_king = ['k'] if attacker_side == 'black' else ['K']

    def on_board(x, y): return 0 <= x < 8 and 0 <= y < 8

    # Pawn attacks
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

    # Bishop/queen diagonal
    for dr, dc in directions['B']:
        nr, nc = r + dr, c + dc
        while on_board(nr, nc):
            sq = board[nr][nc]
            if sq != '.':
                if sq in enemy_bishops or sq in enemy_queen:
                    return True
                break
            nr += dr
            nc += dc

    # Rook/queen horizontal/vertical
    for dr, dc in directions['R']:
        nr, nc = r + dr, c + dc
        while on_board(nr, nc):
            sq = board[nr][nc]
            if sq != '.':
                if sq in enemy_rooks or sq in enemy_queen:
                    return True
                break
            nr += dr
            nc += dc

    # King attacks
    for dr, dc in directions['K']:
        nr, nc = r + dr, c + dc
        if on_board(nr, nc) and board[nr][nc] in enemy_king:
            return True

    return False

def is_in_check(board, state, side):
    king_pos = find_king(board, side)
    if king_pos is None:
        return True
    return is_attacked(board, king_pos[0], king_pos[1], 'black' if side == 'white' else 'white')

def generate_legal_moves(board, state):
    all_moves = generate_all_moves(board, state)
    legal = []
    for move in all_moves:
        nb, ns = apply_move(board, move, state)
        if not is_in_check(nb, ns, state['side_to_move']):
            legal.append(move)
    return legal

def simple_evaluate(board):
    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0,
        '.': 0
    }
    return sum(piece_values.get(piece, 0) for row in board for piece in row)

def alphabeta(board, state, depth, alpha, beta, maximizing, generate_moves_fn, apply_move_fn):
    if depth == 0:
        return simple_evaluate(board), None

    moves = generate_moves_fn(board, state)
    if not moves:
        if is_in_check(board, state, 'white' if maximizing else 'black'):
            return (-100000 if maximizing else 100000), None
        else:
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
        return min_eval, best_move

def engine_move(board, state, depth=3):
    return alphabeta(
        board, state, depth,
        alpha=float('-inf'), beta=float('inf'),
        maximizing=(state['side_to_move'] == 'white'),
        generate_moves_fn=generate_legal_moves,
        apply_move_fn=apply_move
    )[1]

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
    while True:
        print_board(board)
        if state['side_to_move'] == 'white':
            san = input("Your move (SAN): ")
            try:
                move = san_to_move(board, state, san.strip())
            except Exception as e:
                print("Invalid move:", e)
                continue
            board, state = apply_move(board, move, state)
        else:
            print("AI thinking...")
            best = engine_move(board, state, depth=3)
            if best is None:
                print("Game over!")
                break
            board, state = apply_move(board, best, state)
            print(f"AI plays: {best}")

if __name__ == '__main__':
    play_game()
