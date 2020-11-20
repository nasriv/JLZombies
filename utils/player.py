import pygame as pg
from utils.settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    '''create player class structure'''

    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image(0,0,(1024/12),(1024/12))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.player_width = self.rect.width

        # track variables for sprite animation
        self.walking = False
        self.jumping = False
        self.load_sprites()
        self.current_frame = 0
        self.last_frame_update = 0

        # intialize movement and starting location
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # player movement physics
        self.acc_val = 0.6
        self.friction = -0.15
        self.player_grav = 0.3

    def load_sprites(self):
        # function to load in sprites for animations
        wpx = (1024/12) #width of sprite
        hpx = (1024/12) #height of sprite

        nrows = 9
        ncols = 1

        self.walk_frames_R = [self.game.spritesheet.get_image(wpx*row,0,wpx,hpx) for row in range(nrows)]

        for row in range(nrows):
            print(wpx*row, hpx*ncols, wpx, hpx)

        for frame in self.walk_frames_R:
            frame.set_colorkey((255,255,255))

        self.walk_frames_L = []
        for frame in self.walk_frames_R:
            self.walk_frames_L.append(pg.transform.flip(frame, True, False))

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -8

    def update(self):
        self.settings = Settings()
        self.animate() # call function to animate sprite

        self.acc = vec(0, self.player_grav) # set player initial acceleration values

        if self.pos.x > self.settings.screen_width - self.player_width/2:
            self.pos.x = self.settings.screen_width - self.player_width/2
        if self.pos.x <= 0:
            self.pos.x = 0

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -self.acc_val
        if keys[pg.K_RIGHT]:
            self.acc.x = self.acc_val
        if keys[pg.K_UP]:
            self.jump()

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def animate(self):
        '''function to animate sprite motions'''
        now = pg.time.get_ticks()

        # check if walking
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_frame_update > 200:
                self.last_frame_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_R)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_R[self.current_frame]
                else:
                    self.image = self.walk_frames_L[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Spritesheet:
    '''class for loading and parsing sprtesheets'''

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab image from sprtesheet
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image
