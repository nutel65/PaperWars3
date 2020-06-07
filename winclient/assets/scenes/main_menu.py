"""Main menu scene. use run(game, assets) function to open scene."""
import assets

def run(game, renderer):
    while True:
        game.pump_events()
        renderer.update()