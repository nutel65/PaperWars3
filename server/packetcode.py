
# client -> server (request-response) 
CHAT_MESSAGE = 0
LOGIN_REQUEST = LOGIN_RESPONSE = 1 #
REGISTER_REQUEST = REGISTER_RESPONSE = 2
REQUEST_GAME_LIST = REQUEST_GAME_LIST_RESPONSE = 3 #
JOIN_ROOM_REQUEST = JOIN_ROOM_RESPONSE = 4 #
CREATE_ROOM_REQUEST = CREATE_ROOM_RESPONSE = 5 #

CREATE_ENTITY = 50

# server -> client (subscribtion)
GAME_START = 100 #
ROOM_CLOSE = 101 #

OPPONENT_EXIT = 102
OPPONENT_MOVE = 105
OPPONENT_ATTACK = 106
