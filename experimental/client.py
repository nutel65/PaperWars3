#!/usr/bin/env python3

import socket
import time
# from engine import utils


def connect_to_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except socket.error:
        print(f"Cannot establish connection with {host}:{port}")
        return
    print("Connected")
    msg = input("send message:\n> ")
    s.sendall(bytes(msg, "utf-8"))
    print("message sent, waiting for reply...")
    sock.settimeout(5.0)
    data = sock.recv(1024)
    sock.settimeout(None)
    print("received", data)
    

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 23232
    sock = connect_to_server(HOST, PORT)
    sock.close()
    print("closed connection")
    time.wait(5)
