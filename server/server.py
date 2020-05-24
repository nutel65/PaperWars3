#!/usr/bin/env python3

import socket
import threading
import time
import utility
import threadwork
import config
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

    def save_to_database(database):
        ...
    
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

    # INIT THREADS
    unassigned_clients_list = []
    active_clients = []
    services = {}
    
    services["doorman"] = threading.Thread(
        target=threadwork.accept_clients, 
        args=(listening_sock, unassigned_clients_list),
        daemon=True)
    services["doorman"].start()

    services["data_receiver"] = threading.Thread(
        target=threadwork.message_reveiver, 
        args=(active_clients,),
        daemon=True)
    services["data_receiver"].start()


    services["dbmanager"] = threadwork.DBManager()
    services["dbmanager"].start()
    
    services["input_handler"] = threading.Thread(
        target=threadwork.cli_input_handler,
        args=(services, active_clients),
        daemon=True)
    services["input_handler"].start()

    while True:
        if not unassigned_clients_list:
            time.sleep(1)
        else:
            print(unassigned_clients_list)
            active_clients.append(unassigned_clients_list.pop())
    listening_sock.close()

if __name__ == "__main__":
    main()

