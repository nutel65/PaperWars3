"""Contains methods to Use run(game, assets) function to start"""
import assets

def run(game):
    while True:
        game.pump_events()
        game.renderer.update()