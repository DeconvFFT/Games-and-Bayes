# Simple quintris program! v0.2
# Submitted by: Saumya Hetalbhai Mehta, mehtasau
# D. Crandall, Sept 2021
# 
from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
from copy import deepcopy
import numpy as np
from collections import defaultdict
import logging

class HumanPlayer:
    
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
       

        pieces = [ [ " x ", "xxx", " x "], [ "xxxxx" ], [ "xxxx", "   x" ], [ "xxxx", "  x " ], [ "xxx", "x x"], [ "xxx ", "  xx" ] ]

    
        best_move = {}
        previous_piece = str(quintris.get_piece()[0])
        max_eval, best_move = expectimax_small(quintris, 3, "max",best_move, 3)
        
        # self.qlist = []
        
        return best_move[str(previous_piece)]

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            
            commands[c]()


def move_piece_down(quintris):
    while not quintris.check_collision(*quintris.state,quintris.piece,quintris.row+1,quintris.col):
            quintris.row += 1
   

# generate a probability distribution for successors .
# This function take a quintris as input and returns the probability distribution for it's rotations and flips.
# @param: quintris: Quintris game object with a board and piece attached on the board.
# There are total 8 possible rotations for each piece.
#  
def generate_prob(quintris):
    pieces = []
    probs = {}
    #pieces.append(str(quintris.get_piece()[0]))
    quintris1 = deepcopy(quintris)

    for _ in range(3):
        #quintris1 = deepcopy(quintris1)
        quintris1.rotate()
        pieces.append(str(quintris1.get_piece()[0]))
    quintris1 = deepcopy(quintris)
    quintris1.hflip()
    pieces.append(str(quintris1.get_piece()[0]))

    for _ in range(3):
        quintris1 = deepcopy(quintris1)
        quintris1.rotate()
        pieces.append(str(quintris1.get_piece()[0]))

    for p in pieces:
        if p in probs:
            probs[p]+=1
        else:
            probs[p] = 1
    for p in probs.keys():
        probs[p]/=len(pieces)

    return probs


        
# Reset the state of quintris to it's original state
# Function takes quintris, original state of the board, quintris piece, quintris row and quintris column
# @param: quintris:  Quintris game object with a board and piece attached on the board.
# @param: state: Original of the quintris object
# @param: piece: Original quintris piece.
# @param: row: col:  Coordinates for original piece on the quintris.

def reset_qunitris(qunitris, state, piece, row, col):
    qunitris.state = state
    qunitris.piece = piece
    qunitris.row = row
    qunitris.col = col


# Generates successors for the current quintris
# Function takes quintris as input and generates a list of successors containing successor, move string and heuristic
# Reset quintris function called here, resets the quintris with it's original configuration
# 3 ways to generate successors: 0 : Only move piece left and right, 1: move piece left and right along with 1 flip and rotation
# 3: Rotate piece 3 times along with flip and left and right movement.

