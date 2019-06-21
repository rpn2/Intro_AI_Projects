# Main file

from BoardFast import *

import AlphaBetaFast
import time

[board, p1pieces, p2pieces] = InitialState()


player = 1
#not game.check_end()
#j = 0

total_nodes_expanded = [-1,0,0]
numMoves = [-1, 0, 0]
totalElapsedTime = [-1,0,0]

start_time = time.time()
while(not check_end(board, p1pieces, p2pieces)):
    #j = j + 1
    actions = get_actions(player,board,p1pieces,p2pieces)
    action = None
    utility = 0
    print("P",player," turn")
    t = time.time()
    [utility, action, numNodes] = AlphaBetaFast.alphabeta(board,p1pieces,p2pieces,actions,player)
    elapsed = time.time() - t
    totalElapsedTime[player] += elapsed
    print("Elapsed ",elapsed," s")

    numMoves[player] += 1

    total_nodes_expanded[player] += numNodes
    print("Nodes expanded: ", numNodes)
    
    #print(action)
    [board, p1pieces, p2pieces] = move(action,board, p1pieces, p2pieces)
    print_board(board)
    #print("------------------")
    
    #Fancy way to switch players
    player = 2 - (player+1)%2

total_time = time.time() - start_time
print("The winner is...P",check_end(board, p1pieces, p2pieces),"!")
print("P1 expanded ",total_nodes_expanded[1]," nodes, averaging ",total_nodes_expanded[1]/numMoves[1]," per move")
print("P2 expanded ",total_nodes_expanded[2]," nodes, averaging ",total_nodes_expanded[2]/numMoves[2]," per move")
print("P1 took an average of ",totalElapsedTime[1]/numMoves[1]," seconds per move")
print("P2 took an average of ",totalElapsedTime[2]/numMoves[2]," seconds per move")
print("P1 captured ",16-len(p2pieces)," of P2's workers")
print("P2 captured ",16-len(p1pieces)," of P1's workers")
print("Total game time ",total_time," s")
print("Total number of moves: ",numMoves[1]+numMoves[2])
