# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 10:08:58 2018

食物

@author: yaj
"""

import pygame
import random
import scene
import math

class Food(pygame.sprite.Sprite):
    def __init__(self,left,top):
        super().__init__()
        #炸弹
        self.food_boom_img = './images/food/food_boom.png'
        #静止
        self.food_clock_img = './images/food/food_clock.png'
        #加强子弹
        self.food_gun_img = './images/food/food_gun.png'
        #加强大本营
        self.food_iron_img = './images/food/food_gun.png'
        #保护罩
        self.food_protect_img = './images/food/food_protect.png'
        #加分
        self.food_star_img = './images/food/food_star.png'
        #坦克生命+1
        self.food_tank_img = './images/food/food_tank.png'
        
        self.foods = [self.food_boom_img, self.food_clock_img, self.food_gun_img, self.food_iron_img, self.food_protect_img, self.food_star_img, self.food_tank_img]
        
        self.kind = None
        self.food = None
        self.rect = None
		# 是否存在
        self.being = False
		# 存在时间
        self.time = 20000
        
        self.kind = random.randint(0,len(self.foods)-1)
        self.food = pygame.image.load(self.foods[self.kind])#.convert_alpha()
        self.rect = self.food.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.being = True
        
#    def generate(self,left,top):
#        self.kind = random.randint(0,len(self.foods)-1)
#        self.food = pygame.image.load(self.foods[self.kind])#.convert_alpha()
#        self.rect = self.food.get_rect()
#        self.rect.left = left
#        self.rect.top = top
#        self.being = True
        
    def time_out(self, deltT):
        self.time -= deltT
        if self.time <= 0:
            self.being = False
        
        
if __name__ == "__main__":
    bm = scene.Basic_Map(625,625)
    food = Food()
    food.generate(bm)
    print(food.kind)
    print(food.rect)
    print(food.being)
    print(food.time)
    food.time_out(100)
    print(food.time)

        