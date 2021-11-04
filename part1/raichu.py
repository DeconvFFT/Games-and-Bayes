#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
# Names :
# Team-member 1: Monshizadeh, Mahsa
# Team-member 2: Ganapathy, Anitha
# Team-member 3: Mehta, Saumya Hetalbhai
# User id's : mmonshiz, aganapa, mehtasau
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import itertools
import copy
import numpy as np


def isEnemy(player, board, x, y, pawn):
    w = ['w', 'W', '@']
    b = ['b', 'B', '$']
    # print("isEnemy: ", board)
    if pawn == w[0] or pawn == b[0]:
        if (player == "w" and board[x][y] == b[0]) or (player == "b" and board[x][y] == w[0]):
            return True
        else:
            return False
    if pawn == w[1] or pawn == b[1]:
        if (player == "w" and board[x][y] == b[1]) or (player == "b" and board[x][y] == w[1]):
            return True
        else:
            return False
    if pawn == w[2] or pawn == b[2]:
        if (player == "w" and board[x][y] in b) or (player == "b" and board[x][y] in w):
            return True
        else:
            return False


def onBoard(x, y, N):
    if 0 <= x <= (N - 1) and 0 <= y <= (N - 1):
        return True
    return False


def isFriend(player, board, x, y):
    w = ['w', 'W', '@']
    b = ['b', 'B', '$']
    if (player == "w" and board[x][y] in w) or (player == "b" and board[x][y] in b):
        return True
    else:
        return False


# replacing the jumping over enemy pawn with '.' , empty position
def take_enemy_pawn(board, xPos, yPos, N):
    # print("take_enemy_pawn : before")
    # print(board)
    board = replace_pawns(board, xPos, yPos, '.', N)
    # print("take_enemy_pawn : after")
    # print(board)
    # return board[xPos][yPos] == '.'
    return board


def replace_pawns(tempState, xPos1, yPos1, char_replace, N):
    # https://stackoverflow.com/questions/14860460/append-several-variables-to-a-list-in-python
    # https://www.geeksforgeeks.org/python-convert-list-of-strings-and-characters-to-list-of-characters/
    # N = len(tempState)
    # print("replace_pawns")
    # print(tempState)
    res = [i for ele in tempState for i in ele]
    res = np.reshape(res, (N, N))
    res[xPos1][yPos1] = char_replace
    row0 = "".join(res[0])
    row1 = "".join(res[1])
    row2 = "".join(res[2])
    row3 = "".join(res[3])
    row4 = "".join(res[4])
    row5 = "".join(res[5])
    row6 = "".join(res[6])
    row7 = "".join(res[7])
    ll = {
        'row0': row0,
        'row1': row1,
        'row2': row2,
        'row3': row3,
        'row4': row4,
        'row5': row5,
        'row6': row6,
        'row7': row7
    }
    temp_list = []
    temp_list += ll.values()
    return temp_list


def updatePos(board, xPos1, yPos1, xPos2, yPos2, charToReplace, N):
    # tempState = copy.deepcopy(board)
    tempState = copy.deepcopy(board)
    tempState = replace_pawns(tempState, xPos1, yPos1, '.', N)
    tempState = replace_pawns(tempState, xPos2, yPos2, charToReplace, N)
    # Pichu or Pikachu conversion to Raichu
    if xPos2 == (N - 1):
        if charToReplace in ['w', 'W']:
            # tempState[xPos2][yPos2] = '@'
            tempState = replace_pawns(tempState, xPos2, yPos2, '@', N)
    if xPos2 == 0:
        if charToReplace in ['b', 'B']:
            # tempState[xPos2][yPos2] = '$'
            tempState = replace_pawns(tempState, xPos2, yPos2, '$', N)
    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    # print("Inside updatePos")
    # print("tempState")
    # print(tempState)
    # flatList = [col for row in tempState for col in row]
    return tempState


