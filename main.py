import pygame as pg
import sys
import os
from pygame.locals import *
import random

from utils.settings import Settings
from utils.player import *
from utils.platform import Platform
vec = pg.math.Vector2


# ======== [One file pyinstaller utility script] ======
#
# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)
if getattr(sys, 'frozen', False):
    CurrentPath = sys._MEIPASS
else:
    CurrentPath = os.path.dirname(__file__)
# ==================================================

class Game:

    def __init__(self):
        '''intiialize game class'''
        pg.init()  # initialize pygame module
        pg.font.init()  # initialize font module

        # background music
        pg.mixer.init()  # initialize music module
        # pg.mixer.music.load(os.path.join(CurrentPath,'music\\SLOWER-TEMPO2019-12-11_-_Retro_Platforming_-_David_Fesliyan.mp3'))
        # pg.mixer.music.play(-1)

        self.settings = Settings()
        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption(self.settings.title)
        self.clock = pg.time.Clock()

        # load background image
        self.bkgrnd = pg.image.load(os.path.join(CurrentPath,'images\\background_1.png'))

    def new_game(self):
        '''start a new game'''
        # create master sprite group
        self.all_sprites = pg.sprite.Group()

        # load player Spritesheet
        self.spritesheet = Spritesheet(os.path.join(CurrentPath, 'sprites\\test.png'))

        # platform Group
        self.platforms = pg.sprite.Group()
        self.p1 = Platform(0, self.settings.screen_height - 40,
                           self.settings.screen_width / 3, 40)
        self.p2 = Platform(self.settings.screen_width / 2,
                           self.settings.screen_height - 40, self.settings.screen_width / 2, 40)
        self.p3 = Platform(250, self.settings.screen_height - 120,
                           60, 20)
        self.platforms.add(self.p1)
        self.platforms.add(self.p2)
        self.platforms.add(self.p3)

        # create player
        self.player = Player(self, self.settings.screen_width / 2,
                             self.settings.screen_height / 2)

        # add to groups
        self.all_sprites.add(self.p1)
        self.all_sprites.add(self.p2)
        self.all_sprites.add(self.p3)
        self.all_sprites.add(self.player)

        # run game when new game initiated
        self.run_game()

    def _check_events(self):
        '''track user events during game loop'''
        for event in pg.event.get():  # event loop
            if event.type == pg.QUIT:  # check for window quit
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:  # check for q key to quit
                    sys.exit()  # end script

                if event.key == pg.K_END:
                    self.new_game()

    def _update_screen(self):
        '''update screen during game loop'''
        self.screen.blit(self.bkgrnd,(0,0))

        self.all_sprites.draw(self.screen)
        self.all_sprites.update()

        # check for collision
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        # draw all elements then flip display
        pg.display.flip()

    def run_game(self):
        '''main game loop execute function'''
        while True:  # main game loop
            self._check_events()
            self._update_screen()

            self.clock.tick(self.settings.fps)

    def splash_screen(self):
        '''initiate splash screen when starting game'''
        self.screen.blit(
            pg.image.load(
                os.path.join(CurrentPath, 'images\\splash_screen1.png')
            ),
            (0, 0)
        )
        pg.display.update()
        self.splash_wait()

    def splash_wait(self):
        '''wait for user to hit enter to start game'''
        # create animated splash screen
        images = 'splash_screen1 splash_screen2'.split(' ')
        start = False
        while not start:
            self.clock.tick(15)
            for image in images:
                self.screen.blit(
                    pg.image.load(
                        os.path.join(CurrentPath, 'images\\' +
                                     str(image) + '.png')
                    ),
                    (0, 0)
                )
                pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.intro()
                        start = True

    def draw_text(self, text, size, color, x, y):
        '''function to render text on screen'''
        font = pg.font.Font(pg.font.match_font(self.settings.font_style), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def intro(self):
        next = False
        images = 'intro1 intro2'.split()
        while not next:
            self.clock.tick(self.settings.intro_fps)
            for image in images:
                self.screen.blit(
                    pg.image.load(
                        os.path.join(CurrentPath, 'images\\' +
                                     str(image) + '.png')
                    ),
                    (0, 0)
                )
                pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.new_game()
                        next = True


if __name__ == '__main__':
    g = Game()
    g.splash_screen()
