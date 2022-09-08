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

    x_count = 0
    o_count = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                x_count += 1
            elif board[i][j] == 'O':
                o_count += 1

    if x_count < o_count:
        return 'X'
    elif o_count < x_count:
        return 'O'
    else:
        return 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.append((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] != EMPTY:
        raise NameError('illegal move')
    else:
        board_new = copy.deepcopy(board)
        board_new[action[0]][action[1]] = player(board)
        return board_new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[1][1]
    elif board[2][0] == board[1][1] == board[0][2] != EMPTY:
        return board[1][1]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_cells = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                empty_cells += 1
    if empty_cells == 0:
        return True

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return True
    elif board[2][0] == board[1][1] == board[0][2] != EMPTY:
        return True
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return True
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # when player is MaxPlayer

    elif player(board) == 'X':
        v = -1000
        i = 0
        j = 0
        for action in actions(board):
            if MinPlayer(result(board, action)) > v:
                i, j = action
                v = MinPlayer(result(board, action))

        return (i, j)

    # when player is MinPlayer

    else:
        v = 1000
        i = 0
        j = 0
        for action in actions(board):
            if MaxPlayer(result(board, action)) < v:
                i, j = action
                v = MaxPlayer(result(board, action))
        return (i, j)


def MinPlayer(board):
    if terminal(board):
        return utility(board)
    v = 1000
    for action in actions(board):
        v = min(v, MaxPlayer(result(board, action)))
    return v


def MaxPlayer(board):
    if terminal(board):
        return utility(board)
    v = -1000
    for action in actions(board):
        v = max(v, MinPlayer(result(board, action)))
    return v
