# Server response codes
# Error codes: 1 <= x <= 127
# Other codes: >= 128
OK = LOGIN_OK = 0
NOT_IMPLEMENTED = 1
ROOM_FULL = 2
PERMISSION_DENIED = 3
ILLEGAL_ACTION = 4
INTERNAL_ERROR = 5
MISSING_PARAMETERS = 6

SERVER_FULL = 7
HANDSHAKE_OK = 128
PROTOCOL_NOT_SUPPORTED = 129

NO_SUCH_USER = 8
INCORRECT_PASSWORD = 9
USERNAME_TAKEN = 10
ADMIN_LOGIN_OK = 154
GUEST_LOGIN_OK = 155