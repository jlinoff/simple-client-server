#!/usr/bin/env python
'''
Simple receiver.

Receives messages send by the send.py program at periodic intervals.

Here is an example that receives messages from any IPv4 address on
port 8500.

   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ recv.py --host 0.0.0.0 --port 8500

It will receive data sent by this command.

   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ send.py --host 127.0.0.1 --port 8500
'''
import argparse
import inspect
import json
import os
import socket
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

   # Example 2: simple receive
   $ {0}

   # Example 3: poll at 2 second intervals.
   $ {0} -t 2

   # Example 4: increase the receive packet size.
   #            you would probably want to increase the size for the
   #            sender as well.
   $ {0} -s 4096

   # Example 5: specify the host and port explicitly.
   $ {0} -H other_host -p 8601
 '''.format(base)
    afc = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=afc,
                                     description=desc[:-2],
                                     usage=usage,
                                     epilog=epilog)

    parser.add_argument('-b', '--backlog',
                        action='store',
                        type=int,
                        default=5,
                        metavar=('NUMBER'),
                        help='''The socket listen backlog.
Default: %(default)s.
 ''')

    parser.add_argument('-H', '--host',
                        action='store',
                        type=str,
                        default='0.0.0.0',
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
                        default=1024,
                        metavar=('SIZE'),
                        help='''Receive packet size.
Default %(default)s.
 ''')

    parser.add_argument('-t', '--time',
                        action='store',
                        type=float,
                        default=0.200,
                        metavar=('SECONDS'),
                        help='''The time to pause between receive operations.
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


def create_listener(opts):
    '''
    Create the listener.
    '''
    infov(opts, 'creating the listener')
    sock_addr = (opts.host, opts.port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(sock_addr)
    sock.listen(opts.backlog)
    return sock


def receive_recs(opts):
    '''
    Poll for records.
    '''
    infov(opts, 'receiving records')
    listener = create_listener(opts)
    while True:
        conn, addr = listener.accept()
        json_rec = conn.recv(1024)
        rec = json.loads(json_rec.decode('utf-8'))  # same format as sender
        if not opts.quiet:
            print('RCV: {}  {}  {}'.format(addr, rec['time'], rec['data']))
        conn.close()
        time.sleep(opts.time)


def main():
    '''
    Main receive loop.
    '''
    opts = getopts()
    try:
        receive_recs(opts)
    except KeyboardInterrupt:
        print('')
    infov(opts, 'done')


if __name__ == '__main__':
    main()
