#! /usr/bin/env python3

import socket, sys, re
import params

PACKET_SIZE = 1024

def populate_file_buffer():
    # Open the file
    try:
        output = open("bio.txt", 'rb')
    except IOError:
        print('Unable to open bio.txt')
        return

    # Add all the packets to the buffer
    packets = []
    while True:
        data = output.read(PACKET_SIZE)
        if not data:
            break
        packets.append(data)
    return packets

progname = "ftp_server"

packets = populate_file_buffer()

listenPort = 50009
listenAddr = '127.0.0.1'       # Symbolic name meaning all available interfaces

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)
while len(packets) != 0:
    print(packets[0])
    data = packets[0]
    if len(data) == 0:
        print("Zero length read, nothing to send, terminating")
        break
    conn.send(data)
    packets = packets[1:]
print("finished sending file")
conn.shutdown(socket.SHUT_WR)
conn.close()