#!/usr/bin/env python3

import socket
# from engine import utils

HOST = '127.0.0.1'
PORT = 23494

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected")
    print("sending message...")
    s.sendall(b'Hello, world')
    data = s.recv(1024)
    print('Received back:', repr(data))
    input("press to exit")