def generate_successors2(quintris):
        total_moves = [0,1,2]
        store_piece = quintris.piece
        store_col = quintris.col
        store_row  =quintris.row
        store_state = quintris.state
        succ=[]
        move=''

        # Discussed logic of count from total_moves, with Madhav Jariwala: makejari@iu.edu 
        # count  = 0 means you can only move a piece left and right
        # count = 1 means you can flip and rotate a piece once
        # count = 2 means you can rotate a piece 3 times
        try: 
            for count in range(len(total_moves)):
                if count==0:
                    for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                        if j!=store_col:
                            quintris.right()
                            move+='m'
                        move_piece_down(quintris)
                        board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                        quintris1 = deepcopy(quintris)
                        quintris1.state = board, score   
                    
                        succ.append((quintris1,move))
                        quintris.row = store_row
                    
                    reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)
                    move=''
                    for j in range(0,store_col):
                        quintris.left()
                        move+='b'
                        move_piece_down(quintris)
                        try:
                            board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                            quintris1 = deepcopy(quintris)
                            quintris1.state = board, score   
                        
                            succ.append((quintris1,move))
                        
                            quintris.row = store_row
                        except Exception:
                            print(f'quintris col: {quintris.col}')
                
                reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)

                if count==1:
                    quintris.hflip()
                    if quintris.piece != store_piece:
                        move = ''
                        move+='h'
                        for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                            if j!=store_col:
                                quintris.right()
                                move+='m'
                            move_piece_down(quintris)
                            board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                            quintris1 = deepcopy(quintris)
                            quintris1.state = board, score   
                        
                            succ.append((quintris1,move))
                        
                            quintris.row = store_row 
                        reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)

                        move = ''
                        move+='h'
                        for j in range(0,store_col):
                            quintris.left()
                            move+='b'
                            move_piece_down(quintris)
                            board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                            quintris1 = deepcopy(quintris)
                            quintris1.state = board, score   
                        
                            succ.append((quintris1,move))
                            quintris.row = store_row
                    
                        for i in range(3):
                            reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)

                            move = ''
                            move += 'h'
                            quintris.rotate()
                            move += (i+1)*'n'

                            for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                                if j!=store_col:
                                    quintris.right()
                                    move+='m'
                                move_piece_down(quintris) 
                                board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                                quintris1 = deepcopy(quintris)
                                quintris1.state = board, score   
                                
                                succ.append((quintris1,move))
                                quintris.row = store_row
                        
                            reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)
                            move = ''
                            move+='h'
                            move += (i+1)*'n'
                            for j in range(0,store_col):
                                quintris.left()
                                move+='b'
                                move_piece_down(quintris)
                                try:
                                    board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                                    quintris1 = deepcopy(quintris)
                                    quintris1.state = board, score   
                                    
                                    succ.append((quintris1,move))
                                    
                                    quintris.row = store_row
                                except Exception:
                                    print(f'quintris col inside flip: {quintris.col}')
                                    
                
                reset_qunitris(quintris, store_state,store_piece,store_row,store_col)

                if count==2:
                    for i in range(3):
                        reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)  
                        move = ''
                        quintris.rotate()
                        if quintris.piece == store_piece:
                            break
                        move += (i+1)*'n'

                        for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                            if j!=store_col:
                                quintris.right()
                                move+='m'
                            move_piece_down(quintris) 
                            board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                            quintris1 = deepcopy(quintris)
                            quintris1.state = board, score   
                            succ.append((quintris1,move))
                            quintris.row = store_row
                    
                        reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)
                        move = ''
                        move += (i+1)*'n'

                        for j in range(0,store_col):
                            quintris.left()
                            move+='b'
                            move_piece_down(quintris) 
                            board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                            quintris1 = deepcopy(quintris)
                            quintris1.state = board, score   
                            succ.append((quintris1,move))
                            quintris.row = store_row
        except Exception:
            print(f'col: {quintris.col}')
        reset_qunitris(quintris, store_state,store_piece,store_row,store_col)
        return succ

# Generates successors for the current quintris
# Function takes quintris as input and generates a list of successors containing successor, move string and heuristic
# Reset quintris function called here, resets the quintris with it's original configuration
# 3 ways to generate successors: 0 : Only move piece left and right, 1: move piece left and right along with 1 flip and rotation
# 3: Rotate piece 3 times along with flip and left and right movement.

