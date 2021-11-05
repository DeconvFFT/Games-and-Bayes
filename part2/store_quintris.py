# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        
        
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()            
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            
            commands[c]()

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


        ##code added, remove later

        self.total_moves = {0:'NoChange',1:'horizontal_flip_and_rotate',2:'rotate_thrice'}
        store_piece = quintris.piece
        store_col = quintris.col
        store_row  =quintris.row
        store_state = quintris.state
        fringe=[]
        move_string=''
        
        

        # print('HEre')
        
        # print('before row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
        # print('here end')
        
        for count in range(len(self.total_moves)):
            if count==0:
                for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                    if j!=store_col:
                        quintris.right()
                        move_string+='m'
                    # print('move string is: ',move_string)
                    self.go_down(quintris)
                    # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece)) 
                    fringe.append([self.calculate_cost(quintris,quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col)[0],quintris.piece,quintris.row,quintris.col),move_string])
                    quintris.row = store_row
                    # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                
                self.reset_value(quintris, store_state,quintris.piece,store_row,store_col)
                move_string=''
                for j in range(0,store_col):
                    quintris.left()
                    move_string+='b'
                    # print('move string is: ',move_string)
                    self.go_down(quintris)
                    # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                    fringe.append([self.calculate_cost(quintris,quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col)[0],quintris.piece,quintris.row,quintris.col),move_string])
                    # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                    quintris.row = store_row
                # print("\n\nAfter the count =0:", fringe)
            
            self.reset_value(quintris, store_state,quintris.piece,store_row,store_col)

            if count==1:
                quintris.hflip()
                if quintris.piece != store_piece:
                    move_string = ''
                    move_string+='h'
                    for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                        if j!=store_col:
                            quintris.right()
                            move_string+='m'
                        # print('move string is: ',move_string)
                        self.go_down(quintris)
                        # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                        fringe.append([self.calculate_cost(quintris,quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col)[0],quintris.piece,quintris.row,quintris.col),move_string])
                        # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                        quintris.row = store_row 
                    self.reset_value(quintris, store_state,quintris.piece,store_row,store_col)

                    move_string = ''
                    move_string+='h'
                    for j in range(0,store_col):
                        quintris.left()
                        move_string+='b'
                        # print('move string is: ',move_string)
                        self.go_down(quintris)
                        # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                        fringe.append([self.calculate_cost(quintris,quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col)[0],quintris.piece,quintris.row,quintris.col),move_string])
                        # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                        quintris.row = store_row
                
                    for i in range(3):
                        self.reset_value(quintris, store_state,quintris.piece,store_row,store_col)

                        move_string = ''
                        move_string += 'h'
                        quintris.rotate()
                        move_string += (i+1)*'n'

                        for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                            if j!=store_col:
                                quintris.right()
                                move_string+='m'
                            # print('move string is: ',move_string)
                            self.go_down(quintris) 
                            # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                            fringe.append([self.calculate_cost(quintris,quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col)[0],quintris.piece,quintris.row,quintris.col),move_string])
                            # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                            quintris.row = store_row
                    
                        self.reset_value(quintris, store_state,quintris.piece,store_row,store_col)
                        move_string = ''
                        move_string+='h'
                        move_string += (i+1)*'n'
                        for j in range(0,store_col):
                            quintris.left()
                            move_string+='b'
                            # print('move string is: ',move_string)
                            self.go_down(quintris)
                            # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                            fringe.append([self.calculate_cost(quintris,quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col)[0],quintris.piece,quintris.row,quintris.col),move_string])
                            # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                            quintris.row = store_row
            
            self.reset_value(quintris, store_state,store_piece,store_row,store_col)

            if count==2:
                for i in range(3):
                    self.reset_value(quintris, store_state,quintris.piece,store_row,store_col)  
                    # print("Quintris value inside the count==2 before the rotation is :",quintris.piece)
                    move_string = ''
                    quintris.rotate()
                    if quintris.piece == store_piece:
                        # print("You're in rotation flip one and we came across matching result",quintris.piece,store_piece)
                        break
                    move_string += (i+1)*'n'

                    for j in range(store_col,len(quintris.state[0][0])-len(max(quintris.piece))+1):
                        if j!=store_col:
                            quintris.right()
                            move_string+='m'
                        # print('move string is: ',move_string)
                        self.go_down(quintris) 
                        # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                        fringe.append([self.calculate_cost(quintris,quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col)[0],quintris.piece,quintris.row,quintris.col),move_string])
                        # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                        quintris.row = store_row
                
                    self.reset_value(quintris, store_state,quintris.piece,store_row,store_col)
                    move_string = ''
                    move_string += (i+1)*'n'

                    for j in range(0,store_col):
                        quintris.left()
                        move_string+='b'
                        # print('move string is: ',move_string)
                        self.go_down(quintris) 
                        # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                        fringe.append([self.calculate_cost(quintris,quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col)[0],quintris.piece,quintris.row,quintris.col),move_string])
                        # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                        quintris.row = store_row
        
        self.reset_value(quintris, store_state,store_piece,store_row,store_col)
        # print(min(fringe))
        # print(fringe)
        return min(fringe)[1]
        
        

    def reset_value(self,quintris,state,piece,r,c):
        quintris.state = state
        quintris.piece = piece
        quintris.col = c
        quintris.row = r

    def calculate_cost(self,quintris,state,piece,r,c):
        holes_count = [(self.check_holes(state,r,c),(r,c)) for r in range(len(state)) for c in range(len(state[0]))]
        holes_count_sum = (sum([t1[0] for t1 in holes_count])-65) * 500
        column_heights = self.check_column_heights(state)
        game_over_cost = 0
        if max(column_heights)>=quintris.BOARD_HEIGHT- 2:
            game_over_cost = 1000000
        column_heights_cost = (max(column_heights) - min(column_heights)) * 1000
        number_of_empty_columns = sum([i==0 for i in column_heights]) * 30
        rows_full= 0
        for r in range(len(state)):
            rows_completed = [state[r][c] == 'x' for c in range(len(state[0]))]
            if sum(rows_completed) == quintris.BOARD_WIDTH:
                rows_full+=1
        # block_above_cost = self.block_above_holes(state,r,c) * 10
        total_cost = column_heights_cost + (rows_full*-100000) + game_over_cost + number_of_empty_columns + holes_count_sum
        
        return total_cost
        
        

    def go_down(self,quintris):
        while not quintris.check_collision(*quintris.state,quintris.piece,quintris.row+1,quintris.col):
            quintris.row += 1

    def block_above_holes(self,state,r,c):#Not giving good performance
        total_hole_cost = 0
        for j in range(len(state[0])):
            for i in range(len(state)-1,0-1,-1):
                if state[i][j] == ' ':
                    block_above_hole = 0
                    for k in range(i,0-1,-1):
                        if state[k][j] == 'x':
                            total_hole_cost+=block_above_hole
                        else:
                            block_above_hole+=1
        return total_hole_cost

    def check_holes(self,state,r,c):
        count=0
        if state[r][c]==' ':
            if r>0 and r<len(state)-1:
                if state[r+1][c] == 'x':
                    count+=1
                if state[r-1][c] == 'x':
                    count+=1
                else:
                    checker=r-1
                    temp_count=0
                    while checker >= 0:
                        if state[checker][c]=='x':
                            count = count+temp_count+1
                            break
                        temp_count+=1
                        checker-=1
            elif r==len(state)-1:
                if state[r-1][c] == 'x':
                    count+=1
                count+=1
            if c>0 and c<len(state[0])-1:
                if state[r][c+1] == 'x':
                    count+=1
                if state[r][c-1] == 'x':
                    count+=1
            elif c==len(state[0])-1:
                if state[r][c-1] == 'x':
                    count+=1
                count+=1
            elif c==0:
                if state[r][c+1]=='x':
                    count+=1
                count+=1
        return count

    def check_column_heights(self,board):
        # column_heights = [ ((len(board)-r) for r in range(len(board)-1, 0, -1) if board[r][c] == "x") for c in range(0, len(board[0]) ) ]
        column_heights = []
        for c in range(0,len(board[0])):
            column_heights.append(max([len(board)-r for r in range(len(board)-1,0,-1) if board[r][c] == 'x'],default=0))
        return column_heights     
    
       
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
            # time.sleep(0.01)
            
            ##Added code
            temp_quintris = AnimatedQuintris()

            self.total_moves = {0:'NoChange',1:'horizontal_flip_and_rotate',2:'rotate_thrice'}
            temp_quintris.piece = store_piece = quintris.piece
            temp_quintris.col = store_col = quintris.col
            temp_quintris.row = store_row  =quintris.row
            temp_quintris.state = store_state = quintris.state
            fringe=[]
            move_string=''

            # print('HEre')
        
            # print('before row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
            # print('here end')

            for count in range(len(self.total_moves)):
                if count==0:
                    for j in range(store_col,len(temp_quintris.state[0][0])-len(max(temp_quintris.piece))+1):
                        if j!=store_col:
                            temp_quintris.right()
                            # temp_quintris
                            move_string+='m'
                        # print('move string is: ',move_string)
                        self.go_down_animated(temp_quintris)
                        # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece)) 
                        fringe.append([self.calculate_cost_animated(temp_quintris,temp_quintris.place_piece(*temp_quintris.state,temp_quintris.piece,temp_quintris.row,temp_quintris.col)[0],temp_quintris.piece,temp_quintris.row,temp_quintris.col),move_string])
                        temp_quintris.row = store_row
                        # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                    
                    self.reset_value(temp_quintris, store_state,temp_quintris.piece,store_row,store_col)
                    move_string=''
                    for j in range(0,store_col):
                        temp_quintris.left()
                        move_string+='b'
                        # print('move string is: ',move_string)
                        self.go_down(temp_quintris)
                        # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                        fringe.append([self.calculate_cost_animated(temp_quintris,temp_quintris.place_piece(*temp_quintris.state,temp_quintris.piece,temp_quintris.row,temp_quintris.col)[0],temp_quintris.piece,temp_quintris.row,temp_quintris.col),move_string])
                        # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                        temp_quintris.row = store_row
                    # print("\n\nAfter the count =0:", fringe)
                
                self.reset_value_animated(temp_quintris, store_state,store_piece,store_row,store_col)

                if count==1:
                    temp_quintris.hflip()
                    if temp_quintris.piece != store_piece:
                        move_string = ''
                        move_string+='h'
                        for j in range(store_col,len(temp_quintris.state[0][0])-len(max(temp_quintris.piece))+1):
                            if j!=store_col:
                                temp_quintris.right()
                                move_string+='m'
                            # print('move string is: ',move_string)
                            self.go_down_animated(temp_quintris)
                            # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                            fringe.append([self.calculate_cost_animated(temp_quintris,temp_quintris.place_piece(*temp_quintris.state,temp_quintris.piece,temp_quintris.row,temp_quintris.col)[0],temp_quintris.piece,temp_quintris.row,temp_quintris.col),move_string])
                            # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                            temp_quintris.row = store_row 
                        self.reset_value_animated(temp_quintris, store_state,temp_quintris.piece,store_row,store_col)

                        move_string = ''
                        move_string+='h'
                        for j in range(0,store_col):
                            temp_quintris.left()
                            move_string+='b'
                            # print('move string is: ',move_string)
                            self.go_down_animated(temp_quintris)
                            # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                            fringe.append([self.calculate_cost_animated(temp_quintris,temp_quintris.place_piece(*temp_quintris.state,temp_quintris.piece,temp_quintris.row,temp_quintris.col)[0],temp_quintris.piece,temp_quintris.row,temp_quintris.col),move_string])
                            # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                            temp_quintris.row = store_row
                        
                        for i in range(3):
                            self.reset_value(temp_quintris, store_state,temp_quintris.piece,store_row,store_col)

                            move_string = ''
                            move_string += 'h'
                            temp_quintris.rotate()
                            move_string += (i+1)*'n'

                            for j in range(store_col,len(temp_quintris.state[0][0])-len(max(temp_quintris.piece))+1):
                                if j!=store_col:
                                    temp_quintris.right()
                                    move_string+='m'
                                # print('move string is: ',move_string)
                                self.go_down_animated(temp_quintris) 
                                # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                                fringe.append([self.calculate_cost_animated(temp_quintris,temp_quintris.place_piece(*temp_quintris.state,temp_quintris.piece,temp_quintris.row,temp_quintris.col)[0],temp_quintris.piece,temp_quintris.row,temp_quintris.col),move_string])
                                # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                                temp_quintris.row = store_row
                        
                            self.reset_value(temp_quintris, store_state,temp_quintris.piece,store_row,store_col)
                            move_string = ''
                            move_string+='h'
                            move_string += (i+1)*'n'
                            for j in range(0,store_col):
                                temp_quintris.left()
                                move_string+='b'
                                # print('move string is: ',move_string)
                                self.go_down_animated(temp_quintris)
                                # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                                fringe.append([self.calculate_cost_animated(temp_quintris,temp_quintris.place_piece(*temp_quintris.state,temp_quintris.piece,temp_quintris.row,temp_quintris.col)[0],temp_quintris.piece,temp_quintris.row,temp_quintris.col),move_string])
                                # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                                temp_quintris.row = store_row
            
                self.reset_value(temp_quintris, store_state,store_piece,store_row,store_col)

                if count==2:
                    for i in range(3):
                        self.reset_value_animated(temp_quintris, store_state,temp_quintris.piece,store_row,store_col)  
                        # print("Quintris value inside the count==2 before the rotation is :",quintris.piece)
                        move_string = ''
                        temp_quintris.rotate()
                        if temp_quintris.piece == store_piece:  
                            # print("You're in rotation flip one and we came across matching result",quintris.piece,store_piece)
                            break
                        move_string += (i+1)*'n'

                        for j in range(store_col,len(temp_quintris.state[0][0])-len(max(temp_quintris.piece))+1):
                            if j!=store_col:
                                temp_quintris.right()
                                move_string+='m'
                            # print('move string is: ',move_string)
                            self.go_down_animated(temp_quintris) 
                            # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                            fringe.append([self.calculate_cost_animated(temp_quintris,temp_quintris.place_piece(*temp_quintris.state,temp_quintris.piece,temp_quintris.row,temp_quintris.col)[0],temp_quintris.piece,temp_quintris.row,temp_quintris.col),move_string])
                            # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                            temp_quintris.row = store_row
                    
                        self.reset_value_animated(temp_quintris, store_state,temp_quintris.piece,store_row,store_col)
                        move_string = ''
                        move_string += (i+1)*'n'

                        for j in range(0,store_col):
                            temp_quintris.left()
                            move_string+='b'
                            # print('move string is: ',move_string)
                            self.go_down_animated(temp_quintris) 
                            # print('row : {} column : {} piece : {}'.format(quintris.row,quintris.col,quintris.piece))
                            fringe.append([self.calculate_cost_animated(temp_quintris,temp_quintris.place_piece(*temp_quintris.state,temp_quintris.piece,temp_quintris.row,temp_quintris.col)[0],temp_quintris.piece,temp_quintris.row,temp_quintris.col),move_string])
                            # quintris.print_state(*quintris.place_piece(*quintris.state,quintris.piece,quintris.row,quintris.col))
                            temp_quintris.row = store_row
        
            
            self.reset_value_animated(temp_quintris, store_state,store_piece,store_row,store_col)
            min_fringe = min(fringe)[1]
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            # quintris.left()
            for i in range(len(min_fringe)+1):
                if i==len(min_fringe):
                    quintris.down()
                    # quintris.finish()
                else:
                    commands[min_fringe[i]]()

           
    def reset_value_animated(self,temp_quintris,state,piece,r,c):
        temp_quintris.state = state
        temp_quintris.piece = piece
        temp_quintris.col = c
        temp_quintris.row = r

    def calculate_cost_animated(self,temp_quintris,state,piece,r,c):
        holes_count = [(self.check_holes(state,r,c),(r,c)) for r in range(len(state)) for c in range(len(state[0]))]
        holes_count_sum = (sum([t1[0] for t1 in holes_count])-65) * 500
        column_heights = self.check_column_heights(state)
        game_over_cost = 0
        if max(column_heights)>=23:
            game_over_cost = 1000000
        column_heights_cost = (max(column_heights) - min(column_heights)) * 1000
        number_of_empty_columns = sum([i==0 for i in column_heights]) * 50
        rows_full= 0
        for r in range(len(state)):
            rows_completed = [state[r][c] == 'x' for c in range(len(state[0]))]
            if sum(rows_completed) == temp_quintris.BOARD_WIDTH:
                rows_full+=1
        total_cost = column_heights_cost + holes_count_sum + (rows_full*-100000) + game_over_cost +number_of_empty_columns 
        return total_cost

        

    def go_down_animated(self,temp_quintris):
        while not temp_quintris.check_collision(*temp_quintris.state,temp_quintris.piece,temp_quintris.row+1,temp_quintris.col):
            temp_quintris.row += 1


    def check_holes_animated(self,state,r,c):
        count=0
        if state[r][c]==' ':
            if r>0 and r<len(state)-1:
                if state[r+1][c] == 'x':
                    count+=1
                if state[r-1][c] == 'x':
                    count+=1
                else:
                    checker=r-1
                    temp_count=0
                    while checker >= 0:
                        if state[checker][c]=='x':
                            count = count+temp_count+1
                            break
                        temp_count+=1
                        checker-=1
            elif r==len(state)-1:
                if state[r-1][c] == 'x':
                    count+=1
                count+=1
            if c>0 and c<len(state[0])-1:
                if state[r][c+1] == 'x':
                    count+=1
                if state[r][c-1] == 'x':
                    count+=1
            elif c==len(state[0])-1:
                if state[r][c-1] == 'x':
                    count+=1
                count+=1
            elif c==0:
                if state[r][c+1]=='x':
                    count+=1
                count+=1
        return count

    def check_column_heights_animated(self,board):
        # column_heights = [ ((len(board)-r) for r in range(len(board)-1, 0, -1) if board[r][c] == "x") for c in range(0, len(board[0]) ) ]
        column_heights = []
        for c in range(0,len(board[0])):
            column_heights.append(max([len(board)-r for r in range(len(board)-1,0,-1) if board[r][c] == 'x'],default=0))
        return column_heights     

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

    ##Added the code below
    player.previous_state=['a','b']
    player.flag = 0
    ##Code added ended
    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



