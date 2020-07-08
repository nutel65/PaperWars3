import logging
import threading

import pygame

import assets
import globvar
from src import commands
from src import controls
from src import entities
from src import constants
from src import network
from src.utils import tile


def run(renderer, server_url):
    network_service = threading.Thread(target=network.connect, args=(server_url,))
    network_service.start()
    # idk man
    network_service.join()
    network.log_in(username="rafix", password="rafix")

    globvar.scene = constants.MULTIPLAYER_GAME_SCENE
    assets.load_all()
    input_handler = controls.InputHandler(renderer)
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

    input_handler.attach_controller(ctrl)

    

    while True:
        for event in pygame.event.get():
            input_handler.handle(event)
        renderer.update()