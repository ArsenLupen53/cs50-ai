"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if not (0 <= i < 3 and 0 <= j < 3) or board[i][j] is not EMPTY:
        raise ValueError("Invalid action")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []
    lines.extend(board)                                              # rows
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])  # columns
    lines.append([board[k][k] for k in range(3)])                    # diagonal
    lines.append([board[k][2 - k] for k in range(3)])                # anti-diagonal

    for line in lines:
        if line[0] is not EMPTY and line[0] == line[1] == line[2]:
            return line[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not actions(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def max_value(b, alpha, beta):
        if terminal(b):
            return utility(b)
        v = -math.inf
        for a in actions(b):
            v = max(v, min_value(result(b, a), alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v

    def min_value(b, alpha, beta):
        if terminal(b):
            return utility(b)
        v = math.inf
        for a in actions(b):
            v = min(v, max_value(result(b, a), alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v

    best_action = None
    if player(board) == X:
        best = -math.inf
        for a in actions(board):
            v = min_value(result(board, a), -math.inf, math.inf)
            if v > best:
                best, best_action = v, a
    else:
        best = math.inf
        for a in actions(board):
            v = max_value(result(board, a), -math.inf, math.inf)
            if v < best:
                best, best_action = v, a
    return best_action