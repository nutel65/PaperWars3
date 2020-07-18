import sys
import logging
import binascii
import secrets
import json

from flask_socketio import join_room, leave_room, emit
import msgpack

from server import statuscode, packetcode

logger = logging.getLogger(__name__)

class GameRoom():
    def __init__(self):
        self.id = secrets.token_urlsafe()[:6]
        self.game_state = None
        self.players = []
        self.max_players = 2

    def assign_player(self, client_obj):
        if len(self.players) < self.max_players:
            self.players.append(client_obj)
            join_room(self.id, sid=client_obj["sid"])
            return statuscode.OK
        return statuscode.ROOM_FULL

    def remove_player(self, client_obj):
        try:
            self.players.remove(client_obj)
            leave_room(self.id, sid=client_obj["sid"])
        except:
            pass
        return statuscode.OK

    def start_game(self):
        emit(packetcode.GAME_START, room=self.id, broadcast=True, include_self=False)

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "players_count": len(self.players),
            "max_players": self.max_players,
        })

    def __del__(self):
        emit(packetcode.ROOM_CLOSE, room=self.id, broadcast=True, include_self=False)

# class Client():
#     def __init__(self, socket, ip_addr):
#         # self.id = next(client_id_gen)
#         self.socket = socket
#         self.ip_addr = ip_addr
#         self.gameroom_id = None
#         self.context = None

def validate_credentials(dbmanager, username, password):
    query_result = dbmanager.get_user_by_username(username)
    logger.debug(f"{query_result}")
    if not query_result:
        return statuscode.NO_SUCH_USER
    if password != query_result[1]:
        return statuscode.INCORRECT_PASSWORD
    if query_result[2] == 'a':
        return statuscode.ADMIN_LOGIN_OK
    return statuscode.LOGIN_OK

# def logged_only(func, *args, **kwargs):
#     def wrapper():
#         sid = request.sid
#         if sid in logged_in_users:
#             func(*args, **kwargs)
#         else:
#             emit(packetcode.LOGIN_RESPONSE, {'status': status}, room=sid)
#     return wrapper

# class conditional:
#     """
#     A conditional decorator utility.
#     """
#     def __init__(self, decorator, condition):
#         self.decorator = decorator
#         self.condition = condition

#     def __call__(self, func):
#         if not self.condition:
#             return func
#         return self.decorator(func)