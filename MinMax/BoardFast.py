#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

# Game board

# Change the heuristic used by each player here. (Off1,Off2, Def1, Def2, Null)
# heuristicMap = {1 : "Off1", 2: "Def2"}

heuristicMap = {1: 'Off2', 2: 'Def2'}


def InitialState():
    board = [[0 for col in range(8)] for row in range(8)]
    p1pieces = []
    p2pieces = []

    for row in [0, 1]:
        for col in range(8):
            board[row][col] = 2
            p2pieces.append([row, col])

    for row in [6, 7]:
        for col in range(8):
            board[row][col] = 1
            p1pieces.append([row, col])

    for row in board:
        print (row)
    print ('------------------')
    return [board, p1pieces, p2pieces]


def get_actions(player,board,p1pieces,p2pieces):
    # Action is defined by [a,b,c,d] where: [a=starting row, b=starting col, c=ending row, d=ending col]
    actions = []

    if player == 1:
        # Sort by row (choose rows near top first)
        p1pieces.sort()
        for piece in p1pieces:
            [r, c] = [piece[0], piece[1]]

            # If upleft is free (has an enemy or empty space)
            if c > 0 and not board[r - 1][c - 1] == 1:
                actions.append([r, c, r - 1, c - 1])

            # If upright is free (has an enemy or empty space)
            if c < 7 and not board[r - 1][c + 1] == 1:
                actions.append([r, c, r - 1, c + 1])

            # If up is free
            if r > 0 and board[r - 1][c] == 0:
                actions.append([r, c, r - 1, c])
    else:
        # Reverse sort by row (choose rows near bottom first)
        p2pieces.sort()
        p2pieces.reverse()
        for piece in p2pieces:
            [r, c] = [piece[0], piece[1]]

            # If downleft is free (has an enemy or empty space)
            if c > 0 and not board[r + 1][c - 1] == 2:
                actions.append([r, c, r + 1, c - 1])

            # If downright is free (has an enemy or empty space)
            if c < 7 and not board[r + 1][c + 1] == 2:
                actions.append([r, c, r + 1, c + 1])

            # If down is free
            if r < 7 and board[r + 1][c] == 0:
                actions.append([r, c, r + 1, c])

    return actions


def move(action,board,p1pieces,p2pieces):

    # If you are attacking player 1 piece, then remove it, and update player 2 piece
    if board[action[2]][action[3]] == 1:
        p1pieces.remove([action[2], action[3]])
        p2pieces.remove([action[0], action[1]])
        p2pieces.append([action[2], action[3]])
    elif board[action[2]][action[3]] == 2:
    # If you are attacking player 2 piece, then remove it and update player 1 piece
        p2pieces.remove([action[2], action[3]])
        p1pieces.remove([action[0], action[1]])
        p1pieces.append([action[2], action[3]])
    else:
    # If space you're moving to is empty, then just move your piece
        if board[action[0]][action[1]] == 1:
            p1pieces.remove([action[0], action[1]])
            p1pieces.append([action[2], action[3]])
        else:
            p2pieces.remove([action[0], action[1]])
            p2pieces.append([action[2], action[3]])

    # Update board values
    board[action[2]][action[3]] = board[action[0]][action[1]]
    board[action[0]][action[1]] = 0

    return [board, p1pieces, p2pieces]


def check_end(board, p1pieces, p2pieces):

    # returns 0 if nobody has won. returns x if player x won
    if len(p1pieces) == 0:
        return 2
    elif len(p2pieces) == 0:
        return 1
    else:
        for c in range(8):
            if board[0][c] == 1:
                return 1
            if board[7][c] == 2:
                return 2


def print_board(board):
    for row in board:
        print (row)


