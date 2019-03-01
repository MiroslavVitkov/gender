#!/usr/bin/env python3


"""
"""


import algorithm as corpus

from sklearn.ensemble import RandomForestClassifier as Forest



male, female = corpus.read_names()
users = corpus.read_corpus()


def embed(text, known_words={}):
    ret = []
    counter = 0
    for word in text.split():
        if word not in known_words:
            known_words[word] = counter
            counter = counter + 1

        ret.append(known_words[word])

    assert len(ret) == len(text.split())
    return ret


def learn_vocabulary(words, counter, known_words={}):
    for w in words.split():
        known_words[w] = counter
        counter = counter + 1
    return known_words, counter


known_words = {}
for user in users:
    counter = 0
    for tweet in user.tweets:
        known_words, counter = learn_vocabulary(tweet.split(), counter, known_words)


tweets = []
labels = []
for user in users:
    label = corpus.assign_label(user.name, male, female)
    for tweet in user.tweets:
        encoded = embed(tweet, known_words)
        tweets.append(encoded)
        labels.append(label)


print(tweets[7])


f = Forest()



all = [t[0] for t in tweets]
f.fit(all, labels)
