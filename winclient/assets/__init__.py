"""This file loads audio, images, animation and other assets.
Init assets with 'load_all()' before use.
constants:
    TILEMAP_TEXTURES
    SPRITES
    OTHER_IMAGES
    FX_SOUNDS
    SOUNDTRACKS
    ICONS
"""
import logging

import pygame

from src import utils
from src import constants

logger = logging.getLogger(__name__)

TILEMAP_TEXTURES = None
SPRITES = None
ICONS = None
UI_ELEMENTS = None
FX_SOUNDS = None
SOUNDTRACKS = None


def load_all():
    load_sprites()
    load_textures()
    load_ui_elements()
    load_icons()
    load_sounds()


def load_textures():
    global TILEMAP_TEXTURES 
    textures = f"{constants.ASSETS_PATH}/images/textures"
    TILEMAP_TEXTURES = {
        0: pygame.image.load(f"{textures}/default.png").convert(),
        1: pygame.image.load(f"{textures}/dirt.png").convert(),
        2: pygame.image.load(f"{textures}/forest32.png").convert(),
        3: pygame.image.load(f"{textures}/grass32.png").convert(),
        4: pygame.image.load(f"{textures}/sand.png").convert(),
        5: pygame.image.load(f"{textures}/snow.png").convert(),
        6: pygame.image.load(f"{textures}/water.png").convert(),
    }
    logger.info("assets.TILEMAP_TEXTURES initialized")


def load_sprites():
    global SPRITES

    ts = constants.TILE_SIZE
    red_square = pygame.Surface((ts, ts))
    red_square.fill(constants.COLOR_RED)

    green_square = pygame.Surface((ts, ts))
    green_square.fill(constants.COLOR_GREEN)

    blue_square = pygame.Surface((ts, ts))
    blue_square.fill(constants.COLOR_BLUE)
    
    sprites = f"{constants.ASSETS_PATH}/images/sprites"
    SPRITES = {
        "red_square": red_square,
        "green_square": green_square,
        "blue_square": blue_square,
        "red_soldier": pygame.image.load(f"{sprites}/red_soldier32.png").convert_alpha(),
        "purple_soldier": pygame.image.load(f"{sprites}/purple_soldier32.png").convert_alpha(),
    }
    logger.info("assets.SPRITES initialized")


def load_icons():
    global ICONS
    icons = f"{constants.ASSETS_PATH}/images/icons"
    ICONS = {
        "crossed_circle": pygame.image.load(f"{icons}/cancel.png").convert_alpha(),
        "crossed_arrows": pygame.image.load(f"{icons}/move.png").convert_alpha(),
        "red_sword": pygame.image.load(f"{icons}/sword2.png").convert_alpha(),
    }
    logger.info("assets.ICONS initialized")


def load_ui_elements():
    global UI_ELEMENTS
    UI_ELEMENTS = {
        "hl_tile": pygame.image.load(f"{constants.ASSETS_PATH}/images/ui_elements/htwhite32.png").convert_alpha(),
    }
    logger.info("assets.UI_ELEMENTS initialized")


def load_sounds():
    global FX_SOUNDS
    global SOUNDTRACKS

    FX_SOUNDS = {}
    
    SOUNDTRACKS = {}
    logger.info("assets.FX_SOUNDS initialized")
    logger.info("assets.SOUNDTRACKS initialized")