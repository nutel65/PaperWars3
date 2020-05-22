"""Top level API to execute specific tasks."""
import sys
from src import utils
# from src import entities

class Command:
    """Command pattern abstraction."""
    def __init__(self, game_obj, renderer):
        self.game = game_obj
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
        ent.set_pos_px(dest_px)


class EntityAttackCommand(Command):
    """Causes entity to attack other entity."""
    def execute(self, ent, dest_ent):
        raise NotImplementedError


class ExitGameCommand(Command):
    def execute(self):
        sys.exit(0)

class CameraCenterCommand(Command):
    def execute(self):
        self.rdr.camera.set_center()


class CameraZoomCommand(Command):
    """Zooms camera view by passed zoom parameter.
    zoom_mode can be either '+' or '-'.
    """
    def __init__(self, game_obj, renderer, zoom_mode):
        self.game = game_obj
        self.rdr = renderer
        self.zoom_mode = zoom_mode
        self.cam_move_by = CameraMoveByCommand(game_obj, renderer)

    def execute(self):
        cam = self.rdr.camera
        x1, y1 = self.game.client_state.mouse_pos_global
        # set zoom
        if self.zoom_mode == '+':
            zoom_change = 1
        else:
            zoom_change = -1
        try:
            cam._set_zoom_id(cam.zoom_id + zoom_change)
        except ValueError:
            return
        self.game.update_client_state(self.rdr)

        x2, y2 = p2 = self.game.client_state.mouse_pos_global
        diff = (x1 - x2, y1 - y2)
        self.cam_move_by.execute(*diff)
        utils.log(f"Camera ZOOM on: GLOBAL:{p2}; {cam}")


class CameraMoveByCommand(Command):
    """Moves camera (globally) by given vector. Relative map view changes inversely."""
    def execute(self, shift_x, shift_y):
        cam = self.rdr.camera
        x, y = cam.rect.topleft
        shift_x *= cam.get_zoom()
        shift_y *= cam.get_zoom()
        new_topleft = (x + shift_x, y + shift_y)
        cam.set_topleft(new_topleft)
        utils.log(f"Camera MOVE: {cam}")


class PauseGameCommand(Command):
    pass
