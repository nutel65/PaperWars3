import logging
import selectors
import time
import servercli


logger = logging.getLogger("server")

def accept_clients(sock, client_list):
    logger.info("Doorman thread started. Waiting for client...")
    while True:
        client_sock, addr = sock.accept()
        client_list.append((client_sock, addr))
        logger.info(f"Connected with client ({addr[0]})")

def message_reveiver(sockets):
    # TODO: multiplexing clients_list using selectors
    logger.info("Receiver thread started. Waiting for data...")
    while True:
        if sockets:
            data = sockets[0].recv(1024)
            logger.info(f"data received")
            print(f"client message: {data}")
        else:
            time.sleep(1)

def cli_input_handler():
    while True:
        inp = input()
        servercli.exe(inp)
