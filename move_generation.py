# Define the board
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

# ---------- White piece move generation ----------

def generate_white_pawn_moves(board):
    """
    Generate normal white pawn moves:
    - Move forward by 1 square
    - Move forward by 2 squares if on starting rank and path is clear
    - Capture diagonally if opponent piece present
    """
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'P':  # White pawn
                # Forward 1 square
                if r > 0 and board[r-1][c] == '.':
                    moves.append(((r, c), (r-1, c)))
                    # Forward 2 squares from start position
                    if r == 6 and board[r-2][c] == '.':
                        moves.append(((r, c), (r-2, c)))

                # Capture diagonally left
                if r > 0 and c > 0 and board[r-1][c-1].islower():
                    moves.append(((r, c), (r-1, c-1)))
                # Capture diagonally right
                if r > 0 and c < 7 and board[r-1][c+1].islower():
                    moves.append(((r, c), (r-1, c+1)))
    return moves


def generate_white_knight_moves(board):
    """
    Generate white knight moves:
    - Knights move in 'L' shape to 8 possible squares
    - Moves valid if target empty or opponent piece
    """
    moves = []
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'N':  # White knight
                for dr, dc in knight_moves:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.' or target.islower():
                            moves.append(((r, c), (nr, nc)))
    return moves


def generate_white_bishop_moves(board):
    """
    Generate white bishop moves:
    - Moves diagonally in 4 directions until blocked
    - Stop at friendly piece, capture opponent piece and stop
    """
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'B':  # White bishop
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.':
                            moves.append(((r, c), (nr, nc)))
                        elif target.islower():
                            moves.append(((r, c), (nr, nc)))
                            break
                        else:  # Blocked by friendly piece
                            break
                        nr += dr
                        nc += dc
    return moves


def generate_white_rook_moves(board):
    """
    Generate white rook moves:
    - Moves orthogonally in 4 directions until blocked
    - Stop at friendly piece, capture opponent piece and stop
    """
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'R':  # White rook
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.':
                            moves.append(((r, c), (nr, nc)))
                        elif target.islower():
                            moves.append(((r, c), (nr, nc)))
                            break
                        else:
                            break
                        nr += dr
                        nc += dc
    return moves


def generate_white_queen_moves(board):
    """
    Generate white queen moves:
    - Combines rook and bishop moves along 8 directions
    """
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'Q':  # White queen
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.':
                            moves.append(((r, c), (nr, nc)))
                        elif target.islower():
                            moves.append(((r, c), (nr, nc)))
                            break
                        else:
                            break
                        nr += dr
                        nc += dc
    return moves


def generate_white_king_moves(board):
    """
    Generate white king moves:
    - Moves one square in any of 8 directions if not blocked
    """
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'K':  # White king
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.' or target.islower():
                            moves.append(((r, c), (nr, nc)))
    return moves


# ---------- Black piece move generation ----------

def generate_black_pawn_moves(board):
    """
    Generate normal black pawn moves:
    - Move forward by 1 square
    - Move forward by 2 squares if on starting rank and path clear
    - Capture diagonally opponent pieces
    """
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'p':  # Black pawn
                # Forward 1 square
                if r < 7 and board[r+1][c] == '.':
                    moves.append(((r, c), (r+1, c)))
                    # Forward 2 squares from start rank
                    if r == 1 and board[r+2][c] == '.':
                        moves.append(((r, c), (r+2, c)))
                # Capture diagonally left
                if r < 7 and c > 0 and board[r+1][c-1].isupper():
                    moves.append(((r, c), (r+1, c-1)))
                # Capture diagonally right
                if r < 7 and c < 7 and board[r+1][c+1].isupper():
                    moves.append(((r, c), (r+1, c+1)))
    return moves


def generate_black_knight_moves(board):
    """
    Generate black knight moves:
    - Knights move in 'L' shape, valid moves to empty or opponent square
    """
    moves = []
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'n':  # Black knight
                for dr, dc in knight_moves:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.' or target.isupper():
                            moves.append(((r, c), (nr, nc)))
    return moves


def generate_black_bishop_moves(board):
    """
    Generate black bishop moves:
    - Bishop moves diagonally until blocked by friendly
    - Can capture opponent piece and then stop
    """
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'b':  # Black bishop
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.':
                            moves.append(((r, c), (nr, nc)))
                        elif target.isupper():
                            moves.append(((r, c), (nr, nc)))
                            break
                        else:
                            break
                        nr += dr
                        nc += dc
    return moves


def generate_black_rook_moves(board):
    """
    Generate black rook moves:
    - Moves orthogonally until blocked by own piece
    - Can capture opponent piece and stop
    """
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'r':  # Black rook
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.':
                            moves.append(((r, c), (nr, nc)))
                        elif target.isupper():
                            moves.append(((r, c), (nr, nc)))
                            break
                        else:
                            break
                        nr += dr
                        nc += dc
    return moves


def generate_black_queen_moves(board):
    """
    Generate black queen moves:
    - Combines rook and bishop moves in 8 directions
    """
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'q':  # Black queen
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.':
                            moves.append(((r, c), (nr, nc)))
                        elif target.isupper():
                            moves.append(((r, c), (nr, nc)))
                            break
                        else:
                            break
                        nr += dr
                        nc += dc
    return moves


