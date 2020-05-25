"""Every game object that user interacts with, 
should implements one of classes included in this module.
"""
import assets
import pygame
from engine import utils
from src import commands

class Entity():
    """Represents any game object"""
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return f"{type(self).__name__}({self.rect})"


class Camera(Entity):
    """Alters field of view and rendering. Allows to change zoom, and move camera."""
    def __init__(self, renderer, camera_x, camera_y, view_width, view_height):
        self.renderer = renderer
        self.ZOOM_VALUES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 0.9, 1.0, 1.1, 1.25, 1.5, 1.8]
        self.zoom_id = self.ZOOM_VALUES.index(1.0)
        # default rect used to scales 
        self._default_rect = pygame.Rect(camera_x, camera_y, view_width, view_height)
        # what camera sees
        self.rect = pygame.Rect(camera_x, camera_y, view_width, view_height)
        self.tilemap_rect = self.rect.copy()

    def set_topleft(self, dest_px):
        """Set desired global position as top left corner of camera."""
        x, y = dest_px
        self.rect.topleft = dest_px
        self.tilemap_rect.topleft = (-x, -y)

    def set_center(self, new_center):
        """Set desired global position (of map) as a center of display."""
        display_center = self.renderer.DISPLAY_RECT.center
        map_center = utils.global_to_local(self.renderer, new_center)
        shift_x = map_center[0] - display_center[0]
        shift_y = map_center[1] - display_center[1]
        x, y = self.rect.topleft
        self.set_topleft((x + shift_x, y + shift_y))

    def set_zoom_id(self, zoom_id):
        """Set camera's zoom value (and recalculate rects)."""
        if zoom_id < 0:
            raise ValueError("zoom_id cannot be negative.")
        try:
            zoom_value = self.ZOOM_VALUES[zoom_id]
        except IndexError:
            raise ValueError("zoom_id out of range")
        self.zoom_id = zoom_id
        w, h = self._default_rect.size
        self.rect.size = (w // zoom_value, h // zoom_value)
        self.tilemap_rect.size = (w * zoom_value, h * zoom_value)

    def get_zoom(self):
        """Returns true zoom value."""
        tile_size = 32
        basic_zoom = self.ZOOM_VALUES[self.zoom_id]
        true_zoom = int(tile_size * basic_zoom) / tile_size
        return true_zoom

    def normalize_position(self, bound_rect):
        """Shift camera position to fit camera.rect in renderer.DISPLAY_RECT."""
        ...


class Drawable(Entity):
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


class Soldier(Drawable):
    def __init__(self, pos_px, image):
        self.image = assets.SPRITES[image]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_px
        self.RENDER_PRIORITY = 2
        self.MAP_STATIC = True
        self.SCREEN_STATIC = False

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