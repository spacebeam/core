# -*- coding: utf-8 -*-

# This file is part of blueberry.


import uuid
import zmq
import logging
import ujson as json

from tornado import gen
from tornado import httpclient as _http_client


_http_client.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
http_client = _http_client.AsyncHTTPClient()


@gen.coroutine
def run_collector(context, port):
    # Socket ro receive messages on
    receiver = context.socket(zmq.PULL)
    custom_port = int(port) + 1
    receiver.bind("tcp://*:{0}".format(custom_port))
    logging.info("Listen PULL collector on tcp://*:{0}".format(custom_port))
    while True:
        m = yield receiver.recv()
        logging.warning(m)
        yield gen.sleep(0.0020)


@gen.coroutine
def run_producer(context, domain, port):
    # Socket to send messages on
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://*:{0}".format(port))
    # Socket with access to the collector: used to syncronize the batch
    collect = context.socket(zmq.PUSH)
    logging.info('Connecting to ZMQ tcp://localhost:{0}'.format(port + 1))
    collect.connect("tcp://localhost:{0}".format(port + 1))
    # 1,2,3 tersting, testing!
    logging.info("Signal the collector to syncronize the batch")
    while True:
        yield collect.send(b'0')

