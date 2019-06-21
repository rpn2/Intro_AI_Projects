from BoardFast import *
import copy

INF = 999999
numnodes = 0


def minimax(board, p1pieces, p2pieces, actions):
    max_utility = -INF
    max_action = []
    global numnodes
    numnodes = 0
    
    for action in actions:
        board_copy = [x[:] for x in board]
        p1pieces_copy = [x[:] for x in p1pieces]
        p2pieces_copy = [x[:] for x in p2pieces]

        [Newboard, Newp1pieces, Newp2pieces] = move(action,board_copy,p1pieces_copy,p2pieces_copy)
        numnodes = numnodes + 1
        utility = min_value(Newboard, Newp1pieces, Newp2pieces, 1)
        
        if(utility > max_utility):
            max_utility = utility
            max_action = action
    return [max_utility, max_action, numnodes]

def max_value(board, p1pieces, p2pieces, depth):
    global numnodes
    gameEnd = check_end(board, p1pieces, p2pieces)
    if(gameEnd == 2):
        return -10000
    if(gameEnd == 1):
        return 10000
    if(depth == 3):
        return calculateHeuristic(1,board, p1pieces, p2pieces)

    actions = get_actions(1,board, p1pieces, p2pieces)
    max_utility = -INF
    for action in actions:
        board_copy = [x[:] for x in board]
        p1pieces_copy = [x[:] for x in p1pieces]
        p2pieces_copy = [x[:] for x in p2pieces]
        [Newboard, Newp1pieces, Newp2pieces] = move(action,board_copy, p1pieces_copy, p2pieces_copy)
        numnodes = numnodes + 1
        utility = min_value(Newboard, Newp1pieces, Newp2pieces, depth+1)
        if(utility > max_utility):
            max_utility = utility

    return max_utility
           
def min_value(board, p1pieces, p2pieces, depth):
    global numnodes
    gameEnd = check_end(board, p1pieces, p2pieces)
    if(gameEnd == 2):
        return -10000
    if(gameEnd == 1):
        return 10000
    if(depth == 3):
        return calculateHeuristic(1,board, p1pieces, p2pieces)

    actions = get_actions(2,board, p1pieces, p2pieces)
    min_utility = INF
    for action in actions:
        board_copy = [x[:] for x in board]
        p1pieces_copy = [x[:] for x in p1pieces]
        p2pieces_copy = [x[:] for x in p2pieces]
        [Newboard, Newp1pieces, Newp2pieces] = move(action,board_copy, p1pieces_copy, p2pieces_copy)
        numnodes = numnodes + 1
        utility = max_value(Newboard, Newp1pieces, Newp2pieces, depth+1)
        if(utility < min_utility):
            min_utility = utility

    return min_utility
    
    