def generate_successors2_animated(quintris, tmp_quintris):
        total_moves = [0,1,2]
        tmp_quintris.piece = store_piece = quintris.piece
        tmp_quintris.col = store_col = quintris.col
        tmp_quintris.row = store_row  =quintris.row
        tmp_quintris.state = store_state = quintris.state
        succ=[]
        move=''

        # Discussed logic of count from total moves, with Madhav Jariwala: makejari@iu.edu 
        # count  = 0 means you can only move a piece left and right
        # count = 1 means you can flip and rotate a piece once
        # count = 2 means you can rotate a piece 3 times
        
        try: 
            for count in range(len(total_moves)):
                if count==0:
                    for j in range(store_col,len(tmp_quintris.state[0][0])-len(max(tmp_quintris.piece))+1):
                        if j!=store_col:
                            tmp_quintris.right()
                            move+='m'
                        move_piece_down(tmp_quintris)
                        board, score = tmp_quintris.place_piece(*tmp_quintris.state, tmp_quintris.piece, tmp_quintris.row, tmp_quintris.col)
                        quintris2 = deepcopy(tmp_quintris)
                        quintris2.state = board, score   
                    
                        succ.append((quintris2,move))
                        tmp_quintris.row = store_row
                    
                    reset_qunitris(tmp_quintris, store_state,tmp_quintris.piece,store_row,store_col)
                    move=''
                    for j in range(0,store_col):
                        tmp_quintris.left()
                        move+='b'
                        move_piece_down(tmp_quintris)
                        board, score = tmp_quintris.place_piece(*tmp_quintris.state, tmp_quintris.piece, tmp_quintris.row, tmp_quintris.col)
                        quintris1 = deepcopy(tmp_quintris)
                        quintris1.state = board, score   
                    
                        succ.append((quintris1,move))
                    
                        tmp_quintris.row = store_row
                
                reset_qunitris(tmp_quintris, store_state,tmp_quintris.piece,store_row,store_col)

                if count==1:
                    tmp_quintris.hflip()
                    if tmp_quintris.piece != store_piece:
                        move = ''
                        move+='h'
                        for j in range(store_col,len(tmp_quintris.state[0][0])-len(max(tmp_quintris.piece))+1):
                            if j!=store_col:
                                tmp_quintris.right()
                                move+='m'
                            move_piece_down(tmp_quintris)
                            board, score = tmp_quintris.place_piece(*tmp_quintris.state, tmp_quintris.piece, tmp_quintris.row, tmp_quintris.col)
                            quintris1 = deepcopy(tmp_quintris)
                            quintris1.state = board, score   
                        
                            succ.append((quintris1,move))
                        
                            tmp_quintris.row = store_row 
                        reset_qunitris(tmp_quintris, store_state,tmp_quintris.piece,store_row,store_col)

                        move = ''
                        move+='h'
                        for j in range(0,store_col):
                            tmp_quintris.left()
                            move+='b'
                            move_piece_down(tmp_quintris)
                            board, score = tmp_quintris.place_piece(*tmp_quintris.state, tmp_quintris.piece, tmp_quintris.row, tmp_quintris.col)
                            quintris1 = deepcopy(tmp_quintris)
                            quintris1.state = board, score   
                        
                            succ.append((quintris1,move))
                            tmp_quintris.row = store_row
                    
                        for i in range(3):
                            reset_qunitris(tmp_quintris, store_state,tmp_quintris.piece,store_row,store_col)

                            move = ''
                            move += 'h'
                            tmp_quintris.rotate()
                            move += (i+1)*'n'

                            for j in range(store_col,len(tmp_quintris.state[0][0])-len(max(tmp_quintris.piece))+1):
                                if j!=store_col:
                                    tmp_quintris.right()
                                    move+='m'
                                move_piece_down(tmp_quintris) 
                                board, score = tmp_quintris.place_piece(*tmp_quintris.state, tmp_quintris.piece, tmp_quintris.row, tmp_quintris.col)
                                quintris1 = deepcopy(tmp_quintris)
                                quintris1.state = board, score   
                                
                                succ.append((quintris1,move))
                                tmp_quintris.row = store_row
                        
                            reset_qunitris(tmp_quintris, store_state,tmp_quintris.piece,store_row,store_col)
                            move = ''
                            move+='h'
                            move += (i+1)*'n'
                            for j in range(0,store_col):
                                tmp_quintris.left()
                                move+='b'
                                move_piece_down(tmp_quintris)
                                board, score = tmp_quintris.place_piece(*tmp_quintris.state, tmp_quintris.piece, tmp_quintris.row, tmp_quintris.col)
                                quintris1 = deepcopy(tmp_quintris)
                                quintris1.state = board, score   
                                
                                succ.append((quintris1,move))
                                
                                tmp_quintris.row = store_row
                
                reset_qunitris(tmp_quintris, store_state,store_piece,store_row,store_col)

                if count==2:
                    for i in range(3):
                        reset_qunitris(tmp_quintris, store_state,tmp_quintris.piece,store_row,store_col)  
                        move = ''
                        tmp_quintris.rotate()
                        if tmp_quintris.piece == store_piece:
                            break
                        move += (i+1)*'n'

                        for j in range(store_col,len(tmp_quintris.state[0][0])-len(max(tmp_quintris.piece))+1):
                            if j!=store_col:
                                tmp_quintris.right()
                                move+='m'
                            move_piece_down(tmp_quintris) 
                            board, score = tmp_quintris.place_piece(*tmp_quintris.state, tmp_quintris.piece, tmp_quintris.row, tmp_quintris.col)
                            quintris1 = deepcopy(tmp_quintris)
                            quintris1.state = board, score   
                            succ.append((quintris1,move))
                            tmp_quintris.row = store_row
                    
                        reset_qunitris(tmp_quintris, store_state,tmp_quintris.piece,store_row,store_col)
                        move = ''
                        move += (i+1)*'n'

                        for j in range(0,store_col):
                            tmp_quintris.left()
                            move+='b'
                            move_piece_down(tmp_quintris) 
                            board, score = tmp_quintris.place_piece(*tmp_quintris.state, tmp_quintris.piece, tmp_quintris.row, tmp_quintris.col)
                            quintris1 = deepcopy(tmp_quintris)
                            quintris1.state = board, score   
                            succ.append((quintris1,move))
                            tmp_quintris.row = store_row
        except Exception:
            print(f'col: {tmp_quintris.col}')
        reset_qunitris(tmp_quintris, store_state,store_piece,store_row,store_col)
        return succ