def pichu_successors(board, N, player, pichu):
    # print("inside pichu_successors: ", board)
    # currentState = [board[i:i + 8] for i in range(0, len(board), 8)]
    currentState = board
    # print(currentState)
    # currentState = board
    # print("pichu_successors")
    # print("Player = ", player)
    # print(currentState)
    pichu_loc = [(row, col) for col in range(0, N) for row in range(0, N) if board[row][col] == pichu]
    # print("pichu_loc: ", pichu_loc)
    successor = []
    for each_pichu in range(0, len(pichu_loc), 1):
        row = pichu_loc[each_pichu][0]
        col = pichu_loc[each_pichu][1]
        # move pawn down
        if player == 'w':
            if onBoard(row + 1, col + 1, N):  # diagonal move right to empty space
                if not isEnemy(player, currentState, row + 1, col + 1, pichu) \
                        and not isFriend(player, currentState, row + 1, col + 1):
                    successor.append(updatePos(currentState, row, col, row + 1, col + 1, pichu, N))
            if onBoard(row + 1, col - 1, N):  # diagonal move left to empty space
                if not isEnemy(player, currentState, row + 1, col - 1, pichu) \
                        and not isFriend(player, currentState, row + 1, col - 1):
                    successor.append(updatePos(currentState, row, col, row + 1, col - 1, pichu, N))
            # move pawn left diagonally by taking opponents pawn
            if onBoard(row + 2, col - 2, N) \
                    and not isEnemy(player, currentState, row + 2, col - 2, pichu) \
                    and not isFriend(player, currentState, row + 2, col - 2) \
                    and isEnemy(player, currentState, row + 1, col - 1, pichu):
                currentState = take_enemy_pawn(currentState, row + 1, col - 1, N)
                # print("The last call state")
                successor.append(updatePos(currentState, row, col, row + 2, col - 2, pichu, N))
            # move pawn right diagonally by taking opponents pawn
            if onBoard(row + 2, col + 2, N) \
                    and not isEnemy(player, currentState, row + 2, col + 2, pichu) \
                    and not isFriend(player, currentState, row + 2, col + 2) \
                    and isEnemy(player, currentState, row + 1, col + 1, pichu):
                currentState = take_enemy_pawn(currentState, row + 1, col + 1, N)
                successor.append(updatePos(currentState, row, col, row + 2, col + 2, pichu, N))

        if player == 'b':
            if onBoard(row - 1, col + 1, N):  # diagonal move right to empty space
                if not isEnemy(player, currentState, row - 1, col + 1, pichu) \
                        and not isFriend(player, currentState, row - 1, col + 1):
                    successor.append(updatePos(currentState, row, col, row - 1, col + 1, pichu, N))
            if onBoard(row - 1, col - 1, N):  # diagonal move left to empty space
                if not isEnemy(player, currentState, row - 1, col - 1, pichu) \
                        and not isFriend(player, currentState, row - 1, col - 1):
                    successor.append(updatePos(currentState, row, col, row - 1, col - 1, pichu, N))
            # move pawn left diagonally by taking opponents pawn
            if onBoard(row - 2, col - 2, N) \
                    and not isEnemy(player, currentState, row - 2, col - 2, pichu) \
                    and not isFriend(player, currentState, row - 2, col - 2) \
                    and isEnemy(player, currentState, row - 1, col - 1, pichu):
                currentState = take_enemy_pawn(currentState, row - 1, col - 1, N)
                successor.append(updatePos(currentState, row, col, row - 2, col - 2, pichu, N))
            # move pawn right diagonally by taking opponents pawn
            if onBoard(row - 2, col + 2, N) \
                    and not isEnemy(player, currentState, row - 2, col + 2, pichu) \
                    and not isFriend(player, currentState, row - 2, col + 2) \
                    and isEnemy(player, currentState, row - 1, col + 1, pichu):
                currentState = take_enemy_pawn(currentState, row - 1, col + 1, N)
                successor.append(updatePos(currentState, row, col, row - 2, col + 2, pichu, N))
    return successor


