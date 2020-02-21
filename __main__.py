import engine

game = engine.Game()
game.renderer.add_layer(1)
game.renderer.add_layer(2)
game.renderer.add_layer(2)

game.add_entity("soldier", 1, (50, 50), 0)
game.add_entity("soldier", 2, (100, 100), 1)
game.add_entity("soldier", 2, (150, 150), 2)
game.add_entity("soldier", 1, (200, 200), 0)

while True:
    game.renderer.update()
    game.pump_events()