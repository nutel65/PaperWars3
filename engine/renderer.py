class Renderer:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (650, 30)
        pygame.init()
        pygame.display.set_caption("PaperWars")
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.camera = Camera(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.render_queue = []
        self.visible_entities = {}
        self.layers = {}
        self.dirty_rects = []

        self.background = pygame.Surface(self.screen.get_rect().size)
        self.background.fill((0, 128, 0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
    def get_window_size(self):
        return (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def add_layer(self, order: int):
        self.layers[order] = utils.Layer(order)

    def get_entity_layer(self, entity):
        for k, v in self.layers.items():
            if entity in v:
                return k

    def draw(self, entity):
        print("draw", entity)
        screen_x = entity.rect.topleft[0] - self.camera.get_rect().topleft[0]
        screen_y = entity.rect.topleft[1] - self.camera.get_rect().topleft[1]
        if entity.image.get_alpha() is not None:
            self.clear(entity)

        self.screen.blit(entity.image, (screen_x, screen_y)) # area param?
        self.dirty_rects.append(entity.rect)
    
    def clear(self, entity):
        print("clear", entity)
        screen_x = entity.rect.topleft[0] - self.camera.get_rect().topleft[0]
        screen_y = entity.rect.topleft[1] - self.camera.get_rect().topleft[1]

        # search for overlapping entities
        overlapping = []
        for _, layer in self.layers:
            for e in layer:
                if entity.rect.colliderect(e.rect) and e != entity:
                    overlapping.append(e)
        
        # sort overlapping entities by layer

        self.screen.blit(self.background, (screen_x, screen_y), entity.rect) # area param?
        self.dirty_rects.append(entity.rect)

    def update(self):
        print("---- UPDATE ----")

        # sort render list by layer
        self.render_queue.sort(key=self.get_entity_layer, reverse=True)

        # draw each element in render list
        while self.render_queue:
            self.draw(self.render_queue.pop())

        # update dirty rects
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()

        
    def draw_HUD(self): ...

    def draw_GUI(self): ...

