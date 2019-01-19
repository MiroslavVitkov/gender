#!/usr/bin/python3
"""
Collect tweets from Tweeter.
"""


from birdy.twitter import UserClient, StreamClient


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
    print(response.data)


def stream_tweets():
    client = StreamClient(CONSUMER_KEY,
                          CONSUMER_SECRET,
                          ACCESS_TOKEN,
                          ACCESS_TOKEN_SECRET)

    response = client.stream.statuses.filter.post(track='foxnews')
    for data in response.stream():
        print(data)


if __name__ == '__main__':
    stream_tweets()
