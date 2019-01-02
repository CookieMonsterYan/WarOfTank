# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 15:43:44 2018

等级标识

@author: yaj
"""

import pygame

class Level(pygame.sprite.Sprite):
    def __init__(self,kind,left,bottom,levels):
        super().__init__()
        self.imgs = ['./images/level/armor_level.png','./images/level/fire_level.png','./images/level/speed_level.png']
        self.kinds = {
                'armor':0,
                'fire':1,
                'speed':2
                }
        self.img = pygame.image.load(self.imgs[self.kinds[kind]])
        self.rect = self.img.get_rect()
        self.levels = levels - 1
        self.rect.left = left + self.levels//30*self.rect.width + 4
        self.rect.bottom = bottom - self.levels%30*self.rect.height
        



