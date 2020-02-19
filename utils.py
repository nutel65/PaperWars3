import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


def exit_check(event):
    if event.type == QUIT:
        sys.exit(0)
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            sys.exit(0)


def index_to_px(index, shift=(0, 0)):
    x, y = index
    index = (x * 32 + shift[0], y * 32 + shift[1])
    return index


def px_to_index(px, shift=(0, 0)):
    x, y = px
    x -= shift[0]
    y -= shift[1]
    px = (x // 32, y // 32)
    return px


def shifted_point(coords, vector) -> pygame.Rect:
    x, y = coords
    xv, yv = vector
    return (x + xv, y + yv)


def shifted_rect(rect, vector) -> pygame.Rect:
    tmp_rect = rect.copy()
    x, y = tmp_rect.topleft
    tmp_rect.topleft = (x - vector[0], y - vector[1])
    return tmp_rect


def load_textures():
    return {
        0: pygame.image.load("./editor/templates/fill.png").convert_alpha(),
        1: pygame.image.load("./resources/textures/grass.png").convert(),
        2: pygame.image.load("./resources/textures/water.png").convert(),
        3: pygame.image.load("./resources/textures/sand.png").convert(),
        4: pygame.image.load("./resources/textures/dirt.png").convert(),
        5: pygame.image.load("./resources/textures/snow.png").convert(),
        6: pygame.image.load("./resources/textures/water32.png").convert(),
        7: pygame.image.load("./resources/textures/forest32.png").convert(),
        8: pygame.image.load("./resources/textures/grass32.png").convert(),
    }


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def wrap_func(func, *args, **kwargs):
    def wrapper():
        return func(*args, **kwargs)
    return wrapper