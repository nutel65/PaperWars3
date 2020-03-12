class Entity():
    """Represents any game object"""
    def __init__(self, *args, **kwargs):
        self.rect = None

    def __str__(self):
        return f"{type(self).__name__}({self.rect})"


class Drawable(Entity):
    """Represents object that can be drawn"""
    def __init__(self, *args, **kwargs):
        self.rect = None # pygame.Rect
        self.image = None # pygame.Surface
        self.RENDER_PRIORITY = -1 # -1 = always on top
        

class Soldier(Drawable):
    def __init__(self, pos, image):
        self.image = assets.SPRITES[image]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.RENDER_PRIORITY = 1

    def get_pos_px(self):
        return self.rect.topleft

    def set_pos_px(self, x, y)
        self.rect.topleft = (x, y)