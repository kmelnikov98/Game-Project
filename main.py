import pygame as pg
import defs



class Ball(pg.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([70, 70])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (defs.width / 2, defs.height / 2)

    def update(self, direction):
        if direction == 4:
            self.rect.x += 5
        if direction == 3:
            self.rect.x -= 5
        if direction == 2:
            self.rect.y += 5
        if direction == 1:
            self.rect.y -= 5



def drawSquare(screen, xLoc, yLoc, height, width):
    pg.draw.rect(screen, (255, 255 ,255), (xLoc, yLoc, width, height))



def main():

    pg.init()
    gameDisplay = pg.display.set_mode((defs.width, defs.height))

    pg.display.set_caption(defs.game_name)
    clock = pg.time.Clock()

    # drawSquare(gameDisplay, 0, 50, 50, 200)

    all_sprites = pg.sprite.Group()
    ball = Ball()
    all_sprites.add(ball)



    crashed = False
    while not crashed:

        do_update = False
        pressed = pg.key.get_pressed()
        if pressed[pg.K_d]:
            ball.update(4)
        if pressed[pg.K_a]:
            ball.update(3)
        if pressed[pg.K_s]:
            ball.update(2)
        if pressed[pg.K_w]:
            ball.update(1)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True


        gameDisplay.fill((0,0,0))
        all_sprites.draw(gameDisplay)
        pg.display.flip()
        clock.tick(144)

    pg.quit()
    quit()
    return 0


if __name__=='__main__':
    main()
