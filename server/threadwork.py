import logging
import selectors
import time
import servercli
import threading
import traceback
from collections import deque


logger = logging.getLogger("server")

def accept_clients(sock, client_list):
    logger.info("Doorman thread started. Waiting for client...")
    while True:
        client_sock, addr = sock.accept()
        client_list.append((client_sock, addr))
        logger.info(f"Connected with client ({addr[0]})")

def message_reveiver(clients):
    # TODO: multiplexing clients_list using selectors
    logger.info("Receiver thread started. Waiting for data from clients...")
    while True:
        if clients:
            client_num = 0
            client_sock = clients[client_num][0]
            client_addr = clients[client_num][1]
            data = client_sock.recv(1024)
            if not data:
                logger.info(f"Client disconnected ({client_addr})")
                client_sock.close()
                clients.pop(client_num)
                continue
            logger.info(f"data received")
            print(f"client message: {data}")
        else:
            time.sleep(1)

def cli_input_handler(services_list, active_sockets_list):
    servercli.set_services(services_list)
    servercli.set_active_sockets(active_sockets_list)
    while True:
        try:
            inp = input()
            servercli.exe(inp)
        except:
            logger.critical(f"An error occured during command execution:\n{traceback.format_exc()}")

class DBManager(threading.Thread):
    def __init__(self, database=None):
        threading.Thread.__init__(self)
        self.database = database
        self.exitflag = 0
        self.query_queue = deque()
        self.name = "DBManager"
    def run(self):
        logger.info("DBManager service started.")
        while not self.exitflag or self.query_queue:
            if self.query_queue:
                ...
                # TODO: Add real database.
                # database.query(query_queue.popleft())
                print(self.query_queue.popleft())
            else:
                time.sleep(1)
        logger.info("DBManager service stopped.")
    def stop(self):
        self.exitflag = 1
        if self.query_queue:
            logger.info("DBManager: waiting for finishing pending queries...")

    def query(self, query_string):
        if self.exitflag:
            logger.error("DBManager stopped; Could not add new query")
            return
        if not query_string:
            print("query string cannot be empty")
        self.query_queue.append(query_string)

    def status(self):
        message = "DBManager NOT WORKING"
        if self._check_if_alive():
            message = "DBManager OK"
        print(message)

    def _check_if_alive(self):
        self.join(timeout=0.0)
        return self.is_alive()