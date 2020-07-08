#!/usr/bin/env python3

import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import logging

import socketio

from server import statuscode
from server import packetcode

logger = logging.getLogger(__name__)
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

sio = socketio.Client()

target = "http://localhost:5000"
# target = "https://paperwars.herokuapp.com"

def log_in(username="rafix", password="rafix", target=target):
    sio.emit(packetcode.LOGIN_REQUEST, {'username': username, 'password': password})


@sio.event
def connect():
    logger.info('connection established')
    # TODO: show prompt to log in

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

def run():
    sio.connect(target)
    sio.wait()

if __name__ == "__main__":
    run()