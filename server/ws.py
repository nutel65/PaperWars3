import logging
from server import statuscode
from server import utility
from server import packetcode
from server.app import socketio, app, dbmanager
from flask import request
from flask_socketio import emit #, join_room, leave_room

logger = logging.getLogger(__name__)
active_users = {}

@socketio.on('connect')
def on_connect():
    logger.info("Client connected")
    
@socketio.on('disconnect')
def on_disconnect():
    active_users.pop(request.sid)
    logger.info(f'Client disconnected. Removed from active_users. Active users now: {len(active_users)}')

@socketio.on(packetcode.LOGIN_REQUEST)
def on_login(message):
    logger.debug(message)
    username = message.get('username')
    password = message.get('password')
    sid = request.sid
    
    privilege = 'u'
    status = utility.validate_credentials(dbmanager, username, password)
    if status == statuscode.ADMIN_LOGIN_OK:
        privilege = 'a'
    if status == statuscode.LOGIN_OK:
        active_users[sid] = {
            "username": username,
            "room": "lobby",
            "privilege": privilege,
        }
    emit(packetcode.LOGIN_RESPONSE, {'status': status}, room=sid)

# @socketio.on(packetcode.LOGIN_REQUEST)
# def ws_handshake(packet, client_sock):
#     print("packet", packet)
#     major = packet[0]
#     minor = packet[1]
#     patch = packet[2]
#     print(f"Client version {major}.{minor}.{patch}")
#     status = statuscode.HANDSHAKE_OK
#     return status