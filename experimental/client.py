#!/usr/bin/env python3

import socket
import time
# from engine import utils


def connect_to_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except socket.error:
        print(f"Cannot establish connection with {host}:{port}")
        return
    print("Connected")
    msg = input("send message:\n> ")
    sock.sendall(bytes(msg, "utf-8"))
    print("message sent, waiting for reply...")
    print("experimental: settimeout = 5")
    sock.settimeout(5.0)
    try:
        data = sock.recv(1024)
    except socket.timeout:
        print("no reply from server")
    finally:
        print("received", data)
    sock.settimeout(None)
    return sock
    

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 23232
    sock = connect_to_server(HOST, PORT)
    if sock:
        sock.close()
        print("closed connection")
        time.wait(1)
