# -*- coding: utf-8 -*-

# This file is part of blueberry.


import uuid
import logging

from functools import partial
from zmq.eventloop.future import Context
from zmq.eventloop.ioloop import IOLoop

from tornado import ioloop
from tornado import gen, web

from blueberry.tools import options
from blueberry.tools import zstreams


class StatusHandler(web.RequestHandler):

    def initialize(self, **kwargs):
        '''
            Initialize the base handler
        '''
        super(StatusHandler, self).initialize(**kwargs)
        # Page settings
        self.page_size = self.settings.get('page_size')
        # Application domain
        self.domain = self.settings.get('domain')

    def set_default_headers(self):
        '''
            default headers
        '''
        self.set_header("Access-Control-Allow-Origin",
                        self.settings.get('domain', '*'))

    @gen.coroutine
    def get(self):
        message = {'ping':'pong'}
        self.set_status(200)
        self.finish(message)


@gen.coroutine
def run(domain, port):
    context = Context()
    yield zeromq.run_producer(context, domain, port)


def main():
    '''
        Blueberry main function
    '''
    # daemon options
    opts = options.options()
    # Our system uuid
    system_uuid = uuid.uuid4()
    # System spawned
    logging.info('Blueberry system {0} spawned'.format(system_uuid))
    # HTTP daemon application
    application = web.Application(
        [
            (r'/status/?', StatusHandler),    
        ],
        debug=opts.debug,
        domain=opts.domain,
        page_size=opts.page_size,
    )
    # Listen daemon on port
    application.listen(opts.port)
    logging.info('Listen on http://{0}:{1}'.format(opts.host, opts.port))
    # Setting up the ZeroMQ integration
    IOLoop.current().spawn_callback(
        partial(run, opts.domain, opts.stream_port, )
    )
    # Start the eventloop
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    '''
        Just when I thought I was out, they pull me back in!
    '''
    main()
