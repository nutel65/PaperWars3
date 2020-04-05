"""Commonly used utilities, tools and other code,
that is used often but didn't fit anywhere else.
"""
import sys
import os
import pygame
import numpy
import functools
from datetime import datetime
from src import entities
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


# def index_to_px(index, shift=(0, 0)):
#     x, y = index
#     index = (x * 32 + shift[0], y * 32 + shift[1])
#     return index


# def px_to_index(px, shift=(0, 0)):
#     x, y = px
#     x -= shift[0]
#     y -= shift[1]
#     px = (x // 32, y // 32)
#     return px


# def shifted_point(coords, vector):
#     x, y = coords
#     xv, yv = vector
#     return (x + xv, y + yv)


# def shifted_rect(rect, vector):
#     tmp_rect = rect.copy()
#     x, y = tmp_rect.topleft
#     tmp_rect.topleft = (x - vector[0], y - vector[1])
#     return tmp_rect


# class DotDict(dict):
#     """dot.notation access to dictionary attributes"""
#     __getattr__ = dict.get
#     __setattr__ = dict.__setitem__
#     __delattr__ = dict.__delitem__    


class TilemapFileParser():
    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"[Error] FileNotFound: {os.path.abspath(filename)}")
        self._filename = filename

    def parse(self):
        """Parses file and returns result as numpy.array of ints."""
        result = []
        with open(self._filename) as tilemap:
            for line in tilemap.read().splitlines():
                stripped_line = line.strip()
                if len(line) == 0 or stripped_line[0] == "#":
                    continue
                mapped = list(map(int, stripped_line.split(",")))
                result.append(mapped)
        return numpy.array(result)


@functools.lru_cache()
def scale_image(image, scale=1.0):
    """Scales IMGAGE (pygame.Surface) to given SCALE."""
    rect = image.get_rect()
    w = int(rect.w * scale)
    h = int(rect.h * scale)
    return pygame.transform.scale(image, (w, h))


def scale_rect(rect, scale=1.0):
    """Scales RECT (pygame.Rect) to given SCALE."""
    w = int(rect.w * scale)
    h = int(rect.h * scale)
    return pygame.Rect(rect.left, rect.top, w, h)


def local_to_global(renderer, local_pos):
    """Converts local (bounded by camera) position 
    to global (bound to size of tilemap) position.
    """
    zoom = renderer.camera.get_zoom()
    global_x = (local_pos[0] + renderer.camera.rect.x) / zoom + renderer.DISPLAY_RECT.x
    global_y = (local_pos[1] + renderer.camera.rect.y) / zoom + renderer.DISPLAY_RECT.y
    ## DEBUG:
    # ent = next(iter(game.entities))
    # game.renderer.global.blit(ent.image, (global_x, global_y))
    # pygame.display.flip()
    return (global_x, global_y)


def global_to_local(renderer, global_pos):
    """Converts global (bound to size of tilemap)
    position to local (bounded by camera) position.
    """
    zoom = renderer.camera.get_zoom()
    local_x = zoom * (global_pos[0] - renderer.DISPLAY_RECT.x) - renderer.camera.rect.x
    local_y = zoom * (global_pos[1] - renderer.DISPLAY_RECT.y) - renderer.camera.rect.y
    return (local_x, local_y)


def log(msg="", type="Info", time=True, output=print):
    """Pass a message to given output (output is function)."""
    t = ""
    if time:
        t = datetime.now().strftime("%H:%M:%S:%f")[:-3]
    output(f"[{type}]:({t}): {msg}")