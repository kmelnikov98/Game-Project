import pygame as pg
import config as cfg
import numpy as np
import math
import defs
import text
import strings
import playerInfo

wall_sprites = pg.sprite.Group()
enemy_sprites = pg.sprite.Group()
camera_offset = [defs.width / 2, defs.height / 2]
player_info = playerInfo.PlayerInfo(0)

class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(defs.player_size)
        self.image.fill(defs.BLUE)
        self.rect = self.image.get_rect()
        self.orig_image = self.image
        self.rect.center = (0, 0)
        self.orig_pos = [self.rect.center[0], self.rect.center[1]]

    def check_collisions(self, collisions, x_velocity, y_velocity, position_before):

        for collision in collisions:
            if x_velocity < 0 and abs(collision.rect.right - camera_offset[0] - self.orig_pos[0] + (self.rect.width / 2.5)) <= defs.default_player_velocity:
                self.orig_pos[0] = collision.rect.right + (self.rect.width / 2) - camera_offset[0] - 1

            if x_velocity > 0 and abs(collision.rect.left - camera_offset[0] - self.orig_pos[0] - (self.rect.width / 2.5)) <= defs.default_player_velocity:
                self.orig_pos[0] = collision.rect.left - (self.rect.width / 2) - camera_offset[0] + 1

            if y_velocity < 0 and abs(collision.rect.bottom - camera_offset[1] - self.orig_pos[1] + (self.rect.height / 2.5)) <= defs.default_player_velocity:
                self.orig_pos[1] = collision.rect.bottom + (self.rect.height / 2) - camera_offset[1] - 1

            if y_velocity > 0 and abs(collision.rect.top - camera_offset[1] - self.orig_pos[1] - (self.rect.height / 2.5)) <= defs.default_player_velocity:
                self.orig_pos[1] = collision.rect.top - (self.rect.height / 2) - camera_offset[1] + 1


    def update(self):
        global camera_offset
        pressed = pg.key.get_pressed()
        x_velocity = 0
        y_velocity = 0
        position_before = self.orig_pos.copy()
        if pressed[pg.K_d]:
            self.orig_pos[0] += defs.default_player_velocity
            x_velocity = defs.default_player_velocity
        if pressed[pg.K_a]:
            self.orig_pos[0] -= defs.default_player_velocity
            x_velocity = -defs.default_player_velocity
        if pressed[pg.K_s]:
            self.orig_pos[1] += defs.default_player_velocity
            y_velocity = defs.default_player_velocity
        if pressed[pg.K_w]:
            self.orig_pos[1] -= defs.default_player_velocity
            y_velocity = -defs.default_player_velocity

        wall_collision_list = pg.sprite.spritecollide(self, wall_sprites, False)
        self.check_collisions(wall_collision_list, x_velocity, y_velocity, position_before)

        enemy_collision_list = pg.sprite.spritecollide(self, enemy_sprites, True)
        if enemy_collision_list:
            for enemies_collided in enemy_collision_list:
                player_info.player_kill_counter()
                print(player_info.kill_counter)

        camera_offset = [defs.width / 2 - self.orig_pos[0], defs.height / 2 - self.orig_pos[1]]
        self.rect.center = (self.orig_pos[0] + camera_offset[0], self.orig_pos[1] + camera_offset[1])
        self.rotate()


    def rotate(self):
        # The vector to the target (the mouse position).
        direction = np.subtract(pg.mouse.get_pos(), self.rect.center)
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
        angle = (180 * math.atan2(direction[0], direction[1]))/math.pi
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pg.transform.rotozoom(self.orig_image, angle, 1)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)



class Block(pg.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(defs.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Need orig_pos for camera
        self.orig_pos = (self.rect.x, self.rect.y)

    def update(self):
        self.rect.x = self.orig_pos[0] + camera_offset[0]
        self.rect.y = self.orig_pos[1] + camera_offset[1]


class Enemy(pg.sprite.Sprite):

        def __init__(self, x, y, width, height):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.Surface((width, height))
            self.image.fill(defs.RED)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

            # Need orig_pos for camera
            self.orig_pos = [self.rect.x, self.rect.y]

        def update(self):
            self.orig_pos[0] += 2
            self.rect.x = self.orig_pos[0] + camera_offset[0]
            self.rect.y = self.orig_pos[1] + camera_offset[1]



def addAllSprites(all_sprites):
    # Add Player
    all_sprites.add(Player())

    # Add Blocks (x, y, width, height)
    wall_sprites.add(Block(-300, -300, 600, 50))
    wall_sprites.add(Block(-300, -300, 50, 600))
    wall_sprites.add(Block(-300, 300, 600, 50))
    enemy_sprites.add(Enemy(100, 400, 100, 100))

    all_sprites.add(*wall_sprites)
    all_sprites.add(*enemy_sprites)


def main():

    pg.init()
    # Resolution, and fullscreen
    gameDisplay = pg.display.set_mode((defs.width, defs.height), pg.FULLSCREEN) if cfg.toggle_fullscreen else pg.display.set_mode((defs.width, defs.height))
    pg.display.set_caption(defs.game_name)
    clock = pg.time.Clock()

    # init/add the sprites
    all_sprites = pg.sprite.Group()
    addAllSprites(all_sprites)

    # Call the UI that needs to be displayed, related to the player
    kill_text = text.TextUI(defs.kill_font, defs.kill_font_size, defs.WHITE, playerInfo.kill_position_x, playerInfo.kill_position_y)

    crashed = False
    while not crashed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True
            if event.type == pg.KEYDOWN and event.key == pg.K_k:
                crashed = True

        # Update all the sprites, we may need to separate groups later which would complicate things.
        all_sprites.update()

        # Fill before draw so that we have background on the back
        pg.display.update()
        gameDisplay.fill(defs.background_color)
        all_sprites.draw(gameDisplay)
        kill_text.message_display(strings.kill_counter_str + str(player_info.kill_counter), gameDisplay)
        pg.display.flip()
        clock.tick(cfg.target_frame_rate)

    pg.quit()
    quit()
    return 0

if __name__=='__main__':
    main()
