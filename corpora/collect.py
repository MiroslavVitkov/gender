#!/usr/bin/python3
"""
Collect tweets from Tweeter.

dependency - available via pip: https://github.com/inueni/birdy
"""


from birdy.twitter import UserClient, StreamClient

import string


# Not a secret any more!
CONSUMER_KEY = 'mS4tzhkekNhpQXuJGAv2MwWWL'
CONSUMER_SECRET = 'NReza0C8h52nD7Bj9vsrPqUwW1xPOYIh4acBONoSLYaGVHVvSc'
ACCESS_TOKEN = '1085578386368536576-hi7jWx1vnsZfRUkUmZEXgnSuruyDgM'
ACCESS_TOKEN_SECRET = 'UvzxhF32XpUAEeqbLkpU99xAjk8nn6iVVmlTXZytFeD6i'


def read_names(male='./male', female='./female'):
    """Read in a list male names and a list of female names."""
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


def get_given_name(screen_name):
    try:
        for word in screen_name.split():
            assert word.isalpha()
            assert word[0] in string.ascii_uppercase
        return namestring.split()[0]
    except:
        return None


def stream_tweets():
    """Twitter's sampling algorithm outputs about 5 000 000 tweets per 24 hours."""
    client = StreamClient(CONSUMER_KEY,
                          CONSUMER_SECRET,
                          ACCESS_TOKEN,
                          ACCESS_TOKEN_SECRET)

    # https://developer.twitter.com/en/docs/tweets/sample-realtime/api-reference/get-statuses-sample
    response = client.stream.statuses.sample.get()
    for tweet in response.stream():
        # For some reason, many tweets are not tagged with a user!
        try:
            yield tweet, tweet.user
        except:
            pass


def get_user_timeline(screen_name='MiroslavVitkov'):
    """Reads the last 3200 tweets by a user."""
    client = UserClient(CONSUMER_KEY,
                        CONSUMER_SECRET,
                        ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET)

    # https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html
    response = client.api.statuses.user_timeline.get(screen_name=screen_name)
    return response.data


def kur():
    m, f = read_names()

    for t, u in stream_tweets():
        if u.lang == 'en':
            if get_given_name(u.name) in m:
                    print('name: ', u.name, ', scrn: ', u.screen_name, ', lang: ', u.lang)



if __name__ == '__main__':
    tweets = get_user_timeline()
    print(tweets)
    #kur()
#    stream_tweets_by2()
