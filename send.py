#!/usr/bin/env python
'''
Simple sender.

Sends messages over a specific port to a host at periodic intervals.

Here is an example that sends messages to recv_host on port 8500.

   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ send.py --host recv_host --port 8500

Here is what you would run on the recv_host:

   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ recv.py --host 0.0.0.0 --port 8500
'''
import argparse
import datetime
import inspect
import json
import os
import random
import socket
import string
import sys
import time


VERSION = '1.0.1'


def infov(opts, msg, lev=1):
    '''
    Print a verbose message.
    '''
    if opts.verbose > 0:
        print('INFO:{} {}'.format(inspect.stack()[lev][2], msg))


def getopts():
    '''
    Process the command line arguments.
    '''
    # Trick to capitalize the built-in headers.
    # Unfortunately I can't get rid of the ":" reliably.
    def gettext(s):
        lookup = {
            'usage: ': 'USAGE:',
            'positional arguments': 'POSITIONAL ARGUMENTS',
            'optional arguments': 'OPTIONAL ARGUMENTS',
            'show this help message and exit': 'Show this help message and exit.\n ',
        }
        return lookup.get(s, s)

    argparse._ = gettext  # to capitalize help headers
    base = os.path.basename(sys.argv[0])
    name = os.path.splitext(base)[0]
    usage = '\n  {0} [OPTIONS] <DOT_FILE>'.format(base)
    desc = 'DESCRIPTION:{0}'.format('\n  '.join(__doc__.split('\n')))
    epilog = r'''EXAMPLES:
   # Example 1: help
   $ {0} -h

   # Example 2: simple send
   $ {0}

   # Example 3: send at 2 second intervals.
   $ {0} -t 2

   # Example 4: increase the send packet size.
   #            you would probably want to increase the size for the
   #            receiver as well.
   $ {0} -s 4096

   # Example 5: specify the host and port explicitly.
   $ {0} -H other_host -p 8601
 '''.format(base)
    afc = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=afc,
                                     description=desc[:-2],
                                     usage=usage,
                                     epilog=epilog)

    parser.add_argument('-H', '--host',
                        action='store',
                        type=str,
                        default='127.0.0.1',
                        metavar=('HOST'),
                        help='''The host.
Default %(default)s.
 ''')

    parser.add_argument('-p', '--port',
                        action='store',
                        type=int,
                        default=8500,
                        metavar=('PORT'),
                        help='''The port.
Default %(default)s.
 ''')

    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='''Don't display the messages as they are received.
 ''')

    parser.add_argument('-s', '--size',
                        action='store',
                        type=int,
                        default=32,
                        metavar=('SIZE'),
                        help='''Send packet data size.
Default %(default)s.
 ''')

    parser.add_argument('-r', '--rsize',
                        action='store',
                        type=int,
                        default=1024,
                        metavar=('SIZE'),
                        help='''The response packet data size.
Default %(default)s.
 ''')

    parser.add_argument('-t', '--time',
                        action='store',
                        type=float,
                        default=1,
                        metavar=('SECONDS'),
                        help='''The time to pause between send operations.
Default %(default)s.
 ''')

    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='''Increase the level of verbosity.
 ''')

    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s version {0}'.format(VERSION),
                        help="""Show program's version number and exit.
 """)

    opts = parser.parse_args()
    return opts


def create_record(opts):
    '''
    Create a record to send.
    '''
    infov(opts, 'create record with {} bytes of data'.format(opts.size))
    data = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(opts.size))
    rec = {'data': data, 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),}
    json_rec = json.dumps(rec)
    return json_rec.encode('ascii')


def send(opts, rec):
    '''
    Send the record.
    '''
    infov(opts, 'sending {}'.format(rec))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (opts.host, opts.port)
    if not opts.quiet:
        print('SND: {}  {}'.format(addr, rec))
    try:
        sock.connect(addr)
        sock.sendall(bytes(rec))
        response = sock.recv(opts.rsize)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except socket.error:  # need to change this for Python 3
        pass  # we don't care if there is no listener


def main():
    '''
    Main send loop.
    '''
    opts = getopts()
    try:
        while True:
            rec = create_record(opts)
            send(opts, rec)
            time.sleep(opts.time)
    except KeyboardInterrupt:
        print('')
    infov(opts, 'done')


if __name__ == '__main__':
    main()
