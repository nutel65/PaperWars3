import pygame

class Renderer:
    """Provides methods for rendering entities to screen.
    Methods:
        get_window_size() -> (Int, Int)
        draw(Drawable) -> None
        clear(Drawable) -> None
        update() -> None

    """
    def __init__(self, game):
        self.game = game

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (650, 30)
        pygame.init()
        pygame.display.set_caption("PaperWars")

        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.camera = Camera(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # append directly here in order render object
        self.render_request_list = []

        # holds pieces of screen to be updated
        self.dirty_rects = []

        # self.layers = {}
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

        # search for overlapping entities
        # overlapping = []
        # for _, layer in self.layers:
        #     for e in layer:
        #         if entity.rect.colliderect(e.rect) and e != entity:
        #             overlapping.append(e)
        

        self.screen.blit(self.background, (screen_x, screen_y), entity.rect) # area param?
        self.dirty_rects.append(entity.rect)

    def update(self):
        """Processes render_request_list and dirty_rects.
        Call this at the end of main loop.
        """ 
        print("---- UPDATE ----")

        # sort render_request_list to preserve proper order of rendering
        self.render_request_list.sort(key=lambda x: x.RENDER_PRIORITY, reverse=True)

        # redraw each element in render list and then remove them from to-render list
        while self.render_request_list:
            ent = render_request_list.pop()
            self.clear(self.ent)
            self.draw(self.ent)

        # update dirty rects
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()

        
    def draw_HUD(self): ...

    def draw_GUI(self): ...


class Camera:
    """Alters field of view. Allows to zoom in, zoom out, and move camera."""
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._zoom = 1.0
        self._width = width
        self._height = height

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)

    def move(self, vector):
        # todo: use pygame.vector2 for vector variable
        ...
    
    # def set_on_alter_state_command(self, command):
    #     self._on_alter_state_command = command

    def zoom_in(self):
        ...

    def zoom_out(self):
        ...