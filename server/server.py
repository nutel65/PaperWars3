#!/usr/bin/env python3

import socket
import selectors
import threading
import logging
import sys
from collections import deque


# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='./server/logs/lastrun.log',
                    filemode='w+')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger(__name__).addHandler(console)
logger = logging.getLogger(__name__)


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
    #     logger.info("Connected")
    # else:
    #     logger.info("Refused connection. Maximum client amount reached")
    logger.info("retrieving data from socket ...")
    data = sock.recv(1024)
    logger.info(f"data received: {data}")
    msg = input("input message:\n>")
    sock.sendall(bytes(msg, "utf-8"))
    # active_connections.remove(sock)
    

def main():
    print(socket.gethostname())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"Running socket: {HOST}:{PORT}")
        while True:
            logger.info("Waiting for client...")
            client1, addr = s.accept()
            logger.info(f"Connecting with client ({addr[0]})")
            while True:
                exchange(client1, "xd")
            # client1.close()

if __name__ == "__main__":
    main()

