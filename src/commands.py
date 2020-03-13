"""API to access specific tasks as a comand (eg. bound action to button)."""

class Command:
    """Command pattern abstraction."""

    def __init__(self, game):
        self.game = game

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
    """Moves entity to destination px."""

    def execute(self, ent, dest_px):
        # change entity state
        ent.set_pos_px(dest_px)
        # lastly, request rendering of object
        self.game.renderer.render_request_list.append(ent)


class EntityAttackCommand(Command):
    """Causes entity to attack other entity."""

    def execute(self, ent, dest_ent):
        
