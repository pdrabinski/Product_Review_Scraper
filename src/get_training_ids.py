import numpy as np
from os import listdir
from os.path import isfile, join
import re

strip_special_chars = re.compile("[^A-Za-z0-9 ]+")

def cleanSentences(string):
    #since I am using the imdb reviews db, this appeared to be the preferred cleaning process
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, "", string.lower())

def numWords(pos, neg):
    num = []
    for review in pos:
        with open(review, "r") as r:
            line=r.readline()
            counter = len(line.split())
            num.append(counter)
    for review in neg:
        with open(review, "r") as r:
            line=r.readline()
            counter = len(line.split())
            num.append(counter)
    return num

if __name__ == '__main__':
    #IMPORT word vectors
    wordsList = np.load('../data/training/wordsList.npy')
    print('word list loaded...')
    wordsList = wordsList.tolist()
    wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8
    wordVectors = np.load('../data/training/wordVectors.npy')
    print ('word vectors loaded...')

    #load training set
    #find files
    pos_reviews_dir = '../data/training/positiveReviews'
    pos_files = [pos_reviews_dir + f for f in listdir(pos_reviews_dir) if isfile(join(pos_reviews_dir,f))]
    neg_reviews_dir = '../data/training/negativeReviews'
    neg_files = [neg_reviews_dir + f for f in listdir(neg_reviews_dir) if isfile(join(neg_reviews_dir,f))]

    numFiles = len(numWords(pos_files, neg_files))
    maxSeqLength=250
    ids = np.zeros((numFiles, maxSeqLength), dtype='int32')
    fileCounter = 0
    for pf in pos_files:
       with open(pf, "r") as f:
           indexCounter = 0
           line=f.readline()
           cleanedLine = cleanSentences(line)
           split = cleanedLine.split()
           for word in split:
               try:
                   ids[fileCounter][indexCounter] = wordsList.index(word)
               except ValueError:
                   ids[fileCounter][indexCounter] = 399999 #Vector for unkown words
               indexCounter = indexCounter + 1
               if indexCounter >= maxSeqLength:
                   break
           fileCounter = fileCounter + 1

    for nf in neg_files:
       with open(nf, "r") as f:
           indexCounter = 0
           line=f.readline()
           cleanedLine = cleanSentences(line)
           split = cleanedLine.split()
           for word in split:
               try:
                   ids[fileCounter][indexCounter] = wordsList.index(word)
               except ValueError:
                   ids[fileCounter][indexCounter] = 399999 #Vector for unkown words
               indexCounter = indexCounter + 1
               if indexCounter >= maxSeqLength:
                   break
           fileCounter = fileCounter + 1
    #Pass into embedding function and see if it evaluates.

    np.save('idsMatrix', ids)
