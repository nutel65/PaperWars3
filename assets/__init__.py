import pygame

TILEMAP_TEXTURES = {
    # 0: pygame.image.load("textures/water.png").convert_alpha(),
    # 1: pygame.image.load("textures/grass.png").convert(),
}

red_square = pygame.Surface((10, 10))
red_square.fill((255, 0, 0))

green_square = pygame.Surface((10, 10))
green_square.fill((0, 255, 0))

blue_square = pygame.Surface((10, 10))
blue_square.fill((0, 0, 255))

SPRITES = {
    0: red_square,
    1: green_square,
    2: blue_square,
}

OTHER_IMAGES = {}

FX_SOUNDS = {}

SOUNDTRACKS = {}