import pygame
from src import utils

class Camera2D():
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
        self.renderer.update_all()

    def set_center(self, new_center=None):
        """Set a desired new global position (of map) as the center of the camera view."""
        rdr = self.renderer
        if not new_center:
            new_center = utils.local_to_global(rdr, rdr.camera.tilemap_rect.center)
        display_center = rdr.DISPLAY_RECT.center
        map_center = utils.global_to_local(rdr, new_center)
        shift_x = map_center[0] - display_center[0]
        shift_y = map_center[1] - display_center[1]
        x, y = self.rect.topleft
        self.set_topleft((x + shift_x, y + shift_y))
        rdr.update_all()

    def _set_zoom_id(self, zoom_id):
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

    def __str__(self):
        return f"{type(self).__name__}({self.rect}, ({self.get_zoom()}x))"
