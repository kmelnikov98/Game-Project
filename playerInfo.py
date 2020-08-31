import pygame as pg
import config as cfg
import numpy as np
import math
import defs
import text
import strings

kill_position_x = 180
kill_position_y = 100

class PlayerInfo():
            # Defines basic parameters that will be expanded later
            def __init__(self, kill_counter):
                self.kill_counter = kill_counter
                self.exp_counter = 0
                self.health = 0
                self.stamina = 0

            def player_kill_counter(self):
                self.kill_counter += 1
