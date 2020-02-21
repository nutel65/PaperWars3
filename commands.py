import utils
import collections

# class CommandQueue:
#     def __init__(self):
#         self._queue = collections.deque()

#     def add(self, command):
#         self._queue.append(command)

#     def execute_commands(self):
#         while self._queue:
#             self._queue.popleft().execute()


class Command:
    def execute(self):
        raise NotImplementedError


class RecalculateEntitiesVisibilityCommand(Command):
    def __init__(self, game):
        self.game = game
        self.rect = game.renderer.camera.get_rect()

    def execute(self):
        self.game.renderer.visible_entities.empty()
        for ent in self.game.entities:
            if self.rect.colliderect(ent.rect):
                self.game.renderer.visible_entities.add(ent)
                

class EntityMoveCommand(Command): ...

class EntityAttackCommand(Command): ...

