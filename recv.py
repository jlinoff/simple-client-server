#!/usr/bin/env python
'''
Simple receiver.

Receives messages send by the send.py program at periodic intervals.

Here is an example that receives messages from any IPv4 address on
port 8500.

Command to open the port:

   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ recv.py 0.0.0.0 8500

The optional arguments are:

   HOST  - hostname, default 127.0.0.1
   PORT  - port, default 8500
   SECS  - seconds to pause, default 0.200 (200ms).
'''
import json
import socket
import sys
import time


HOST = '0.0.0.0'  # Listen on all NICs.
PORT = 8500


def create_listener(host, port):
    '''
    Create the listener.
    '''
    sock_addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(sock_addr)
    sock.listen(5)
    return sock


def receive_recs(host, port, pause):
    '''
    Poll for records.
    '''
    listener = create_listener(host, port)
    while True:
        conn, addr = listener.accept()
        json_rec = conn.recv(1024)
        rec = json.loads(json_rec.decode('utf-8'))  # same format as sender
        print('RCV: {}  {}  {}'.format(addr, rec['time'], rec['data']))
        conn.close()
        time.sleep(pause)


def main():
    '''
    Main receive loop.
    '''
    host = HOST if len(sys.argv) < 2 else sys.argv[1]
    port = PORT if len(sys.argv) < 3 else int(sys.argv[2])
    secs = 0.200 if len(sys.argv) < 4 else float(sys.argv[3])
    receive_recs(host, port, secs)


if __name__ == '__main__':
    main()
