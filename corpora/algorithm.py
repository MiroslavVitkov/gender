#!/usr/bin/python3
"""
Collect tweets from Tweeter.

dependency - available via pip: https://github.com/inueni/birdy
"""


from birdy.twitter import UserClient, StreamClient, BirdyException

from collections import deque
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
        assert len(names.split()) > 1
        return names.split()[-1]
    except:
        return None


def stream_tweets():
    """Twitter's sampling algorithm outputs about 5 000 000 tweets per 24 hours."""
    class Stream:
        def __init__(me):
            me.client = StreamClient(CONSUMER_KEY
                                    ,CONSUMER_SECRET
                                    ,ACCESS_TOKEN
                                    ,ACCESS_TOKEN_SECRET)
            # https://developer.twitter.com/en/docs/tweets/sample-realtime/api-reference/get-statuses-sample
            me.response = me.client.stream.statuses.sample.get()

        def __call__(me):
            for tweet in me.response.stream():
            # For some reason, many tweets are not tagged with a user!
                try:
                    yield tweet, tweet.user
                except:
                    pass

    while True:
        try:
            s = Stream()
            for t, u in s():
                yield t, u
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            pass



class Queue:
    def __init__(me):
        me.q = deque()
        me.size = 0


    def push_left(me, val):
        me.q.appendleft(val)
        me.size = me.size + 1


    def pop_right(me):
        val = me.q.pop()
        me.size = me.size - 1
        return val


    def peek_left(me):
        val = me.q.popleft()
        me.q.appendleft(val)
        return val


    def empty(me):
        return me.size == 0


class UserTimeline:
    """Read up to 3200 most recent tweets per user."""


    TWEETS_PER_FETCH = 50
    UC = UserClient(CONSUMER_KEY
                   ,CONSUMER_SECRET
                   ,ACCESS_TOKEN
                   ,ACCESS_TOKEN_SECRET)


    def __init__(me, screen_name, client=UC):
        me.screen_name = screen_name
        me.queue = Queue()
        me.client = client
        # https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html
        me.request = me.client.api.statuses.user_timeline.get

        response = me.request(screen_name=me.screen_name
                             ,count=me.TWEETS_PER_FETCH)
        for tweet in response.data:
            me.queue.push_left(tweet)


    def __iter__(me):
        return me


    def __next__(me):
        if me.queue.size == 1:
            me._fetch_more()

        if me.queue.empty():
            raise StopIteration

        return me.queue.pop_right()


    def _fetch_more(me):
        tweet = me.queue.peek_left()
        last_id=tweet.id

        response = me.request(screen_name=me.screen_name
                             ,count=me.TWEETS_PER_FETCH
                             ,max_id=last_id-1)

        for tweet in response.data:
            me.queue.push_left(tweet)


class Opts:
    DEFAULT=0
    EMPTY=1
    def __init__(me, type):
        me.female_names='./female'
        me.male_names='./male'
        me.output='./corpus'

        if type == me.DEFAULT:
            me.max_tweets = 200
            me.is_en = True
            me.is_known = True
            me.min_tweets = 10
            me.starts_with= False
            me.is_verified = True

        elif type == me.EMPTY:
            me.max_tweets = 0
            me.is_en = False
            me.is_known = False
            me.min_tweets = 0
            me.starts_with= False
            me.is_verified = False

        else:
            assert(False)

    def __eq__(me, other):
        return me.__dict__ == other.__dict__



def collect_users(opts):
    """Determine eligible twitter users to take part in the survey."""
    m, f = read_names(opts.male_names, opts.female_names)

    def is_en(user):
        return user.lang == 'en'

    def is_known(user):
        n = get_given_name(user.name)
        if get_family_name(user.name) is None:
            return False

        if n in m or n in f:
            return True
        else:
            return False

    def min_tweets(user, min=10):
        return user.statuses_count >= min

    def starts_with(user):
        """Try to exclude people, posing as the opposite gender."""
        try:
            assert (user.name[0] == get_given_name(user.name)[0] or
                    user.name[0] == get_family_name(user.name)[0])
            return True
        except:
            return False

    def is_verified(user):
        return user.verified

    for t, u in stream_tweets():
        if opts.is_en and not is_en(u):
            continue
        if opts.is_known and not is_known(u):
            continue
        if opts.min_tweets and not min_tweets(u):
            continue
        if opts.starts_with and not starts_with(u):
            continue
        if opts.is_verified and not is_verified(u):
            continue

        yield u


def collect_corpus(opts):
    with open(opts.output, 'w') as f:

        users = []
        for user in collect_users(opts):
            if user in users:
                continue
            users.append(user)

            f.write('user = ' + user.name + ',\n')

            count = 0
            for tweet in UserTimeline(user.screen_name):
                if count == opts.max_tweets:
                    break
                f.write('text = ' + tweet.text + ',\n')
                count = count + 1

            print('Wrоте', count, 'tweets by '
                 ,user.name, ', ', user.screen_name, ', ', user.description
                 , '\n')


if __name__ == '__main__':
    opts = Opts(Opts.DEFAULT)
    collect_corpus(opts)
