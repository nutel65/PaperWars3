import logging
import threading
import secrets

import pygame

import assets
import globvar
from src import commands
from src import controls
from src import sprites
from src import constants
from src import network
from src.utils import tile

logger = logging.getLogger(__name__)

def run(renderer, server_url):
    globvar.scene = constants.MULTIPLAYER_GAME_SCENE
    logger.info("Switched to MULTIPLAYER_GAME_SCENE")
    globvar.reset()

    network_service = threading.Thread(target=network.connect, args=(server_url,))
    network_service.start()
    assets.load_all()
    # idk man
    # TODO: show loading screen or sth
    network_service.join()
    if not globvar.connected:
        logger.info("Connection error: server not responding.")
        return -1
    network.log_in(username=f"guest_{secrets.token_urlsafe()[:6]}", password="")

    input_handler = controls.InputHandler(renderer)
    renderer._redraw_tilemap()

    ent1 = sprites.Soldier(tile(1, 1), image=assets.SPRITES["green_square"])
    ent2 = sprites.Soldier(tile(2, 5), image=assets.SPRITES["blue_square"])

    # add controller for first sprite
    ctrl = controls.KeyboardController()
    move_cmd = commands.SpriteMoveCommand(renderer)
    ctrl.bind_key(pygame.K_a, move_cmd, ent1, tile(1, 1))
    ctrl.bind_key(pygame.K_s, move_cmd, ent1, tile(5, 5))
    ctrl.bind_key(pygame.K_d, move_cmd, ent1, tile(10, 10))
    ctrl.bind_key(pygame.K_f, move_cmd, ent1, tile(15, 15))

    attack_cmd = commands.SpriteAttackCommand(renderer)
    ctrl.bind_key(pygame.K_x, attack_cmd, ent1, ent2)

    input_handler.attach_controller(ctrl)

    while True:
        for event in pygame.event.get():
            input_handler.handle(event)
        renderer.update()
    return 0