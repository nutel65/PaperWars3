import pygame
import entities
import commands
import utils
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
    
    def set_on_alter_state_command(self, command):
        self._on_alter_state_command = command

    def zoom_in(self):
        ...

    def zoom_out(self):
        ...


class Renderer:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (650, 30)
        pygame.init()
        pygame.display.set_caption("PaperWars")
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.camera = Camera(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.dirty_rects = []
        self.background = pygame.Surface(self.screen.get_rect().topleft)
        self.background.fill(0, 128, 0)
        
        # self.draw_queue = utils.DrawQueue()

    def get_window_size(self):
        return (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def draw(self, entity):
        screen_x = entity.rect.topleft[0] - camera.rect.topleft[0]
        screen_y = entity.rect.topleft[1] - camera.rect.topleft[1]
        self.screen.blit(entity.surface, (screen_x, screen_y)) # area param?
        self.dirty_rects.append(entity.rect)
    
    def clear(self, entity):
        screen_x = entity.rect.topleft[0] - camera.rect.topleft[0]
        screen_y = entity.rect.topleft[1] - camera.rect.topleft[1]
        self.screen.blit(self.background, (screen_x, screen_y), entity.rect) # area param?
        self.dirty_rects.append(entity.rect)

    def draw_HUD(self): ...

    def draw_GUI(self): ...


class Game:
    def __init__(self):
        self.renderer = Renderer()
        self.renderer.camera.set_on_alter_state_command(
            commands.RecalculateEntitiesVisibilityCommand(self))
        self.entities = []
        self.command_queue = commands.CommandQueue() # ???

    def get_visible_entities(self):
        return [e for e in self.entities if e.visible]

    def start_loop(self):
        while(True):
            pass
    