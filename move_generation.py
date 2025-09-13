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

def generate_white_pawn_moves(board):
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'P':  # white pawn
                # Forward move by one
                if r > 0 and board[r-1][c] == '.':
                    moves.append(((r, c), (r-1, c)))
                    
                    # Two-step move if in starting position
                    if r == 6 and board[r-2][c] == '.':
                        moves.append(((r, c), (r-2, c)))
                
                # Capture moves diagonally
                if r > 0 and c > 0 and board[r-1][c-1].islower():
                    moves.append(((r, c), (r-1, c-1)))
                if r > 0 and c < 7 and board[r-1][c+1].islower():
                    moves.append(((r, c), (r-1, c+1)))
    return moves

def generate_white_knight_moves(board):
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
                        else:
                            break
                        nr += dr
                        nc += dc
    return moves

def generate_white_rook_moves(board):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    
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
                        else:  # Own piece blocking
                            break
                        nr += dr
                        nc += dc
    return moves

def generate_white_queen_moves(board):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Rook-like directions
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Bishop-like directions
    
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

def generate_black_pawn_moves(board):
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'p':
                if r < 7 and board[r+1][c] == '.':
                    moves.append(((r, c), (r+1, c)))
                    if r == 1 and board[r+2][c] == '.':
                        moves.append(((r, c), (r+2, c)))
                if r < 7 and c > 0 and board[r+1][c-1].isupper():
                    moves.append(((r, c), (r+1, c-1)))
                if r < 7 and c < 7 and board[r+1][c+1].isupper():
                    moves.append(((r, c), (r+1, c+1)))
    return moves

def generate_black_knight_moves(board):
    moves = []
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'n':
                for dr, dc in knight_moves:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.' or target.isupper():
                            moves.append(((r, c), (nr, nc)))
    return moves

def generate_black_bishop_moves(board):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'b':
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
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'r':
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
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'q':
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
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'k':
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == '.' or target.isupper():
                            moves.append(((r, c), (nr, nc)))
    return moves