def generate_black_king_moves(board):
    """
    Generate black king moves:
    - One square in any direction to empty or opponent square
    """
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'k':  # Black king
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.' or target.isupper():
                            moves.append(((r, c), (nr, nc)))
    return moves


# ---------- Special moves ----------

def generate_white_pawn_moves_with_promotion(board):
    """
    Generate white pawn moves including promotion moves.
    Promotions are moves to the 0th rank with piece options:
    'Q', 'R', 'B', 'N'
    Returns moves of form:
    - ((from_r, from_c), (to_r, to_c)) for normal moves
    - ((from_r, from_c), (to_r, to_c), promotion_piece) for promotions
    """
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'P':
                # Forward 1 move (non promotion)
                if r > 1 and board[r-1][c] == '.':
                    moves.append(((r, c), (r-1, c)))
                # Forward 1 move (promotion)
                if r == 1 and board[0][c] == '.':
                    for promo in ['Q', 'R', 'B', 'N']:
                        moves.append(((r, c), (0, c), promo))

                # Captures (normal and promotion)
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nc < 8:
                        # Promotion capture
                        if r == 1 and board[0][nc].islower():
                            for promo in ['Q', 'R', 'B', 'N']:
                                moves.append(((r, c), (0, nc), promo))
                        # Normal capture
                        elif r > 1 and board[r-1][nc].islower():
                            moves.append(((r, c), (r-1, nc)))
    return moves


def generate_white_castling_moves(board, castling_rights):
    """
    Generate white castling moves based on castling rights.
    castling_rights is a dict with boolean keys 'K' for kingside and 'Q' for queenside.
    This example does not check for check or attacks.
    """
    moves = []
    r, c = 7, 4  # King's starting position

    # Kingside castling
    if castling_rights.get('K', False):
        if board[7][5] == '.' and board[7][6] == '.':
            moves.append(((7, 4), (7, 6)))

    # Queenside castling
    if castling_rights.get('Q', False):
        if board[7][1] == '.' and board[7][2] == '.' and board[7][3] == '.':
            moves.append(((7, 4), (7, 2)))

    return moves


def generate_white_pawn_en_passant(board, en_passant_target):
    """
    Generate white pawn moves for en passant captures.
    en_passant_target is a tuple (row, column) where en passant capture is possible,
    or None if no en passant available.
    Valid only if white pawn is on rank 4 (row 3), adjacent to target.
    """
    moves = []
    if not en_passant_target:
        return moves

    er, ec = en_passant_target
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'P':
                # White pawn must be on row 3 and adjacent to en passant column
                if r == 3 and abs(c - ec) == 1 and er == 2:
                    moves.append(((r, c), (er, ec)))
    return moves

def generate_black_pawn_moves_with_promotion(board):
    """
    Generate black pawn moves including promotion moves.
    Promotions happen when a black pawn moves to row 7 (last rank).
    Returns moves with a promotion piece as a third tuple item.
    """
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'p':
                # Forward 1 move (non promotion)
                if r < 6 and board[r+1][c] == '.':
                    moves.append(((r, c), (r+1, c)))
                # Forward 1 move (promotion)
                if r == 6 and board[7][c] == '.':
                    for promo in ['q', 'r', 'b', 'n']:
                        moves.append(((r, c), (7, c), promo))

                # Capture moves (normal and promotion)
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nc < 8:
                        # Promotion capture
                        if r == 6 and board[7][nc].isupper():
                            for promo in ['q', 'r', 'b', 'n']:
                                moves.append(((r, c), (7, nc), promo))
                        # Normal capture
                        elif r < 6 and board[r+1][nc].isupper():
                            moves.append(((r, c), (r+1, nc)))
    return moves


def generate_black_castling_moves(board, castling_rights):
    """
    Generate black castling moves if castling rights allow.
    King starts at (0, 4).
    castling_rights is dict with keys 'k' (kingside), 'q' (queenside).
    This example does not check for checks or attacks along path.
    """
    moves = []
    r, c = 0, 4  # Black king start square

    # Kingside castling
    if castling_rights.get('k', False):
        # Squares between king and rook must be empty
        if board[0][5] == '.' and board[0][6] == '.':
            moves.append(((r, c), (0, 6)))

    # Queenside castling
    if castling_rights.get('q', False):
        # Squares between king and rook must be empty
        if board[0][1] == '.' and board[0][2] == '.' and board[0][3] == '.':
            moves.append(((r, c), (0, 2)))

    return moves


def generate_black_pawn_en_passant(board, en_passant_target):
    """
    Generate black pawn en passant captures.
    en_passant_target is the square (row, col) where en passant capture is possible.
    Valid if black pawn is on 5th rank (row 4) and adjacent to target.
    """
    moves = []
    if not en_passant_target:
        return moves

    er, ec = en_passant_target
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'p':
                # Black pawn must be on row 4 and adjacent to target col
                if r == 4 and abs(c - ec) == 1 and er == 5:
                    moves.append(((r, c), (er, ec)))
    return moves
