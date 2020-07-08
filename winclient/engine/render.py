"""Provides classes for rendering graphics on the screen."""
import os
import functools
import logging

import pygame

import assets
import globvar
from src import utils
from src import constants
from engine.camera import Camera2D

logger = logging.getLogger(__name__)

class Renderer2D:
    """2D rendering to the screen."""
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
            constants.SDL_WINDOW_POS_X,
            constants.SDL_WINDOW_POS_Y
        )
        pygame.init()
        pygame.display.set_caption(constants.WINDOW_CAPTION)
        self.frame_clock = pygame.time.Clock()
        # append directly here in order render object
        self.render_request_list = []
        # holds pieces of screen to be updated
        self.dirty_rects = []
        self.DISPLAY_RECT = pygame.Rect(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        logger.info("Pygame display initialized")
        assets.load_textures()
        # array = utils.TilemapFileParser("assets/maps/test.tm").parse()
        # array = utils.TilemapFileParser("assets/maps/map1.tm").parse()
        array = utils.TilemapFileParser("winclient/assets/maps/calib_map.tm").parse()
        self._tmr = TilemapRenderer(array)
        self.camera = Camera2D(self, *self._tmr.render_full().get_rect())
        self.enqueue_all()

    def get_window_size(self):
        return (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)

    def _in_render_area(self, ent):
        """Returns True if entity is located in draw area."""
        if ent.SCREEN_STATIC:
            ent_screen_rect = ent.rect
        else:
            ent_screen_rect = utils.translate_to_screen_rect(
                ent.rect, self.camera, display_rect=self.DISPLAY_RECT)
        # If ent.MAP_STATIC, then filter out requests which are completely out of self.DISPLAY_RECT
        # else just filter out those that are completely out of self.screen.rect
        if ent.MAP_STATIC:
            if ent_screen_rect.colliderect(self.DISPLAY_RECT):
                return True
        elif ent_screen_rect.colliderect(self.screen.get_rect()):
            return True
        return False

    def _draw(self, entity):
        """Render single entity (call its draw() method)."""
        # TODO: Draw parially entities that are parially out of self.DISPLAY_RECT
            
        if entity.SCREEN_STATIC:
            # Don't scale entity while it is SCREEN_STATIC.
            zoom = 1.0
            # Don't
            ent_screen_rect = entity.rect
        else:
            zoom = self.camera.get_zoom()
            # DISPLAY_RECT DISABLED
            ent_screen_rect = utils.translate_to_screen_rect(entity.rect, self.camera)

        entity.draw(self.screen, ent_screen_rect, scale=zoom) # area param?
        self.dirty_rects.append(ent_screen_rect)
        return 1
    
    def _clear(self, entity):
        """Draw background over last object's position."""
        # if entity.previous_rect is set, then use it instead of entity.rect
        rect_to_clear = entity.previous_rect
        if not rect_to_clear:
            logger.debug("Omitted _clear function.")
            return 0
            # testing if works ^
        if entity.SCREEN_STATIC:
            logger.debug("clearing static object", type="DEBUG")
            ent_screen_rect = rect_to_clear
        else:
            ent_screen_rect = utils.translate_to_screen_rect(rect_to_clear, self.camera)
        zoom = self.camera.get_zoom()
        x = rect_to_clear.x * zoom
        y = rect_to_clear.y * zoom
        size = utils.scale_rect(rect_to_clear, scale=zoom).size
        tr = pygame.Rect((x, y), size)

        self.screen.blit(self.background, ent_screen_rect.topleft, tr)
        self.dirty_rects.append(ent_screen_rect)
        entity.previous_rect = None
        return 1

    def update(self):
        """Processes render_request_list and dirty_rects.
        Call this at the end of main loop.
        """ 
        counter = 0
        for ent in self.render_request_list:
            count1 = self._clear(ent)
            counter += count1

        # Filter out redundant entities to draw .
        self.render_request_list = list(filter(self._in_render_area, self.render_request_list))

        # sort render_request_list to preserve proper order of rendering
        self.render_request_list.sort(key=lambda x: x.RENDER_PRIORITY, reverse=True)

        # redraw each element in render list and then remove them from that list
        while self.render_request_list:
            ent = self.render_request_list.pop()
            if ent._hp <= 0:
                logger.debug("skipped rendering dead entity")
                continue
            count2 = self._draw(ent)
            counter += count2

        if counter > 0:
            logger.info(f"RENDERER: rendered total {counter} rectangles")

        # update dirty rects
        pygame.display.update(self.dirty_rects)
        if self.dirty_rects:
            logger.info(f"RENDERER:  updated total {len(self.dirty_rects)} rectangles")
        self.dirty_rects.clear()
        self.frame_clock.tick(constants.MAX_FPS)
    
    def enqueue_all(self, from_iterable=None):
        """Add all entities to render_request_list from iterable
        or globvar.entities (by default)
        """
        if not from_iterable:
            from_iterable = globvar.entities
        self.render_request_list.extend(from_iterable)

    def _redraw_tilemap(self):
        """Clear screen and draw tilemap. Does not redraw entities
        (To do so, use renderer.update_all method instead).
        """
        x, y = self.camera.rect.topleft
        width, height = self.DISPLAY_RECT.size
        tmprect = pygame.Rect(x, y, width, height)
        self.screen.fill(constants.BACKGROUND_COLOR)
        self.background = self._tmr.render_full(scale=self.camera.get_zoom())
        self.screen.blit(self.background, self.DISPLAY_RECT, tmprect)
        self.dirty_rects.append(self.DISPLAY_RECT)

    def update_all(self):
        """Redraw every visible object, including background redraw.
        Do NOT use this every frame.
        """
        self._redraw_tilemap()
        self.enqueue_all()


class TilemapRenderer():
    def __init__(self, tilemap_array):
        self._tilemap_array = tilemap_array

    @functools.lru_cache()
    def render_full(self, scale=1.0):
        """Renders whole tilemap and returns it as 'pygame.Surface'"""
        # Set new tile size.
        ts = scale * constants.TILE_SIZE
        # Get number of rows and columns in tilemap array.
        rows_num, cols_num = self._tilemap_array.shape
        # Create tilemap surface.
        result_surface = pygame.Surface((cols_num * ts, rows_num * ts))
        # Default texture if texture id not found in assets.
        default = assets.TILEMAP_TEXTURES[0]
        for i in range(rows_num):
            for n_row, item_id in enumerate(self._tilemap_array[i]):
                texture = assets.TILEMAP_TEXTURES.get(item_id, default)
                scaled_texture = utils.scale_image(texture, scale)
                result_surface.blit(scaled_texture, (n_row * ts, i * ts))
        return result_surface
                

    def render_area(self, rect):
        raise NotImplementedError