"""This file contains GameState class that holds global information about game's state"""
import pygame
from engine import utils

class GameState():
    """This class holds global informations about game's state.
    Variables:
        local
        socket
    """

    def __init__(self, game_obj):
        self.game = game_obj
        self.default_local = {}
        self.local = {
            "current_scene": "game",
            "game_paused": False,
            "player_turn": 0,
            "remaining_turn_time": 50,
            "last_click_pos": (-100, -100),
            "selected_entity": None,
            "pressed_keys": [],
        }
        self.socket = {
            "is_connected": False,
            "host_ip": None,
            "client_ip": None,
            "port": "5000", 
        }

    def get_global_mouse_pos(self):
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        return utils.local_to_global(self.game.renderer, pygame.mouse.get_pos())
        # zoom = self.game.renderer.camera.get_zoom()
        # screen_x = (mouse_x + self.game.renderer.camera.rect.topleft[0]) / zoom + self.game.renderer.DISPLAY_RECT.x
        # screen_y = (mouse_y + self.game.renderer.camera.rect.topleft[1]) / zoom + self.game.renderer.DISPLAY_RECT.y
        ## DEBUG:
        # ent = next(iter(self.game.entities))
        # self.game.renderer.screen.blit(ent.image, (screen_x, screen_y))
        # pygame.display.flip()
        # return (screen_x, screen_y)

    def get_screen_mouse_pos(self):
        return pygame.mouse.get_pos()

        