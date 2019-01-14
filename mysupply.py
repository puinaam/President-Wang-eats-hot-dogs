# -*- coding: utf-8 -*-

import pygame
from random import *

class Bomb_Supply(pygame.sprite.Sprite):                                       #30 x 40
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sc/100.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = randint(10, self.width - self.rect.width), -60
        self.speed = 6
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.bottom < self.height-60:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = \
                        randint(10, self.width - self.rect.width), -60