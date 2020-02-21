import pygame
import entities
import commands
import collections
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

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.camera = Camera(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.dirty_rects = []
        self.render_list = []
        self.visible_entities = {}
        self.layers = {}

        self.background = pygame.Surface(self.screen.get_rect().size)
        self.background.fill((0, 128, 0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
    def get_window_size(self):
        return (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def add_layer(self, order: int):
        self.layers[order] = utils.Layer(order)

    def get_entity_layer(self, entity):
        for k, v in self.layers.items():
            if entity in v:
                return k

    def draw(self, entity):
        print("draw", entity)
        screen_x = entity.rect.topleft[0] - self.camera.get_rect().topleft[0]
        screen_y = entity.rect.topleft[1] - self.camera.get_rect().topleft[1]
        if entity.image.get_alpha() is not None:
            self.clear(entity)

        self.screen.blit(entity.image, (screen_x, screen_y)) # area param?
        self.dirty_rects.append(entity.rect)
    
    def clear(self, entity):
        print("clear", entity)
        screen_x = entity.rect.topleft[0] - self.camera.get_rect().topleft[0]
        screen_y = entity.rect.topleft[1] - self.camera.get_rect().topleft[1]

        # search for overlapping entities
        overlapping = []
        for _, layer in self.layers:
            for e in layer:
                if entity.rect.colliderect(e.rect) and e != entity:
                    overlapping.append(e)
        
        # sort overlapping entities by layer

        self.screen.blit(self.background, (screen_x, screen_y), entity.rect) # area param?
        self.dirty_rects.append(entity.rect)

    def update(self):
        print("---- UPDATE ----")

        # sort render list by layer
        self.render_list.sort(key=self.get_entity_layer, reverse=True)

        # draw each element in render list
        while self.render_list:
            self.draw(self.render_list.pop())

        # update dirty rects
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()

        
    def draw_HUD(self): ...

    def draw_GUI(self): ...


class Game:
    def __init__(self):
        self.entities = set()
        self.command_queue = collections.deque() # ???
        self.renderer = Renderer()
        self.renderer.camera.set_on_alter_state_command(
            commands.RecalculateEntitiesVisibilityCommand(self))
        self.renderer.visible_entities = self.get_visible_entities()

    def get_visible_entities(self):
        return {ent for ent in self.entities if ent.visible}

    def pump_events(self):
        pygame.event.pump()

    def add_entity(self, entity_type, layer_name, *args, **kwargs):
        if entity_type == "soldier":
            ent = entities.Soldier(*args, **kwargs)

        self.entities.add(ent)
        self.renderer.layers[layer_name].add(ent)
        self.renderer.render_list.append(ent)