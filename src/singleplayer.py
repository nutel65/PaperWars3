"""All action for single player game."""
import pygame
from src import controls

def run(game):
    evt_handler = controls.EventHandler(game)
    game.renderer.update_tilemap()
    game.add("soldier", (32, 32), image="green_square")
    game.add("soldier", (320, 320), image="blue_square")
    # game.add("soldier", (150, 150), image="red_square")

    done = False
    while not done:
        for event in pygame.event.get():
            done = controls.exit_check(event)
            evt_handler.handle(event)
        game.update_state()
        game.renderer.update()