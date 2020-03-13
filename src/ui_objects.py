from src.entities import Drawable

class Button(Drawable):
    obj_list = []

    def __init__(self, position=(0, 0), shift=(0, 0), size=(0, 0), func=None,
                 args=[], sprite=None, desc_on_hover="", desc_on_click=""):
        Button.obj_list.append(self)
        self.size = size
        # x, y = position
        # xv, yv = shift
        # position = (x + xv, y + yv)
        position = utils.shifted_point(position, shift)
        self.area = pygame.Rect(position, self.size)
        if func:
            self.set_on_click(func, args)
        if sprite:
            self._surface = sprite
        else:
            self._surface = pygame.Surface(self.size)
            self._surface.fill((169, 0, 169))
        self.desc_on_hover = desc_on_hover
        self.desc_on_click = desc_on_click
        self.draw()

    def delete(self):
        Button.obj_list.remove(self)

    def draw(self):
        screen.blit(self._surface, self.area.topleft)
        dirty_rects.append(self.area.copy())

    def set_on_click(self, function, arguments):
        self._func = function
        self._args = arguments

    def on_click(self):
        self._func(*self._args)