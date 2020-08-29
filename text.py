import pygame as pg
import config as cfg
import numpy as np
import math
import defs

class TextUI():

    def __init__(self, text, font_type, font_size, text_colour):
        self.font_text = pg.font.Font(font_type, font_size)
        self.textSurface = self.font_text.render(text, True, text_colour)

    def message_display(self, game_display):
        TextSurf, TextRect = (self.textSurface, self.textSurface.get_rect())
        TextRect.center = ((defs.width/2),(defs.height/2))
        game_display.blit(TextSurf, TextRect)
