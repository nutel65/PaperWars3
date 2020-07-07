"""This module contains functions for handling user input."""
import pygame
from src import commands
from src import utils

def pump_events(self):
    pygame.event.pump()


def exit_check(event):
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True


class EventHandler():
    def __init__(self, game, renderer):
        self.renderer = rdr = renderer
        self.keyboard_controllers = []
        self.game = game
        self.exit_game = commands.ExitGameCommand(game, rdr)
        self.zoom_in = commands.CameraZoomCommand(game, rdr, '+')
        self.zoom_out = commands.CameraZoomCommand(game, rdr, '-')
        # self.reset_zoom = commands.CameraZoomCommand(game, 1.0)
        self.camera_move_by = commands.CameraMoveByCommand(game, rdr)
        self.camera_center = commands.CameraCenterCommand(game, rdr)

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            for controller in self.keyboard_controllers:
                if event.key in controller.bindings:
                    control = controller.bindings[event.key]
                    args = control[1]
                    kwargs = control[2]
                    control[0].execute(*args, **kwargs)
                    utils.log("Capturing external controller keybind", type="DEBUG")
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
        # if event.key == pygame.K_0:
        #     self.reset_zoom.execute()

        if event.key == pygame.K_LEFT:
            self.camera_move_by.execute(-32, 0)
        if event.key == pygame.K_RIGHT:
            self.camera_move_by.execute(32, 0)
        if event.key == pygame.K_UP:
            self.camera_move_by.execute(0, -32)
        if event.key == pygame.K_DOWN:
            self.camera_move_by.execute(0, 32)

        if event.key == pygame.K_RETURN:
            self.camera_center.execute()

    def _handle_mouse_click(self, event):
        # left click
        if event.button == 1:
            glob_pos = self.game.client_state.mouse_pos_global
            screen_pos = self.game.client_state.mouse_pos_window
            utils.log(f"map: {glob_pos}; screen: {screen_pos}")
            self.game.client_state.last_click_pos = glob_pos
            # # center camera on clicked area
            # self.camera_center_on.execute(glob_pos)

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