def pikachu_successors(board, N, player, pikachu):
    pikachu_loc = [(row, col) for col in range(0, N) for row in range(0, N) if board[row][col] == pikachu]
    currentState = board
    # print("pikachu_successors")
    # print(pikachu_loc)
    # print("Player = ", player)
    successor = []
    for each_pikachu in range(0, len(pikachu_loc), 1):
        row = pikachu_loc[each_pikachu][0]
        col = pikachu_loc[each_pikachu][1]
        # move pawn down 1 or 2 squares either forward, left, or right (but not diagonally)
        if player == 'w':
            if onBoard(row + 1, col, N):  # forward by 1 move
                if not isEnemy(player, currentState, row + 1, col, pikachu) \
                        and not isFriend(player, currentState, row + 1, col):
                    successor.append(updatePos(currentState, row, col, row + 1, col, pikachu, N))
            if onBoard(row + 2, col, N):  # forward by 2 move
                if not isEnemy(player, currentState, row + 1, col, pikachu) \
                        and not isFriend(player, currentState, row + 1, col) \
                        and not isEnemy(player, currentState, row + 2, col, pikachu) \
                        and not isFriend(player, currentState, row + 2, col):
                    successor.append(updatePos(currentState, row, col, row + 2, col, pikachu, N))
            if onBoard(row, col - 1, N):  # left by 1 move
                if not isEnemy(player, currentState, row, col - 1, pikachu) \
                        and not isFriend(player, currentState, row, col - 1):
                    successor.append(updatePos(currentState, row, col, row, col - 1, pikachu, N))
            if onBoard(row, col - 2, N):  # left by 2 move
                if not isEnemy(player, currentState, row, col - 2, pikachu) \
                        and not isFriend(player, currentState, row, col - 2) \
                        and not isEnemy(player, currentState, row, col - 1, pikachu) \
                        and not isFriend(player, currentState, row, col - 1):
                    successor.append(updatePos(currentState, row, col, row, col - 2, pikachu, N))
            if onBoard(row, col + 1, N):  # right by 1 move
                if not isEnemy(player, currentState, row, col + 1, pikachu) \
                        and not isFriend(player, currentState, row, col + 1):
                    successor.append(updatePos(currentState, row, col, row, col + 1, pikachu, N))
            if onBoard(row, col + 2, N):  # right by 2 move
                if not isEnemy(player, currentState, row, col + 2, pikachu) \
                        and not isFriend(player, currentState, row, col + 2) \
                        and not isEnemy(player, currentState, row, col + 1, pikachu) \
                        and not isFriend(player, currentState, row, col + 1):
                    successor.append(updatePos(currentState, row, col, row, col + 2, pikachu, N))

            # move pawn forward by 2 steps,after taking opponents pawn
            if onBoard(row + 2, col, N):
                if not isEnemy(player, currentState, row + 2, col, pikachu) \
                        and not isFriend(player, currentState, row + 2, col) \
                        and not isFriend(player, currentState, row + 1, col) \
                        and isEnemy(player, currentState, row + 1, col, pikachu):
                    currentState = take_enemy_pawn(currentState, row + 1, col, N)
                    successor.append(updatePos(currentState, row, col, row + 2, col, pikachu, N))
            # move pawn left by 2 steps,after taking opponents pawn
            if onBoard(row, col - 2, N):
                if not isEnemy(player, currentState, row, col - 2, pikachu) \
                        and not isFriend(player, currentState, row, col - 2) \
                        and not isFriend(player, currentState, row, col - 1) \
                        and isEnemy(player, currentState, row, col - 1, pikachu):
                    currentState = take_enemy_pawn(currentState, row, col - 1, N)
                    successor.append(updatePos(currentState, row, col, row, col - 2, pikachu, N))
            # move pawn right by 2 steps,after taking opponents pawn
            if onBoard(row, col + 2, N):
                if not isEnemy(player, currentState, row, col + 2, pikachu) \
                        and not isFriend(player, currentState, row, col + 2) \
                        and not isFriend(player, currentState, row, col + 1) \
                        and isEnemy(player, currentState, row, col + 1, pikachu):
                    currentState = take_enemy_pawn(currentState, row, col + 1, N)
                    successor.append(updatePos(currentState, row, col, row, col + 2, pikachu, N))

            # move pawn forward by 3 steps,after taking opponents pawn
            if onBoard(row + 3, col, N):
                if not isEnemy(player, currentState, row + 3, col, pikachu) \
                        and not isFriend(player, currentState, row + 3, col) \
                        and not isFriend(player, currentState, row + 2, col) \
                        and isEnemy(player, currentState, row + 2, col, pikachu) \
                        and not isFriend(player, currentState, row + 1, col) \
                        and not isEnemy(player, currentState, row + 1, col, pikachu):
                    currentState = take_enemy_pawn(currentState, row + 2, col, N)
                    successor.append(updatePos(currentState, row, col, row + 3, col, pikachu, N))
            # move pawn left by 3 steps,after taking opponents pawn
            if onBoard(row, col - 3, N):
                if not isEnemy(player, currentState, row, col - 3, pikachu) \
                        and not isFriend(player, currentState, row, col - 3) \
                        and not isFriend(player, currentState, row, col - 2) \
                        and isEnemy(player, currentState, row, col - 2, pikachu) \
                        and not isFriend(player, currentState, row, col - 1) \
                        and not isEnemy(player, currentState, row, col - 1, pikachu):
                    currentState = take_enemy_pawn(currentState, row, col - 2, N)
                    successor.append(updatePos(currentState, row, col, row, col - 3, pikachu, N))
            # move pawn right by 3 steps,after taking opponents pawn
            if onBoard(row, col + 3, N):
                if not isEnemy(player, currentState, row, col + 3, pikachu) \
                        and not isFriend(player, currentState, row, col + 3) \
                        and not isFriend(player, currentState, row, col + 2) \
                        and isEnemy(player, currentState, row, col + 2, pikachu) \
                        and not isFriend(player, currentState, row, col + 1) \
                        and not isEnemy(player, currentState, row, col + 1, pikachu):
                    currentState = take_enemy_pawn(currentState, row, col + 2, N)
                    successor.append(updatePos(currentState, row, col, row, col + 3, pikachu, N))

        if player == 'b':
            if onBoard(row - 1, col, N):  # forward by 1 move
                if not isEnemy(player, currentState, row - 1, col, pikachu) \
                        and not isFriend(player, currentState, row - 1, col):
                    successor.append(updatePos(currentState, row, col, row - 1, col, pikachu, N))
            if onBoard(row - 2, col, N):  # forward by 2 move
                if not isEnemy(player, currentState, row - 1, col, pikachu) \
                        and not isFriend(player, currentState, row - 1, col) \
                        and not isEnemy(player, currentState, row - 2, col, pikachu) \
                        and not isFriend(player, currentState, row - 2, col):
                    successor.append(updatePos(currentState, row, col, row - 2, col, pikachu, N))
            if onBoard(row, col - 1, N):  # left by 1 move
                if not isEnemy(player, currentState, row, col - 1, pikachu) \
                        and not isFriend(player, currentState, row, col - 1):
                    successor.append(updatePos(currentState, row, col, row, col - 1, pikachu, N))
            if onBoard(row, col - 2, N):  # left by 2 move
                if not isEnemy(player, currentState, row, col - 2, pikachu) \
                        and not isFriend(player, currentState, row, col - 2) \
                        and not isEnemy(player, currentState, row, col - 1, pikachu) \
                        and not isFriend(player, currentState, row, col - 1):
                    successor.append(updatePos(currentState, row, col, row, col - 2, pikachu, N))
            if onBoard(row, col + 1, N):  # right by 1 move
                if not isEnemy(player, currentState, row, col + 1, pikachu) \
                        and not isFriend(player, currentState, row, col + 1):
                    successor.append(updatePos(currentState, row, col, row, col + 1, pikachu, N))
            if onBoard(row, col + 2, N):  # right by 2 move
                if not isEnemy(player, currentState, row, col + 2, pikachu) \
                        and not isFriend(player, currentState, row, col + 2) \
                        and not isEnemy(player, currentState, row, col + 1, pikachu) \
                        and not isFriend(player, currentState, row, col + 1):
                    successor.append(updatePos(currentState, row, col, row, col + 2, pikachu, N))

            # move pawn forward by 2 steps,after taking opponents pawn
            if onBoard(row - 2, col, N):
                if not isEnemy(player, currentState, row - 2, col, pikachu) \
                        and not isFriend(player, currentState, row - 2, col) \
                        and not isFriend(player, currentState, row - 1, col) \
                        and isEnemy(player, currentState, row - 1, col, pikachu):
                    currentState = take_enemy_pawn(currentState, row - 1, col, N)
                    successor.append(updatePos(currentState, row, col, row - 2, col, pikachu, N))
            # move pawn left by 2 steps,after taking opponents pawn
            if onBoard(row, col - 2, N):
                if not isEnemy(player, currentState, row, col - 2, pikachu) \
                        and not isFriend(player, currentState, row, col - 2) \
                        and not isFriend(player, currentState, row, col - 1) \
                        and isEnemy(player, currentState, row, col - 1, pikachu):
                    currentState = take_enemy_pawn(currentState, row, col - 1, N)
                    successor.append(updatePos(currentState, row, col, row, col - 2, pikachu, N))
            # move pawn right by 2 steps,after taking opponents pawn
            if onBoard(row, col + 2, N):
                if not isEnemy(player, currentState, row, col + 2, pikachu) \
                        and not isFriend(player, currentState, row, col + 2) \
                        and not isFriend(player, currentState, row, col + 1) \
                        and isEnemy(player, currentState, row, col + 1, pikachu):
                    currentState = take_enemy_pawn(currentState, row, col + 1, N)
                    successor.append(updatePos(currentState, row, col, row, col + 2, pikachu, N))

            # move pawn forward by 3 steps,after taking opponents pawn
            if onBoard(row - 3, col, N):
                if not isEnemy(player, currentState, row - 3, col, pikachu) \
                        and not isFriend(player, currentState, row - 3, col) \
                        and not isFriend(player, currentState, row - 2, col) \
                        and isEnemy(player, currentState, row - 2, col, pikachu) \
                        and not isFriend(player, currentState, row - 1, col) \
                        and not isEnemy(player, currentState, row - 1, col, pikachu):
                    currentState = take_enemy_pawn(currentState, row - 2, col, N)
                    successor.append(updatePos(currentState, row, col, row - 3, col, pikachu, N))
            # move pawn left by 3 steps,after taking opponents pawn
            if onBoard(row, col - 3, N):
                if not isEnemy(player, currentState, row, col - 3, pikachu) \
                        and not isFriend(player, currentState, row, col - 3) \
                        and not isFriend(player, currentState, row, col - 2) \
                        and isEnemy(player, currentState, row, col - 2, pikachu) \
                        and not isFriend(player, currentState, row, col - 1) \
                        and not isEnemy(player, currentState, row, col - 1, pikachu):
                    currentState = take_enemy_pawn(currentState, row, col - 2, N)
                    successor.append(updatePos(currentState, row, col, row, col - 3, pikachu, N))
            # move pawn right by 3 steps,after taking opponents pawn
            if onBoard(row, col + 3, N):
                if not isEnemy(player, currentState, row, col + 3, pikachu) \
                        and not isFriend(player, currentState, row, col + 3) \
                        and not isFriend(player, currentState, row, col + 2) \
                        and isEnemy(player, currentState, row, col + 2, pikachu) \
                        and not isFriend(player, currentState, row, col + 1) \
                        and not isEnemy(player, currentState, row, col + 1, pikachu):
                    currentState = take_enemy_pawn(currentState, row, col + 2, N)
                    successor.append(updatePos(currentState, row, col, row, col + 3, pikachu, N))
    return successor


