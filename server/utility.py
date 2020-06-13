import binascii
import logging
import msgpack
import sys
from server import statuscode

logger = logging.getLogger(__name__)


def id_gen(prefix=""):
    i = 1
    while True:
        yield f"{prefix}{i}"
        i += 1

# def setup_logger(name, redirect=None):
#     # set up logging to file - see previous section for more details
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(name)-16s %(levelname)-8s %(message)s',
#                         datefmt='%m-%d %H:%M',
#                         filename=redirect,
#                         filemode='w+')
#     # define a Handler which writes INFO messages or higher to the sys.stderr
#     # set a format which is simpler for console use
#     # tell the handler to use this format
#     # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#     # console = logging.StreamHandler()
#     ## console.setLevel(0)
#     # console.setFormatter(formatter)
#     # add the handler to the root logger
#     # logging.getLogger(name).addHandler(console)
#     return logging.getLogger(name)

class GameRoom():
    game_id_gen = id_gen("G_")
    def __init__(self):
        self.id = next(game_id_gen)
        self.game_state = ...
        self.assigned_clients = [None, None]

    def assign_client(client_obj):
        i = self.assigned_client.index(None)
        self.assigned_client[i] = client_obj
        # if both clients are online then start game

    def start_game(self):...

class Client():
    # client_id_gen = utility.id_gen("C_")
    def __init__(self, socket, ip_addr):
        # self.id = next(client_id_gen)
        self.socket = socket
        self.ip_addr = ip_addr
        self.gameroom_id = None
        self.context = None

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