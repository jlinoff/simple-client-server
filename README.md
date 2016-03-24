# simple-client-server
Very simple client/server example in python 2.x and 3.x.

Not too long ago I was talking to a colleague about doing some
network traffic analysis and they suggested setting up a rather
complex client/server arrangement. I suggest an alternative setup
using a simple client/server and wrote up this example to show how to
do it. It was well received so I thought that I would make it
available to all.

There are two programs: `send.py` and `recv.py`.

The `send.py` script sends unique, time-stamped messages every second
to an IP address on a user specified port.

The `recv.py` program receives the information sent by the `send.py`
script.

In both programs the first argument is the IP address and the second
is the port.

Here is very simple networking example that shows how send and receive
messages over sockets on a single host.

```bash
   $ # Step 1. Open a terminal window, update the firewall and
   $ #         start sending messages.
   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ send.py 127.0.0.1 8500

   $ # Step 2. Open another terminal window and start receiving
   $ #         messages.
   $ recv.py 0.0.0.0 8500
```

Here is another example that shows how to send and receive messages
on two different hosts.

```bash
   [send_host]$ # Step 1. Open a terminal window on the send host, update
   [send_host]$ #         the firewall and start sending messages.
   [send_host]$ firewall-cmd --zone=public --add-port=8500/tcp
   [send_host]$ send.py recv_host  8500

   [recv_host]$ # Step 2. Open a terminal window on the receive host and
   [recv_host]$ #         start receiving messages.
   [recv_host]$ firewall-cmd --zone=public --add-port=8500/tcp
   [recv_host]$ recv.py '0.0.0.0'  8500
```

As you can see it is very simple to use.

It is also easy to customize to meet your needs.

You can use the basic idea to create test drivers or just to get a
very basic understanding of networking.
