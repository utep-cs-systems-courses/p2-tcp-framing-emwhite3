#! /usr/bin/env python3

import socket, sys, re, _thread
import params, argparse

PACKET_SIZE = 1024
in_transit = []
mutex = _thread.allocate_lock()


# client working thread that sends a file to an
# accepted client
# @params: connection object
def client_thread(conn, packets):
    mutex.acquire()
    while len(packets) != 0:
        data = packets[0]
        if len(data) == 0:
            print("Zero length read, nothing to send, terminating")
            break
        conn.send(data)
        packets = packets[1:]
    print("finished sending file")
    conn.shutdown(socket.SHUT_WR)
    conn.close()
    mutex.release()


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

parser = argparse.ArgumentParser()
parser.add_argument("ip")
parser.add_argument("port")
parser.add_argument("file")
args = parser.parse_args()

packets = populate_file_buffer()
#print(packets)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((args.ip, int(args.port)))
s.listen(20)

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)
if conn:
    _thread.start_new_thread(client_thread, (conn, packets, ))
    exit_program = input("Enter \"quit\" to exit program\n")
else:
    print('Closing server')
    sock.close()