import pygame
import game_objects
import commands
import collections
import utils
import os

class Camera:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._zoom = 1.0
        self._width = width
        self._height = height

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)

    def move(self, vector):
        # todo: use pygame.vector2 for vector variable
        ...
    
    def set_on_alter_state_command(self, command):
        self._on_alter_state_command = command

    def zoom_in(self):
        ...

    def zoom_out(self):
        ...



class Game:
    def __init__(self):
        self.entities = set()
        self.command_queue = collections.deque() # ???
        self.renderer = Renderer()
        self.renderer.camera.set_on_alter_state_command(
            commands.RecalculateEntitiesVisibilityCommand(self))
        self.renderer.visible_entities = self.get_visible_entities()

    def get_visible_entities(self):
        return {ent for ent in self.entities if ent.visible}

    def pump_events(self):
        pygame.event.pump()

    def add_entity(self, entity_type, *args, **kwargs):
        if entity_type == "soldier":
            ent = game_objects.Soldier(*args, **kwargs)

        self.entities.add(ent)
        self.renderer.layers[ent.RENDER_PRIORITY].add(ent)
        self.renderer.render_queue.append(ent)