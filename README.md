# a2
## Part3 Mahsa
### (1) a description of how you formulated each problem; (2) a brief description of how your program works; 

I use the naive bayse and assume that the probabbilty of each word given a lablel are independent from each other. So the parobabilty of the truthful/deceptive given words of the sentence (which we call posterior) is proportional to probabilty of all the words given truthful/deceptive (and we assume that all are independent give label (which is our likelihood) so we can write it as a product of the probabilities of each word given label) times the probabilty of truthful/deceptive. 

The calculation of the likelihood of different class values involves multiplying a lot of small numbers together. This can lead to an underflow of numerical precision.Therefore I used log for calculation.

It is possible to see some words in the test which we didn't see in the train set so the probability of that word given label will be zero. To handel this I used Dirichlet prior and I used small number (By experience I understand that it should be a number more than and les than or equal to 1). I used cross validation on my dataset and write a code name optimizer whih you can see in in part3 folder and figure out the best number for my dirichlet prior. ( I have a plot name optimizer.png to find the best value for my drichlet prior)

I have a preprocessing function too. It remoces the punctuations from the sentences.

To run the code the only thing you need to do is to write "python3 ./SeekTruth.py deceptive.train.txt deceptive.test.txt" in you command line.

The accuracy for this part is 86%.


### (3) and discussion of any problems you faced, any assumptions, simplifications,
and/or design decisions you made.

I have not faced any issues. But my preprocessing part was so simple so if we do some more advanced preprocessing we will get better accuracy. Also, it may be helpful to ignore tokens that do not occur more than a handful of times (as it said in the assignment pdf); Since the TA told me that my accuracy os well enough so I did ot do them.