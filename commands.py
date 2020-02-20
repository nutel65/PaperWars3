import utils
import collections

class CommandQueue:
    def __init__(self):
        self._queue = collections.deque()

    def add(self, command):
        self._queue.append(command)

    def execute_commands(self):
        while self._queue:
            self._queue.popleft().execute()


class Command:
    def execute(self):
        raise NotImplementedError


class RecalculateEntitiesVisibilityCommand(Command):
    def __init__(self, game):
        self.game = game
        rect = game.renderer.camera.get_rect()
        self.indices = self.rect.collidelistall(game.entities)

    def execute(self):
        for i in range(len(self.game.entities)):
            if i in self.indices:
                self.game.entities[i].visible = True
            else:
                self.game.entities[i].visible = False

class EntityMoveCommand(Command): ...

class EntityAttackCommand(Command): ...

