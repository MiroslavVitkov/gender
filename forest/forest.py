#!/usr/bin/env python3


"""
"""


import algorithm as corpus

from joblib import dump, load
import numpy as np
import string
import datetime
from scipy.sparse import csr_matrix, lil_matrix
from sklearn.ensemble import RandomForestClassifier as Forest


def log(msg):
    t = datetime.datetime.now().time()
    print(str(t) + ': ' + msg)


def learn_vocabulary(words, counter = [0], known_words={}):
    for w in words:
        if w not in known_words:
            known_words[w] = counter[0]
            counter[0] = counter[0] + 1
    return known_words


log('Reading corpus...')
male, female = corpus.read_names()
users = corpus.read_corpus('corpus')


log('Learning vocabulary...')
known_words = {}
for user in users:
    for tweet in user.tweets:
        tweet = ''.join(tweet)
        known_words = learn_vocabulary(tweet.split())
num_words = len(known_words)


def train():
    log('    Constructing matrix...')
    labels = []
    num_tweets = sum([len(user.tweets) for user in users])

    # Columns are features, rows are observations.
    mat = lil_matrix((num_tweets, num_words), dtype=int)

    row = 0
    for user in users:
        label = corpus.assign_label(user.name.split()[0], male, female)
        log('        user ' + user.name + ', label ' + str(label))
        for tweet in user.tweets:
            for word in tweet.split():
                mat[row,known_words[word]] = mat[row,known_words[word]] + 1
            row = row + 1
            labels.append(label)

    log('    Fitting model...')
    f = Forest()
    f.fit(mat, labels)
    dump(f, 'model')

    return f


f = None
try:
    log('Loading model from file...')
    f = load('model')
    log('    done!')
except:
    log('    failed!')
    log('Training model on input data.')
    f = train()


log('Evaluating model...')
predicted = []
actual = []
users = corpus.read_corpus('corpus_test')
for user in users:
    label = corpus.assign_label(user.name.split()[0], male, female)
    log('    user ' + user.name + ', label ' + str(label))
    for tweet in user.tweets:
#        observation = [[0]*num_words]
        observation = lil_matrix((1, num_words), dtype=int)
        for word in tweet.split():
            if word in known_words:
                observation[0,known_words[word]] = observation[0,known_words[word]] + 1
        p = f.predict(observation)[0]
        predicted.append(p)
        actual.append(label)


predicted = np.array(predicted)
actual = np.array(actual)
print(sum(predicted == actual) / len(predicted))
