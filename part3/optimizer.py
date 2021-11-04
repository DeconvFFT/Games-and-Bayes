# SeekTruth.py : Classify text objects into two categories
#
# Mahsa Monshizadeh 2000757990
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


def pre_processing(data):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for sentence in range(len(data)):
        new_sentence = ""
        for c in data[sentence]:
            if c not in punctuations:
                new_sentence = new_sentence + c
        data[sentence] = new_sentence
    return data

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#


def classifier(cross_train, cross_trainR, cross_test, m):
    # This is just dummy code -- put yours here!
    truthful_words = {}
    deceptive_words = {}
    truthful_words_count = 0
    deceptive_words_count = 0
    truthful_sentences_count = 0
    deceptive_sentences_count = 0
    train_data = pre_processing(cross_train)
    test_data = pre_processing(cross_test)
    all_unique_words = []
    
    for sentence in range(len(train_data)):
        if cross_trainR[sentence] == "truthful":
            truthful_sentences_count += 1
            for word in train_data[sentence].split(" "):
                if word not in all_unique_words:
                    all_unique_words.append(word)
                truthful_words_count += 1
                if word in truthful_words:
                    truthful_words[word] += 1
                else:
                    truthful_words[word] = 1
        else:
            deceptive_sentences_count += 1
            for word in train_data[sentence].split(" "):
                if word not in all_unique_words:
                    all_unique_words.append(word)
                deceptive_words_count += 1
                if word in deceptive_words:
                    deceptive_words[word] += 1
                else:
                    deceptive_words[word] = 1

    predicted_labels = []
    for sentence in test_data:
        Prob_of_truthful_given_sentence = math.log(truthful_sentences_count/(truthful_sentences_count + deceptive_sentences_count))
        Prob_of_deceptive_given_sentence = math.log(deceptive_sentences_count/(truthful_sentences_count + deceptive_sentences_count))
        for word in sentence.split(" "):
            if word not in truthful_words:
                Prob_of_truthful_given_sentence += math.log(m/(truthful_words_count + m*len(all_unique_words)))
            else:
                Prob_of_truthful_given_sentence += math.log((m+truthful_words[word])/(truthful_words_count + m*len(all_unique_words)))
            
            if word not in deceptive_words:
                Prob_of_deceptive_given_sentence += math.log(m/(deceptive_words_count + m*len(deceptive_words)))
            else:
                Prob_of_deceptive_given_sentence += math.log((m+deceptive_words[word])/(deceptive_words_count + m*len(deceptive_words)))

        if Prob_of_truthful_given_sentence > Prob_of_deceptive_given_sentence:
            predicted_labels.append("truthful")
        else:
            predicted_labels.append("deceptive")

    return predicted_labels

def accur(cross_train, cross_trainR, cross_test, cross_testR, m):
    results= classifier(cross_train, cross_trainR, cross_test, m)
    correct_ct = sum([ (results[i] == cross_testR[i]) for i in range(0, len(cross_testR))])
    return 100.0 * correct_ct / len(cross_testR)


def cross_validation(train_data):
    n = len(train_data["objects"])
    phi = np.array(train_data["objects"])
    t = np.array(train_data["labels"])
    # p = np.random.permutation(n)
    # phi, t = phi[p], t[p]
    p = np.random.permutation(len(phi))
    phi, t = phi[p], t[p]
    train = phi[:(2*n)//3]
    trainR = t[:(2*n)//3]
    test = phi[(2*n)//3:]
    testR = t[(2*n)//3:]

    length = len(train)
    m_accuracies = []
    for m in np.arange(0.1, 1.1, 0.1):
        accuracy = []
        for i in range(10):
            if i == 0:
                cross_train = train[(i+1)*length//10:]
                cross_trainR = trainR[(i+1)*length//10:]
            elif i == 9:
                cross_train = train[:i*length//10]
                cross_trainR = trainR[:i*length//10]
            else:
                cross_train = np.concatenate((train[:i*length//10],train[(i+1)*length//10:]))
                cross_trainR = np.concatenate((trainR[:i*length//10],trainR[(i+1)*length//10:]))
            cross_test = train[i*length//10:(i+1)*length//10]
            cross_testR = trainR[i*length//10:(i+1)*length//10]
            acc = accur(cross_train, cross_trainR, cross_test, cross_testR, m)
            accuracy.append(acc)

        avg_acc = 0
        for a in accuracy:
            avg_acc += a
        m_accuracies.append(avg_acc/10)
    best_m = 0
    best_accuracy = 0
    for i in range(len(m_accuracies)):
        if m_accuracies[i]>best_accuracy:
            best_m = i/10 + 0.1
            best_accuracy= m_accuracies[i]
    return m_accuracies, best_accuracy, best_m


def plot(m_accuracies):
    m = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    plt.plot(m, m_accuracies) 
    plt.xlabel("m")
    plt.ylabel("accuracy")
    plt.title("accuracy respect to m")
    plt.savefig("optimizer.png")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    m_accuracies, best_accuracy, best_m = cross_validation(train_data)

    plot(m_accuracies)
