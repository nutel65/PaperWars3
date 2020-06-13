#!/usr/bin/env python3
import sys
sys.path.append("..")

import socketio
import logging
from server import statuscode
from server import packetcode

username = "rafix"
password = "rafix"
target = "http://localhost:5000"
# target = "https://paperwars.herokuapp.com"

logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-16s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        # filename=f'./server/logs/{filename}',
                        filemode='w+')
logger = logging.getLogger(__name__)
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

sio = socketio.Client()

@sio.event
def connect():
    logger.info('connection established')
    sio.emit(packetcode.LOGIN_REQUEST, {'username': username, 'password': password})

@sio.event
def disconnect():
    logger.info('disconnected from server')

@sio.on(packetcode.LOGIN_RESPONSE)
def login_response(data):
    status = data["status"]
    logger.info(f'login response received with {data}')
    if status == statuscode.LOGIN_OK or status == statuscode.ADMIN_LOGIN_OK:
        logger.info("Successfully logged in.")
    elif status == statuscode.NO_SUCH_USER:
        logger.info("No such user in database")
    elif status == statuscode.INCORRECT_PASSWORD:
        logger.info("Incorrect password")
    else:
        logger.info(f"Login error. Status code: {data[status]}")

if __name__ == "__main__":
    sio.connect(target)
    sio.wait()

