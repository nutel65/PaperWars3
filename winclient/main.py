"""PaperWars Windows client // entry point."""
# import sys
# sys.path.append("/winclient")
import os
import pygame
import common.assets
from engine import GameInstance
from engine.render import Renderer2D
from src import controls

game = GameInstance()
renderer = Renderer2D(game.entities)
assets.load_all()


def run(game, renderer):
    evt_handler = controls.EventHandler(game, renderer)
    renderer.redraw_tilemap()
    game.add_ent("soldier", (32, 32), image="green_square", renderer=renderer)
    game.add_ent("soldier", (320, 320), image="blue_square", renderer=renderer)
    # game.add_ent("soldier", (150, 150), image="red_square", renderer=renderer)

    done = False
    while not done:
        for event in pygame.event.get():
            done = controls.exit_check(event)
            evt_handler.handle(event)
        game.update_client_state(renderer)
        game.fetch_data_from_server()
        renderer.update()

run(game, renderer)
# game.reset()