#!/usr/bin/env python3

import socketio
import statuscode
import packetcode
import logging

logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-16s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        # filename=f'./server/logs/{filename}',
                        filemode='w+')
logger = logging.getLogger(__name__)
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on(packetcode.LOGIN_RESPONSE)
def login_response(data):
    print('login response received with ', data)

if __name__ == "__main__":
    sio.connect('http://localhost:5000')
    print("connected. sending login request")
    sio.emit(packetcode.LOGIN_REQUEST, {'login': 'rafix', 'password': 'pwd'})
    print("login request sent")
    sio.wait()

