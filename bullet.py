# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 09:32:38 2018

子弹

@author: yaj
"""

import pygame
import scene


class Bullet(pygame.sprite.Sprite):
    def __init__(self, basic_map, from_who):
        super().__init__()
        self.bullets = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']
        self.direction_x, self.direction_y = 0, -1
        self.bullet = pygame.image.load(self.bullets[0])
        self.rect = self.bullet.get_rect()
        self.rect.left = 0
        self.rect.right = 0
        self.speed = 6
        self.being = False
        self.stronger = False #是否是加强子弹
        self.left = basic_map.map_left
        self.top = basic_map.map_top
        self.right = basic_map.width - basic_map.map_left
        self.bottom = basic_map.height - basic_map.map_top
        self.from_who = from_who
        
    def turn(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        if self.direction_x == 0 and self.direction_y == -1:
            self.bullet = pygame.image.load(self.bullets[0])
        elif self.direction_x == 0 and self.direction_y == 1:
            self.bullet = pygame.image.load(self.bullets[1])
        elif self.direction_x == -1 and self.direction_y == 0:
            self.bullet = pygame.image.load(self.bullets[2])
        elif self.direction_x == 1 and self.direction_y == 0:
            self.bullet = pygame.image.load(self.bullets[3])
        else:
            raise ValueError('Bullet class -> direction value error.')
        
    def move(self):
        self.rect = self.rect.move(self.direction_x*self.speed, self.direction_y*self.speed)
        #到地图边缘消失
        if (self.rect.top < self.top) or (self.rect.bottom > self.bottom) or (self.rect.left < self.left) or (self.rect.right > self.right):
            self.being = False
    
    def strong(self):
        self.stronger = True

if __name__=="__main__":
    bm = scene.Basic_Map(625,625)
    bullet = Bullet(bm)
    print(bullet.being)
    print(bullet.rect)
    print(bullet.speed)
    try:
        bullet.turn(1,1)
        print(bullet.rect)
    except ValueError as err:
        print(err)
    bullet.turn(1,0)
    print(bullet.rect)
    bullet.move()
    print(bullet.rect)
    bullet.strong()
    print(bullet.stronger)


