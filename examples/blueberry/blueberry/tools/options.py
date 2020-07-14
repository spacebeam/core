# -*- coding: utf-8 -*-

# This file is part of blueberry.

# Distributed under the terms of the last AGPL License.

__author__ = 'Jean Chassoul'

import os
import tornado.options
from tornado.options import parse_config_file

config_path = 'blueberry.conf'


def options():
    '''
        blueberry configuration options
    '''
    # set config up
    tornado.options.define(
        'config',
        type=str,
        help='path to config file',
        callback=lambda path: parse_config_file(path, final=False))
    # debugging
    tornado.options.define(
        'debug',
        default=False,
        type=bool,
        help=('Turn on autoreload and log to stderr only'))
    # server domain
    tornado.options.define(
        'domain',
        default='*',
        type=str,
        help=('Application domain, e.g: "torchup.org"'))
    # server host
    tornado.options.define(
        'host',
        default='127.0.0.1',
        type=str,
        help=('Server hostname'))
    # server port
    tornado.options.define(
        'port',
        default=57999,
        type=int,
        help=('Server port'))
    # page size
    tornado.options.define(
        'page_size',
        default=297,
        type=int,
        help=('Set a custom page size'))
    # Parse config gile, then command line...
    # so command line switches take precedence
    if os.path.exists(config_path):
        print('Loading %s' % (config_path))
        tornado.options.parse_config_file(config_path)
    else:
        print('No config file at %s' % (config_path))
    tornado.options.parse_command_line()
    result = tornado.options.options
    for required in ('domain', 'host', 'port'):
        if not result[required]:
            raise Exception('%s required' % required)
    return result
