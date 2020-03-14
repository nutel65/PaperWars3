"""API to access specific tasks as a comand (eg. bound action to button)."""
import sys

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


class CameraZoomInCommand(Command):
    def execute(self):
        self.game.renderer.camera._zoom += 0.2
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)


class CameraZoomOutCommand(Command):
    def execute(self):
        self.game.renderer.camera._zoom -= 0.2
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)


class CameraMoveCommand(Command):
    # FIXME: Not working properly
    def __init__(self, game_obj, direction, scalar=100):
        self.game = game_obj
        self.direction = direction
        self.scalar = scalar

    def execute(self):
        x, y = self.game.renderer.camera.rect.topleft
        if self.direction == "up":
            y -= self.scalar
        if self.direction == "down":
            y += self.scalar
        if self.direction == "right":
            x += self.scalar
        if self.direction == "left":
            x -= self.scalar
        self.game.renderer.camera.move((x, y))
        self.game.renderer.update_tilemap()
        self.game.renderer.enqueue_all(self.game.entities)


class PauseGameCommand(Command):
    pass
