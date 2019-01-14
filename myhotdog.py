# -*- coding: utf-8 -*-
import pygame
from random import *

BIG=2
SMALL=1
speed=5

class Smallhotdog(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sc/hotdog.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("sc/hotdog_down1.png").convert_alpha(), \
            pygame.image.load("sc/hotdog_down2.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = speed
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(10, self.width - self.rect.width-5), \
                        randint(-100,-60)
                        # randint(-1 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.attack=False
        self.size=SMALL
        self.score_counted=False
        
    def move(self):
        if self.rect.top < self.height-60-60:
            self.rect.top += self.speed
        else:
            self.active=False
            self.attack=True

class Bighotdog(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sc/bighotdog.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("sc/bighotdog_down1.png").convert_alpha(), \
            pygame.image.load("sc/bighotdog_down2.png").convert_alpha(), \
            pygame.image.load("sc/bighotdog_down3.png").convert_alpha(), \
            pygame.image.load("sc/bighotdog_down4.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = speed
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(10, self.width - self.rect.width-5), \
                        randint(-100,-60)
                        # randint(-1 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.attack=False
        self.eating=False
        self.size=BIG
        self.score_counted=False
        
    def move(self):
        if self.rect.top < self.height-60-120:
            self.rect.top += self.speed
        else:
            if self.eating==True:
                if self.rect.top<self.height-60-60:
                    self.rect.top += self.speed
                else:    
                    self.active=False
                    self.eating=False
            else:
                self.active=False
                self.attack=True

