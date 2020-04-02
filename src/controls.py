"""This module contains functions for handling user input."""
import pygame
from src import commands
from engine import utils

def pump_events(self):
    pygame.event.pump()


def exit_check(event):
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True


class EventHandler():
    def __init__(self, game):
        self.game = game
        self.exit_game = commands.ExitGameCommand(game)
        self.zoom_in = commands.CameraZoomCommand(game, 2.0)
        self.zoom_out = commands.CameraZoomCommand(game, 0.5)
        self.reset_zoom = commands.CameraZoomCommand(game, 1.0)
        self.camera_left = commands.CameraMoveCommand(game, "left", 50)
        self.camera_right = commands.CameraMoveCommand(game, "right", 50)
        self.camera_up = commands.CameraMoveCommand(game, "up", 50)
        self.camera_down = commands.CameraMoveCommand(game, "down", 50)
        self.camera_center_on_px = commands.CameraCenterOnCommand(game)

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
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
        if event.key == pygame.K_0:
            self.reset_zoom.execute()
        if event.key == pygame.K_LEFT:
            self.camera_left.execute()
        if event.key == pygame.K_RIGHT:
            self.camera_right.execute()
        if event.key == pygame.K_UP:
            self.camera_up.execute()
        if event.key == pygame.K_DOWN:
            self.camera_down.execute()
        if event.key == pygame.K_RETURN:
            self.camera_center_on_px.execute(self.game.state.get_global_mouse_pos())

    def _handle_mouse_click(self, event):
        click_pos = self.game.state.get_global_mouse_pos()
        utils.log(click_pos)
        self.game.state.local["last_click_pos"] = click_pos

    def _handle_mouse_motion(self, event):
        ...