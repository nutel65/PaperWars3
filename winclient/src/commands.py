"""Top level API to execute specific tasks."""
import os
import logging

import pygame

from src import utils
# from src import entities

logger = logging.getLogger(__name__)

class Command:
    """Command pattern abstraction."""
    def __init__(self, renderer):
        self.rdr = renderer

    def execute(self, *args, **kwargs):
        raise NotImplementedError


class CustomCommand(Command):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        return self.func(*self.args, **self.kwargs)


class EntityMoveCommand(Command):
    """Moves entity to destination px."""
    def execute(self, ent, dest_px):
        # TODO: prevent moving outside the map
        ent.set_pos(dest_px[0], dest_px[1])


class EntityAttackCommand(Command):
    """Causes entity to attack other entity."""
    def execute(self, ent, dest_ent):
        ent.attack(dest_ent)


class ExitGameCommand(Command):
    def execute(self):
        logger.info("Executing exit command.")
        # sys.exit(0)
        # close connections or so
        os._exit(0)

class CameraCenterCommand(Command):
    def execute(self):
        self.rdr.camera.set_center()


class CameraZoomCommand(Command):
    """Zooms camera view by passed zoom parameter.
    zoom_mode can be either '+' or '-'.
    """
    def __init__(self, renderer, zoom_mode):
        self.rdr = renderer
        self.zoom_mode = zoom_mode
        self.cam_move_by = CameraMoveByCommand(renderer)

    def execute(self):
        cam = self.rdr.camera
        x1, y1 = utils.local_to_global(self.rdr, pygame.mouse.get_pos())
        # set zoom
        if self.zoom_mode == '+':
            zoom_change = 1
        else:
            zoom_change = -1
        try:
            cam._set_zoom_id(cam.zoom_id + zoom_change)
        except ValueError:
            return

        x2, y2 = utils.local_to_global(self.rdr, pygame.mouse.get_pos())
        diff = (x1 - x2, y1 - y2)
        self.cam_move_by.execute(*diff)
        logger.debug(f"Camera ZOOM on: GLOBAL:{(x2, y2)}; {cam}")


class CameraMoveByCommand(Command):
    """Moves camera (globally) by given vector. Relative map view changes inversely."""
    def execute(self, shift_x, shift_y):
        cam = self.rdr.camera
        x, y = cam.rect.topleft
        shift_x *= cam.get_zoom()
        shift_y *= cam.get_zoom()
        new_topleft = (x + shift_x, y + shift_y)
        cam.set_topleft(new_topleft)
        logger.debug(f"Camera MOVE: {cam}")


class PauseGameCommand(Command):
    pass