def raichu_successors(board, N, player, raichu):
    currentState = board
    raichu_loc = [(row, col) for col in range(0, N) for row in range(0, N) if board[row][col] == raichu]
    # print("raichu_successors")
    # print(raichu_loc)
    # print("Player = ", player)
    successor = []
    for each_raichu in range(0, len(raichu_loc), 1):
        row = raichu_loc[each_raichu][0]
        col = raichu_loc[each_raichu][1]
        if player in ['w' 'b']:
            for r in range(row, -1, -1):  # diagonal left, top
                if onBoard(row - r, col - r):
                    if isFriend(player, currentState, row - r, col - r):
                        break
                    elif isEnemy(player, currentState, row - r, col - r, raichu):
                        successor.append(updatePos(currentState, row, col, row - r, col - r, raichu))
                        break
                    elif not isFriend(player, currentState, row - r, col - r):
                        successor.append(updatePos(currentState, row, col, row - r, col - r, raichu))
            i = 1
            for r in range(row, N, 1):
                if onBoard(row + i, col + i):
                    if isFriend(player, currentState, row + i, col + i):
                        break
                    elif isEnemy(player, currentState, row + i, col + i, raichu):
                        successor.append(updatePos(currentState, row, col, row + i, col + i, raichu))
                        break
                    elif not isFriend(player, currentState, row + i, col + i):
                        successor.append(updatePos(currentState, row, col, row + i, col + i, raichu))
                    i += 1
            i = 0
            # move queen to the right
            for r in range(row, -1, -1):
                if onBoard(row - i, col + i):
                    if isFriend(player, currentState, row - i, col + i):
                        break
                    elif isEnemy(player, currentState, row - i, col + i, raichu):
                        successor.append(updatePos(currentState, row, col, row - i, col + i, raichu))
                        break
                    elif not isFriend(player, currentState, row - i, col + i):
                        successor.append(updatePos(currentState, row, col, row - i, col + i, raichu))
                    i += 1
            i = 1
            for r in range(row, N, 1):
                if onBoard(row + i, col - i):
                    if isFriend(player, currentState, row + i, col - i):
                        break
                    elif isEnemy(player, currentState, row + i, col - i, raichu):
                        successor.append(updatePos(currentState, row, col, row + i, col - i, raichu))
                        break
                    elif not isFriend(player, currentState, row + i, col - i):
                        successor.append(updatePos(currentState, row, col, row + i, col - i, raichu))
                    i += 1
            # move queen up
            for i in range(row - 1, -1, -1):
                if isFriend(player, currentState, i, col):
                    break
                elif isEnemy(player, currentState, i, col, raichu):
                    successor.append(updatePos(currentState, row, col, i, col, raichu))
                    break
                elif not isFriend(player, currentState, i, col):
                    successor.append(updatePos(currentState, row, col, i, col, raichu))

            # move queen down
            for i in range(row + 1, N, 1):
                if isFriend(player, currentState, i, col):
                    break
                elif isEnemy(player, currentState, i, col, raichu):
                    successor.append(updatePos(currentState, row, col, i, col, raichu))
                    break
                elif not isFriend(player, currentState, i, col):
                    successor.append(updatePos(currentState, row, col, i, col, raichu))

            # move queen left
            for i in range(col - 1, -1, -1):
                if isFriend(player, currentState, row, i):
                    break
                elif isEnemy(player, currentState, row, i, raichu):
                    successor.append(updatePos(currentState, row, col, row, i, raichu))
                    break
                elif not isFriend(player, currentState, row, i):
                    successor.append(updatePos(currentState, row, col, row, i, raichu))

            # move queen right
            for i in range(col + 1, N, 1):
                if isFriend(player, currentState, row, i):
                    break
                elif isEnemy(player, currentState, row, i, raichu):
                    successor.append(updatePos(currentState, row, col, row, i, raichu))
                    break
                elif not isFriend(player, currentState, row, i):
                    successor.append(updatePos(currentState, row, col, row, i, raichu))
    return successor


