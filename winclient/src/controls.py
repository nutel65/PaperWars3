"""This module contains functions for handling user input."""
import logging

import pygame

import globvar
from src import commands
from src import utils
from src import constants
# from src import widgets

logger = logging.getLogger(__name__)

# def pump_events(self):
#     pygame.event.pump()


class InputHandler():
    def __init__(self, renderer):
        self.renderer = rdr = renderer
        self.keyboard_controllers = []
        self.exit_game = commands.ExitGameCommand(rdr)
        self.zoom_in = commands.CameraZoomCommand(rdr, '+')
        self.zoom_out = commands.CameraZoomCommand(rdr, '-')
        self.camera_move_by = commands.CameraMoveByCommand(rdr)
        self.camera_center = commands.CameraCenterCommand(rdr)

    def handle(self, event):
        if event.type == pygame.QUIT:
            self.exit_game.execute()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_game.execute()
            for controller in self.keyboard_controllers:
                if event.key in controller.bindings:
                    logger.debug("Capturing external controller keybind")
                    control = controller.bindings[event.key]
                    args = control[1]
                    kwargs = control[2]
                    control[0].execute(*args, **kwargs)
                    break
            self._handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

    def _handle_keydown(self, event):
        ts = constants.TILE_SIZE
        if globvar.scene == constants.MULTIPLAYER_GAME_SCENE:
            if event.key == pygame.K_EQUALS:
                self.zoom_in.execute()
            elif event.key == pygame.K_MINUS:
                self.zoom_out.execute()
            elif event.key == pygame.K_LEFT:
                self.camera_move_by.execute(-ts, 0)
            elif event.key == pygame.K_RIGHT:
                self.camera_move_by.execute(ts, 0)
            elif event.key == pygame.K_UP:
                self.camera_move_by.execute(0, -ts)
            elif event.key == pygame.K_DOWN:
                self.camera_move_by.execute(0, ts)
            if event.key == pygame.K_RETURN:
                self.camera_center.execute()
        elif globvar.scene == constants.MAIN_MENU_SCENE:
            pass

    def _handle_mouse_click(self, event):
        screen_pos = pygame.mouse.get_pos()
        glob_pos = None
        # left click
        if event.button == 1:
            ...
            # clicked_widget = widgets.get_widget_at(screen_pos)
            # if clicked_widget:
            #     logger.debug(f"clicked widget {clicked_widget}")
            #     clicked_widget.on_click()
            #     return

        if globvar.scene == constants.MULTIPLAYER_GAME_SCENE:
            glob_pos = utils.local_to_global(self.renderer, screen_pos)
            # globvar.last_click_pos_global = glob_pos

            # in-game left click
            if event.button == 1:
                # get_sprite_at(glob_pos)
                ...

            # in-game right click
            elif event.button == 2:
                ...

            # in-game scroll up
            elif event.button == 4:
                self.zoom_in.execute()

            # in-game scroll down
            elif event.button == 5:
                self.zoom_out.execute()

        elif globvar.scene == constants.MAIN_MENU_SCENE:
            pass
        
        w = constants.WINDOW_WIDTH
        h = constants.WINDOW_HEIGHT
        wp = int(screen_pos[0] / w * 100)
        hp = int(screen_pos[1] / h * 100)
        logger.debug(f"map: {glob_pos}; screen: {screen_pos}, (w={wp}%, h={hp}%)")

    def _handle_mouse_motion(self, event):
        ...

    def attach_controller(self, controller):
        if isinstance(controller, KeyboardController):
            self.keyboard_controllers.append(controller)
        else:
            raise TyperError(f"Such controller instance not supported ({controller})")


class KeyboardController:
    def __init__(self):
        self.bindings = {}

    def bind_key(self, pygame_key, command, *command_args, **command_kwargs):
        self.bindings[pygame_key] = [command, command_args, command_kwargs]