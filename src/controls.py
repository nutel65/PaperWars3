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
        self.camera_move_by = commands.CameraMoveByCommand(game)
        self.camera_center = commands.CameraCenterCommand(game)

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
            self.camera_move_by.execute(-32, 0)
        if event.key == pygame.K_RIGHT:
            self.camera_move_by.execute(32, 0)
        if event.key == pygame.K_UP:
            self.camera_move_by.execute(0, -32)
        if event.key == pygame.K_DOWN:
            self.camera_move_by.execute(0, 32)

        if event.key == pygame.K_RETURN:
            # renderer = self.game.renderer
            # map_center = utils.local_to_global(renderer, renderer.camera.tilemap_rect.center)
            self.camera_center.execute()

    def _handle_mouse_click(self, event):
        glob_pos = self.game.client_state.mouse_pos_global
        screen_pos = self.game.client_state.mouse_pos_window
        utils.log(f"map: {glob_pos}; screen: {screen_pos}")
        self.game.client_state.last_click_pos = glob_pos
        # # center camera on clicked area
        # self.camera_center_on.execute(glob_pos)


    def _handle_mouse_motion(self, event):
        ...