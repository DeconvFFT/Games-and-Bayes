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

        # for p in pieces: 
        #     quintris1 = deepcopy(quintris)
        #     board,score = quintris1.place_piece(quintris1.get_board(),0, p, 0,7)
        #     print(f'piece: {p}, board: {board}')
        #     quintris1.state = board, score
        
        # succ, _  = generate_successors(quintris)
        # for shat in succ:


        #     shat[0].print_board(False)
        self.qlist = []
        expectimax(self, quintris, 3, "max", 3)
        print(f'best moves: {self.qlist}')
        #quintris.print_board(False)



        return moves

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

def check_collision(board, score, piece, row, col):
    return col+len(piece[0]) > QuintrisGame.BOARD_WIDTH or row+len(piece) > QuintrisGame.BOARD_HEIGHT \
    or any( [ any( [ (c != " " and board[i_r+row][col+i_c] != " ") for (i_c, c) in enumerate(r) ] ) for (i_r, r) in enumerate(piece) ])


def move_piece_down(qunitris):
    while not qunitris.check_collision(*quintris.state, qunitris.piece, qunitris.row+1,qunitris.col):
        qunitris.row+=1
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

def generate_successors(quintris):
    succ = []
    probs = {}
    count = 0
    col = quintris.get_piece()[2]
    #print(f'quintris.get_piece(): {quintris.get_piece()}')
    
    quintris1 = deepcopy(quintris)
    for i in range(0,col):
        quintris1 = deepcopy(quintris1)

        quintris1.left()
        #move_piece_down(quintris, quintris1, quintris1.get_piece()[1],quintris1.get_piece()[2])

        move_str = "b"*(i+1)
        #quintris1.down()
        #val = heuristic(quintris1)
        move_piece_down(quintris1)

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
            succ.append((quintris1,move_str))

        quintris1 = deepcopy(shat[0])
        quintris1.hflip()
        #val = heuristic(quintris1)
        move_piece_down(quintris1)
        succ.append((quintris1,"h"))

        for i in range(3):
            quintris1 = deepcopy(quintris1)
            for _ in range(0,i):
                quintris1.rotate()
            #val = heuristic(quintris1)
            move_str =  shat[1]+"n"*(i+1)
            move_piece_down(quintris1)
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
        succ.append((quintris1,move_str))

    quintris1 = deepcopy(quintris)
    quintris1.hflip()
    move_piece_down(quintris1)
    #val = heuristic(quintris1)
    succ.append((quintris1,"h"))

    for i in range(3):
        #quintris1 = deepcopy(quintris1)
        for _ in range(0,i):
                quintris1.rotate()
        #quintris1.rotate()
        #val = heuristic(quintris1)
        move_str = "n"*(i+1)
        move_piece_down(quintris1)
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
        
# def max_value(quintris, alpha, beta):
#     for shat in generate_successors(quintris):
#         alpha =  max(alpha, (min_value(shat, alpha, beta)))
#         if alpha >= beta:
#             return alpha
#     return alpha

# def min_value(quintris, alpha, beta):
#     for shat in generate_successors(quintris):
#         beta =  min(alpha, (max_value(shat, alpha, beta)))
#         if beta <= alpha:
#             return beta
#     return beta


# def terminal(quintris):
#     return QuintrisGame.check_collision(*quintris.state,quintris.get_piece()[0], quintris.get_piece()[1],quintris.get_piece()[2])


# def maximax(qunitris, depth, player):

#     if depth ==0:
#         return heuristic(quintris)
        
#     if player == "max":
#         max_eval = -np.Infinity
#         succ, _ = generate_successors(quintris)
#         for shat in succ:
#             eval = maximax(shat[0], depth-1,"chance")
#             max_eval = max(max_eval, eval)
#             print(f'max_eval:{max_eval}, "depth:{depth}')
#         return max_eval

#     # add a max layer for next tile
#     elif player == "chance":
#         max_eval = -np.Infinity
#         succ, _ = generate_successors(quintris)
#         for shat in succ:
#             eval = maximax(shat[0], depth-1,"chance")
#             max_eval = max(max_eval, eval)
#             print(f'max_eval:{max_eval}, "depth:{depth}')
#         return max_eval
#     pass

