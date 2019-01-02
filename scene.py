# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 13:05:33 2018

地图

@author: yaj
"""


import pygame
import random
import numpy as np


#墙
class Wall(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.wall = pygame.image.load(img)
        self.rect = self.wall.get_rect()
        self.being = False


#石头墙
class Brick(Wall):
    def __init__(self):
        super().__init__('./images/scene/brick.png')
        
#钢墙
class Iron(Wall):
    def __init__(self):
        super().__init__('./images/scene/iron.png')
#冰
class Ice(Wall):
    def __init__(self):
        super().__init__('./images/scene/ice.png')

#河道
class River(Wall):
    def __init__(self):
        if random.randint(0,9) < 5:
            super().__init__('./images/scene/river1.png')
        else:
            super().__init__('./images/scene/river2.png')
 
#树
class Tree(Wall):
    def __init__(self):
        super().__init__('./images/scene/tree.png')       


#地图基本框架
class Basic_Map():
    def __init__(self, height, width):
        self.blcok_size = 24
        self.home_size = 2*self.blcok_size
        self.tank_size = 2*self.blcok_size
        if width < 12*self.blcok_size or height < 12*self.blcok_size:
            raise ValueError('地图的宽高过小')
        self.height = height
        self.width = width
        self.nheight = height//self.blcok_size
        self.nwidth = width//self.blcok_size
        if self.nheight%2 != 0 or self.nwidth%2 != 0:
            raise ValueError("地图的宽高必须是{}偶数倍".format(self.blcok_size))
        
        self.map_matrix = np.zeros((self.nheight,self.nwidth))
        #老家得代码为-1
        self.map_matrix[self.nheight-1,self.nwidth//2-1] = -1
        self.map_matrix[self.nheight-1,self.nwidth//2] = -1
        self.map_matrix[self.nheight-2,self.nwidth//2-1] = -1
        self.map_matrix[self.nheight-2,self.nwidth//2] = -1
        #老家周围得墙得代码为-2
        self.map_matrix[self.nheight-3,self.nwidth//2-2] = -2
        self.map_matrix[self.nheight-3,self.nwidth//2-1] = -2
        self.map_matrix[self.nheight-3,self.nwidth//2] = -2
        self.map_matrix[self.nheight-3,self.nwidth//2+1] = -2
        self.map_matrix[self.nheight-2,self.nwidth//2-2] = -2
        self.map_matrix[self.nheight-2,self.nwidth//2+1] = -2
        self.map_matrix[self.nheight-1,self.nwidth//2-2] = -2
        self.map_matrix[self.nheight-1,self.nwidth//2+1] = -2
        #出生点代码为-3
        self.map_matrix[self.nheight-2,self.nwidth//2-4] = -3
        self.map_matrix[self.nheight-1,self.nwidth//2-4] = -3
        self.map_matrix[self.nheight-2,self.nwidth//2-3] = -3
        self.map_matrix[self.nheight-1,self.nwidth//2-3] = -3
        self.map_matrix[self.nheight-2,self.nwidth//2+2] = -3
        self.map_matrix[self.nheight-1,self.nwidth//2+2] = -3
        self.map_matrix[self.nheight-2,self.nwidth//2+3] = -3
        self.map_matrix[self.nheight-1,self.nwidth//2+3] = -3
        #敌人出生点代码为-4
        self.map_matrix[0,0] = -4
        self.map_matrix[1,0] = -4
        self.map_matrix[0,1] = -4
        self.map_matrix[1,1] = -4
        self.map_matrix[0,self.nwidth//2-2] = -4
        self.map_matrix[1,self.nwidth//2-2] = -4
        self.map_matrix[0,self.nwidth//2-1] = -4
        self.map_matrix[1,self.nwidth//2-1] = -4
        self.map_matrix[0,self.nwidth//2] = -4
        self.map_matrix[1,self.nwidth//2] = -4
        self.map_matrix[0,self.nwidth//2+1] = -4
        self.map_matrix[1,self.nwidth//2+1] = -4
        self.map_matrix[0,self.nwidth-2] = -4
        self.map_matrix[1,self.nwidth-2] = -4
        self.map_matrix[0,self.nwidth-1] = -4
        self.map_matrix[1,self.nwidth-1] = -4
        self.map_matrix[self.nheight//2-2,0] = -4
        self.map_matrix[self.nheight//2-1,0] = -4
        self.map_matrix[self.nheight//2-2,1] = -4
        self.map_matrix[self.nheight//2-1,1] = -4
        self.map_matrix[self.nheight//2-2,self.nwidth-2] = -4
        self.map_matrix[self.nheight//2-1,self.nwidth-2] = -4
        self.map_matrix[self.nheight//2-2,self.nwidth-1] = -4
        self.map_matrix[self.nheight//2-1,self.nwidth-1] = -4
        
        self.map_top = (height - self.nheight*self.blcok_size)/2
        self.map_left = (width - self.nwidth*self.blcok_size)/2
        self.home_top = height - self.map_top - self.home_size
        self.home_left = width/2 - self.home_size/2
        self.home_walls_top = []
        self.home_walls_left = []
        for x in range(-1,3):
            for y in range(-1,2):
                if not (x,y) in [(0,0),(1,0),(0,1),(1,1)]:
                    self.home_walls_left.append(self.home_left+x*self.blcok_size)
                    self.home_walls_top.append(self.home_top+y*self.blcok_size)
        self.birth_point_1_top = self.home_top
        self.birth_point_1_left = self.home_left-3*self.blcok_size
        self.birth_point_2_top = self.home_top
        self.birth_point_2_left = self.home_left+3*self.blcok_size
        self.enemy_points_top = [self.map_top,
                                 self.map_top,
                                 self.map_top,
                                 self.map_top,
                                 self.map_top+(self.nheight/2-2)*self.blcok_size,
                                 self.map_top+(self.nheight/2-2)*self.blcok_size
                ]
        self.enemy_points_left = [self.map_left,
                                  self.map_left+(self.nwidth/2-2)*self.blcok_size,
                                  self.map_left+(self.nwidth/2)*self.blcok_size,
                                  self.width - self.map_left - 2*self.blcok_size,
                                  self.map_left,
                                  self.width - self.map_left - 2*self.blcok_size,
                ]
        
#地图        
class Map():
    def __init__(self, basic_map):
        self.basic_map = basic_map
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup  = pygame.sprite.Group()
        self.iceGroup = pygame.sprite.Group()
        self.riverGroup = pygame.sprite.Group()
        self.treeGroup = pygame.sprite.Group()
        self.home_wall_iron = pygame.sprite.Group()
        self.small_map = self.basic_map.map_matrix.copy()
        
    def get_map(self):
        rate_brick = 0.4
        rate_iron = 0.1
        (rows,cols) = self.small_map.shape
        total_grids = rows*cols
        
        #生成随机地图
        while (True):
            self.small_map = self.basic_map.map_matrix.copy()
            self.brickGroup.empty()
            self.ironGroup.empty()
            self.iceGroup.empty()
            self.riverGroup.empty()
            self.treeGroup.empty()
            
            #brick
            num_brik = round(rate_brick*total_grids)
            x = np.random.randint(0,rows,num_brik)
            y = np.random.randint(0,cols,num_brik)
            for i in range(num_brik):
                if self.small_map[x[i],y[i]] == 0:
                    self.small_map[x[i],y[i]] = 1
                    brick = Brick()
                    brick.rect.left = self.basic_map.map_left + y[i]*self.basic_map.blcok_size
                    brick.rect.top = self.basic_map.map_top + x[i]*self.basic_map.blcok_size
                    brick.being = True
                    self.brickGroup.add(brick)
            #iron
            num_iron = round(rate_iron*total_grids)
            x = np.random.randint(0,rows,num_iron)
            y = np.random.randint(0,cols,num_iron)
            for i in range(num_iron):
                if self.small_map[x[i],y[i]] == 0:
                    self.small_map[x[i],y[i]] = 11
                    iron = Iron()
                    iron.rect.left = self.basic_map.map_left + y[i]*self.basic_map.blcok_size
                    iron.rect.top = self.basic_map.map_top + x[i]*self.basic_map.blcok_size
                    iron.being = True
                    self.ironGroup.add(iron)
                    
            if self._check_connection():
                break
        
        for i in range(len(self.basic_map.home_walls_left)):
            iron = Iron()
            iron.rect.left = self.basic_map.home_walls_left[i]
            iron.rect.top = self.basic_map.home_walls_top[i]
            iron.being = False
#            self.ironGroup.add(iron)
            self.home_wall_iron.add(iron)
        for i in range(len(self.basic_map.home_walls_left)):
            brick = Brick()
            brick.rect.left = self.basic_map.home_walls_left[i]
            brick.rect.top = self.basic_map.home_walls_top[i]
            brick.being = True
            self.brickGroup.add(brick)
#            self.home_wall_brick.append(brick)
        
    def protect_home(self, stronger=False):
        if stronger:
            for iron in self.home_wall_iron:
                iron.being = True
                if not self.ironGroup.has(iron):
                    self.ironGroup.add(iron)
            pass
        else:
            for iron in self.home_wall_iron:
                iron.being = False
                if self.ironGroup.has(iron):
                    self.ironGroup.remove(iron)
            pass
        
    def print_map(self):
        print(self.small_map)

    def _check_connection(self):
        _small_map = self.small_map.copy()
        (rows,cols) = self.small_map.shape
        check_birth_point = False
        enemy_points = []
        grow_list = []
        for i in range(rows):
            for j in range(cols):
                if _small_map[i,j] == -3: 
                    _small_map[i,j] = 0
                    if (not check_birth_point):
                        check_birth_point = True
                        grow_list.append((i,j))
                elif _small_map[i,j] == -4:
                    _small_map[i,j] = 0
                    enemy_points.append((i,j))
                elif _small_map[i,j] == -2:
                    _small_map[i,j] = 1
                elif _small_map[i,j] == -1:
                    _small_map[i,j] = 10
        
        if not check_birth_point:
            raise ValueError("缺少出生点")
        
        
        
        while (len(grow_list)>0):
            (r,c) = grow_list.pop()
            _small_map[r,c] = 100
            for (i,j) in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                if i >= 0 and i < rows and j >= 0 and j < cols and _small_map[i,j] < 10:
                    grow_list.append((i,j))
                    
#        print(enemy_points)
        for (r,c) in grow_list:
            if _small_map[r,c] != 100:
                return False
        else:
            return True
            
        

if __name__ == "__main__":
    bm = Basic_Map(625,625)
    m = Map(bm)
    m.get_map()    
    m.print_map()
    



