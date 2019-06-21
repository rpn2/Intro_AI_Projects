from BoardFast import *
import copy
import operator

MAX_DEPTH = 5
INF = 999999
player = 0
numnodes = 0



def alphabeta(board, p1pieces, p2pieces, actions, inPlayer):
    global player
    player = inPlayer
    global numnodes
    numnodes = 0

    max_utility = -INF
    max_action = []
    alpha = -INF
    beta = INF
   
    
    
    #orderedactions = moveordering(board, p1pieces, p2pieces, actions,True) 
    
    for action in actions:
        '''board_copy = copy.deepcopy(board)
        p1pieces_copy = copy.deepcopy(p1pieces)
        p2pieces_copy = copy.deepcopy(p2pieces)'''
        board_copy = [x[:] for x in board]
        p1pieces_copy = [x[:] for x in p1pieces]
        p2pieces_copy = [x[:] for x in p2pieces]
        [Newboard, Newp1pieces, Newp2pieces] = move(action,board_copy,p1pieces_copy,p2pieces_copy)
        numnodes = numnodes + 1
        utility = min_value(Newboard, Newp1pieces, Newp2pieces, 1, alpha, beta)

        #In the first iteration, we do not check against beta for pruning,
        #We just check to see if this is the best action found so far.
        if(utility > max_utility):
            max_utility = utility
            max_action = action
            
        alpha = max_utility
    return [max_utility, max_action,numnodes]

def max_value(board, p1pieces, p2pieces, depth, inAlpha, inBeta):
    alpha = copy.deepcopy(inAlpha)
    beta = copy.deepcopy(inBeta)
    
    global numnodes
    
    gameEnd = check_end(board, p1pieces, p2pieces)
    if(gameEnd == (2-(player+1)%2)):
        return -10000
    if(gameEnd == player):
        return 10000
    if(depth == MAX_DEPTH):        
        return calculateHeuristic(player,board, p1pieces, p2pieces)

    actions = get_actions(player,board, p1pieces, p2pieces)
    utility = -INF
    
    #orderedactions = moveordering(board, p1pieces, p2pieces, actions,True) 

    for action in actions:
        '''board_copy = copy.deepcopy(board)
        p1pieces_copy = copy.deepcopy(p1pieces)
        p2pieces_copy = copy.deepcopy(p2pieces)'''

        board_copy = [x[:] for x in board]
        p1pieces_copy = [x[:] for x in p1pieces]
        p2pieces_copy = [x[:] for x in p2pieces]
        [Newboard, Newp1pieces, Newp2pieces] = move(action,board_copy, p1pieces_copy, p2pieces_copy)
        numnodes = numnodes + 1
        utility = max(utility, min_value(Newboard, Newp1pieces, Newp2pieces, depth+1, alpha, beta))
        if(utility >= beta):
            return utility
        alpha = max(alpha, utility)

    return utility
           
def min_value(board, p1pieces, p2pieces, depth, inAlpha, inBeta):
    alpha = copy.deepcopy(inAlpha)
    beta = copy.deepcopy(inBeta)
    global numnodes
    
    gameEnd = check_end(board, p1pieces, p2pieces)
    if(gameEnd == (2-(player+1)%2)):
        return -10000
    if(gameEnd == player):
        return 10000
    if(depth == MAX_DEPTH):        
        return calculateHeuristic(player,board, p1pieces, p2pieces)

    actions = get_actions((2-(player+1)%2),board, p1pieces, p2pieces)
    utility = INF

    #orderedactions = moveordering(board, p1pieces, p2pieces, actions,False)
    
    for action in actions:
        '''board_copy = copy.deepcopy(board)
        p1pieces_copy = copy.deepcopy(p1pieces)
        p2pieces_copy = copy.deepcopy(p2pieces)'''
        board_copy = [x[:] for x in board]
        p1pieces_copy = [x[:] for x in p1pieces]
        p2pieces_copy = [x[:] for x in p2pieces]
        [Newboard, Newp1pieces, Newp2pieces] = move(action,board_copy, p1pieces_copy, p2pieces_copy)
        numnodes = numnodes + 1
        utility = min(utility, max_value(Newboard, Newp1pieces, Newp2pieces, depth+1, alpha, beta))
        if(utility <= alpha):
            return utility
        beta = min(beta, utility)
        
    return utility
    
def moveordering(board, p1pieces, p2pieces, actions,desc):

    dictofactions = {}

    for action in actions:
        '''board_copy = copy.deepcopy(board)
        p1pieces_copy = copy.deepcopy(p1pieces)
        p2pieces_copy = copy.deepcopy(p2pieces)'''
        board_copy = [x[:] for x in board]
        p1pieces_copy = [x[:] for x in p1pieces]
        p2pieces_copy = [x[:] for x in p2pieces]
        [Newboard, Newp1pieces, Newp2pieces] = move(action,board_copy, p1pieces_copy, p2pieces_copy)
        dictofactions[tuple(action)] = calculateHeuristic(player,Newboard, Newp1pieces, Newp2pieces)
         
    #order
    sortedlist = sorted(dictofactions.items(), key =operator.itemgetter(1)) 
    if desc:
        sortedlist.reverse()

    orderedlist = []
    for x in sortedlist:        
        orderedlist.append(x[0])
        
    return orderedlist

    


