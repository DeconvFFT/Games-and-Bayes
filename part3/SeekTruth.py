# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import math

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
    for sentence in range(len(data["objects"])):
        new_sentence = ""
        for c in data["objects"][sentence]:
            if c not in punctuations:
                new_sentence = new_sentence + c
        data["objects"][sentence] = new_sentence
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
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    truthful_words = {}
    deceptive_words = {}
    truthful_words_count = 0
    deceptive_words_count = 0
    truthful_sentences_count = 0
    deceptive_sentences_count = 0
    train_data = pre_processing(train_data)
    test_data = pre_processing(test_data)
    all_unique_words = []
    m = 0.5
    for sentence in range(len(train_data["objects"])):
        if train_data["labels"][sentence] == train_data["classes"][0]:
            truthful_sentences_count += 1
            for word in train_data["objects"][sentence].split(" "):
                if word not in all_unique_words:
                    all_unique_words.append(word)
                truthful_words_count += 1
                if word in truthful_words:
                    truthful_words[word] += 1
                else:
                    truthful_words[word] = 1
        else:
            deceptive_sentences_count += 1
            for word in train_data["objects"][sentence].split(" "):
                if word not in all_unique_words:
                    all_unique_words.append(word)
                deceptive_words_count += 1
                if word in deceptive_words:
                    deceptive_words[word] += 1
                else:
                    deceptive_words[word] = 1

    predicted_labels = []
    for sentence in test_data["objects"]:
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
            predicted_labels.append(train_data["classes"][0])
        else:
            predicted_labels.append(train_data["classes"][1])
                    
    return predicted_labels


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

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
