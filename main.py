import pygame as pg
import defs


def main():

    pg.init()
    gameDisplay = pg.display.set_mode((defs.width, defs.height))
    pg.display.set_caption(defs.game_name)
    clock = pg.time.Clock()

    crashed = False
    while not crashed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True

        pg.display.flip()
        clock.tick(144)

    pg.quit()
    quit()
    return 0


if __name__=='__main__':
    main()
