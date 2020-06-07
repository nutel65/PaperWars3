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
        self.image = None # pygame.Surface
        self.rect = None # pygame.Rect
        self.RENDER_PRIORITY = 1 # int
        # SCREEN_STATIC has precedence over MAP_STATIC
        self.MAP_STATIC = False # if true object behaves like part of map while rendering
        self.SCREEN_STATIC = False # determines whether object moves / zooms along with camera
        raise NotImplementedError

    def draw(self, dest_surf, pos_px, area=None, scale=1.0):
        """Intended to be called from renderer.
        Override this method for custom drawing behaviour.
        """
        scaled_image = utils.scale_image(self.image, scale)
        dest_surf.blit(scaled_image, pos_px, area)


class Sprite(Drawable):
    """Entity representable with single image."""
    def __init__(self, pos_px, image, renderer):
        self.image = assets.SPRITES[image]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_px
        self._renderer = renderer
        self.RENDER_PRIORITY = 2
        self.MAP_STATIC = True
        self.SCREEN_STATIC = False

    def get_pos_px(self):
        return self.rect.topleft

    def set_pos_px(self, x, y):
        self.rect.topleft = (x, y)
        self._renderer.render_request_list.append(self)


# class Tile(Drawable):
#     """Represents single tile in tilemap."""
#     def __init__(self, pos_px, texture_id):
#         self.image = assets.TILEMAP_TEXTURES[texture_id]
#         self.rect = self.image.get_rect
#         self.rect.topleft = pos_px
#         self.RENDER_PRIORITY = 1