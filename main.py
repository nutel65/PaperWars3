"""Run this file to start game. 
All initial configuration happens here.
"""
from engine import GameInstance
import assets
from engine.render import Renderer2D

game = GameInstance()
renderer = Renderer2D(game.entities)
assets.load_all()

import assets
import pygame
from src import controls

def run(game, renderer):
    evt_handler = controls.EventHandler(game, renderer)
    renderer.redraw_tilemap()
    game.add("soldier", (32, 32), image="green_square", renderer=renderer)
    game.add("soldier", (320, 320), image="blue_square", renderer=renderer)
    # game.add("soldier", (150, 150), image="red_square")

    done = False
    while not done:
        for event in pygame.event.get():
            done = controls.exit_check(event)
            evt_handler.handle(event)
        game.update_state(renderer)
        renderer.update()

run(game, renderer)
# game.reset()