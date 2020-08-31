import pygame as pg
import config as cfg
import numpy as np
import math
import defs

# Contains code for text display, and positioning

class TextUI():

    def __init__(self, font_type, font_size, text_colour, x_pos, y_pos):
        self.font_text = pg.font.Font(font_type, font_size)
        self.text_colour = text_colour
        self.x_pos = x_pos
        self.y_pos = y_pos

    def message_display(self, text, game_display):
        textSurface = self.font_text.render(text, True, self.text_colour)
        TextSurf, TextRect = (textSurface, textSurface.get_rect())
        TextRect.center = (self.x_pos, self.y_pos)
        game_display.blit(TextSurf, TextRect)
