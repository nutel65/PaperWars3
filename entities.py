import pygame

# todo check out inheritance from pygame.Sprite
class Entity:
    def __init__(self, pos):
        self.visible = True # is object inside camera view
        self.surface = pygame.Surface(10, 10)
        self.surface.fill(255, 0, 0)
        self.rect = self.surface.get_rect()

    # def move_to(self, )

class Soldier(Entity):
    ...