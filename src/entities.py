"""Every game object that user interacts with, 
should implements one of classes included in this module.
"""
import assets
import pygame
from src import commands

class Entity():
    """Represents any game object"""
    def __init__(self, *args, **kwargs):
        self.rect = None

    def __str__(self):
        return f"{type(self).__name__}({self.rect})"


class Camera(Entity):
    """Alters field of view and rendering. Allows to change zoom, and move camera."""
    def __init__(self, camera_x, camera_y, view_width, view_height):
        self._zoom = 1.0
        # default rect used to scale
        self._default_rect = pygame.Rect(camera_x, camera_y, view_width, view_height)
        # what camera sees
        self.rect = pygame.Rect(camera_x, camera_y, view_width, view_height)

    def move(self, pos_px):
        self.rect.topleft = pos_px

    def set_zoom(self, zoom_value):
        self._zoom = zoom_value
        w, h = self._default_rect.size
        self.rect.size = (w // zoom_value, h // zoom_value)

    def get_zoom(self):
        return self._zoom


class Drawable(Entity):
    """Represents object that can be drawn"""
    def __init__(self, *args, **kwargs):
        self.image = None # pygame.Surface
        self.rect = None # pygame.Rect
        self.RENDER_PRIORITY = None # int

    def draw(self, dest_surf, pos_px, area=None):
        """Intended to be called from renderer."""
        dest_surf.blit(self.image, pos_px, area)


class Soldier(Drawable):
    def __init__(self, pos_px, image):
        self.image = assets.SPRITES[image]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_px
        self.RENDER_PRIORITY = 2

    def get_pos_px(self):
        return self.rect.topleft

    def set_pos_px(self, x, y):
        self.rect.topleft = (x, y)


# class Tile(Drawable):
#     """Represents single tile in tilemap."""
#     def __init__(self, pos_px, texture_id):
#         self.image = assets.TILEMAP_TEXTURES[texture_id]
#         self.rect = self.image.get_rect
#         self.rect.topleft = pos_px
#         self.RENDER_PRIORITY = 1