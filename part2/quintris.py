# Simple quintris program! v0.2
# D. Crandall, Sept 2021

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
        print(f' printing board before the  moves')
       
        # succ, probs = generate_successors(quintris)
        # Ex = 0
        # print(f'probs: {probs}')
        # for shat in succ:
        #     #piece = str(shat[0].get_piece()[0])
        #     print(f'shat: {shat[0].get_piece()}, move: {shat[1]}')
        #     #Ex+=probs[piece]*shat[2]
        # #print(f'Expectation: {Ex}')

        pieces = [ [ " x ", "xxx", " x "], [ "xxxxx" ], [ "xxxx", "   x" ], [ "xxxx", "  x " ], [ "xxx", "x x"], [ "xxx ", "  xx" ] ]

    
        #succ = generate_successors(quintris)
        # for shat in succ:
        #     shat[0].print_board(False)
        #     print(f'successors: {shat[0].piece}, move: {shat[1]}, eval: {shat[2]}')
        # best_move = 'b'
        # expectimax(self, quintris, 3, "max",best_move, 3)
        best_move = {}
        print(f'quintris orig:{quintris.get_piece()}')
        previous_piece = str(quintris.get_piece()[0])
        max_eval, best_move = expectimax_small(quintris, 3, "max",best_move, 3)
        for x in best_move:
            print(f'x:{x}, best move:{best_move[x]}')
        print(f'max_eval:{max_eval}, best_move: {best_move[str(previous_piece)]}')
        # self.qlist = []
        
        return best_move[str(previous_piece)]

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            
            commands[c]()

# def generate_prob(quintris):
#     succ_list = []
#     #quintris.place_piece(piece)
#     probs = new_pieces_prob(quintris)
#     print(f'probs: {probs}')
#     pass    
# 

## check collision

# def check_collision(board, score, piece, row, col):
#     return col+len(piece[0]) > 25 or row+len(piece) > 15 \
#     or any( [ any( [ (c != " " and board[i_r+row][col+i_c] != " ") for (i_c, c) in enumerate(r) ] ) for (i_r, r) in enumerate(piece) ])


def move_piece_down(quintris):
    while not quintris.check_collision(*quintris.state,quintris.piece,quintris.row+1,quintris.col):
            quintris.row += 1
    # board, score = quintris.place_piece(quintris.get_board(),0, qunitris1.get_piece()[0],row, col)
    # print(f'board:{board}')
    # quintris.state = board, score
    # quintris.print_board(False)

    #return quintris

# generate a probability distribution for successors    
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

def generate_successors1(quintris):
    succ = []
    probs = {}
    count = 0
    col = quintris.get_piece()[2]
    # print(f'quintris.get_piece(): {quintris.get_piece()}')
    # print(f'quintris.get_board(): {quintris.get_board()}')

    quintris1 = deepcopy(quintris)
    for i in range(0,col):
        quintris1 = deepcopy(quintris1)

        quintris1.left()
        #move_piece_down(quintris, quintris1, quintris1.get_piece()[1],quintris1.get_piece()[2])

        move_str = "b"*(i+1)
        #quintris1.down()
        #val = heuristic(quintris1)
        move_piece_down(quintris1)
        #quintris1.print_board(False)
        succ.append((quintris1, move_str))

    quintris1 = deepcopy(quintris)
    for i in range(col, len(quintris1.get_board()[0])):
        quintris1 = deepcopy(quintris1)
        p = quintris1.get_piece()[0]
        maxlen = max([len(x) for x in p])

        if (i<len(quintris1.get_board()[0]) - maxlen):
            quintris1.right()

            move_str = "m"* (i-col+1)
            #val = heuristic(quintris1)
            move_piece_down(quintris1)
           # quintris1.print_board(False)

            succ.append((quintris1, move_str))
    

        
    


    prev_succ = deepcopy(succ)
    for shat in prev_succ:
        quintris1 = deepcopy(shat[0])
        
        for i in range(3):
            quintris1 = deepcopy(quintris1)
            for _ in range(0,i):
                quintris1.rotate()
            #val = heuristic(quintris1)
            move_str = shat[1]+"n"*(i+1)
            #print(f'move_str: {move_str}')
            move_piece_down(quintris1)
            #quintris1.print_board(False)

            succ.append((quintris1,move_str))

        quintris1 = deepcopy(shat[0])
        quintris1.hflip()
        #val = heuristic(quintris1)
        move_piece_down(quintris1)
        #quintris1.print_board(False)
        succ.append((quintris1,"h"))

        for i in range(3):
            quintris1 = deepcopy(quintris1)
            for _ in range(0,i):
                quintris1.rotate()
            #val = heuristic(quintris1)
            move_str =  shat[1]+"n"*(i+1)
            move_piece_down(quintris1)
            #quintris1.print_board(False)
            succ.append((quintris1,move_str))

    quintris1 = deepcopy(quintris)

    for i in range(3):
        quintris1 = deepcopy(quintris1)
        for _ in range(0,i):
                quintris1.rotate()
        #quintris1.rotate()
        #val = heuristic(quintris1)
        move_str = "n"*(i+1)
        move_piece_down(quintris1)
        #quintris1.print_board(False)
        succ.append((quintris1,move_str))

    quintris1 = deepcopy(quintris)
    quintris1.hflip()
    move_piece_down(quintris1)
    #quintris1.print_board(False)
    #val = heuristic(quintris1)
    succ.append((quintris1,"h"))

    for i in range(3):
        quintris1 = deepcopy(quintris1)
        for _ in range(0,i):
                quintris1.rotate()
        #quintris1.rotate()
        #val = heuristic(quintris1)
        move_str = "n"*(i+1)
        move_piece_down(quintris1)
       # quintris1.print_board(False)
        succ.append((quintris1,move_str))
    #print(f'len(succ)L {len(succ)}')
    for shat in succ:
        p = str(shat[0].get_piece()[0])
       # print(p)
        if p in probs:
            probs[p]+=1
        else:
            probs[p] = 1

    for p in probs.keys():
        probs[p]/=len(succ)

    
    # moves = ['b','m','h','n']
    # count =0
    # print(f'quintris: {quintris}')
    # for m in moves:
    #     quintris1 = deepcopy(quintris)
        
    #     if m == "b":
    #         quintris1.left()

    #     elif m == "m":
    #         quintris1.right()

    #     elif m == "h":
    #         quintris1.hflip()

    #     elif m == "n":
    #         quintris1.rotate()
    #     p = str(quintris1.get_piece()[0])

    #     if p in succ:
    #         probs[p]+=1
    #     else:
    #         probs[p] = 1
        
    #     #quintris1.down()
    #     # quintris1.print_board(False)
    #     score = heuristic(quintris1)
    #     succ.append((quintris1, m,score))
    #     count+=1
    #     # replist = [x for x in succ if x[1]==quintris1]
    #     # if len(replist)==0:
    #     #     succ.append((m,quintris1))
    # for p in probs.keys():
    #     probs[p]/=count
    # for shat in succ:
    #     print(f'successor: {shat[0].get_piece(),shat[1], shat[2]}')
    # print(len(succ))
    return succ,probs
        

