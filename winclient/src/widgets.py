"""Implements UI and HUD objects"""
import logging

# import pygame
# import pygame.freetype

# import globvar
# from src import sprites
# from src import commands
# from src import constants
# from src import utils

logger = logging.getLogger(__name__)




#####################################
# TODO: use external library for GUI eg. thorpy (https://www.pygame.org/wiki/gui)
#####################################




# def get_widget_at(screen_pos):
#     for widget in globvar.widgets:
#         if widget.rect.collidepoint(screen_pos) and widget.SCREEN_STATIC:
#             return widget


# class Widget(sprites.Drawable):
#     # NOTE: For interface variables, check sprites.Drawable docstring
#     # NOTE: SCREEN_STATIC has precedence over MAP_STATIC
#     RENDER_PRIORITY = 5
#     MAP_STATIC = False # if true object behaves like part of map while rendering
#     SCREEN_STATIC = True # determines whether object moves / zooms along with camera
#     def __init__(self):
#         globvar.widgets.append(self)

#     def on_click(self):
#         pass


# class TextArea(Widget):
#     pygame.freetype.init()
#     font = pygame.freetype.SysFont(pygame.font.get_default_font(), constants.FONT_SIZE)

#     def __init__(
#             self,
#             topleft_pos_perc, # in % of screen size
#             size_perc, # in % of screen size
#             fill_color=None,
#             text="",
#             # background_image=None,
#             # desc_on_hover="",
#             # desc_on_click="",
#         ):
#         super().__init__()
#         w = constants.WINDOW_WIDTH
#         h = constants.WINDOW_HEIGHT
#         self.image = pygame.Surface((
#             w * size_perc[0] // 100,
#             h * size_perc[1] // 100,
#         ))
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (
#             w * topleft_pos_perc[0] // 100,
#             h * topleft_pos_perc[1] // 100,
#         )
#         if fill_color:
#             self.image.fill(fill_color)
#         if text:
#             self.set_text(text, self.font)
#         self.image_copy = self.image.copy()
    
#     def set_text(self, text, font, color=(0, 0, 0)):
#         self.text = text
#         font.origin = True
#         words = text.split(' ')
#         width, height = self.image.get_size()
#         line_spacing = font.get_sized_height() + 2
#         x, y = 0, line_spacing
#         space = font.get_rect(' ')
#         for word in words:
#             bounds = font.get_rect(word)
#             if x + bounds.width + bounds.x >= width:
#                 x, y = 0, y + line_spacing
#             if x + bounds.width + bounds.x >= width:
#                 # raise ValueError("word too wide for the surface")
#                 logger.warning("word too wide for the surface")
#                 return
#             if y + bounds.height - bounds.y >= height:
#                 # raise ValueError("text to long for the TextArea surface")
#                 logger.warning(f"text to long for the TextArea surface ({y + bounds.height - bounds.y}/{height})")
#                 return
#             font.render_to(self.image, (x, y), None, color)
#             x += bounds.width + space.width
#         globvar.render_request_list.append(self)
#         return x, y


# class Button(Widget):
#     """If background_image supplied:
#     - button_size is ignored, and set to fit image 
#     - fill_color is ignored
#     """
#     def __init__(
#             self,
#             topleft_pos_perc, # in % of screen size
#             button_size=None,
#             fill_color=None,
#             background_image=None,
#             background_scale=1.0,
#             command=None,
#             *command_args,
#             **command_kwargs
#         ):
#         super().__init__()
#         if background_image:
#             self.image = utils.scale_image(background_image, background_scale)
#         elif button_size:
#             if not fill_color:
#                 raise ValueError("fill_color not specified.")
#             self.image = pygame.Surface(button_size)
#             self.image.fill(fill_color)
#         else:
#             raise ValueError("size or background_image not supplied.")
#         self.rect = self.image.get_rect()
#         w = constants.WINDOW_WIDTH
#         h = constants.WINDOW_HEIGHT
#         self.rect.topleft = (
#             w * topleft_pos_perc[0] // 100,
#             h * topleft_pos_perc[1] // 100,
#         )
#         if not isinstance(command, commands.Command):
#             raise ValueError("command argument should be commands.Command instance")
#         self.command = command
#         self.command_args = command_args
#         self.command_kwargs = command_kwargs

#     def on_click(self, *args, **kwargs):
#         self.command.execute(
#             *self.command_args, *args, **self.command_kwargs, **kwargs
#         )