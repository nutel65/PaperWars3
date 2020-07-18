import logging
import json

from flask import request
from flask_socketio import emit #, join_room, leave_room

from server import statuscode
from server import utility
from server import packetcode
from server.app import socketio, app, dbmanager, rooms

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
def on_login(data):
    logger.debug(data)
    username = data.get('username')
    password = data.get('password')
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
            "room": "/lobby",
            "privilege": privilege,
        }
    emit(packetcode.LOGIN_RESPONSE, {'status': status}, room=sid)


# @socketio.on(packetcode.CHANGE)
# def CHANGE(data):
#     logger.debug(data)
#     CHANGE = data.get()
#     sid = request.sid
    
#     emit(packet
# code.CHANGE, {'status': status}, room=sid)


@socketio.on(packetcode.CREATE_ROOM_REQUEST)
def on_create_room(data):
    logger.debug(data)
    sid = request.sid
    try:
        rooms.append(utility.GameRoom())
        status = statuscode.OK
    except:
        status = statuscode.INTERNAL_ERROR
    emit(packetcode.CREATE_ROOM_RESPONSE, {'status': status}, room=sid)


@socketio.on(packetcode.JOIN_ROOM_REQUEST)
def on_join_room(data):
    logger.debug(data)
    sid = request.sid
    try:
        room_id = data["room_id"]
        status = rooms[room_id].assign_player(active_users[sid])
    except KeyError:
        status = statuscode.MISSING_PARAMETERS
    except:
        status = statuscode.INTERNAL_ERROR
    emit(packetcode.JOIN_ROOM_RESPONSE, {"status": status}, room=sid)


@socketio.on(packetcode.REQUEST_GAME_LIST)
def on_request_game_list(data):
    logger.debug(data)
    sid = request.sid
    try:
        game_list = json.dumps([repr(room) for room in rooms])
        status = statuscode.OK
    except:
        status = statuscode.INTERNAL_ERROR
    emit(packetcode.REQUEST_GAME_LIST_RESPONSE, {"status": status, "game_list": game_list}, room=sid)

