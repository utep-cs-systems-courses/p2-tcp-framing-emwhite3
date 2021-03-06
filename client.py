#! /usr/bin/env python3

import socket, sys, re, time

PACKET_SIZE = 1024

try:
    output = open('output.txt', 'wb')
except IOError as e:
    print('Unable to open output.txt')

server, usage  = "127.0.0.1:50009", False

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)


s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break


if s is None:
    print('could not open socket')
    sys.exit(1)

delay = 1 # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")

while 1:
    data = s.recv(1024)
    print("Received '%s'" % data.decode())
    output.write(data)
    if len(data) == 0:
        break
print("Zero length read.  Closing")
s.close()
