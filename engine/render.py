import pygame
import os
import functools
import assets

class Renderer:
    """Provides methods for rendering entities to screen.
    Methods:
        get_window_size() -> (Int, Int)
        draw(Drawable) -> None
        clear(Drawable) -> None
        update() -> None
    """
    
    def __init__(self):

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (650, 30)
        pygame.init()
        pygame.display.set_caption("PaperWars")

        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        print("[Info]: Pygame display initialized")
        self.camera = Camera(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # append directly here in order render object
        self.render_request_list = []

        # holds pieces of screen to be updated
        self.dirty_rects = []

        # setup and draw black background
        self.background = pygame.Surface(self.screen.get_rect().size)
        self.background.fill((0, 128, 0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
    def get_window_size(self):
        return (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        

    # def add_layer(self, order: int):
    #     self.layers[order] = utils.Layer(order)

    # def get_entity_layer(self, entity):
    #     for k, v in self.layers.items():
    #         if entity in v:
    #             return k

    def draw(self, entity):
        """Render single entity"""
        print("draw", entity)
        screen_x = entity.rect.topleft[0] - self.camera.get_rect().topleft[0]
        screen_y = entity.rect.topleft[1] - self.camera.get_rect().topleft[1]

        # take care of background blit if object's image is transparent
        if entity.image.get_alpha() is not None:
            self.clear(entity)

        self.screen.blit(entity.image, (screen_x, screen_y)) # area param?
        self.dirty_rects.append(entity.rect)
    
    def clear(self, entity):
        """Draw background over current object's position"""
        print("clear", entity)
        screen_x = entity.rect.topleft[0] - self.camera.get_rect().topleft[0]
        screen_y = entity.rect.topleft[1] - self.camera.get_rect().topleft[1]

        self.screen.blit(self.background, (screen_x, screen_y), entity.rect) # area param?
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
            self.clear(ent)
            self.draw(ent)
            counter += 1
        if counter > 0:
            print(f"[Info]: Rendered {counter} objects")

        # update dirty rects
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()

        
    def draw_HUD(self): ...

    def draw_GUI(self): ...


class Camera:
    """Alters field of view. Allows to zoom in, zoom out, and move camera."""

    def __init__(self, camera_x, camera_y, view_width, view_height, output_width=None, output_height=None):
        self._zoom = 1.0
        self._camera_x = camera_x
        self._camera_y = camera_y
        self._view_width = view_width
        self._view_height = view_height
        self._output_width = output_width
        self._output_height = output_height

    def get_rect(self):
        return pygame.Rect(self._camera_x, self._camera_y, self._view_width, self._view_height)

    def move(self, vector):
        # todo: use pygame.vector2 for vector variable
        ...

    def zoom_in(self):
        ...

    def zoom_out(self):
        ...

    def translate_rect(rect):
        ...


class TilemapRenderer():
    def __init__(self, tilemap_array):
        self._tilemap_array = tilemap_array


    @functools.lru_cache
    def render_full(self, scale=1.0):
        height, width = self._tilemap_array.shape
        result_surface = pygame.Surface((width * 32 * scale, height * 32 * scale))
        texture_surface_template = pygame.Surface((32 * scale, 32 * scale))
        for i in range(height):
            for n_row, item_code in enumerate(array[i]):
                texture = assets.TILEMAP_TEXTURES.get(item_code, assets.TILEMAP_TEXTURES["default"])
                scaled_texture = pygame.transform.scale(texture, texture_surface_template)
                new_surface.blit() (n_row * 32, i * 32) # blit scaled_texture to this
        return new_surface
    
    def render_area(self, rect):
        ...