def calculateHeuristic(player,board,p1pieces,p2pieces,):
    heuristic = heuristicMap[player]

    h = 0
    if heuristic == 'Null':
        return 0

    if heuristic == 'Off1':
        opponentPieces = 0
        if player == 1:
            opponentPieces = len(p2pieces)
        else:
            opponentPieces = len(p1pieces)

        h = 2 * (30 - opponentPieces) + random.random()
    elif heuristic == 'Def1':

        ownPieces = 0
        if player == 1:
            ownPieces = len(p1pieces)
        else:
            ownPieces = len(p2pieces)

        h = 2 * ownPieces + random.random()
    elif heuristic == 'Def2':
        if player == 1:

            # Heuristic is your score minus opponents score. Note: It is the opponent's turn.
            # Your score is a sum of features: your pieces alive (weighted by how close to bottom), your protected pieces (someone is behind them in the current and adjacent columns), horizontal connections,
            # vertical connections, opponent's pieces close to base (neg), pieces in danger (neg, weighted by how close your piece is to the top)
            # Opponent's score is a sum of features: their pieces alive (weighted by how close to bottom), attacking pieces, horizontal connections, vertical connections, runaways (nobody in current
            # and adjacent columns going down)

            your_score = 0
            opponent_score = 0

            feature_piecesAlive = 0
            feature_protected = 0
            feature_horizontal = 0
            feature_vertical = 0
            feature_opponentsClose = 0
            feature_inDanger = 0

            feature_opponentAlive = 0
            feature_attacking = 0
            feature_opponentHorizontal = 0
            feature_opponentVertical = 0
            feature_runaway = 0

            for piece in p1pieces:
                [r, c] = [piece[0], piece[1]]
                feature_piecesAlive += r
                if c > 0 and board[r][c - 1] == 1:
                    feature_horizontal += 1
                if r > 0 and board[r - 1][c] == 1:
                    feature_vertical += 1
                if r < 7:
                    protected = False
                    for row in range(r + 1, 8):
                        for col in range(c - 1, c + 2):
                            if col >= 0 and col <= 7 \
                                and board[row][col] == 1:
                                protected = True
                    if protected:
                        feature_protected += 1
                if r > 0 and c > 0 and board[r - 1][c - 1] == 2 or r \
                    > 0 and c < 7 and board[r - 1][c + 1] == 2:
                    feature_inDanger -= 7 - r
            for piece in p2pieces:
                [r, c] = [piece[0], piece[1]]
                feature_opponentAlive += r
                if r > 4:
                    feature_opponentsClose -= r
                if c > 0 and board[r][c - 1] == 2:
                    feature_opponentHorizontal += 1
                if r > 0 and board[r - 1][c] == 2:
                    feature_opponentVertical += 1
                if r < 7 and c > 0 and board[r + 1][c - 1] == 1 or r \
                    < 7 and c < 7 and board[r + 1][c + 1] == 1:
                    feature_attacking += 1
                if r < 7:
                    runaway = True
                    for row in range(r + 1, 8):
                        for col in range(c - 1, c + 2):
                            if col >= 0 and col <= 7 \
                                and board[row][col] == 1:
                                runaway = False
                    if runaway:
                        feature_runaway += 1

            your_score = feature_piecesAlive + feature_protected \
                + feature_horizontal * 2 + feature_vertical * 2 \
                + feature_opponentsClose + feature_inDanger
            opponent_score = feature_opponentAlive + feature_attacking \
                + feature_opponentHorizontal + feature_opponentVertical \
                + feature_runaway

            h = your_score - opponent_score + random.random()
        if player == 2:

            # Heuristic is your score minus opponents score. Note: It is the opponent's turn.
            # Your score is a sum of features: your pieces alive (weighted by how close to top), your protected pieces (someone is behind them in the current and adjacent columns), horizontal connections,
            # vertical connections, opponent's pieces close to base (neg), pieces in danger (neg, weighted by how close your piece is to the bottom)
            # Opponent's score is a sum of features: their pieces alive (weighted by how close to top), attacking pieces, horizontal connections, vertical connections, runaways (nobody in current
            # and adjacent columns going up)

            your_score = 0
            opponent_score = 0

            feature_piecesAlive = 0
            feature_protected = 0
            feature_horizontal = 0
            feature_vertical = 0
            feature_opponentsClose = 0
            feature_inDanger = 0

            feature_opponentAlive = 0
            feature_attacking = 0
            feature_opponentHorizontal = 0
            feature_opponentVertical = 0
            feature_runaway = 0

            for piece in p2pieces:
                [r, c] = [piece[0], piece[1]]
                feature_piecesAlive += (7-r)
                if c > 0 and board[r][c - 1] == 1:
                    feature_horizontal += 1
                if r < 7 and board[r + 1][c] == 1:
                    feature_vertical += 1
                if r > 0:
                    protected = False
                    for row in range(0, r):
                        for col in range(c - 1, c + 2):
                            if col >= 0 and col <= 7 \
                                and board[row][col] == 2:
                                protected = True
                    if protected:
                        feature_protected += 1
                if r < 7 and c > 0 and board[r + 1][c - 1] == 1 or r \
                    < 7 and c < 7 and board[r + 1][c + 1] == 1:
                    feature_inDanger -= r
            for piece in p1pieces:
                [r, c] = [piece[0], piece[1]]
                feature_opponentAlive += 7-r
                if r < 3:
                    feature_opponentsClose -= (7-r)
                if c > 0 and board[r][c - 1] == 1:
                    feature_opponentHorizontal += 1
                if r < 7 and board[r + 1][c] == 1:
                    feature_opponentVertical += 1
                if r > 0 and c > 0 and board[r - 1][c - 1] == 2 or r \
                    > 0 and c < 7 and board[r - 1][c + 1] == 2:
                    feature_attacking += 1
                if r > 0:
                    runaway = True
                    for row in range(0, r):
                        for col in range(c - 1, c + 2):
                            if col >= 0 and col <= 7 \
                                and board[row][col] == 2:
                                runaway = False
                    if runaway:
                        feature_runaway += 1

            your_score = feature_piecesAlive + feature_protected \
                + feature_horizontal * 2 + feature_vertical * 2 \
                + feature_opponentsClose + feature_inDanger
            opponent_score = feature_opponentAlive + feature_attacking \
                + feature_opponentHorizontal + feature_opponentVertical \
                + feature_runaway

            h = your_score - opponent_score + random.random()
    elif heuristic == 'SimpleDef2':
        numberOfThreats = 0
        if player == 1:
            for piece in p1pieces:
                [r, c] = [piece[0], piece[1]]
                # Check for threats on upleft
                if c > 0 and board[r - 1][c - 1] == 2:
                    numberOfThreats = numberOfThreats + 1

                # Check for threats on upright
                if c < 7 and board[r - 1][c + 1] == 2:
                    numberOfThreats = numberOfThreats + 1
            h = 2 * (32 - numberOfThreats) + random.random()
        else:
            for piece in p2pieces:
                [r, c] = [piece[0], piece[1]]
                # Check for threats on upleft
                if c > 0 and board[r + 1][c - 1] == 1:
                    numberOfThreats = numberOfThreats + 1
                # Check for threats on upright
                if c < 7 and board[r + 1][c + 1] == 1:
                    numberOfThreats = numberOfThreats + 1
    elif heuristic == 'Off2':
        if player == 1:

            # Heuristic is your score minus opponents score. Note: It is the opponent's turn.
            # Your score is a sum of features: your pieces alive (weighted by how close they are to the top), any runaway pieces (weighted by distance to top), horizontal connections, vertical connections
            # Opponent's score is a sum of features: number of pieces alive, horizontal connections, vertical connections.

            your_score = 0
            opponent_score = 0

            
            feature_piecesAlive = 0
            feature_runaway = 0
            feature_almostWin = 0
            feature_horizontal = 0
            feature_vertical = 0

            feature_opponentAlive = 0
            feature_opponentHorizontal = 0
            feature_opponentVertical = 0
            

            for piece in p1pieces:
                [r, c] = [piece[0], piece[1]]
                feature_piecesAlive += (7-r)*max(1,7-r-1)
                if c > 0 and board[r][c - 1] == 1:
                    feature_horizontal += r*max(1,r-5)
                if r > 0 and board[r - 1][c] == 1:
                    feature_vertical += 1
                if r > 0:
                    runaway = True
                    for row in range(r - 1, 8):
                        for col in range(c - 1, c + 2):
                            if col >= 0 and col <= 7 \
                                and board[row][col] == 2:
                                runaway = False
                    if runaway:
                        feature_runaway += 1
                if (r < 2):
                    safe = True
                    if(c > 0 and board[r-1][c-1] == 2):
                        safe = False
                    if(c < 7 and board[r-1][c+1] == 2):
                        safe = False
                    if(safe):
                        feature_almostWin += (7-r)
            for piece in p2pieces:
                [r, c] = [piece[0], piece[1]]
                feature_opponentAlive += r * max(1,r-3)
                if c > 0 and board[r][c - 1] == 2:
                    feature_opponentHorizontal += (7-r)
                if r > 0 and board[r - 1][c] == 2:
                    feature_opponentVertical += 1
                

            your_score = feature_piecesAlive*2 + feature_runaway*0 \
                + feature_horizontal + feature_vertical + feature_almostWin * 0
            opponent_score = feature_opponentAlive \
                + feature_opponentHorizontal*2 + feature_opponentVertical

            h = your_score - opponent_score + random.random()

        

    return h
