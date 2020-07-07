"""PaperWars Windows client // entry point."""
import os
import pygame
import assets
from src import commands
from engine import GameInstance
from engine.render import Renderer2D
from src import controls
from src.utils import tile

game = GameInstance()
renderer = Renderer2D(game.entities)
assets.load_all()


def run(game, renderer):
    evt_handler = controls.EventHandler(game, renderer)
    renderer._redraw_tilemap()

    game.add_ent("soldier", tile(1, 1), image="green_square", renderer=renderer)
    game.add_ent("soldier", tile(10, 10), image="blue_square", renderer=renderer)
    renderer.enqueue_all()

    # add controller for first entity
    ctrl = controls.KeyboardController()
    ent = game.entities[0]
    ctrl.bind_key(pygame.K_a, commands.EntityMoveCommand(game, renderer), ent, tile(1, 1))
    ctrl.bind_key(pygame.K_s, commands.EntityMoveCommand(game, renderer), ent, tile(5, 5))
    ctrl.bind_key(pygame.K_d, commands.EntityMoveCommand(game, renderer), ent, tile(10, 10))
    ctrl.bind_key(pygame.K_f, commands.EntityMoveCommand(game, renderer), ent, tile(15, 15))
    evt_handler.attach_controller(ctrl)


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