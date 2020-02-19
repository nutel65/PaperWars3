import pygame as _pygame
# todo check out inheritance from pygame.Sprite
class Entity:
    def __init__(self, pos):
        self.active = True
        self.surface = _pygame.Surface()
        self.rect = self.surface.get_rect()

class Soldier(Entity):
    ...