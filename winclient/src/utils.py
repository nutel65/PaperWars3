"""Commonly used utilities, tools and other code,
that is used often but didn't fit anywhere else.
"""
import sys
import os
import functools
from datetime import datetime

import numpy
import pygame

import globvar
from src import constants


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
    # w = rect.w * scale
    # h = rect.h * scale
    return pygame.transform.scale(image, (w, h))


def scale_rect(rect, scale=1.0):
    """Scales RECT (pygame.Rect) to given SCALE."""
    w = int(rect.w * scale)
    h = int(rect.h * scale)
    x = rect.x
    y = rect.y
    return pygame.Rect(x, y, w, h)


def local_to_global(renderer, local_pos):
    """Converts local (bounded by camera) position 
    to global (bound to size of tilemap) position.
    """
    zoom = renderer.camera.get_zoom()
    global_x = (local_pos[0] + renderer.camera.rect.x) / zoom + renderer.DISPLAY_RECT.x
    global_y = (local_pos[1] + renderer.camera.rect.y) / zoom + renderer.DISPLAY_RECT.y
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
    """Pass a message to given output function."""
    t = ""
    if time:
        t = datetime.now().strftime("%H:%M:%S:%f")[:-3]
    output(f"[{type}]:({t}): {msg}")


def tile(tile_x, tile_y):
    """Returns global position from tile array indices.
    e.g tile(2, 1) -> (64, 32)
    """
    ts = constants.TILE_SIZE
    return (tile_x * ts, tile_y * ts)


def translate_to_screen_rect(rect, camera, display_rect=None):
        """Returns screen position (in form of pygame.Rect) for entity to be rendered to."""
        if not display_rect:
            display_rect = pygame.Rect(0, 0, 0, 0)
        zoom = camera.get_zoom()
        screen_x = (rect.topleft[0] * zoom) - camera.rect.topleft[0] + display_rect.x
        screen_y = (rect.topleft[1] * zoom) - camera.rect.topleft[1] + display_rect.y
        
        width, height = rect.size
        return scale_rect(pygame.Rect(screen_x, screen_y, width, height), zoom)


def entity_at_pos(pos):
    for ent in globvar.entities:
        if ent.get_pos() == pos:
            return ent
