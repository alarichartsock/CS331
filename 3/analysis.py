import sys
import re
import numpy as np

def preprocessing(testFile, trainingFile):
    """
    Takes testFile and trainingFile, both are file paths for test/training data.
    Outputs two files with the vocabulary and vectorized data.
    """

    # Processes test and train
    test = processFile(testFile)
    train = processFile(trainingFile)

    # Generates vocabulary with test file as the input
    vocab = generateVocabulary(test)

    # Vectorizes test and train given vocab
    testVector = vectorizeArray(test, vocab)
    trainVector = vectorizeArray(train, vocab)

    # Opens preprocessed_train and test to write to file
    testOutput = open('preprocessed_train.txt', 'w')
    trainOutput = open('preprocessed_test.txt', 'w')

    # Joins vocab array with , and adds classlabel to the end of it
    testOutput.write(",".join(vocab) + ",classlabel\n")
    for i in testVector:
        testOutput.write(str(i) + "\n")

    trainOutput.write(",".join(vocab) + ",classlabel\n")
    for i in trainVector:
        trainOutput.write(str(i) + "\n")

    # Closes file write methods
    testOutput.close()
    trainOutput.close()

    # Returns testVectgor, trainVector, and Vocab in a tuple
    return (testVector, trainVector, vocab)


def vectorizeArray(data, vocab):
    """
    Vectorizes data with the vocab array. 
    Returns an array of vectors, each corresponding to a sentence.
    """

    arrays = []
    # For each sentence in data, separate classifier and the sentence.
    for sentence in data:
        classified = sentence[1]
        sentence = sentence[0]
        array = []
        # For each definition in vocab, find if the sentence contains it.
        # If it does, then append a 1 to that spot. If it doesn't then append a 0
        for definition in vocab:
            found = False
            for word in sentence:
                if word == definition:
                    found = True

            if found:
                array.append(1)
            else:
                array.append(0)
        # Append classifier to end of array
        array.append(classified)

        # Append array to the arrays variable
        arrays.append(array)

    # Return all arrays
    return arrays


def generateVocabulary(data):
    """
    Generates a unique set of words sorted alphabetically derived from the training data.
    """
    vocab = []

    # For i in data, append to vocab if it doesn't already exist in vocab
    for i in data:
        i = i[0]
        for j in i:
            if j in vocab:
                pass
            else:
                vocab.append(j)

    # Sort vocab (done alphabetically)
    vocab = sorted(vocab)

    # Return vocab for futher usage
    return vocab


def processFile(file):
    """
    Takes file and slices it into sentences between newlines. 
    Then sends these individual sentences to be procesed by sentenceProcessing
    Returns a list of processed arrays. 
    """
    test = open(file, 'r')  # turns file input into a list I can work with
    input = test.read().split('\n')

    ret = []
    for i in input:
        if len(i) > 0:
            ret.append(sentenceProcessing(i))

    return ret


def sentenceProcessing(sent):
    """
    Takes sentence
    Processing: splits sentence into words, removes and stores classifier, removes non letters and replaces with blank strings, removes blank strings
    Returns a tuple with the processed input and classifier
    """
    input = sent.split(' ') # Splits sentence into words

    input = list(filter(None, input))

    classified = int(input.pop()) # Removes and stores classifier

    for i in range(len(input)):
        input[i] = input[i].lower()
        regex = re.compile('[^a-zA-Z]')
        input[i] = regex.sub('', input[i]) # Removes non letters and replaces with blank strings

    try: 
        input.remove("") # Removes blank strings
    except ValueError: # Handles edge case of blank strings not existing
        pass

    return (input, classified)


def classification(input):
    """Not currently implemented."""
    raise NotImplementedError


def main():
    if len(sys.argv) > 1:
        """Takes two arguments, testset and trainingset. 
        Both are text files and are passed to preprocessing for processing."""
        try:
            testSet = sys.argv[1]
        except IndexError:
            print(
                "Please provide arguments in the format of python analysis.py [testset] [trainingset]")
            raise Exception("Error: Please provide an argument ")

        try:
            trainingSet = sys.argv[2]
        except IndexError:
            print(
                "Please provide arguments in the format of python analysis.py [testset] [trainingset]")
            raise Exception("Error: Please provide an argument ")
    else:
        print("Please provide an argument ")

    process = preprocessing(testSet, trainingSet)


main()
