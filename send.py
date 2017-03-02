#!/usr/bin/env python
'''
Simple sender.

Sends messages over a specific port to a host at periodic intervals.

Here is an example that sends messages to recv_host on port 8500.

   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ send.py recv_host 8500

The optional arguments are:

   HOST  - hostname, default 127.0.0.1
   PORT  - port, default 8500
   SECS  - seconds to pause, default 1.
'''
import datetime
import json
import random
import socket
import string
import sys
import time


HOST = '127.0.0.1'
PORT = 8500


def create_record():
    '''
    Create a record to send.
    '''
    data = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    rec = {'data': data, 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),}
    json_rec = json.dumps(rec)
    return json_rec.encode('ascii')


def send(rec, host, port):
    '''
    Send the record.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (host, port)
    print('SND: {}  {}'.format(addr, rec))
    try:
        sock.connect(addr)
        sock.sendall(bytes(rec))
        response = sock.recv(1024)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except socket.error:  # need to change this for Python 3
        pass  # we don't care if there is no listener


def main():
    '''
    Main send loop.
    '''
    host = HOST if len(sys.argv) < 2 else sys.argv[1]
    port = PORT if len(sys.argv) < 3 else int(sys.argv[2])
    secs = 1 if len(sys.argv) < 4 else float(sys.argv[3])
    while True:
        rec = create_record()
        send(rec, host, port)
        time.sleep(secs)


if __name__ == '__main__':
    main()
