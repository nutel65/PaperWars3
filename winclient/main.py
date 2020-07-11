"""PaperWars Windows client // entry point."""
import logging

import globvar
from src import constants
from src.scenes import main_menu, multiplayer_game
from engine.render import Renderer2D

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(name)-16s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S',
    # filename=f'./server/logs/{filename}',
    filemode='w+'
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

globvar.reset()
renderer = Renderer2D()

if __name__ == "__main__":
    # multiplayer_game.run(renderer, constants.LOCAL_SERVER_URL)
    # multiplayer_game.run(renderer, constants.PRODUCTION_SERVER_URL)
    main_menu.run(renderer, constants.PRODUCTION_SERVER_URL)