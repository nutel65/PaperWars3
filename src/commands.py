"""API to access specific game tasks accesible for user as a command."""
import sys
from engine import utils

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
        self.game.renderer.camera = render.Camera()
        raise NotImplementedError


class ExitGameCommand(Command):
    def execute(self):
        sys.exit(0)


class CameraZoomAndCenterCommand(Command):
    """Zooms camera view by passed zoom parameter.
    center_on can be either 'mouse' or 'center'
    """
    def __init__(self, game_obj, zoom=None, center_on="mouse"):
        self.game = game_obj
        self.zoom = zoom
        self.center_on = center_on

    def execute(self):
        zoom = float(self.zoom) if self.zoom else self.game.client_state.camera_zoom
        if self.center_on == "mouse":
            new_center = self.game.client_state.mouse_pos_global
        elif self.center_on == "center":
            rdr = self.game.renderer
            new_center = utils.local_to_global(rdr, rdr.camera.tilemap_rect.center)
        else:
            raise ValueError(f"centerOn argument '{self.center_on}' not valid."
                              "Use 'center' or 'mouse' instead.")
        cam = self.game.renderer.camera
        # set zoom
        cam.set_zoom(zoom)
        # center camera
        cam.set_center(new_center)
        utils.log(f"Camera RESIZE/CENTERED on: GLOBAL:{new_center}; {cam}")
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)


class CameraMoveByCommand(Command):
    """Moves camera by given vector. Relative map view changes inversely."""
    def execute(self, shift_x, shift_y):
        x, y = self.game.renderer.camera.rect.topleft
        self.game.renderer.camera.move((x + shift_x, y + shift_y))
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)
        utils.log(f"Camera MOVE: {self.game.renderer.camera}")


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