#!/usr/bin/env python3

import sys
import os
import logging

import socketio

from src.network import sio
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from server import statuscode
from server import packetcode

logger = logging.getLogger(__name__)


@sio.event
def connect():
    logger.info('Connection established.')
    # TODO: show prompt to log in


@sio.event
def disconnect():
    logger.info('Disconnected from the server.')


@sio.on(packetcode.LOGIN_RESPONSE)
def login_response(data):
    status = data["status"]
    logger.debug(f'login response received with {data}')
    if status == statuscode.LOGIN_OK or status == statuscode.ADMIN_LOGIN_OK:
        logger.info("SERVER: Successfully logged in.")
    elif status == statuscode.NO_SUCH_USER:
        logger.info("SERVER: No such user in database")
    elif status == statuscode.INCORRECT_PASSWORD:
        logger.info("SERVER: Incorrect password")
    else:
        logger.info(f"SERVER: Login error. Status code: {data['status']}")

