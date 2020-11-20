import pygame as pg
from utils.settings import *
vec = pg.math.Vector2

class Platform(pg.sprite.Sprite):
    '''create plaform structure'''

    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
