# Part2: Quintris

## Evaluation function: 
    For evaluation function, I have used a weighted sum of 5 different functions. 
    - Total number of rows cleared
    - Wavyness of the board
    - Total number of holes on the board
    - Number of empty columns on the board
    - Sum of heights of columns on the board

### Total number of rows cleared: 
    This function measuers the number of rows cleared. I try to maximise this function as the more rows we clear, the higher we score.

### Wayvness of the board:
    This function measures the difference between column heights. I try to minimise this function as the less wavy a board is(the smoother the board is), the better our board is.

### Total number of holes on the board:
    This function measures the sum of number of holes per column. A hole is defined as "an empty square surrounded by 'x'  or the floor on it's top, bottom, left and right. If we have holes in the board, we won't be able to place a piece nearby to fill that hole. I try to minimise this function as the less number of holes we have, the better our board is.

### Number of empty columns on the board:
    This function measures the number of columns with no 'x's in it. I try to minimise this function because, if we have more number of empty columns, it might be possible that our board only adds 'x' on one side of the board. I try to minimise this function to ensure we don't have too many empty columns and have a balanced distribution of 'x' among the columns.

## Sum of heights of columns on the board:
    This function measures the sum of heights of all columns. This gives us the total height of the board. I try to minimise this function as the smaller our board, the higher our chances of scoring more.


For expectimax, I consider depth as the level at which a node is. So a tree with one MAX and one CHANCE layer has deoth 2. This simplification helps with the implementation of expetimax.
## Expectimax:
    This version of expectimax works with a game tree of depth 5 . I consider current piece (MAX), successors of current piece (CHANCE), next piece (MAX) and successors of next piece (CHANCE)  and 6 different pieces (MAX) and their successors (CHANCE) layers. The tree is arranged as follows: CURRENT NODE (MAX1) - > 15 X 8 SUCCESSORS (CHANCE1) -> FOR EACH SUCCESSOR, 1 NEXT NODE (MAX2) -> FOR NEXT NODE, 15 X 8 SUCCESSORS (CHANCE2) -> FOR EACH SUCCESSOR, 6 PIECES NODES (MAX3) -> FOR EACH OF THE 6 PIECES, 15 X 8 SUCCESSORS (TERMINAL) NODES.
    For CHANCE1, probability of each successor is 1, because we already know the next piece. For CHANCE2, the probability of each successor is 1/6, since there are 6 different pieces.

## Expectimax small: 
    This version of expectimax works with a game tree of depth 4 . I consider current piece (MAX), successors of current piece (CHANCE), next piece (MAX) and successors of next piece (CHANCE) layers. The tree is arranged as follows: CURRENT NODE (MAX1) - > 15 X 8 SUCCESSORS (CHANCE1) -> FOR EACH SUCCESSOR, 1 NEXT NODE (MAX2) -> FOR NEXT NODE, 15 X 8 SUCCESSORS (TERMINAL).
    For CHANCE1, probability of each successor is 1, because we already know the next piece. 

## Working of the algorithm:
    I generate best possible moves for the current piece based on the board configuration with the maximum evaluation. I have used expectimax small version of expectimax to generate best possible moves because the full expectimax even though gave better moves, took too long to return a valid move. 

## Problems faced:
    - With some configurations of the board, place_piece function adds another column to the board and it makes the column count as 16 instead of 15. For now, I have handled such situations using exception handling. 
    - With some distributions, like repeated sequence of "+" like shapes, too many holes are created on the board and hence I end up getting a lower score.
    - For the expectimax with game depth 5, it took the algorithm a lot of time to generate one correct move and it makes it impossible to use for the animated version (sometimes taking as long as 10 minutes to generate a move) and it was unfeasible to debug as well owing to the size of the search tree.

## Experiments: 
    - I experimented with different values for the weights of evaluation function.  What I observed was, if the values were too far apart like 1000000 for total_rows_cleared and -100 for total_holes, the algorithm tends to give out worse moves.  When the values were close, like 500 for total_rows_cleared and -50 for total_holes, the algorithm tends to give better moves. 