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
