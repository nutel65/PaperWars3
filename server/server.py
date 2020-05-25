#!/usr/bin/env python3

import config
import selectors
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
    # clients_db = {
    #     #client_id: client_object,
    # }
    
    print(socket.gethostname())
    listening_sock = socket.socket(
        family=socket.AF_INET, 
        type=socket.SOCK_STREAM) # | socket.SOCK_NONBLOCK)
    listening_sock.bind((config.SERVER_IP, config.SERVER_PORT))
    listening_sock.listen()
    logger.info(f"Server running at: {config.SERVER_IP}:{config.SERVER_PORT}")

    # unassigned_clients_list = []
    unlogged_clients = []
    logged_clients = {}
    services = {}
    selector = selectors.DefaultSelector()
    
    # INIT THREADS
    services["doorman"] = threading.Thread(
        target=threadwork.accept_clients, 
        args=(listening_sock, unlogged_clients, selector),
        daemon=True)
    services["doorman"].start()

    # services["packet_receiver"] = threading.Thread(
    #     target=threadwork.message_reveiver, 
    #     args=(unlogged_clients,),
    #     daemon=True)
    # services["packet_receiver"].start()
    services["packet_receiver"] = threadwork.PacketReceiver(selector)
    services["packet_receiver"].start()

    services["dbmanager"] = threadwork.DBManager("db_here")
    services["dbmanager"].start()
    
    services["input_handler"] = threading.Thread(
        target=threadwork.cli_input_handler,
        args=(services, unlogged_clients),
        daemon=True)
    services["input_handler"].start()

    while True:
        time.sleep(5)
        print(map(selector.get_map()))
        # if not unassigned_clients_list:
        #     time.sleep(1)
        # else:
        #     unlogged_clients.append(unassigned_clients_list.pop())
    listening_sock.close()

if __name__ == "__main__":
    main()

