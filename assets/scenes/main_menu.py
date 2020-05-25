"""Main menu scene. use run(game, assets) function to open scene."""
import assets

def run(game):
    while True:
        game.pump_events()
        game.renderer.update()