def successors(board, N, player):
    choose_player_pawns = {
        'w': ['w', 'W', '@'],
        'b': ['b', 'B', '$']
    }
    successors_list = []
    # https://stackoverflow.com/questions/6614891/turning-a-list-into-nested-lists-in-python
    # currentState = [board[i:i + N] for i in range(0, len(board), N)]
    currentState = board
    # print("Current state:")
    # print(currentState)
    next_pichu_pos = pichu_successors(currentState, N, player, choose_player_pawns[player][0])
    next_pikachu_pos = pikachu_successors(currentState, N, player, choose_player_pawns[player][1])
    next_raichu_pos = raichu_successors(currentState, N, player, choose_player_pawns[player][2])
    # print(next_pichu_pos)
    successors_list = list(itertools.chain(next_pichu_pos, next_pikachu_pos, next_raichu_pos))
    # print("Succ list :", successors_list)
    return successors_list


# if player = w, pichu = w, pikachu = W , raichu = @
# if player = B, pichu = b, pikachu = B , raichu = $
# returns the counts pichu, pikachu, raichu
def count_pawns(board, player):
    w = ['w', 'W', '@']
    b = ['b', 'B', '$']
    if player == 'w':
        return [board.count(pawn) for pawn in w]
    else:
        return [board.count(pawn) for pawn in b]


