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

if __name__ == "__main__":
    moves = generate_white_pawn_moves(board)
    for move in moves:
        print(move)
