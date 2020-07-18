"""This file loads audio, images, animation and other assets.
Init assets with 'load_all()' before use.
"""
import os
import logging

import pygame

from src import utils
from src import constants

logger = logging.getLogger(__name__)

TEXTURES = None
SPRITES = None
ICONS = None
BUTTONS = None
FX_SOUNDS = None
SOUNDTRACKS = None


def load_all():
    load_sprites()
    load_textures()
    load_buttons()
    load_icons()
    load_sounds()


def load_textures():
    global TEXTURES 
    textures_path = f"{constants.ASSETS_PATH}/images/textures"
    TEXTURES = _map_dir_to_dict(
        textures_path,
        lambda filename: int(filename[:filename.index("_")]),
        lambda filename: pygame.image.load(f"{textures_path}/{filename}").convert()
    )
    logger.info("assets.TEXTURES initialized")


def load_sprites():
    global SPRITES

    ts = constants.TILE_SIZE
    red_square = pygame.Surface((ts, ts))
    red_square.fill(constants.COLOR_RED)

    green_square = pygame.Surface((ts, ts))
    green_square.fill(constants.COLOR_GREEN)

    blue_square = pygame.Surface((ts, ts))
    blue_square.fill(constants.COLOR_BLUE)
    
    sprites_path = f"{constants.ASSETS_PATH}/images/sprites"
    SPRITES = {
        "red_square": red_square,
        "green_square": green_square,
        "blue_square": blue_square,
    }
    sprites_path = f"{constants.ASSETS_PATH}/images/buttons"
    SPRITES.update(_map_dir_to_dict(
        sprites_path,
        lambda filename: filename[:filename.index(".")],
        lambda filename: pygame.image.load(f"{sprites_path}/{filename}").convert()
    ))
    logger.info("assets.SPRITES initialized")


def load_icons():
    global ICONS
    icons_path = f"{constants.ASSETS_PATH}/images/icons"
    ICONS = _map_dir_to_dict(
        icons_path,
        lambda filename: filename[:filename.index(".")],
        lambda filename: pygame.image.load(f"{icons_path}/{filename}").convert()
    )
    logger.info("assets.ICONS initialized")


def load_buttons():
    global BUTTONS
    # buttons = {
    #     "hl_tile": pygame.image.load(f"{constants.ASSETS_PATH}/images/buttons/htwhite32.png").convert_alpha(),
    # }
    buttons_path = f"{constants.ASSETS_PATH}/images/buttons"
    BUTTONS = _map_dir_to_dict(
        buttons_path,
        lambda filename: filename[:filename.index(".")],
        lambda filename: pygame.image.load(f"{buttons_path}/{filename}").convert()
    )
    logger.info("assets.buttons initialized")


def load_sounds():
    pass
    # global FX_SOUNDS
    # global SOUNDTRACKS
    
    # SOUNDTRACKS = {}
    # logger.info("assets.FX_SOUNDS initialized")
    # logger.info("assets.SOUNDTRACKS initialized")


def _map_dir_to_dict(dirpath, key_func, value_func, key_func_args=[], value_func_args=[]):
    """Returns dictionary for every filename in dirpatch, where:
    keys are return results of calling key_func with filename, and
    values are return results of calling value_func with filename.
    """
    return {
        key_func(filename, *key_func_args): value_func(filename, *value_func_args)
        for filename
        in os.listdir(dirpath)
        if filename.endswith(".png")
    }
    

    