def board_to_string(board, N):
    return "\n".join(board[i:i + N] for i in range(0, len(board), N))


def isTerminal(board, opponent):
    pawns_count = count_pawns(board, opponent)
    if sum(pawns_count) == 0:
        return True
    else:
        return False


def opponent_player(player):
    return 'b' if player == 'w' else 'w'


# pichu's = 1, pikachu's = 3, raichu's = 11
def heuristic(board, player, opponent):
    player_pawn = count_pawns(board, player)
    opponent_pawn = count_pawns(board, opponent)
    player_heuristic = 1 * player_pawn[0] + 3 * player_pawn[1] + 11 * player_pawn[2]
    opponent_heuristic = 1 * opponent_pawn[0] + 3 * opponent_pawn[1] + 11 * opponent_pawn[2]
    # print(player)
    # print(player_pawn, opponent_pawn)
    # print(player_heuristic, opponent_heuristic)
    if player == 'w':
        h_val = player_heuristic - opponent_heuristic
    else:
        h_val = opponent_heuristic - player_heuristic
    # print("player, hval :", player, h_val)
    return h_val


def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    start = time.time()
    # print("Start time : ", start)
    elapsed = 0
    while elapsed < timelimit:
        elapsed = time.time() - start
        depth = 9999
        opponent = opponent_player(player)
        if not isTerminal(board, opponent) or depth != 0:
            alpha = 99999
            beta = -99999
            # h_val = heuristic(board, player, opponent)
            # print("In find best move:\n", board)
            listOfSuccessors = successors(board, N, player)
            eval = []
            for each_succ in listOfSuccessors:
                yield ''.join(each_succ)
                eval.append(minValue(each_succ, alpha, beta, depth - 1, player))
            result = listOfSuccessors[np.argmax(eval)]
            res = ''.join(result)
            yield res
            # return ''.join(result)
        else:
            if heuristic(board, player, opponent) > 0:
                print("You have Won!")
                # print(board)
                res = ''.join(board)
                yield res
                # return board
            else:
                print("You have Lost!")
                print(board)
                res = ''.join(board)
                yield res
                # return board




