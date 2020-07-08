import logging

from flask import request
from flask_socketio import emit #, join_room, leave_room

from server import statuscode
from server import utility
from server import packetcode
from server.app import socketio, app, dbmanager

logger = logging.getLogger(__name__)
active_users = {}

@socketio.on('connect')
def on_connect():
    logger.info("Client connected")
    
@socketio.on('disconnect')
def on_disconnect():
    popped = active_users.pop(request.sid, default=None)
    if popped:
        logger.info(f'Logged client disconnected. Removed from active_users. Active users now: {len(active_users)}')
    else:
        logger.info("Guest client just disconnected.")

@socketio.on(packetcode.LOGIN_REQUEST)
def on_login(message):
    logger.debug(message)
    username = message.get('username')
    password = message.get('password')
    sid = request.sid
    
    status = utility.validate_credentials(dbmanager, username, password)
    
    if status == statuscode.LOGIN_OK or statuscode.ADMIN_LOGIN_OK:
        privilege = None
        if status == statuscode.ADMIN_LOGIN_OK:
            privilege = 'a'
        else:
            privilege = 'u'
        active_users[sid] = {
            "username": username,
            "room": "lobby",
            "privilege": privilege,
        }
    emit(packetcode.LOGIN_RESPONSE, {'status': status}, room=sid)