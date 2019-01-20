#!/usr/bin/python3
"""
Collect tweets from Tweeter.

depends: https://github.com/inueni/birdy
"""


from birdy.twitter import UserClient, StreamClient

import string


# Not a secret any more!
CONSUMER_KEY = 'mS4tzhkekNhpQXuJGAv2MwWWL'
CONSUMER_SECRET = 'NReza0C8h52nD7Bj9vsrPqUwW1xPOYIh4acBONoSLYaGVHVvSc'
ACCESS_TOKEN = '1085578386368536576-hi7jWx1vnsZfRUkUmZEXgnSuruyDgM'
ACCESS_TOKEN_SECRET = 'UvzxhF32XpUAEeqbLkpU99xAjk8nn6iVVmlTXZytFeD6i'


def stream_all_tweets():
    client = StreamClient(CONSUMER_KEY,
                          CONSUMER_SECRET,
                          ACCESS_TOKEN,
                          ACCESS_TOKEN_SECRET)

    # https://developer.twitter.com/en/docs/tweets/sample-realtime/api-reference/get-statuses-sample
#    response = client.stream.statuses.sample.get()
    response = client.stream.statuses.user_timeline.post(user='MiroslavVitkov')
    for tweet in response.stream():
        # For some reason, many tweets are not tagged with a user!
        try:
            u = tweet.user
            #print('name: ', u.name, ', scrn: ', u.screen_name, ', lang: ', u.lang)
            yield tweet, u
        except:
            pass


def stream_tweets_by(user='MiroslavVitkov'):
    client = UserClient(CONSUMER_KEY,
                        CONSUMER_SECRET,
                        ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET)

#    response = client.api.users.show.get(screen_name='twitter')
    response = client.api.statuses.user_timeline.get(screen_name='twitter')
    print(response.data)


    import sys
    sys.exit()


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


def get_given_name(namestring):
    try:
        for word in namestring.split():
            assert word.isalpha()
            assert word[0] in string.ascii_uppercase
        return namestring.split()[0]
    except:
        return None


def user_has_enough_tweets(username='MiroslavVitkov', min_tweets=10):
    # how do I get all tweets of a user??
    pass


if __name__ == '__main__':
    stream_tweets_by('foxnews')

    m, f = read_names()
    for t, u in stream_all_tweets():
        if u.lang == 'en':
            if get_given_name(u.name):
                if u.name.split()[0] in m:
                    print('name: ', u.name, ', scrn: ', u.screen_name, ', lang: ', u.lang)
