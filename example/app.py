#!/usr/bin/env python2.7
# -`*- coding: utf-8 -*-

"""
test for Server-Side events in flask

inspiration from:
http://www.html5rocks.com/en/tutorials/eventsource/basics/
https://github.com/niwibe/sse.git
https://github.com/niwibe/django-sse.git
https://github.com/jkbr/chat
"""

from gevent import monkey
monkey.patch_all()

import flask
app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'asdf'

import redis
red = redis.Redis()

import os
import sys
dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(dir, '..')))

from sse import PeriodicStream, RedisSseStream
import random


def numGen():
    prev = 50
    while True:
        vals = [prev]
        vals.append(prev + random.randrange(-10, 10))
        vals.append(prev + random.randrange(-20, 20))
        vals.append(prev + random.randrange(-30, 30))
        vals.append(prev + random.randrange(-40, 40))
        prev = vals[-1]
        if prev > 100:
            prev = 100
        if prev < 0:
            prev = 0
        for i in vals:
            yield i


numgen = numGen()
numgen2 = numGen()


def ping(subscriber, freq):
    "Alternate between sending 'PING' and 'PONG' messages"

    if (subscriber.counter / freq) % 2 == 0:
        subscriber.sse.add_message("PING", event='ping')
    else:
        subscriber.sse.add_message("PONG", event='ping')


def foo(subscriber, freq):
    subscriber.sse.add_message(numgen2.next(), event='graph')


def data_points(subscriber):
    subscriber.sse.add_message(red.get('nextval'), event='graph')


app.add_url_rule('/stream/periodic',
    view_func=PeriodicStream.as_view(str('PeriodicStream'),
        {'foo': (1, foo), 'ping': (10, ping)}))

app.add_url_rule('/stream/redis',
    view_func=RedisSseStream.as_view(str('RedisSseStream'),
        {'graphvals': data_points},
        red.pubsub()))


@app.route('/graph')
def visit():
    nextval = numgen.next()
    red.set('nextval', nextval)
    red.publish('stream', 'graphvals')
    return '<!doctype html><head><body>%d</body></html>' % nextval


@app.route('/')
def home():
    return flask.render_template('home.html')


if __name__ == '__main__':
    app.run()
