"""This file holds global information about game's state"""

class GameState():
    """This class holds global informations about game's state.
    Variables:
        local
        socket
    """

    def __init__(self, game_obj):
        self.default_local = {}

        self.local = {
            "current_scene": "main_menu",
            "game_paused": False,
            "player_turn": 1,
            "remaining_turn_time": 50,
        }

        self.socket = {
            "is_connected": False,
            "host_ip": None,
            "client_ip": None,
            "port": "5000", 
        }