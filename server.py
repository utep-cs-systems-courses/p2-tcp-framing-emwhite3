#! /usr/bin/env python3

import socket, sys, re
import params

PACKET_SIZE = 1024

def populate_file_buffer():
    # Open the file
    try:
        file = open("bio.txt", 'rb')
    except IOError:
        print('Unable to open', filename)
        return

    # Add all the packets to the buffer
    packets = []
    while True:
        data = file.read(PACKET_SIZE)
        if not data:
            break
        packets.append(data)
    return packets


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False),
    )

progname = "FTP_server"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)
while not packet:
    data = packets[0]
    if len(data) == 0:
        print("Zero length read, nothing to send, terminating")
        break
    conn.send(data.encode())
    packets = packets[1:]
print("finished sending file")
conn.shutdown(socket.SHUT_WR)
conn.close()