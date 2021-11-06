# <div align="center"> CS B551 - Assignment 2: Games and Bayesian Classifiers
#####  <div align="center"> CSCI B551 - Elements of Artificial Intelligence!

<br>

##### Team-member 1: Ganapathy, Anitha (aganapa) <br>
##### Team-member 2: Mehta, Saumya Hetalbhai (mehtasau) <br>
##### Team-member 3: Monshizadeh, Mahsa (mmonshiz) <br>

<br>
---

# Part1: Raichu (Anitha)

##### [Raichu] (https://github.iu.edu/cs-b551-fa2021/mmonshiz-aganapa-mehtasau-a2/blob/master/part1)

Raichu is a popular childhood game played on an n x n grid (where n = 8 is an even number) with three kinds of pieces (Pichus, Pikachus, and Raichus) of two different colors (black and white). This game is similar to the game of checkers we all have loved and grown up playing the game.

### AIM
***To take on as many opponents pawns as possible and get our raichu to play an optimum game.***

## Input
Initially the board starts empty, except for a row of white Pikachus on the second row of the board, a row of white Pichus on the
third row of the board, and a row of black Pichus on row n - 2 and a row of black Pikachus on row n - 1:

we assume the White player to be the max player.

## Solution

I have implemented the Minimax algorithm with alpha beta pruning and implemented the the depth level being pre determined.


## Evaluation function:
- I have considered the remaining pawns on the board and assigned the pawn values as pichu = 1, pikachu = 3, raichu = 11.
- Final evaluation , I have subtracted the scores of ot the players.
- Positive values means max player has the advantage , negative values means the min players has the advantage.

## Problems faced:
- I faced a lot of problem in abstraction of the parts of the codes that can be reused for every pawns(pichus, pikachus and raichus)
- the assignment of which player goes next to calculate the max value for the max player and min value for the min player in the minimax algorithm.

## Experiments
- I have written an helper code file, which helps me to visualize the old board and new board display in a matrix format.
- This helped me to see if the move the AI made was a right one and if there was a need to optimize the code.

## References:

- I found this video to be very useful interms of understanding the algorithm and class course work very helpful in implementation.
- **https://www.youtube.com/watch?v=l-hh51ncgDI&t=573s**

---
# Part 2: The Game of Quintris (Saumya)

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
   
---   
   
## Part3: Truth be Told (Mahsa)
### (1) a description of how you formulated each problem; (2) a brief description of how your program works; 

I use the naive bayse and assume that the probabbilty of each word given a lablel are independent from each other. So the parobabilty of the truthful/deceptive given words of the sentence (which we call posterior) is proportional to probabilty of all the words given truthful/deceptive (and we assume that all are independent give label (which is our likelihood) so we can write it as a product of the probabilities of each word given label) times the probabilty of truthful/deceptive. (we are ignoring the denominator P(review_words) in Bayes rule, because it is the same for both labels. ) 

The calculation of the likelihood of different class values involves multiplying a lot of small numbers together. This can lead to an underflow of numerical precision.Therefore I used log for calculation.

It is possible to see some words in the test which we didn't see in the train set so the probability of that word given label will be zero. To handel this I used Dirichlet prior and I used small number (By experience I understand that it should be a number more than and les than or equal to 1). I used cross validation on my dataset and write a code name optimizer whih you can see in in part3 folder and figure out the best number for my dirichlet prior. ( I have a plot name optimizer.png to find the best value for my drichlet prior)

I have a preprocessing function too. It remoces the punctuations from the sentences.

To run the code the only thing you need to do is to write "python3 ./SeekTruth.py deceptive.train.txt deceptive.test.txt" in you command line.

The accuracy for this part is 86%.


### (3) and discussion of any problems you faced, any assumptions, simplifications,
and/or design decisions you made.

I have not faced any issues. But my preprocessing part was so simple so if we do some more advanced preprocessing we will get better accuracy. Also, it may be helpful to ignore tokens that do not occur more than a handful of times (as it said in the assignment pdf); Since the TA told me that my accuracy os well enough so I did ot do them.
