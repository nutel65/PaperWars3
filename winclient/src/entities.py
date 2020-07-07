"""Every game object that user interacts with, 
should implements one of classes included in this module.
"""
import assets
import pygame
from src import utils
from src import commands

class Entity2D():
    """Represents any game object"""
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return f"{type(self).__name__}({self.rect})"


class Drawable(Entity2D):
    """Represents object that can be drawn"""
    def __init__(self, *args, **kwargs):
        # NOTE: SCREEN_STATIC has precedence over MAP_STATIC
        self.RENDER_PRIORITY = 1 # int
        self.MAP_STATIC = False # if true object behaves like part of map while rendering
        self.SCREEN_STATIC = False # determines whether object moves / zooms along with camera
        self.image = None # pygame.Surface
        self.rect = None # pygame.Rect
        raise NotImplementedError("Override this method")

    def draw(self, dest_surf, pos_px, area=None, scale=1.0):
        """Intended to be called from renderer.
        Override this method for custom drawing behaviour.
        """
        scaled_image = utils.scale_image(self.image, scale)
        dest_surf.blit(scaled_image, pos_px, area)


class Sprite(Drawable):
    """Entity representable with single image."""
    def __init__(self, pos_px, image, renderer):
        self.RENDER_PRIORITY = 2
        self.MAP_STATIC = True
        self.SCREEN_STATIC = False
        self.image = assets.SPRITES[image]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_px
        self._renderer = renderer
        self.previous_rect = None # set after changinging object's position

    def get_pos(self):
        """Return global top left position of entity (in pixels)."""
        return self.rect.topleft

    def _set_previous_rect(self):
        self.previous_rect = self.rect.copy()

    def set_pos(self, x, y):
        """Set / change object position (top left corner) to given position (in pixels)."""
        self._set_previous_rect()
        self.rect.topleft = (x, y)
        # print("prev rect", self.previous_rect)
        # print("current rect", self.rect)
        self._renderer.render_request_list.append(self)

class Soldier(Sprite):
    def __init__(self, pos_px, image, renderer):
        super().__init__(pos_px, image, renderer)
        self._hp = 5
        self._ad = 2

    def attack(self, entity):
        entity.minus_hp(self._ad)

    def minus_hp(self, amount):
        utils.log("Entity is attacked")
        self._hp -= amount
        if self._hp <= 0:
            utils.log("Entity killed")
            self._renderer.render_request_list.append(self)
            self._set_previous_rect()


# class Tile(Drawable):
#     """Represents single tile in tilemap."""
#     def __init__(self, pos_px, texture_id):
#         self.image = assets.TILEMAP_TEXTURES[texture_id]
#         self.rect = self.image.get_rect
#         self.rect.topleft = pos_px
#         self.RENDER_PRIORITY = 1