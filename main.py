import pygame as pg
import config as cfg
import numpy as np
import math
import defs

class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(defs.player_size)
        self.image.fill(defs.BLUE)
        self.rect = self.image.get_rect()
        self.orig_image = self.image
        self.rect.center = (defs.width / 2, defs.height / 2)

    def update(self):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_d]:
            self.rect.x += defs.default_player_velocity
        if pressed[pg.K_a]:
            self.rect.x -= defs.default_player_velocity
        if pressed[pg.K_s]:
            self.rect.y += defs.default_player_velocity
        if pressed[pg.K_w]:
            self.rect.y -= defs.default_player_velocity

        self.rotate()

    def rotate(self):
        # The vector to the target (the mouse position).
        direction = np.subtract(pg.mouse.get_pos(), self.rect.center)
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
        angle = (180*math.atan2(direction[0], direction[1]))/math.pi
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pg.transform.rotozoom(self.orig_image, angle, 1)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)


def drawSquare(screen, color, xLoc, yLoc, height, width):
    pg.draw.rect(screen, color, (xLoc, yLoc, width, height))


def main():

    pg.init()
    gameDisplay = pg.display.set_mode((defs.width, defs.height))

    pg.display.set_caption(defs.game_name)
    clock = pg.time.Clock()

    all_sprites = pg.sprite.Group()
    player = Player()
    all_sprites.add(player)

    crashed = False
    while not crashed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True

        all_sprites.update()
        gameDisplay.fill(defs.background_color)
        all_sprites.draw(gameDisplay)
        pg.display.flip()
        clock.tick(cfg.target_frame_rate)

    pg.quit()
    quit()
    return 0


if __name__=='__main__':
    main()
