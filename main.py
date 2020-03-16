"""Run this file to start game. 
All initial configuration happens here.
"""
import engine
import assets
from src import singleplayer

game = engine.Game()
assets.load_all()

singleplayer.run(game)
# game.reset()