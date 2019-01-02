# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 11:36:48 2018

老家

@author: yaj
"""


import pygame
import scene


class Home(pygame.sprite.Sprite):
    def __init__(self, basic_map):
        super().__init__()
        self.homes = ['./images/home/home1.png', './images/home/home2.png', './images/home/home_destroyed.png']
        self.home = pygame.image.load(self.homes[0])
        self.rect = self.home.get_rect()  
        self.rect.left, self.rect.top = basic_map.home_left, basic_map.home_top
        self.alive = True
        
    def destory(self):
        self.home = pygame.image.load(self.homes[-1])
        self.alive = False
        

if __name__ == "__main__":
    bm = scene.Basic_Map(625,625)
    home = Home(bm)
    print(home.rect)
    print(home.alive)
    home.destory()
    print(home.alive)

























