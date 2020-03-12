import pygame
import socket
import renderer
import state

class Game:
    """Main engine class, that connects together other engine pieces.

    variables:
        entities    List of all entities.
        renderer    Provides method to represent game's state graphically
        state       Container for all usefull information about game state

    methods:
        pump_events()   Called every frame to prevent Windows
                        from "program stopped working" message.
        add_entity()    Easy and convenient way to add new entities.
    """
    
    def __init__(self):
        self.entities = set()
        # self.command_queue = collections.deque() # ???

        self.renderer = renderer.Renderer()
        # self.renderer.camera.set_on_alter_state_command(
        #     commands.RecalculateEntitiesVisibilityCommand(self))
        # self.renderer.visible_entities = self.get_visible_entities()

    # def get_visible_entities(self):
    #     return {ent for ent in self.entities if ent.visible}

        self.socket = None
        self.state = state.GameState(self)

    def pump_events(self):
        pygame.event.pump()

    def add_entity(self, entity_type, *args, **kwargs):
        if entity_type == "soldier":
            ent = game_objects.Soldier(*args, **kwargs)

        self.entities.add(ent)
        # self.renderer.layers[ent.RENDER_PRIORITY].add(ent)
        self.renderer.render_request_list.append(ent)