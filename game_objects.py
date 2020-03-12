import pygame
import assets


class Drawable():
    def __init__(self):
        self.rect = None # pygame.Rect
        self.image = None # pygame.Surface
        self.RENDER_PRIORITY = -1


class Entity():
    def __init__(self, *args, **kwargs):
        self.rect = None
        self.image = None

    def __str__(self):
        return f"{type(self).__name__}({self.rect})"
        

class Soldier(Entity):
    def __init__(self, pos, image):
        self.image = assets.SPRITES[image]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.RENDER_PRIORITY = 1