def maxValue(board, alpha, beta, depth, player):
    opponent = opponent_player(player)
    # print("In maxValue")
    if isTerminal(board, opponent) or depth == 0:
        h_val = heuristic(board, player, player)
        # return find_best_move(board,  N, player, timelimit)
        return h_val
    else:
        for successor in successors(board, len(board), player):
            # print("depth maxvalue(): ", depth)
            value = minValue(successor, alpha, beta, depth - 1, player)
            # print("max func eval")
            # print(value)
            if value > alpha:
                alpha = value
            if alpha >= beta:
                return alpha
        return alpha


def minValue(board, alpha, beta, depth, player):
    opponent = opponent_player(player)
    # print("minValue")
    # print(board)
    if isTerminal(board, opponent) or depth == 0:
        h_val = heuristic(board, player, opponent)
        # return find_best_move(board, N, player, timelimit)
        return h_val
    else:
        for successor in successors(board, N, opponent):
            # print("depth minvalue(): ", depth)
            value = maxValue(successor, alpha, beta, depth - 1, player)
            # print("min func eval")
            # print(value)
            if value < beta:
                beta = value
            if alpha >= beta:
                return beta
        return beta


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
    (_, N, player, board, timelimit) = sys.argv
    N = int(N)
    timelimit = int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N * N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Timelimit : ",timelimit)
    print("Here's what I decided:")
    board = [board[i:i + N] for i in range(0, len(board), N)]
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
    # new_board = find_best_move(board, N, player, timelimit)
    # print(new_board)
