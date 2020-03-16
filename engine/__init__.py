"""This file imports main engine class 'Game'"""
import pygame
from engine import game_socket
from engine import render
from src import commands
from src import state
from src import entities

class Game:
    """Main engine class, that connects together other engine pieces.

    variables:
        entities    List of all entities.
        renderer    Represents game state graphically.
        state       Aggregation for all usefull information about game state.

    methods:
        add()       Easy and convenient way to add new entities.
        reset()     Resets state of game to default settings 
    """
    
    def __init__(self):
        self.state = state.GameState(self)
        self.entities = set()
        self.renderer = render.Renderer()
        self.socket = None

    def add(self, entity_type, *args, **kwargs):
        """Easy and convenient way to add new entities."""
        if entity_type == "soldier":
            ent = entities.Soldier(*args, **kwargs)
        elif entity_type == "button":
            raise NotImplementedError
        else:
            raise ValueError(f"Entity type {entity_type} does not exist.")
        self.entities.add(ent)
        self.renderer.render_request_list.append(ent)

    def reset():
        commands.ResetGameCommand(self).execute()
