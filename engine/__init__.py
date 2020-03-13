"""This file imports main engine class 'Game'"""
import pygame
from engine import game_socket
from engine import renderer
from src import state
from src import entities

class Game:
    """Main engine class, that connects together other engine pieces.

    variables:
        entities    List of all entities.
        renderer    Provides method to represent game's state graphically
        state       Container for all usefull information about game state

    methods:
        pump_events()   Called every frame to prevent Windows
                        from "program stopped working" message.
        add_entity()    Easy and convenient way to add new entities.
    """
    
    def __init__(self):
        self.state = state.GameState(self)
        self.entities = set()
        self.renderer = renderer.Renderer()
        self.socket = None

    def pump_events(self):
        pygame.event.pump()

    def add_entity(self, entity_type, *args, **kwargs):
        if entity_type == "soldier":
            ent = entities.Soldier(*args, **kwargs)

        self.entities.add(ent)
        self.renderer.render_request_list.append(ent)

    def reset(self):
        self.entities.clear()
        self.renderer.camera = renderer.Camera()
        self.state = state.GameState(self)
