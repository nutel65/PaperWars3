"""API to access specific tasks as a comand (eg. bound action to button)."""

class Command:
    """Command abstraction"""
    def execute(self):
        raise NotImplementedError


# class RecalculateEntitiesVisibilityCommand(Command):
#     def __init__(self, game):
#         self.game = game
#         self.rect = game.renderer.camera.get_rect()

#     def execute(self):
#         self.game.renderer.visible_entities.empty()
#         for ent in self.game.entities:
#             if self.rect.colliderect(ent.rect):
#                 self.game.renderer.visible_entities.add(ent)
                

class EntityMoveCommand(Command):
    def __init__(self, game, obj, dest_px):
        self.game = game
        self.dest_px = dest_px
        self.obj = obj

    def execute(self):
        # change object state
        self.obj.set_pos_px(self.dest_px)
        # lastly, request rendering of object
        self.game.renderer.render_request_list.append(self.obj)


class EntityAttackCommand(Command): ...

