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


def get_given_name(names):
    try:
        for n in names.split():
            assert n.isalpha()
            assert n[0] in string.ascii_uppercase
        return names.split()[0]
    except:
        return None


def get_family_name(names):
    try:
        assert get_given_name(names) is not None
        assert len(names) > 1
        return names.split()[-1]
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


def collect_users():
    """Determine eligible twitter users to take part in the survey."""
    m, f = read_names()

    def is_en(user):
        return user.lang == 'en'

    def is_known(user):
        n = get_given_name(user.name)
        if n in m or n in f:
            return True
        else:
            return False

    def has_tweets(user, min=10):
        tweets = get_user_timeline(user.screen_name)
        return len(tweets) >= min

    def starts_with(user):
        """Try to exclude people, posing as the opposite gender."""
        try:
            return True
            assert (user.name[0] == get_given_name(user.name)[0] or
                    user.name[0] == get_family_name(user.name)[0])
            return True
        except:
            return False

    for t, u in stream_tweets():
        if is_en(u) and is_known(u) and has_tweets(u) and starts_with(u):
            print(u.name)
            yield u


def collect_corpus():
    with open('corpus', 'w') as f:

        for user in collect_users():
            f.write('user = ' + user.name + ',\n')

            for tweet in get_user_timeline(user.screen_name):
                f.write('text = ' + tweet.text + ',\n')


if __name__ == '__main__':
    collect_corpus()
