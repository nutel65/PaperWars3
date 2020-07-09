import logging
import threading

import pygame

import assets
import globvar
from src import constants
from src import controls
from src import commands
from src import entities
from src import network
from src import widgets


def run(renderer, server_url):
    globvar.scene = constants.MAIN_MENU_SCENE
    # network_service = threading.Thread(target=network.connect, args=(server_url,))
    # network_service.start()
    # # TODO: show loading screen or sth
    # network_service.join()
    # network.log_in(username="rafix", password="rafix")

    # assets.load_all()
    input_handler = controls.InputHandler(renderer)

    debug_command = commands.CustomCommand(print, "testing custom command")
    globvar.widgets.append(widgets.Button(
        topleft_pos=(30, 60),
        button_size=(100, 200),
        fill_color=constants.COLOR_RED,
        command=debug_command,
    ))

    # add controller for debugging purpose
    ctrl = controls.KeyboardController()
    input_handler.attach_controller(ctrl)

    btn1 = globvar.widgets[0]
    trigger_button_command = commands.CustomCommand(btn1.on_click)
    # ctrl.bind_key(pygame.K_b, trigger_button_command)

    move_cmd = commands.EntityMoveCommand(renderer)
    ctrl.bind_key(pygame.K_a, move_cmd, btn1, (100, 200))

    renderer.enqueue_all()

    while True:
        for event in pygame.event.get():
            input_handler.handle(event)
        renderer.update()