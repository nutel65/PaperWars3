"""Every game object that user interacts with, 
should implements one of classes included in this module.
"""
import logging

import pygame

import globvar
from src import utils

logger = logging.getLogger(__name__)


class Sprite(pygame.sprite.DirtySprite):
    """Represents object that can be drawn.
    Interface variables:

    image (required) <pygame.Surface>

    rect_global (required) <pygame.Rect>

    # previous_rect (optional) <pygame.Rect> # set it, after object moved

    visible # if False, skip the sprite during rendering.
    """
    def __init__(self):
        super().__init__(globvar.sprites)
        # self.visible = 1
        # self.dirty = 1
        # self.layer = 0
        # self.rect_global = None

    def update(self, pos=None, *args, **kwargs, ):
        if pos:
            self.rect_global.topleft = pos
            self.dirty = 1

    @property
    def rect(self):
        return utils.translate_to_screen_rect(self.rect_global, globvar.renderer.camera)
        
    def __str__(self):
        return f"{type(self).__name__}({self.rect_})"


class Soldier(Sprite):
    def __init__(self, pos_px, image):
        super().__init__()
        self.image = image
        self.rect_global = image.get_rect(topleft=pos_px)
        self._hp = 5
        self._ad = 2

    def attack(self, sprite):
        sprite.minus_hp(self._ad)

    def minus_hp(self, amount):
        logger.info("sprite is attacked")
        self._hp -= amount
        if self._hp <= 0:
            logger.info("sprite killed")
            self.visible = False # TODO: Delete the sprite permamently