def reset_qunitris(qunitris, state, piece, row, col):
    qunitris.state = state
    qunitris.piece = piece
    qunitris.row = row
    qunitris.col = col

def generate_successors2(quintris):
        total_moves = [0,1,2]
        store_piece = quintris.piece
        store_col = quintris.col
        store_row  =quintris.row
        store_state = quintris.state
        succ=[]
        move=''

        # Discussed logic of count from total moves, with Madhav Jariwala: makejari@iu.edu 
        # count  = 0 means you can only move a piece left and right
        # count = 1 means you can flip and rotate a piece once
        # count = 2 means you can rotate a piece 3 times
         
        for count in range(len(total_moves)):
            if count==0:
                for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                    if j!=store_col:
                        quintris.right()
                        move+='m'
                    move_piece_down(quintris)
                    board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                    h = heuristic(board)
                    quintris1 = deepcopy(quintris)
                    quintris1.state = board, score   
                   
                    succ.append((quintris1,move,h ))
                    quintris.row = store_row
                
                reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)
                move=''
                for j in range(0,store_col):
                    quintris.left()
                    move+='b'
                    move_piece_down(quintris)
                    board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                    h = heuristic(board)
                    quintris1 = deepcopy(quintris)
                    quintris1.state = board, score   
                   
                    succ.append((quintris1,move,h ))
                   
                    quintris.row = store_row
            
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
                        h = heuristic(board)
                        quintris1 = deepcopy(quintris)
                        quintris1.state = board, score   
                    
                        succ.append((quintris1,move,h ))
                       
                        quintris.row = store_row 
                    reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)

                    move = ''
                    move+='h'
                    for j in range(0,store_col):
                        quintris.left()
                        move+='b'
                        move_piece_down(quintris)
                        board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                        h = heuristic(board)
                        quintris1 = deepcopy(quintris)
                        quintris1.state = board, score   
                      
                        succ.append((quintris1,move,h ))
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
                            h = heuristic(board)
                            quintris1 = deepcopy(quintris)
                            quintris1.state = board, score   
                            
                            succ.append((quintris1,move,h ))
                            quintris.row = store_row
                    
                        reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)
                        move = ''
                        move+='h'
                        move += (i+1)*'n'
                        for j in range(0,store_col):
                            quintris.left()
                            move+='b'
                            move_piece_down(quintris)
                            board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                            h = heuristic(board)
                            quintris1 = deepcopy(quintris)
                            quintris1.state = board, score   
                            
                            succ.append((quintris1,move,h ))
                            
                            quintris.row = store_row
            
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
                        h = heuristic(board)
                        quintris1 = deepcopy(quintris)
                        quintris1.state = board, score   
                        succ.append((quintris1,move,h ))
                        quintris.row = store_row
                
                    reset_qunitris(quintris, store_state,quintris.piece,store_row,store_col)
                    move = ''
                    move += (i+1)*'n'

                    for j in range(0,store_col):
                        quintris.left()
                        move+='b'
                        move_piece_down(quintris) 
                        board, score = quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                        h = heuristic(board)
                        quintris1 = deepcopy(quintris)
                        quintris1.state = board, score   
                        succ.append((quintris1,move,h ))
                        quintris.row = store_row
        
        reset_qunitris(quintris, store_state,store_piece,store_row,store_col)
        return succ



