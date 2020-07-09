"""Implements UI and HUD objects"""
import pygame

import globvar
from src import entities
from src import commands
from src import constants


def get_widget_at(screen_pos):
    for widget in globvar.widgets:
        if widget.rect.collidepoint(screen_pos) and widget.SCREEN_STATIC:
            return widget


class Widget(entities.Drawable):
    # NOTE: For interface variables, check entities.Drawable docstring
    # NOTE: SCREEN_STATIC has precedence over MAP_STATIC
    RENDER_PRIORITY = 5
    MAP_STATIC = False # if true object behaves like part of map while rendering
    SCREEN_STATIC = True # determines whether object moves / zooms along with camera


class Button(Widget):
    """If background_image supplied:
    - button_size is ignored, and set to fit image 
    - fill_color is ignored
    """
    def __init__(
            self, 
            topleft_pos,
            button_size=None,
            fill_color=None,
            background_image=None,
            # desc_on_hover="",
            # desc_on_click="",
            command=None,
            *command_args,
            **command_kwargs
        ):
        if background_image:
            self.image = background_image
        elif button_size:
            if not fill_color:
                raise ValueError("fill_color not specified.")
            self.image = pygame.Surface(button_size)
            self.image.fill(fill_color)
        else:
            raise ValueError("size or background_image not supplied.")
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft_pos
        self.command = command
        self.command_args = command_args
        self.command_kwargs = command_kwargs

    def on_click(self, *args, **kwargs):
        self.command.execute(
            *self.command_args, *args, **self.command_kwargs, **kwargs
        )

class TextArea(Widget):
    pass