"""Implements UI and HUD objects"""
from src import entities

class Button(entities.Drawable):
    # TODO: Refactor this class.
    obj_list = []

    def __init__(self, position=(0, 0), shift=(0, 0), size="auto", command=None,
                 args=[], image=None, desc_on_hover="", desc_on_click=""):
        Button.obj_list.append(self)
        if size == "auto":
            ...
        else:
            self.size = size
        # x, y = position
        # xv, yv = shift
        # position = (x + xv, y + yv)
        position = utils.shifted_point(position, shift)
        self.area = pygame.Rect(position, self.size)
        if command:
            self.set_on_click(command, args)
        if image:
            self._surface = image
        else:
            self._surface = pygame.Surface(self.size)
            self._surface.fill((169, 0, 169))
        self.desc_on_hover = desc_on_hover
        self.desc_on_click = desc_on_click
        self.draw()

    def delete(self):
        Button.obj_list.remove(self)

    def draw(self, dest_surf, pos_px, rect=None):
        dest_surf.blit(self._surface, self.area.topleft, rect)

    def set_on_click(self, command):
        self._on_click = command

    def on_click(self):
        self._on_click.execute()