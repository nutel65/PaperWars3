import engine
import engine.commands

game = engine.Game()
# game.renderer.add_layer(0) # tilemap tiles
# game.renderer.add_layer(1) # entities
# game.renderer.add_layer(2) # other UI elements

game.add_entity("soldier", (50, 50), image=0)
game.add_entity("soldier", (100, 100), image=1)
game.add_entity("soldier", (150, 150), image=2)
game.add_entity("soldier", (200, 200), imgage=0)

while True:
    game.renderer.update()
    game.pump_events()