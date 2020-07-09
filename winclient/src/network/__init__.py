import sys
import os
import logging
import time

import socketio
from socketio.exceptions import ConnectionError

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from server import statuscode
from server import packetcode

logger = logging.getLogger(__name__)

sio = socketio.Client()

def connect(server_url):
    from src.network import _events
    attempts = 3
    for i in range(attempts):
        logger.info(f"Connecting to the server... (attempt {i + 1}/3)")
        try:
            sio.connect(server_url)
            break
        except ConnectionError as e:
            if i < attempts - 1:
                sleeptime = 2 + i
                logger.error(f"Unable to connect to the server: {e}; Trying again in {sleeptime} second...")
                time.sleep(sleeptime)
            else:
                logger.error("Server unreachable.")
    else:
        return
    logger.info("Connected. Log in, before joining the game.")
    # sio.wait()

def log_in(username, password):
    sio.emit(packetcode.LOGIN_REQUEST, {'username': username, 'password': password})
    logger.info("Login request send.")
