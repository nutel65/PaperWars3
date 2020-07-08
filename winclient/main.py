"""PaperWars Windows client // entry point."""
import os
import logging

import pygame

import assets
import globvar
from src import commands
from src import controls
from src import entities
from src.utils import tile
from engine.render import Renderer2D

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(name)-16s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S',
    # filename=f'./server/logs/{filename}',
    filemode='w+'
)

renderer = Renderer2D()
assets.load_all()


def run(renderer):
    evt_handler = controls.EventHandler(renderer)
    renderer._redraw_tilemap()

    entities.add_ent("soldier", tile(1, 1), image="green_square", renderer=renderer)
    entities.add_ent("soldier", tile(5, 0), image="blue_square", renderer=renderer)
    renderer.enqueue_all()

    # add controller for first entity
    ctrl = controls.KeyboardController()
    ent = globvar.entities[0]
    move_cmd = commands.EntityMoveCommand(renderer)
    ctrl.bind_key(pygame.K_a, move_cmd, ent, tile(1, 1))
    ctrl.bind_key(pygame.K_s, move_cmd, ent, tile(5, 5))
    ctrl.bind_key(pygame.K_d, move_cmd, ent, tile(10, 10))
    ctrl.bind_key(pygame.K_f, move_cmd, ent, tile(15, 15))

    attack_cmd = commands.EntityAttackCommand(renderer)
    ent2 = globvar.entities[1]
    ctrl.bind_key(pygame.K_x, attack_cmd, ent, ent2)

    evt_handler.attach_controller(ctrl)

    done = False
    while not done:
        for event in pygame.event.get():
            done = controls.exit_check(event)
            evt_handler.handle(event)
        renderer.update()

if __name__ == "__main__":
    run(renderer)