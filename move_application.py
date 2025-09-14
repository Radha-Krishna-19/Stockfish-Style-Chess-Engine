from copy import deepcopy

def apply_move(board, move, state):
    """
    Returns a new board and updated state after applying a move.
    Supports normal moves, promotion, castling, and en passant.
    state: dict with 'castling_rights' (dict), 'en_passant' (tuple or None), 'side_to_move' ('white'/'black')
    """
    new_board = deepcopy(board)
    new_state = deepcopy(state)
    from_sq, to_sq = move[0], move[1]
    moving_piece = new_board[from_sq[0]][from_sq[1]]

    # Handle castling
    if moving_piece.upper() == 'K' and abs(to_sq[1] - from_sq[1]) == 2:
        row = from_sq[0]
        if to_sq[1] == 6:  # Kingside
            new_board[row][5] = new_board[row][7]
            new_board[row][7] = '.'
        elif to_sq[1] == 2:  # Queenside
            new_board[row][3] = new_board[row][0]
            new_board[row][0] = '.'

    # Handle en passant capture
    if moving_piece.upper() == 'P' and state.get('en_passant'):
        target = state['en_passant']
        if to_sq == target:
            if moving_piece == 'P':
                new_board[to_sq[0]+1][to_sq[1]] = '.'
            else:
                new_board[to_sq[0]-1][to_sq[1]] = '.'

    # Handle promotion
    if len(move) == 3:
        promo = move[2]
        new_board[to_sq[0]][to_sq[1]] = promo
    else:
        new_board[to_sq[0]][to_sq[1]] = moving_piece
    new_board[from_sq[0]][from_sq[1]] = '.'

    # Update en passant target
    new_state['en_passant'] = None
    if moving_piece.upper() == 'P' and abs(to_sq[0] - from_sq[0]) == 2:
        ep_row = (from_sq[0] + to_sq[0]) // 2
        new_state['en_passant'] = (ep_row, from_sq[1])

    # Update castling rights
    def disable_castle(r, c, color):
        rights = new_state['castling_rights']
        if color == 'white':
            if (r, c) == (7, 4): rights['K'], rights['Q'] = False, False
            if (r, c) == (7, 7): rights['K'] = False
            if (r, c) == (7, 0): rights['Q'] = False
        else:
            if (r, c) == (0, 4): rights['k'], rights['q'] = False, False
            if (r, c) == (0, 7): rights['k'] = False
            if (r, c) == (0, 0): rights['q'] = False

    if moving_piece == 'K':
        disable_castle(from_sq[0], from_sq[1], 'white')
    elif moving_piece == 'k':
        disable_castle(from_sq[0], from_sq[1], 'black')
    elif moving_piece == 'R':
        disable_castle(from_sq[0], from_sq[1], 'white')
    elif moving_piece == 'r':
        disable_castle(from_sq[0], from_sq[1], 'black')

    # Change side to move
    new_state['side_to_move'] = 'black' if state['side_to_move'] == 'white' else 'white'

    return new_board, new_state

def undo_move(prev_board, prev_state):
    """Restore previous board and state (for search)."""
    return deepcopy(prev_board), deepcopy(prev_state)
