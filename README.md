# simple-client-server
[![Releases](https://img.shields.io/github/release/jlinoff/simple-client-server.svg?style=flat)](https://github.com/jlinoff/simple-client-server/releases)

Very simple client/server example in python 2.x and 3.x.

## Introduction

Not too long ago I was talking to a colleague about doing some
network traffic analysis and they suggested setting up a rather
complex client/server arrangement. I suggested an alternative setup
using a simple client/server and wrote up this example to show how to
do it. It was well received so I thought that I would make it
available to all.

## Contents

There are two programs: `send.py` and `recv.py`.

The `send.py` script sends unique, time-stamped messages every second
to an IP address on a user specified port.

The `recv.py` program receives the information sent by the `send.py`
script.

## send.py Program Arguments

These are the important program arguments for send.py. There are others. They can be seen in the help.

| Short      | Long           | Type   | Default   | Description |
| ---------- | -------------- | ------ | --------: | ----------- |
| -h         | --help         |        |           | Print the program help and exit. |
| -H HOST    | --host HOST    | string | 127.0.0.1 | The host name. |
| -p PORT    | --port PORT    | int    | 8500      | The communications port. |
| -t SECONDS | --time SECONDS | float  | 1.0       | Send data every SECONDS seconds. |
| -v         | --verbose      |        |           | Increase the level of verbosity. |
| -V         | --version      |        |           | Print the program version and exit. |

## recv.py Program Arguments

These are the important program arguments for recv.py. There are others. They can be seen in the help.

| Short      | Long           | Type   | Default   | Description |
| ---------- | -------------- | ------ | --------: | ----------- |
| -h         | --help         |        |           | Print the program help and exit. |
| -H HOST    | --host HOST    | string | 127.0.0.1 | The host name. |
| -p PORT    | --port PORT    | int    | 8500      | The communications port. |
| -t SECONDS | --time SECONDS | float  | 1.0       | Poll for data every SECONDS seconds. |
| -v         | --verbose      |        |           | Increase the level of verbosity. |
| -V         | --version      |        |           | Print the program version and exit. |

## Single Host Example

Here is very simple networking example that shows how send and receive
messages over sockets on a single host.

```bash
   $ # Step 1. Open a terminal window, update the firewall and
   $ #         start sending messages.
   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ send.py --host 127.0.0.1 --port 8500

   $ # Step 2. Open another terminal window and start receiving
   $ #         messages.
   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ recv.py --host 0.0.0.0 --port 8500
```

## Two Host Example

Here is another example that shows how to send and receive messages
on two different hosts.

```bash
   [send_host]$ # Step 1. Open a terminal window on the send host, update
   [send_host]$ #         the firewall and start sending messages.
   [send_host]$ firewall-cmd --zone=public --add-port=8500/tcp
   [send_host]$ send.py --host recv_host --port 8500

   [recv_host]$ # Step 2. Open a terminal window on the receive host and
   [recv_host]$ #         start receiving messages.
   [recv_host]$ firewall-cmd --zone=public --add-port=8500/tcp
   [recv_host]$ recv.py --host 0.0.0.0 --port 8500
```

## Real Life Example

Here is the sample output from a run done my Mac using two VirtualBox
VM's running CentOS 7.2. I configured internal networking to allow my
hosts to communicate directly.

This is the output from the receiver. I started it before the sender
to make sure that all records were captured.

```bash
   $ # receiver
   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ ./recv.py --host 0.0.0.0 --port 8500
   RCV: ('10.0.3.16', 51128)  2016-03-24 11:54:50.312326  4pkbqjzjfdflj36s0fxjar9bu0kruova
   RCV: ('10.0.3.16', 51129)  2016-03-24 11:54:51.317053  m6gd0j7zf7tjuo9a45ozj7die7api5dq
   RCV: ('10.0.3.16', 51130)  2016-03-24 11:54:52.320206  3icraxzww4scack7v2ypg1hjeqf2rumh
   RCV: ('10.0.3.16', 51131)  2016-03-24 11:54:53.323279  3p6emwbmjmmmvljuxp84xm1w9fx4t5vu
   RCV: ('10.0.3.16', 51132)  2016-03-24 11:54:54.325794  00v44q8k4hkz8qs6ofw7pe5fcedpc8uh
   .
   .
```

This the output from the sender.

```bash
   $ # sender
   $ firewall-cmd --zone=public --add-port=8500/tcp
   $ ./send.py --host 10.0.3.15 --port 8500
   SND: ('10.0.3.15', 8500)  {"data": "4pkbqjzjfdflj36s0fxjar9bu0kruova", "time": "2016-03-24 11:54:50.312326"}
   SND: ('10.0.3.15', 8500)  {"data": "m6gd0j7zf7tjuo9a45ozj7die7api5dq", "time": "2016-03-24 11:54:51.317053"}
   SND: ('10.0.3.15', 8500)  {"data": "3icraxzww4scack7v2ypg1hjeqf2rumh", "time": "2016-03-24 11:54:52.320206"}
   SND: ('10.0.3.15', 8500)  {"data": "3p6emwbmjmmmvljuxp84xm1w9fx4t5vu", "time": "2016-03-24 11:54:53.323279"}
   SND: ('10.0.3.15', 8500)  {"data": "00v44q8k4hkz8qs6ofw7pe5fcedpc8uh", "time": "2016-03-24 11:54:54.325794"}
   .
   .
```

## Summary

As you can see it is very simple to use.

It is also easy to customize to meet your needs.

You can use the basic idea to create test drivers or just to get a
very basic understanding of networking.
