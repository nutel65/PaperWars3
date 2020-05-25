import api
import logging
import selectors
import servercli
import threading
import time
import traceback
from collections import deque

logger = logging.getLogger("server")

class ThreadWorker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exitflag = 0
        self.name = "ThreadWorker"

    def stop(self):
        self.exitflag = 1

    def status(self):
        message = f"{self.name} NOT WORKING"
        if self._check_if_alive():
            message = f"{self.name} OK"
        print(message)

    def _check_if_alive(self):
        self.join(timeout=0.0)
        return self.is_alive()

def accept_clients(listening_sock, client_list, selector):
    logger.info("Doorman thread started. Waiting for client...")
    while True:
        client_sock, addr = listening_sock.accept()
        client_sock.setblocking(False)
        client_list.append((client_sock, addr))
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # data param sets if user is logged
        selector.register(client_sock, events, data="unlogged") 
        logger.info(f"Client connected ({addr[0]}:{addr[1]})")

# def message_reveiver(clients):
#     logger.info("DataReceiver thread started.")
#     while True:
#         # TODO: multiplexing clients list using selectors
#         if clients:
#             client_num = 0
#             client_sock = clients[client_num][0]
#             addr = clients[client_num][1]
#             data = client_sock.recv(1024)
#             if not data:
#                 logger.info(f"Client disconnected ({addr[0]}:{addr[1]})")
#                 client_sock.close()
#                 clients.pop(client_num)
#                 continue
#             logger.info(f"({client_num})({addr[0]}:{addr[1]}) => {data}")
#         else:
#             time.sleep(1)

class PacketReceiver(ThreadWorker):
    def __init__(self, selector):
        ThreadWorker.__init__(self)
        self.query_queue = deque()
        self.name = "PacketReceiver"
        self.selector = selector
        
    def run(self):
        # TODO: multiplexing clients list using selectors
        logger.info(f"{self.name} service started.")
        while True:
            # FIXME: wmpty selector throws exception on windows
            events = self.selector.select(timeout=None)
            for key, mask in events:
                if key.data == "logged":
                    handle_logged(key, mask)
                elif key.data == "unlogged":
                    handle_unlogged(key)
                else:
                    raise ValueError("Register data is neither 'logged' nor 'unlogged'")

            # if self.unlogged:



            #     client_num = 0
            #     client_sock = self.unlogged[client_num][0]
            #     addr = self.unlogged[client_num][1]
            #     data = client_sock.recv(1024)
            #     if not data:
            #         logger.info(f"Client disconnected ({addr[0]}:{addr[1]})")
            #         client_sock.close()
            #         self.unlogged.pop(client_num)
            #         continue
            #     logger.info(f"({client_num})({addr[0]}:{addr[1]}) => {data}")
            # else:
            #     time.sleep(1)

    def handle_unlogged(self, register):
        sock = register.fileobj
        packet = sock.recv(4096)
        status = api.handshake(packet, sock)
        if status == 128:
            register.data = "logged"
        else:
            self.selector.unregister(sock)
            sock.close()
        logger.info(f"{status} {config.SERVER_CODES[status]}")

    def handle_logged(self, register):
        print("handle_logged not implemented, disconnecting...")
        sock = register.fileobj
        self.selector.unregister(sock)
        sock.close()

    def stop(self):
        self.exitflag = 1
        if self.query_queue:
            logger.info(f"{self.name}: waiting for finishing pending queries...")

    def query(self, query_string):
        if self.exitflag:
            logger.error(f"{self.name} stopped; Could not add new query")
            return
        if not query_string:
            print("query string cannot be empty")
        self.query_queue.append(query_string)

def cli_input_handler(services_list, active_sockets_list):
    servercli.set_services(services_list)
    servercli.set_active_sockets(active_sockets_list)
    while True:
        try:
            inp = input()
            servercli.exe(inp)
        except:
            logger.critical(f"An error occured during command execution:\n{traceback.format_exc()}")

class DBManager(ThreadWorker):
    def __init__(self, database=None):
        ThreadWorker.__init__(self)
        self.database = database
        self.query_queue = deque()
        self.name = "DBManager"

    def run(self):
        logger.info(f"{self.name} service started.")
        while not self.exitflag or self.query_queue:
            if self.query_queue:
                ...
                # TODO: Add real database.
                # database.query(query_queue.popleft())
                print(self.query_queue.popleft())
            else:
                time.sleep(1)
        logger.info(f"{self.name} service stopped.")
    def stop(self):
        self.exitflag = 1
        if self.query_queue:
            logger.info(f"{self.name}: waiting for finishing pending queries...")

    def query(self, query_string):
        if self.exitflag:
            logger.error(f"{self.name} stopped; Could not add new query")
            return
        if not query_string:
            print("query string cannot be empty")
        self.query_queue.append(query_string)