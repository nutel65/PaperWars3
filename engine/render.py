"""Provides classes for rendering graphics on the screen."""
import pygame
import os
import functools
import assets
from src import utils
from src import commands
from src.entities import Camera


class Renderer:
    """Provides methods for rendering entities to screen.
    public methods:
        get_window_size() returns (int, int)
        update()
        update_tilemap()
        enqueue_all()
    """
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (650, 30)
        pygame.init()
        pygame.display.set_caption("PaperWars")

        self.MAX_FPS = 60
        self.frame_clock = pygame.time.Clock()

        # append directly here in order render object
        self.render_request_list = []
        # holds pieces of screen to be updated
        self.dirty_rects = []

        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480
        self.DISPLAY_RECT = pygame.Rect(50, 50, self.WINDOW_WIDTH - 100, self.WINDOW_HEIGHT - 100)
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        utils.log("Pygame display initialized")


        assets.load_textures()
        # array = utils.TilemapFileParser("assets/maps/test.tm").parse()
        array = utils.TilemapFileParser("assets/maps/map1.tm").parse()
        self._tmr = TilemapRenderer(array)
        self.camera = Camera(*self._tmr.render_full().get_rect())

    def get_window_size(self):
        return (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def _draw(self, entity):
        """Render single entity (call its draw() method)"""
        screen_x = entity.rect.topleft[0] - self.camera.rect.topleft[0]
        screen_y = entity.rect.topleft[1] - self.camera.rect.topleft[1]
        # # additional clear if object's image is transparent (to prevent overlapping).
        # if entity.image.get_alpha() is not None:
        #     self._clear(entity)
        # self.screen.blit(entity.image, (screen_x, screen_y)) # area param?
        entity.draw(self.screen, (screen_x, screen_y)) # area param?
        self.dirty_rects.append(entity.rect)
    
    def _clear(self, entity):
        """Draw background over current object's position"""
        screen_x = entity.rect.topleft[0] - self.camera.rect.topleft[0]
        screen_y = entity.rect.topleft[1] - self.camera.rect.topleft[1]

        self.screen.blit(self.background, (screen_x, screen_y), entity.rect)
        self.dirty_rects.append(entity.rect)

    def update(self):
        """Processes render_request_list and dirty_rects.
        Call this at the end of main loop.
        """ 
        # sort render_request_list to preserve proper order of rendering
        self.render_request_list.sort(key=lambda x: x.RENDER_PRIORITY, reverse=True)
        # redraw each element in render list and then remove them from that list
        counter = 0
        while self.render_request_list:
            ent = self.render_request_list.pop()
            self._clear(ent)
            self._draw(ent)
            counter += 1
        if counter > 0:
            utils.log(f"RENDERER: Rendered total {counter} objects")

            
        # update dirty rects
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()
        self.frame_clock.tick(self.MAX_FPS)
    
    def enqueue_all(self, iterable):
        self.render_request_list.extend(iterable)

    def update_tilemap(self):
        x, y = self.camera.rect.topleft
        width, height = self.DISPLAY_RECT.size
        tmprect = pygame.Rect(x, y, width, height)
        self.screen.fill((0, 128, 0))
        self.background = self._tmr.render_full(scale=self.camera._zoom)
        self.screen.blit(self.background, self.DISPLAY_RECT, tmprect)
        pygame.display.flip()
        utils.log("RENDERER: Rendered tilemap")



class TilemapRenderer():
    """Provides methods for rendering tilemaps."""
    def __init__(self, tilemap_array):
        self._tilemap_array = tilemap_array

    @functools.lru_cache()
    def render_full(self, scale=1.0):
        """Renders whole tilemap and returns it as 'pygame.Surface'"""
        # Set new tile size.
        ts = int(32 * scale)
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



