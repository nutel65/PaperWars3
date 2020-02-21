import pygame
import assets


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