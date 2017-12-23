import tensorflow as tf
import numpy as np
import pandas as pd
from glob import glob

def getSentenceMatrix(sentence):
    maxSeqLength = 250
    batchSize = 24
    # arr = np.zeros([batchSize, maxSeqLength])
    sentenceMatrix = np.zeros([batchSize,maxSeqLength], dtype='int32')
    split = sentence.split()[:250]
    for i,word in enumerate(split):
        try:
            sentenceMatrix[0,i] = wordsList.index(word)
        except ValueError:
            sentenceMatrix[0,i] = 399999 #Vector for unkown words
    return sentenceMatrix

if __name__ == '__main__':
    numDimensions = 300
    maxSeqLength = 250
    batchSize = 24
    lstmUnits = 64
    numClasses = 2
    iterations = 100000

    """
    Using LSTM that was pre-trained on IMDB reviews.
    """
    wordsList = np.load('../data/training/wordsList.npy').tolist()
    wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8
    wordVectors = np.load('../data/training/wordVectors.npy')

    tf.reset_default_graph()

    labels = tf.placeholder(tf.float32, [batchSize, numClasses])
    input_data = tf.placeholder(tf.int32, [batchSize, maxSeqLength])

    data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype=tf.float32)
    data = tf.nn.embedding_lookup(wordVectors,input_data)

    lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
    lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.25)
    value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)

    weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
    bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
    value = tf.transpose(value, [1, 0, 2])
    last = tf.gather(value, int(value.get_shape()[0]) - 1)
    prediction = (tf.matmul(last, weight) + bias)

    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint('models'))

    """
    Use pre-trained LSTM to predict sentiment of scraped reviews.
    """
    d = '../data/reviews/'
    file_paths = glob(d + 'clean/*.p')
    for doc in file_paths:
        df = pd.read_pickle(doc)
        brand = df['Brand'].values[1]
        inputMatrices = df['Review'].apply(lambda x: getSentenceMatrix(x))
        print(brand, 'inputMatrices done...')
        sentiment = inputMatrices.apply(lambda x: sess.run(prediction, {input_data: x}))
        print(brand, 'sentiment prediction done...')
        df['Sentiment'] = sentiment
        df.to_pickle(d + 'sentiment/' + brand + '_sentiment' + '.p')
        print(brand, 'done...')
