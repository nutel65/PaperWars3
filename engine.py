import pygame
import entities
import os

class Camera:
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
    
    def zoom_in(self):
        ...

    def zoom_out(self):
        ...

    # request recalculate_entities_activity() somehow


class Renderer:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (650, 30)
        pygame.init()
        pygame.display.set_caption("PaperWars")
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.camera = Camera(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def get_window_size(self):
        return (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def _draw(self): ...
            
    def get_active_entities(self): ...

    def draw_HUD(self): ...

    def draw_GUI(self): ...


class Game:
    def __init__(self):
        self.renderer = Renderer()
        self.entities = []
        self.command_queue = None

    def start_loop(self):
        ...

    def recalculate_entities_activity(self):
        rect = self.renderer.camera.get_rect()
        indices = rect.collidelistall(self.entities)

        for i in range(len(self.entities)):
            if i in indices:
                self.entities[i].active = True
            else:
                self.entities[i].active = False
    