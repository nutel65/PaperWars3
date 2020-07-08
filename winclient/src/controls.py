"""This module contains functions for handling user input."""
import logging

import pygame

import globvar
from src import commands
from src import utils
from src import constants

logger = logging.getLogger(__name__)

def pump_events(self):
    pygame.event.pump()


def exit_check(event):
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True


class EventHandler():
    def __init__(self, renderer):
        self.renderer = rdr = renderer
        self.keyboard_controllers = []
        self.exit_game = commands.ExitGameCommand(rdr)
        self.zoom_in = commands.CameraZoomCommand(rdr, '+')
        self.zoom_out = commands.CameraZoomCommand(rdr, '-')
        self.camera_move_by = commands.CameraMoveByCommand(rdr)
        self.camera_center = commands.CameraCenterCommand(rdr)

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            for controller in self.keyboard_controllers:
                if event.key in controller.bindings:
                    control = controller.bindings[event.key]
                    args = control[1]
                    kwargs = control[2]
                    control[0].execute(*args, **kwargs)
                    logger.debug("Capturing external controller keybind")
                    break
            self._handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_EQUALS:
            self.zoom_in.execute()
        if event.key == pygame.K_MINUS:
            self.zoom_out.execute()

        ts = constants.TILE_SIZE
        if event.key == pygame.K_LEFT:
            self.camera_move_by.execute(-ts, 0)
        if event.key == pygame.K_RIGHT:
            self.camera_move_by.execute(ts, 0)
        if event.key == pygame.K_UP:
            self.camera_move_by.execute(0, -ts)
        if event.key == pygame.K_DOWN:
            self.camera_move_by.execute(0, ts)

        if event.key == pygame.K_RETURN:
            self.camera_center.execute()

    def _handle_mouse_click(self, event):
        # left click
        if event.button == 1:
            screen_pos = pygame.mouse.get_pos()
            glob_pos = utils.local_to_global(self.renderer, screen_pos)
            logger.debug(f"map: {glob_pos}; screen: {screen_pos}")
            globvar.last_click_pos_global = glob_pos
            # # center camera on clicked area

        # right click
        if event.button == 2:
            ...

        # scroll up
        if event.button == 4:
            self.zoom_in.execute()

        # scroll down
        if event.button == 5:
            self.zoom_out.execute()

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