# Expectimax logic
# Max nodes at depth d followed by chance nodes at depth d-1
# Two kinds of chance nodes: 1.) Successors of current node. 2.) Successors of next node.
# For 1.), Probability of pieces = 1. Since we already know the next piece.
# For 2.), Probability is 1/6 since there are 6 different pieces to choose from 
# @param: depth: Depth at which we call expectimax
# @param: best_move: Move from quintris to it's successor with maximum evaluation.
# @param: game_depth: Depth of the game tree. 
def expectimax(quintris, depth, player,best_move, game_depth = 5):
    previous_piece = str(quintris.get_piece()[0])

    if depth ==0: #or terminal(quintris):
        h = heuristic(quintris.get_board())
        
        return h, best_move
    if player == "max":
        max_eval = -np.Infinity
        if str(previous_piece) not in best_move:
            best_move[str(previous_piece)] = 'b'
        succ = generate_successors2(quintris)
        for shat in succ:

                
            maxeval, best_move = expectimax(shat[0], depth-1,"chance", best_move,5)

            if (maxeval >= max_eval):
                best_move[str(previous_piece)] = shat[1]
                max_eval = maxeval
           

        if (depth == game_depth):
            print(f'in max=> maxeval:{maxeval},best_move:{best_move} ')
        return max_eval, best_move

    else:
        # calculate chance layer using 6 shapes
        Ex = 0
        if depth == game_depth-1:

            quintris1 = deepcopy(quintris)
            quintris1.piece = quintris.get_next_piece()
            quintris1.row = 0
            quintris1.col = 0
            maxeval, best_move = expectimax(quintris1, depth-1,"max", best_move,5)
            Ex = 1*maxeval
            return Ex, best_move
        else:
            pieces = [ [ " x ", "xxx", " x "], [ "xxxxx" ], [ "xxxx", "   x" ], [ "xxxx", "  x " ], [ "xxx", "x x"], [ "xxx ", "  xx" ] ]
            for piece in pieces:
                quintris1 = deepcopy(quintris)
                quintris1.piece = piece
                quintris1.row = 0
                quintris1.col = 0
                maxeval, best_move = expectimax(quintris1, depth-1,"max", best_move,5)
                Ex+= 1/6*maxeval
            return Ex, best_move


# Expectimax with a depth of only 3. 
# considers only the current node and it's successors and the next node and it's successors.
# Max nodes at depth d followed by chance nodes at depth d-1
# @param: depth: Depth at which we call expectimax
# @param: best_move: Move from quintris to it's successor with maximum evaluation.
# @param: game_depth: Depth of the game tree. 

