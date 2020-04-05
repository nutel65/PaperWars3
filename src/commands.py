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
        self.self.state = state.GameState(self)


class ExitGameCommand(Command):
    def execute(self):
        sys.exit(0)


class CameraZoomCommand(Command):
    """Zooms camera view by passed zoom parameter."""
    def __init__(self, game_obj, zoom=1.0):
        self.game = game_obj
        self.zoom = float(zoom)

    def execute(self):
        self.game.renderer.camera.set_zoom(self.zoom)
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)
        utils.log(f"Camera RESIZE: {self.game.renderer.camera}")


class CameraMoveByCommand(Command):
    """Moves camera by passed values. Relative map view changes inversely."""
    def execute(self, shift_x, shift_y):
        x, y = self.game.renderer.camera.rect.topleft
        self.game.renderer.camera.move((x + shift_x, y + shift_y))
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)
        utils.log(f"Camera MOVE: {self.game.renderer.camera}")


class CameraCenterOnCommand(Command):
    """Sets map centered relatively to given global position."""
    def execute(self, new_center):
        cam = self.game.renderer.camera
        cam.set_center(new_center)
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)
        utils.log(f"Camera CENTERED on: GLOBAL:{new_center}; {cam}")


class PauseGameCommand(Command):
    pass