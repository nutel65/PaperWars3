#!/usr/bin/env python3

import socket
# from server import exchange
# from engine import utils

HOST = '127.0.0.1'
PORT = 23232

def connect_to_server(host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM):
    s.connect((host, port))
    print("Connected")
    msg = input("send message:\n> ")
    s.sendall(bytes(msg, "utf-8"))
    print("message sent, waiting for reply...")
    data = s.recv(1024)
    print("received", data)
    input("press to exit")