"""Every game object that user interacts with, 
should implements one of classes included in this module.
"""
import logging

import pygame

import globvar
from src import utils
from src import commands

logger = logging.getLogger(__name__)

def get_sprite_at(pos_px):
    # TODO: TEST IT
    for ent in globvar.entities:
        if ent.rect.collidepoit(pos_px):
            return ent

class Entity2D():
    """Represents any game object"""
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return f"{type(self).__name__}({self.rect})"


class Drawable(Entity2D):
    """Represents object that can be drawn.
    Interface variables:
    image (required) <pygame.Surface>
    rect (required) <pygame.Rect>
    previous_rect (optional) <pygame.Rect> # set it, after object moved
    hidden # if True, skip the entity during rendering.
    """
    # NOTE: SCREEN_STATIC has precedence over MAP_STATIC
    RENDER_PRIORITY = 1 # int
    MAP_STATIC = False # if true object behaves like part of map while rendering
    SCREEN_STATIC = False # determines whether object moves / zooms along with camera

    def draw(self, dest_surf, pos_px, area=None, scale=1.0):
        """Intended to be called from renderer.
        Override this method for custom drawing behaviour.
        """
        scaled_image = utils.scale_image(self.image, scale)
        dest_surf.blit(scaled_image, pos_px, area)

    def get_pos(self):
        """Return global top left position of entity (in pixels)."""
        return self.rect.topleft

    def _set_previous_rect(self):
        self.previous_rect = self.rect.copy()

    def set_pos(self, x, y):
        """Set / change object position (top left corner) to given position (in pixels)."""
        self._set_previous_rect()
        self.rect.topleft = (x, y)
        globvar.render_request_list.append(self)


class Sprite(Drawable):
    """Entity representable with single image."""
    MAP_STATIC = True
    def __init__(self, pos_px, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_px


class Soldier(Sprite):
    def __init__(self, pos_px, image):
        super().__init__(pos_px, image)
        self._hp = 5
        self._ad = 2

    def attack(self, entity):
        entity.minus_hp(self._ad)

    def minus_hp(self, amount):
        logger.info("Entity is attacked")
        self._hp -= amount
        if self._hp <= 0:
            logger.info("Entity killed")
            self.hidden = True # TODO: Delete the entity permamently
            globvar.render_request_list.append(self)
            self._set_previous_rect()