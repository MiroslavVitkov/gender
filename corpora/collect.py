#!/usr/bin/python3
"""
Collect tweets from Tweeter.

depends: https://github.com/inueni/birdy
"""


from birdy.twitter import UserClient, StreamClient

import string


CONSUMER_KEY = 'mS4tzhkekNhpQXuJGAv2MwWWL'
CONSUMER_SECRET = 'NReza0C8h52nD7Bj9vsrPqUwW1xPOYIh4acBONoSLYaGVHVvSc'
ACCESS_TOKEN = '1085578386368536576-hi7jWx1vnsZfRUkUmZEXgnSuruyDgM'
ACCESS_TOKEN_SECRET = 'UvzxhF32XpUAEeqbLkpU99xAjk8nn6iVVmlTXZytFeD6i'


def querry_user():
    client = UserClient(CONSUMER_KEY,
                        CONSUMER_SECRET,
                        ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET)

    response = client.api.users.show.get(screen_name='twitter')
    # resource = client.userstream.user.get()
    print(response.data)


def stream_tweets_by(user='foxnews'):
    client = StreamClient(CONSUMER_KEY,
                          CONSUMER_SECRET,
                          ACCESS_TOKEN,
                          ACCESS_TOKEN_SECRET)

    response = client.stream.statuses.filter.post(track=user)
    for data in response.stream():
        print(data)


def stream_all_tweets():
    client = StreamClient(CONSUMER_KEY,
                          CONSUMER_SECRET,
                          ACCESS_TOKEN,
                          ACCESS_TOKEN_SECRET)

    # https://developer.twitter.com/en/docs/tweets/sample-realtime/api-reference/get-statuses-sample
    response = client.stream.statuses.sample.get()
    for tweet in response.stream():
        # For some reason, many tweets are not tagged with a user!
        try:
            u = tweet.user
            #print('name: ', u.name, ', scrn: ', u.screen_name, ', lang: ', u.lang)
            yield tweet, u
        except:
            pass


def read_names(male='male', female='female'):
    def to_list(fname):
        with open(fname) as f:
            l = f.readlines()
            l = [x.strip() for x in l]
            return l

    m = to_list(male)
    f = to_list(female)

    assert len(list(set(m).intersection(f))) == 0
    assert len(m) == len(f)

    return m, f


def is_proper_name(str):
    for word in str.split():
        if not word.isalpha():
            return False
        if word[0] not in string.ascii_uppercase:
            return False
    return True


def get_given_name(namestring):
    try:
        for word in namestring.split():
            assert word.isalpha()
            assert word[0] in string.ascii_uppercase
        return namestring.split()[0]
    except:
        return None

if __name__ == '__main__':
    m, f = read_names()
    for t, u in stream_all_tweets():
        if u.lang == 'en':
            if get_given_name(u.name):
                if u.name.split()[0] in m:
                    print('name: ', u.name, ', scrn: ', u.screen_name, ', lang: ', u.lang)
