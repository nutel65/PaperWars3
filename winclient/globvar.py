import pygame

globvar = __import__(__name__)

scene = 0
renderer = None
connected = False


# remaining_turn_time = 30
# player_turn = 0
# last_click_pos_global = None
# keys_pressed = []

def reset():
    globvar.sprites = pygame.sprite.LayeredDirty()
    # globvar.widgets = []