def expectimax_small(quintris, depth, player,best_move, game_depth):
     
    previous_piece = str(quintris.get_piece()[0])
    if depth ==0: 
        h = heuristic(quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)[0], quintris.BOARD_WIDTH, quintris.BOARD_HEIGHT)
        return h, best_move

    if player == "max":
        max_eval = -np.Infinity
        succ = generate_successors2(quintris)
        if str(previous_piece) not in best_move:
                best_move[str(previous_piece)] = 'b'
        for shat in succ:
            maxeval, best_move = expectimax_small(shat[0], depth-1,"chance", best_move,game_depth)
            if (maxeval >= max_eval):
                best_move[str(previous_piece)] = shat[1]
                max_eval = maxeval
        return max_eval, best_move

    else:
        Ex = 0
        quintris1 = deepcopy(quintris)
        placement_col = 0
        placement_col_list = []
        board = quintris.state[0]
        for col in range(len(board[0])):
            if board[0][col]!='x':
                placement_col_list.append(col)
        placement_col = random.choice(placement_col_list)
        quintris1.piece = quintris.get_next_piece()
        quintris1.row = 0
        quintris1.col = placement_col
        maxeval, best_move = expectimax_small(quintris1, depth-1,"max", best_move,game_depth)
        Ex = 1*maxeval
        return Ex, best_move
        
# Expectimax with a depth of only 3. 
# considers only the current node and it's successors and the next node and it's successors.
# Max nodes at depth d followed by chance nodes at depth d-1
# @param: depth: Depth at which we call expectimax
# @param: best_move: Move from quintris to it's successor with maximum evaluation.
# @param: game_depth: Depth of the game tree.
# @param:tmp_quintris: Temporary copy of AnimatedQuintris()

def expectimax_small_animated(quintris,tmp_quintris, depth, player,best_move, game_depth):
     
    previous_piece = str(quintris.get_piece()[0])
    if depth ==0: 
        h = heuristic(quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)[0], quintris.BOARD_WIDTH, quintris.BOARD_HEIGHT)
        return h, best_move

    if player == "max":
        max_eval = -np.Infinity
        succ = generate_successors2_animated(quintris,tmp_quintris)
        if str(previous_piece) not in best_move:
                best_move[str(previous_piece)] = 'b'
        for shat in succ:
            maxeval, best_move = expectimax_small_animated(shat[0],tmp_quintris, depth-1,"chance", best_move,game_depth)
            if (maxeval >= max_eval):
                best_move[str(previous_piece)] = shat[1]
                max_eval = maxeval
        return max_eval, best_move

    else:
        Ex = 0
        quintris1 = deepcopy(quintris)
        placement_col = 0
        placement_col_list = []
        board = quintris.state[0]
        for col in range(len(board[0])):
            if board[0][col]!='x':
                placement_col_list.append(col)
        placement_col = random.choice(placement_col_list)
        quintris1.piece = quintris.get_next_piece()
        quintris1.row = 0
        quintris1.col = placement_col
        maxeval, best_move = expectimax_small_animated(quintris1,tmp_quintris, depth-1,"max", best_move,game_depth)
        Ex = 1*maxeval
        return Ex, best_move



# Converts the board into numpy array
# Takes a board as input and returns a 2d array of the board.
# @param: board: board of the quintris
def convert_board(board):
    a = np.empty((25, 15), dtype='U1')
    for r in range(len(board)):
        innerl = [" "]* 15
        for c in range(len(board[0])):
            innerl[c] = board[r][c]
        a[r] = innerl
    return np.array(a)



# Get column heights from the board
# Generates a dictionary with key as column and value as it's height
# @param: board: board of the quintris

def get_col_heights(board, width, height):
    # initializing col heights
    col_heights = {}  
    
    for col in range(width):
        zero_count = 0
        min_idx = np.Infinity  

        for row in range(height):
            
            if board[row][col] == "x":
                # column height would be nrows-max index at which x is at that column.
                # Because, we are placing the tetris on the bottom of the board.
                min_idx = min(min_idx, row)

                col_height = len(board) - min_idx

                col_heights[col] = col_height
            else:
                zero_count+=1
                if(zero_count == len(board)):
                    col_heights[col] = 0
       
    return np.array([h for h in col_heights.values()])


# Get total number of holes by on the board 
# Accepts board and list of column heights as input and returns a list of number of holes per column
# @param: board: board of the quintris
# @param: col_heights: List of column heights

def get_col_holes(board, col_heights, width):
    board_array = convert_board(board)
    col_holes = []  
    for c in range(board_array.shape[1]):
        if(c>=width):
            continue
        i = len(board) - col_heights[c]
        if i ==0:
            col_holes.append(0)
        else:
            col_holes.append(np.count_nonzero(board_array[i:, c] !="x"))
    return col_holes

# Get total number of lines cleared
# Accepts board as input and returns a list of number of lines completed
# @param: board: board of the quintris

