"""Commonly used utilities, tools and other code,
that is used often but didn't fit anywhere else
"""
import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


def exit_check(event):
    if event.type == QUIT:
        return True
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            return True


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


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__