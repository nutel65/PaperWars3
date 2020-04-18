"""API to access specific game tasks accesible for user as a command."""
import sys
from engine import utils
# from src import entities

class Command:
    """Command pattern abstraction."""
    def __init__(self, game_obj):
        self.game = game_obj

    def execute(self):
        raise NotImplementedError


class EntityMoveCommand(Command):
    """Moves entity to destination px."""
    def execute(self, ent, dest_px):
        ent.set_pos_px(dest_px)
        self.game.renderer.render_request_list.append(ent)


class EntityAttackCommand(Command):
    """Causes entity to attack other entity."""
    def execute(self, ent, dest_ent):
        raise NotImplementedError


class ResetGameCommand(Command):
    """Resets game state."""
    def execute(self):
        self.game.entities.clear()
        # self.game.renderer.camera = entities.Camera()
        raise NotImplementedError


class ExitGameCommand(Command):
    def execute(self):
        sys.exit(0)


class CameraZoomCommand(Command):
    """Zooms camera view by passed zoom parameter.
    zoom can be either '+' or '-'.
    """
    def __init__(self, game_obj, zoom=None):
        self.game = game_obj
        self.zoom = zoom
        self.cam_move_by = CameraMoveByCommand(self.game)

    def execute(self):
        cam = self.game.renderer.camera
        x1, y1 = self.game.client_state.mouse_pos_global
        # set zoom
        cam.set_zoom(self.zoom)
        self.game.update_state()
        x2, y2 = p2 = self.game.client_state.mouse_pos_global
        diff = (x1 - x2, y1 - y2)
        # diff = (x2 - x1, y2 - y1)
        # print(p1, p2, diff)
        self.cam_move_by.execute(*diff)

        utils.log(f"Camera ZOOM on: GLOBAL:{p2}; {cam}")
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)


class CameraCenterCommand(Command):
    def execute(self):
        rdr = self.game.renderer
        new_center = utils.local_to_global(rdr, rdr.camera.tilemap_rect.center)
        rdr.camera.set_center(new_center)
        rdr.update_tilemap()
        rdr.enqueue_all(self.game.entities)
        utils.log(f"Camera CENTERE on: GLOBAL:{new_center}; {rdr.camera}")


class CameraMoveByCommand(Command):
    """Moves camera (local) by given vector. Relative map view changes inversely."""
    def execute(self, shift_x, shift_y):
        cam = self.game.renderer.camera
        x, y = cam.rect.topleft
        shift_x *= cam.get_zoom()
        shift_y *= cam.get_zoom()
        new_topleft = (x + shift_x, y + shift_y)
        cam.set_topleft(new_topleft)
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)
        utils.log(f"Camera MOVE: {cam}")


# class CameraCenterOnCommand(Command):
#     """Sets map centered relatively to given global position."""
#     def execute(self, new_center):
#         cam = self.game.renderer.camera
#         cam.set_center(new_center)
#         self.game.renderer.update_tilemap()
#         self.game.renderer.enqueue_all(self.game.entities)
#         utils.log(f"Camera CENTERED on: GLOBAL:{new_center}; {cam}")


class PauseGameCommand(Command):
    pass