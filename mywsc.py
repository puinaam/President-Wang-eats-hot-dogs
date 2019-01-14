# -*- coding: utf-8 -*-

import pygame

class Mywsc(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image1 = pygame.image.load("sc/wsc1.png").convert_alpha()
        self.image2 = pygame.image.load("sc/wsc2.png").convert_alpha()
        self.image_icon=pygame.image.load("sc/wsc_icon.png").convert_alpha()   #60 x 60
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("sc/wsc_down1.png").convert_alpha(), \
            pygame.image.load("sc/wsc_down2.png").convert_alpha(), \
            pygame.image.load("sc/wsc_down3.png").convert_alpha(), \
            pygame.image.load("sc/wsc_down4.png").convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]                       #background x,y
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 60
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image1)                      #碰撞检测掩模
        self.active=True
        self.lives=3

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width