def expectimax(mode, quintris, depth, player, game_depth = 3):
    best_move = 'b'

    if depth ==0: #or terminal(quintris):
        #print(f'end heuristic: {heuristic(quintris)}')
        return heuristic(quintris)
    
    if player == "max":
        max_eval = -np.Infinity
        #print(f'Inside max..')
        #quintris.print_board(False)

        succ, _ = generate_successors(quintris)
        for quintris1,move in succ:
            # print('successor of max...')
            # if (depth == game_depth -1):
            #     print("successor of next..")
                

            # next_piece = shat[0].get_next_piece()
            # shat[0]
            #move_piece_down(shat[0])
           # print(f'piece after down: {quintris1.get_piece()}')
            #shat[0].state =  shat[0].place_piece(*shat[0].state,shat[0].piece,shat[0].row, shat[0].col )
            #print(f'board after down: {quintris1.get_board()}')

            
            
            eval = expectimax(mode,quintris1, depth-1,"chance", 3)
            if (eval >= max_eval):
                best_move = move
            max_eval = max(max_eval, eval)
            

        #quintris.print_board(False)
        mode.qlist.append((quintris, best_move, max_eval))
        print(f'max_value: {max_eval}, bestmove: {best_move}, depth:{depth}')

        return max_eval

    else:
        # calculate chance layer using 6 shapes
        Ex = 0
       # print(f'else depth: {depth}')
        if depth == game_depth-1:
            # quintris1 = deepcopy(quintris)
            # quintris.print_board(False)
            # print(f'quintris.get_next_piece(): {quintris.get_next_piece()}')
            # board,score = quintris1.place_piece(quintris.get_board(), quintris.get_score(), quintris.get_next_piece(),0,7 )
            # quintris1.state = board,score
            #print(f'successor of current ... ')

            quintris1 = deepcopy(quintris)
            board,score = quintris1.place_piece(*quintris1.state, quintris1.get_next_piece(), 0,0)
            quintris1.state = board,score
            quintris1.print_board(False)
            #quintris.print_board(False)

            Ex = 1*expectimax(mode,quintris1, depth,"max", 3)
            #print(f'Ex for successor of current from next piece: {Ex}')
            return Ex
        else:
            pieces = [ [ " x ", "xxx", " x "], [ "xxxxx" ], [ "xxxx", "   x" ], [ "xxxx", "  x " ], [ "xxx", "x x"], [ "xxx ", "  xx" ] ]
            for piece in pieces:
                #piece = str(shat[0].get_piece()[0])
                quintris1 = deepcopy(quintris)
                board,score = quintris1.place_piece(*quintris1.state, piece, 0,0 )
                quintris1.state = board,score
               # print(f'chance nodes')
                #quintris.print_board(False)

                Ex+= 1/6*expectimax(mode,quintris1, depth,"max", 3)
                #print(f'depth:{depth}, E: {Ex}')

            return Ex

    # max_eval = -np.Infinity
    # max_prob = -np.Infinity
    # succ, probs = generate_successors(quintris)
    # quintris.print_board(False)
    # for shat in succ:
    #     eval = heuristic(shat[0])
    #     if eval > max_eval:
    #         max_eval = eval
    #         best_move = shat[1]
    #         max_qunitris = quintris
    #         max_prob = probs[str(shat[0].get_piece()[0])] 

    # # chance nodes one level up from the max node
    # Ex = max_prob*max_eval
    # print(f'max_eval:{max_eval}, "best_move:{best_move}, "max_prob:{max_prob}, Ex: {Ex}')

    # return Ex, best_move, max_qunitris


# def minimax(quintris, depth, alpha, beta, max_player):

#     if depth ==0 or terminal(quintris):
#         return heuristic(quintris)
    
#     if max_player:
#         max_eval = -np.Infinity
#         for shat in generate_successors(quintris):
#             eval = minimax(shat, depth-1, alpha, beta, False)
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval
    
#     else:
#         min_eval = np.Infinity()
#         for shat in generate_successors(quintris):
#             eval = minimax(shat, depth-1, alpha, beta, True)
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval



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
    board_array = convert_board(board)
    #print(f'board_array: {board_array}')
    col_heights = []    
    for col in range(board_array.shape[1]):
        if "x" in board_array[:,col]:
            # column height would be nrows-max index at which x is at that column.
            # Because, we are placing the tetris on the bottom of the board.
            col_height = board_array.shape[0] - np.min(np.where(board_array[:,col] == "x"))
            col_heights.append(col_height)
        else:
            col_heights.append(0)
            
    return np.array(col_heights)


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
   # print(f'col_holes: {col_holes}')
    return col_holes


# get total number of lines cleared
def get_lines_cleared(board):
    board = convert_board(board)
    complete = [i for i in range(board.shape[0]) if np.sum(board[i,:] == " ") == 0]
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

def heuristic(qunitris):
    #lines_cleared+total_height+sum_diff_col_heights+holes
    ### Evaluations ###
    # Referred to this article for heuristic functions: https://meatfighter.com/nintendotetrisai/#Java_Version
    # column heights

    col_heights = get_col_heights(qunitris.get_board())
    #print(f'col heights: {col_heights}')
    max_height = np.max(col_heights)
    #print(f'max height: {max_height}')
    
    # total column height
    total_col_height = np.sum(col_heights)
    
    # get holes by column
    col_holes = get_col_holes(qunitris.get_board(), col_heights)

    total_holes = np.sum(col_holes)

    ## get board wavyness
    wavyness = get_wavyness(col_heights)
    #print(f'wavyness: {wavyness}')

    total_lines_cleared = get_lines_cleared(qunitris.get_board())

    #print(f'total_lines_cleared: {total_lines_cleared}')

    # row_transitions = get_row_transitions(qunitris.get_board(), max_height)
    # #print(f'row_transitions: {row_transitions}')

    # col_transitions = get_column_transitions(qunitris.get_board(), col_heights)
    # #print(f'col_transitions: {col_transitions}')

    empty_cols = get_empty_cols(qunitris.get_board())
   # print(f'empty_cols: {empty_cols}')

    # row_transitions, col_transitions,
    return -0.510066*total_col_height+ 0.760666*total_lines_cleared+ -0.35663*total_holes-0.184483*wavyness

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
        c = random.choice("mnbh")
        # print(f'max piece: {quintris.get_piece()} move: {c}')
        # print(f'Printing max successors.....')
        # max_successor = generate_successors(quintris)
        # print(f'min piece: {quintris.get_next_piece()} move: {c}')

        # print(f'Printing min successors.....')
        # quintris.place_piece(quintris.get_next_piece())
        # min_successors = generate_successors(moves,quintris, "max")
        #pass
        #expectimax(quintris, 2, "max", 2)

        return c * random.randint(1, 10)
       
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



