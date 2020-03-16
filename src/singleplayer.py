"""All action for single player game happens here."""
import assets
import pygame
from src import utils
from src import controls

def run(game):
    event_handler = controls.EventHandler(game)
    game.renderer.update_tilemap()
    game.add("soldier", (50, 50), image="green_square")
    game.add("soldier", (100, 100), image="blue_square")
    game.add("soldier", (150, 150), image="red_square")

    done = False
    while not done:
        for event in pygame.event.get():
            done = controls.exit_check(event)
            event_handler.handle(event)
        game.renderer.update()