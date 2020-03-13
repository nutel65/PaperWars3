"""All action for single player in game happens here"""
import assets
from src import utils

def run(game):
    game.add_entity("soldier", (50, 50), image="green_square")
    game.add_entity("soldier", (100, 100), image="blue_square")
    game.add_entity("soldier", (150, 150), image="red_square")

    done = False
    while not done:
        game.pump_events()
        game.renderer.update()
        utils.exit_check()
    game.reset()