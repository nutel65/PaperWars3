#!/usr/bin/env python3

import socket
from engine import utils

HOST = '127.0.0.1'
PORT = 23494
active_connections = []

def handle_client(sock):
    if len(active_connections) < 2:
        active_connections.append(sock)
        utils.log("Connected", type="SERVER")
    else:
        utils.log("Refused connection. Maximum client amount reached", type="SERVER")
    with sock:
        while True:
            data = sock.recv(1024)
            if data == b"":
                utils.log("breaking connection...", type="SERVER")
                break
            sock.sendall(data)
    active_connections.remove(sock)
    

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        utils.log(f"Opened socket: {HOST}:{PORT}", type="SERVER")
        while True:
            client_sock, addr = s.accept()
            utils.log(f"Connecting ... ({addr[0]})", type="SERVER")
            handle_client(client_sock)

if __name__ == "__main__":
    main()

