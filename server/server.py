#!/usr/bin/env python3

import config
import random
import selectors
import servercli
import socket
import threading
import threadwork
import time
import utility
from collections import deque

logger = utility.setup_logger()

class GameRoom():
    game_id_gen = utility.id_gen("G_")
    def __init__(self):
        self.id = next(game_id_gen)
        self.game_state = ...
        self.assigned_clients = [None, None]

    def assign_client(client_obj):
        i = self.assigned_client.index(None)
        self.assigned_client[i] = client_obj
        # if both clients are online then start game

    def start_game(self):...

class Client():
    # client_id_gen = utility.id_gen("C_")
    def __init__(self, socket, ip_addr):
        # self.id = next(client_id_gen)
        self.socket = socket
        self.ip_addr = ip_addr
        self.gameroom_id = None
        self.context = None
    
def main():
    print(socket.gethostname())
    listening_sock = socket.socket(
        family=socket.AF_INET, 
        type=socket.SOCK_STREAM)
    listening_sock.setblocking(False)
    listening_sock.bind((config.SERVER_IP, config.SERVER_PORT))
    listening_sock.listen()
    logger.info(f"Server running at: {config.SERVER_IP}:{config.SERVER_PORT}")

    services = {}
    selector = selectors.DefaultSelector()
    selector.register(listening_sock, selectors.EVENT_READ, data={"type": "listener"})
    
    # INIT THREADS
    # services["doorman"] = threading.Thread(
    #     target=threadwork.accept_clients, 
    #     args=(listening_sock, selector),
    #     daemon=True)
    # services["doorman"].start()

    services["packrec"] = threadwork.PacketReceiver(selector)
    services["packrec"].start()

    services["dbmanager"] = threadwork.DBManager("db_here")
    services["dbmanager"].start()
    
    services["cli"] = threadwork.CLIService()
    servercli.set_services(services)
    services["cli"].start()

    while True:
        keys = list(services.keys())
        try:
            k = random.choice(keys)
        except:
            break
        services[k].join()
        services.pop(k)

    print("all services stopped")
    listening_sock.close()

if __name__ == "__main__":
    main()

