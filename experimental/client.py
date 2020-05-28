#!/usr/bin/env python3

import socket
import time
import binascii
# from engine import utils

def send(sock, data):
    ...

def handshake(sock, version):
    major = binascii.a2b_hex(format(version[0], '02x'))
    minor = binascii.a2b_hex(format(version[1], '02x'))
    patch = binascii.a2b_hex(format(version[2], '02x'))
    sock.sendall(major + minor + patch)


def connect_to_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except socket.error:
        print(f"Cannot establish connection with {host}:{port}")
        return
    print("Connected")
    msg = input("send message:\n> ")

    handshake(sock, [1, 0, 0])

    print("handshake sent, waiting for reply...")
    data = sock.recv(1024)
    print("received", data)
    return sock
    

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 23232
    sock = connect_to_server(HOST, PORT)
    if sock:
        sock.close()
        print("closed connection")
        time.sleep(1)
