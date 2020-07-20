"""Provides classes for rendering graphics on the screen."""
import os
import functools
import logging
import time

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
        globvar.renderer = self
        # compability things
        if os.name == "nt":
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
                constants.SDL_WINDOW_POS_X,
                constants.SDL_WINDOW_POS_Y
            )

        # setup display
        pygame.init()
        pygame.display.set_caption(constants.WINDOW_CAPTION)
        screen_size = (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.DISPLAY_RECT = pygame.Rect((0, 0), screen_size)
        self.screen = pygame.display.set_mode(screen_size
        )
        self.background = pygame.Surface(screen_size)
        self.background.fill(constants.BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        logger.info("Pygame display initialized")
        
        assets.load_textures()
        # map_array = utils.TilemapFileParser("winclient/assets/maps/test.tm").parse()
        # map_array = utils.TilemapFileParser("winclient/assets/maps/map1.tm").parse()
        map_array = utils.TilemapFileParser("winclient/assets/maps/calib_map.tm").parse()
        self._tmr = TilemapRenderer(map_array)
        self.camera = Camera2D(self, *self._tmr.render_full().get_rect())
        self.frame_clock = pygame.time.Clock()

    # def _draw(self, sprite):
    #     ent_screen_rect = utils.translate_to_screen_rect(sprite.rect, self.camera)
    #     sprite.draw(self.screen, ent_screen_rect, scale=zoom) # area param?

    def update(self):
        start_time = time.time()

        # log some info
        count = sum([1 if s.dirty else 0 for s in globvar.sprites])
        if count > 0:
            logger.info(f"RENDERER: Sprites to update: {count}")

        # call update on all sprites
        globvar.sprites.update()

        # clear and draw dirty sprites
        # FIXME: clearing not working properly
        dirty_rects = globvar.sprites.draw(self.screen, bgd=self.background)

        # update dirty rects
        pygame.display.update(dirty_rects)

        # performance stuff
        max_frame_time = 1000 / constants.MAX_FPS
        frame_time = (time.time() - start_time) * 1000
        frame_time_usage_percent = int(frame_time / max_frame_time * 100)
        if frame_time_usage_percent > 90:
            logger.warning(f"Frame time: {frame_time_usage_percent}% [{int(frame_time)} ms]")
        self.frame_clock.tick(constants.MAX_FPS)
        return frame_time_usage_percent, int(frame_time)

    def _redraw_tilemap(self):
        """Clear screen and draw tilemap. Does not redraw sprites
        (To do so, use renderer.redraw_all method instead).
        """
        x, y = self.camera.rect.topleft
        width, height = self.DISPLAY_RECT.size
        tmprect = pygame.Rect(x, y, width, height)
        self.screen.fill(constants.BACKGROUND_COLOR)
        self.background = self._tmr.render_full(scale=self.camera.get_zoom())
        self.screen.blit(self.background, self.DISPLAY_RECT, tmprect)
        pygame.display.flip()

    def redraw_all(self):
        """Redraw every visible object, including background.
        Do NOT use this every frame.
        """
        self._redraw_tilemap()
        for sprite in globvar.sprites:
            sprite.dirty = 1


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
        default = assets.TEXTURES[0]

        for i in range(rows_num):
            for n_row, item_id in enumerate(self._tilemap_array[i]):
                texture = assets.TEXTURES.get(item_id, default)
                scaled_texture = utils.scale_image(texture, scale)
                result_surface.blit(scaled_texture, (n_row * ts, i * ts))
        return result_surface
                
    def render_area(self, rect):
        raise NotImplementedError