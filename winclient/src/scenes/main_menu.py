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
from src import pygame_textinput
from src.scenes import multiplayer_game

logger = logging.getLogger(__name__)

def run(renderer, server_url):
    globvar.scene = constants.MAIN_MENU_SCENE
    logger.info("Switched to MAIN_MENU_SCENE")
    globvar.reset()
    # network_service = threading.Thread(target=network.connect, args=(server_url,))
    # network_service.start()
    # # TODO: show loading screen or sth
    # network_service.join()
    # network.log_in(username="rafix", password="rafix")

    # assets.load_all()
    assets.load_buttons()
    input_handler = controls.InputHandler(renderer)

    debug_command = commands.CustomCommand(print, "testing custom command")
    # btn2 = widgets.Button(
    #     topleft_pos_perc=(10, 10),
    #     button_size=(50, 50),
    #     fill_color=constants.COLOR_RED,
    #     command=debug_command,
    # )
    run_multiplayer_game_command = commands.CustomCommand(
        func=multiplayer_game.run,
        renderer=renderer,
        server_url=server_url
    )
    btn1 = widgets.Button(
        topleft_pos_perc=(20, 32),
        background_image=assets.BUTTONS["new_game"],
        background_scale=0.5,
        command=run_multiplayer_game_command
    )

    # add controller for debugging purpose
    ctrl = controls.KeyboardController()
    input_handler.attach_controller(ctrl)

    # trigger_button_command = commands.CustomCommand(btn1.on_click)
    # # ctrl.bind_key(pygame.K_b, trigger_button_command)

    # move_cmd = commands.EntityMoveCommand(renderer)
    # ctrl.bind_key(pygame.K_a, move_cmd, btn1, (100, 200))

    widgets.TextArea((0, 0), (100, 7), constants.COLOR_YELLOW, "test 123")

    nickname_input_box = pygame_textinput.TextInput((30, 20), initial_string="nickname placeholder")

    renderer.enqueue_all()
    while True:
        events = pygame.event.get()
        for event in events:
            input_handler.handle(event)
        nickname_input_box.update(events)
        renderer.update()