"""This file imports main engine class 'Game'"""
import pygame
from engine import render
from src import commands
from src import state
from src import entities
from src import utils

class GameInstance:
    """Main engine class, that connects together other engine pieces."""
    def __init__(self):
        # self.state = state.GameState(self)
        self.client_state = state.ClientState()
        self.game_state = state.GameState()
        # self.connection_state = state.ConnectionState()
        self.entities = set()

    def add(self, entity_type, *args, **kwargs):
        """Easy and convenient way to add new entities."""
        if entity_type == "soldier":
            ent = entities.Sprite(*args, **kwargs)
        elif entity_type == "button":
            raise NotImplementedError
        else:
            raise ValueError(f"Entity type {entity_type} does not exist.")
        self.entities.add(ent)
        # self.renderer.render_request_list.append(ent)

    def update_state(self, renderer):
        # update client state
        cs = self.client_state
        mouse_pos = pygame.mouse.get_pos()
        cs.mouse_pos_window = mouse_pos
        cs.mouse_pos_global = utils.local_to_global(renderer, mouse_pos)
        cs.keys_pressed = pygame.key.get_pressed()
        cs.camera_zoom = renderer.camera.get_zoom()
        cs.camera_pos = renderer.camera.rect.topleft

        # update game state
        gs = self.game_state
        gs.remaining_turn_time = ... # todo: calculate remaining time