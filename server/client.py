#!/usr/bin/env python3

import socket
import time
import binascii
import utility
import statuscode

logger = utility.setup_logger("client", filename="clientrun.log")

def send(sock, data):
    ...

def handshake(sock, version):
    # major = binascii.a2b_hex(format(version[0], '02x'))
    # minor = binascii.a2b_hex(format(version[1], '02x'))
    # patch = binascii.a2b_hex(format(version[2], '02x'))
    major = utility.int_to_bhex(version[0])
    minor = utility.int_to_bhex(version[1])
    patch = utility.int_to_bhex(version[2])
    sock.sendall(major + minor + patch)
    logger.info("Handshake sent, waiting for reply...")
    data = sock.recv(1024)
    if not data:
        logger.error("Server closed connection unexpectedly.")
        return statuscode.CONNECTION_LOST
    elif len(data) == 1:
        return utility.bhex_to_int(data)


def connect_to_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except socket.error:
        logger.error(f"Cannot establish connection with {host}:{port}")
        return
    logger.info(f"Connected with server ({host}:{port})")
    status = handshake(sock, [1, 0, 0])
    if status == statuscode.HANDSHAKE_OK:
        logger.info("HANDSHAKE_OK")
    elif status == statuscode.PROTOCOL_NOT_SUPPORTED:
        raise Exception("PROTOCOL_NOT_SUPPORTED")
    elif status == statuscode.SERVER_FULL:
        raise Exception("SERVER_FULL")
    else:
        raise Exception(F"UNCAUGHT CODE ERROR: {status}")
    return sock
    

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 23232
    sock = connect_to_server(HOST, PORT)
    if sock:
        sock.close()
        logger.info("closing connection")
        time.sleep(1)