def get_lines_cleared(board):
    #board = convert_board(board)
    # code referenced from : QunitrisGame.py
    complete = complete = [ i for (i, s) in enumerate(board) if s.count(' ') == 0 ]
    # end of code referenced from : QunitrisGame.py
    return len(complete)


# returns the total transitions possible in a column
# column transition is an empty cell adjacent to a "x" in the same column

def get_column_transitions(board, col_heights):
    total = 0
    board = convert_board(board)
    for col in range(len(col_heights)):
        # if the column is empty or has "x" only on the bottom of the board
        if col_heights[col]<=1:
            continue
        else:
            # column transitions possible for cells  with more than 1 "x" and it's neighbours are empty
            for row in range(board.shape[0] - col_heights[col], board.shape[0]-1):
                if board[row][col] != board[row+1][col]:
                    total+=1
    return total

# returns the total transitions possible in a column
# column transition is an empty cell adjacent to a "x" in the same column
def get_row_transitions(board, max_col_height):
    total = 0
    board = convert_board(board)

    for row in range(board.shape[0]-max_col_height, board.shape[0]):
        for col in range(0, board.shape[1]-1):
            if board[row][col] != board[row][col+1]:
                total+=1
    return total

# Returns how smooth the board is
# Accepts column heights as input and returns the difference between consecutive column heights in the board
# @param: col_heights: List of column heights
def get_wavyness(col_heights):
    bump =0
    for i in range(len(col_heights)-1):
        bump+=abs(col_heights[i+1]-col_heights[i])
    return bump        


#checks how many empty columns are available in the board
# Accepts board as input and returns the number of empty columns on the board
# @param: board: board of quintris
def get_empty_cols(board):
    board = convert_board(board)
    empty_cols = np.count_nonzero(np.count_nonzero(board == "x", axis=0) ==0)
    return empty_cols


# Evaluation function
# Accepts board as input and returns the evaluation of that board
# Heuristic is weighted sum of 1.) Total column height 2.) Total holes on the board 3.) Total lines cleared
# 4.) Wavyness of the board. 5.) Number of empty columns
# We want to minimise Total column height, total holes on board, number of empty columns and wavyness of the board.
# We want to maximise the total number of rows cleared.

def heuristic(board, width, height):

    ### Evaluations ###
    # Referred to this article for heuristic functions: https://meatfighter.com/nintendotetrisai/#Java_Version
    # column heights

    col_heights = get_col_heights(board, width, height)
    max_height = np.max(col_heights)

    # total column height
    total_col_height = np.sum(col_heights)

    # get holes by column
    col_holes = get_col_holes(board, col_heights,width)

    total_holes = np.sum(col_holes)

    ## get board wavyness
    wavyness = get_wavyness(col_heights)

    total_lines_cleared = get_lines_cleared(board)


    # Not using row transitions and column transitions
    # row_transitions = get_row_transitions(qunitris.get_board(), max_height)
    # col_transitions = get_column_transitions(qunitris.get_board(), col_heights)

    empty_cols = get_empty_cols(board)
    return -100* total_col_height + 500* total_lines_cleared -10* empty_cols -50*total_holes -20 * wavyness

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times  
        # 
        #Returning best move obtained for quintris from expectimax     
        best_move = {}
        previous_piece = str(quintris.get_piece()[0])
        
        
        max_eval, best_move = expectimax_small(quintris, 3, "max",best_move, 3)
        #max_eval, best_move = expectimax(quintris, 5, "max",best_move, 5)
        return best_move[str(previous_piece)]
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            #Returning best moves for the quintris using expectimax
            #Also added quintris.down() after we exhaust our move to immediately place the tile in it's correct position.
            tmp_quintris = AnimatedQuintris()
            #succ  = generate_successors2_animated(quintris, tmp_quintris)
            
            best_move = {}
            previous_piece = str(quintris.get_piece()[0])
            max_eval, best_move = expectimax_small_animated(quintris,tmp_quintris, 3, "max",best_move, 3)
            print(f'max_eval:{max_eval}, best_move: {best_move[str(previous_piece)]}')  
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            moves = best_move[str(previous_piece)]
            for i in range(len(moves)+1):
                if i == len(moves):
                    quintris.down()
                else:
                    commands[moves[i]]()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]



try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



