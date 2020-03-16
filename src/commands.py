"""API to access specific game tasks accesible for user as a command."""
import sys
from src import utils

class Command:
    """Command pattern abstraction."""
    def __init__(self, game_obj):
        self.game = game_obj

    def execute(self):
        raise NotImplementedError


class EntityMoveCommand(Command):
    """Moves entity to destination px."""
    def execute(self, ent, dest_px):
        # change entity state
        ent.set_pos_px(dest_px)
        # lastly, request rendering of object
        self.game.renderer.render_request_list.append(ent)


class EntityAttackCommand(Command):
    """Causes entity to attack other entity."""
    def execute(self, ent, dest_ent):
        raise NotImplementedError


class ResetGameCommand(Command):
    def execute(self):
        self.game.entities.clear()
        self.game.renderer.camera = render.Camera()
        self.self.state = state.GameState(self)


class ExitGameCommand(Command):
    def execute(self):
        sys.exit(0)


class CameraZoomCommand(Command):
    def __init__(self, game_obj, zoom=1.0):
        self.game = game_obj
        self.zoom = float(zoom)

    def execute(self):
        self.game.renderer.camera.set_zoom(self.zoom)
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)
        utils.log(f"Camera RESIZE: {self.game.renderer.camera}")


class CameraMoveCommand(Command):
    def __init__(self, game_obj, direction, scalar):
        self.game = game_obj
        self.direction = direction
        self.scalar = scalar

    def execute(self):
        x, y = self.game.renderer.camera.rect.topleft
        if self.direction == "up":
            y -= self.scalar
        elif self.direction == "down":
            y += self.scalar
        elif self.direction == "right":
            x += self.scalar
        elif self.direction == "left":
            x -= self.scalar
        else:
            raise NotImplementedError(f"{self.direction} not implemented")
        self.game.renderer.camera.move((x, y))
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)
        utils.log(f"Camera MOVE: {self.game.renderer.camera}")




class PauseGameCommand(Command):
    pass
