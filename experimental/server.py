#!/usr/bin/env python3

import socket
import selectors
import threading
from engine import utils
from collections import deque

HOST = '127.0.0.1'
PORT = 23232
connections = {
    
}
request_queue = deque()

def id_gen(prefix=""):
    i = 1
    while True:
        yield f"{prefix}{i}"
        i += 1

game_id_gen = id_gen("G_")
client_id_gen = id_gen("C_")


class GameRoom():
    def __init__(self):
        self.id = next(game_id_gen)
        self.game = ...

class Client():
    def __init__(self):
        self.id = next(client_id_gen)
        
def process_request(data):
    ...

def exchange(sock, msg):
    # if len(active_connections) < 2:
    #     active_connections.append(sock)
    #     utils.log("Connected", type="SERVER")
    # else:
    #     utils.log("Refused connection. Maximum client amount reached", type="SERVER")
    utils.log("retrieving data from socket ...")
    data = sock.recv(1024)
    utils.log(f"data received: {data}")
    msg = input("input message:\n>")
    sock.sendall(bytes(msg, "utf-8"))
    # active_connections.remove(sock)
    

def main():
    print(socket.gethostname())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        utils.log(f"Running socket: {HOST}:{PORT}", type="SERVER")
        while True:
            utils.log("Waiting for client...", type="SERVER")
            client1, addr = s.accept()
            utils.log(f"Connecting with client ({addr[0]})", type="SERVER")
            while True:
                exchange(client1, "xd")
            # client1.close()

if __name__ == "__main__":
    main()

