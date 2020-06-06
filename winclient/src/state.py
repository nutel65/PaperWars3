"""This file contains snapshot of program state updated after every frame."""
# import pygame
from dataclasses import dataclass
# from engine import utils

scenes = {"main_menu": 'function goes here',
          "game_paused": ...,
          "game_running": ...,
          "settings": ...,

         }


@dataclass
class GameState:
    player_turn = 0
    # start_turn_time = datetime.get_now()
    remaining_turn_time = 50


@dataclass
class ClientState:
    current_scene = "main_menu"
    last_click_pos = (-100, -100)
    mouse_pos_window = (-100, -100)
    mouse_pos_global = (-100, -100)
    keys_pressed = []
    camera_zoom = 1.0
    camera_pos = (0, 0)
    

# @dataclass
# class ConnectionState:
#     connected = False
#     host_ip = None
#     client_ip = None
#     port = "5000"         

    

        