def expectimax(mode, quintris, depth, player,best_move, game_depth = 5):
     
    # print(f'board: {quintris.state}')
    # print(f'bestmove: {best_move}')
    # print(f'depth: {depth}')
    if depth ==0: #or terminal(quintris):
        h = heuristic(quintris.get_board())
        #print(f'depth 0:{h}' )
        #quintris.print_board(False)
        return h, best_move
    if player == "max":
        max_eval = -np.Infinity

        succ = generate_successors2(quintris)
        for shat in succ:

                
            maxeval, best_move = expectimax(mode,shat[0], depth-1,"chance", best_move,5)

            if (maxeval >= max_eval):
                best_move = shat[1]
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
            maxeval, best_move = expectimax(mode,quintris1, depth-1,"max", best_move,5)
            Ex = 1*maxeval
            return Ex, best_move
        else:
            pieces = [ [ " x ", "xxx", " x "], [ "xxxxx" ], [ "xxxx", "   x" ], [ "xxxx", "  x " ], [ "xxx", "x x"], [ "xxx ", "  xx" ] ]
            for piece in pieces:
                quintris1 = deepcopy(quintris)
                quintris1.piece = piece
                quintris1.row = 0
                quintris1.col = 0
                maxeval, best_move = expectimax(mode,quintris1, depth-1,"max", best_move,5)
                Ex+= 1/6*maxeval
            return Ex, best_move


# Expectimax with a depth of only 3. 
# considers only the current node and it's successors and the next node and it's successors.

def expectimax_small(quintris, depth, player,best_move, game_depth):
     
    previous_piece = str(quintris.get_piece()[0])
    if depth ==0: 
        h = heuristic(quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)[0])
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
        quintris1.piece = quintris.get_next_piece()
        quintris1.row = 0
        quintris1.col = 0
        maxeval, best_move = expectimax_small(quintris1, depth-1,"max", best_move,game_depth)
        Ex = 1*maxeval
        return Ex, best_move
        

def convert_board(board):
    a = np.empty((25, 15), dtype='U1')
    for r in range(len(board)):
        innerl = [" "]* 15
        for c in range(len(board[0])):
            innerl[c] = board[r][c]
        a[r] = innerl
    return np.array(a)



# get column heights:
def get_col_heights(board):
    # initializing col heights
    #board_array = convert_board(board)
    col_heights = {}  
    
    for col in range(len(board[0])):
        zero_count = 0
        min_idx = np.Infinity  

        for row in range(len(board)):

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


# get column holes
def get_col_holes(board, col_heights):
    # initializing col heights
    board_array = convert_board(board)
    col_holes = []  
    for c in range(board_array.shape[1]):
        i = len(board) - col_heights[c]
        if i ==0:
            col_holes.append(0)
        else:
            col_holes.append(np.count_nonzero(board_array[i:, c] !="x"))
    return col_holes

# get total number of lines cleared
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

# it is how smoooth the tetris board is
# It measures the difference between consecutive column heights in the board
def get_wavyness(col_heights):
    bump =0
    for i in range(len(col_heights)-1):
        bump+=abs(col_heights[i+1]-col_heights[i])
    return bump        


## checks how many empty columns are available in the board
def get_empty_cols(board):
    board = convert_board(board)
    empty_cols = np.count_nonzero(np.count_nonzero(board == "x", axis=0) ==0)
    return empty_cols

def evaluate():
    pass

def heuristic(board):

    ### Evaluations ###
    # Referred to this article for heuristic functions: https://meatfighter.com/nintendotetrisai/#Java_Version
    # column heights

    col_heights = get_col_heights(board)
    #print(f'col heights: {col_heights}')
    max_height = np.max(col_heights)
    #print(f'max height: {max_height}')
    
    # total column height
    total_col_height = np.sum(col_heights)
    #print(f'total_col_height: {total_col_height}')

    # get holes by column
    col_holes = get_col_holes(board, col_heights)

    total_holes = np.sum(col_holes)
    #print(f'total_holes: {total_holes}')

    ## get board wavyness
    wavyness = get_wavyness(col_heights)
    #print(f'wavyness: {wavyness}')

    total_lines_cleared = get_lines_cleared(board)


    # Not using row transitions and column transitions
    # row_transitions = get_row_transitions(qunitris.get_board(), max_height)
    # #print(f'row_transitions: {row_transitions}')

    # col_transitions = get_column_transitions(qunitris.get_board(), col_heights)
    #print(f'col_transitions: {col_transitions}')

    empty_cols = get_empty_cols(board)
    return -100* total_col_height + 200* total_lines_cleared +5* empty_cols -50*total_holes -10 * wavyness

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
        best_move = {}
        previous_piece = str(quintris.get_piece()[0])
        max_eval, best_move = expectimax_small(quintris, 3, "max",best_move, 3)
        print(f'max_eval:{max_eval}, best_move: {best_move[str(previous_piece)]}')        
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

            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()


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



