# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 10:42:51 2018

Tanks

@author: yaj
"""


import pygame
import random
from bullet import Bullet
import time
import food

class Tank(pygame.sprite.Sprite):
    def __init__(self, tank_kind, basic_map, img, armor_level, gun_level, speed_level, direction_x_s, direction_y_s, sp_left, sp_top):
        '''
        tank_kind:
            0:己方坦克
            1:敌方坦克
        '''
        super().__init__()
        self.being = True
        #坦克类型
        self.kind = tank_kind
        #地图信息
        self.basic_map = basic_map
        self.left = basic_map.map_left
        self.top = basic_map.map_top
        self.right = basic_map.width - basic_map.map_left
        self.bottom = basic_map.height - basic_map.map_top
        #出生方向        
        self.direction_x_s = direction_x_s
        self.direction_y_s = direction_y_s
        self.direction_x = direction_x_s
        self.direction_y = direction_y_s
        #加载坦克图像
        self.tank = pygame.image.load(img).convert_alpha()
        self.tank_imgs = []
        if direction_x_s == 0 and direction_y_s == -1:
            self.tank_imgs.append(self.tank.subsurface((0,0),(48,48)))
            self.tank_imgs.append(self.tank.subsurface((48, 0), (48, 48)))
        elif direction_x_s == 0 and direction_y_s == 1:
            self.tank_imgs.append(self.tank.subsurface((0,48),(48,48)))
            self.tank_imgs.append(self.tank.subsurface((48, 48), (48, 48)))
        elif direction_x_s == -1 and direction_y_s == 0:
            self.tank_imgs.append(self.tank.subsurface((0,48*2),(48,48)))
            self.tank_imgs.append(self.tank.subsurface((48, 48*2), (48, 48)))
        elif direction_x_s == 1 and direction_y_s == 0:
            self.tank_imgs.append(self.tank.subsurface((0,48*3),(48,48)))
            self.tank_imgs.append(self.tank.subsurface((48, 48*3), (48, 48)))
        else:
            raise ValueError('Tank class -> direction value error.')   
        self.tank_img_index = 1
        self.tank_img = self.tank_imgs[self.tank_img_index]
        self.rect = self.tank_img.get_rect()
        self.rect.left = sp_left
        self.rect.top = sp_top
        
        #装甲
        if armor_level <= 0:
            raise ValueError('Tank class -> armor level must bigger than 0.')
        self.armor = armor_level
        #速度
        if speed_level <= 0:
            raise ValueError('Tank class -> speed level must bigger than 0.')
        self.speed = round(3*(1.0+speed_level/10))
        #射击cd
        if gun_level <= 0:
            raise ValueError('Tank class -> gun level must bigger than 0.')
        self.shoot_cd = 5000/(1.0 + gun_level/10)
        self.shoot_cding = 0
        #子弹
        self.bullet_speed_factor = 1.0 + gun_level/10
        if gun_level > 5:
            self.bullet_stronger = True
        else:
            self.bullet_stronger = False
        
        #保护罩
        self.protect_mask = pygame.image.load('./images/others/protect.png').convert_alpha()
        self.protect_mask1 = self.protect_mask.subsurface((0,0),(48,48))
        self.protect_mask2 = self.protect_mask.subsurface((48,0),(48,48))        
        self.protected = False
        
    def reset(self,armor_level, gun_level, speed_level, sp_left, sp_top):
        self.rect.left = sp_left
        self.rect.top = sp_top
        #装甲
        if armor_level <= 0:
            raise ValueError('Tank class -> armor level must bigger than 0.')
        self.armor = armor_level
        #速度
        if speed_level <= 0:
            raise ValueError('Tank class -> speed level must bigger than 0.')
        self.speed = round(3*(1.0+speed_level/10))
        #射击cd
        if gun_level <= 0:
            raise ValueError('Tank class -> gun level must bigger than 0.')
        self.shoot_cd = 5000/(1.0 + gun_level/10)
        self.shoot_cding = 0
        #子弹
        self.bullet_speed_factor = 1.0 + gun_level/10
        if gun_level > 5:
            self.bullet_stronger = True
        else:
            self.bullet_stronger = False
    
    def shoot(self):
        if self.shoot_cding > 0:
            return None
        bullet = Bullet(self.basic_map,self.kind)
        bullet.speed = round(bullet.speed*self.bullet_speed_factor)
        bullet.stronger = self.bullet_stronger
        bullet.being = True
        bullet.turn(self.direction_x,self.direction_y)
        #子弹位置
        if self.direction_x == 0 and self.direction_y == -1:
            bullet.rect.left = self.rect.left + (48-12)/2
            bullet.rect.bottom = self.rect.top - 1
        elif self.direction_x == 0 and self.direction_y == 1:
            bullet.rect.left = self.rect.left + (48-12)/2
            bullet.rect.top = self.rect.bottom + 1
        elif self.direction_x == -1 and self.direction_y == 0:
            bullet.rect.right = self.rect.left - 1
            bullet.rect.top = self.rect.top + (48-12)/2
        elif self.direction_x == 1 and self.direction_y == 0:
            bullet.rect.left = self.rect.right + 1
            bullet.rect.top = self.rect.top + (48-12)/2
        else:
            raise ValueError('Tank class -> direction value error.')
        self.shoot_cding = self.shoot_cd
        return bullet
    
    def shoot_reload(self,deltT):
        self.shoot_cding = max(self.shoot_cding-deltT,0)
   
    def be_shooted(self, bullet):
        '''
        返回是否被击毁
        '''
        if self.protected:
            return False
        if isinstance(bullet,pygame.sprite.Sprite):
            if bullet.from_who != self.kind:
                if bullet.stronger:
                    self.armor -= 3
                else:
                    self.armor -= 1
        else:
            for b in bullet:
                if b.from_who != self.kind:
                    if b.stronger:
                        self.armor -= 3
                    else:
                        self.armor -= 1
        
        if self.armor <= 0:
            return True
        else:
            return False
    
    def turn(self,direction):
        '''
        direction:
            up
            down
            left
            right
        '''
        if direction == 'up':
            self.direction_x = 0
            self.direction_y = -1
            self.tank_imgs[0] = self.tank.subsurface((0,0),(48,48))
            self.tank_imgs[1] = self.tank.subsurface((48, 0), (48, 48))
            pass
        elif direction == 'down':
            self.direction_x = 0
            self.direction_y = 1
            self.tank_imgs[0] = self.tank.subsurface((0,48),(48,48))
            self.tank_imgs[1] = self.tank.subsurface((48, 48), (48, 48))
            pass
        elif direction == 'left':
            self.direction_x = -1
            self.direction_y = 0
            self.tank_imgs[0] = self.tank.subsurface((0,48*2),(48,48))
            self.tank_imgs[1] = self.tank.subsurface((48, 48*2), (48, 48))
            pass
        elif direction == 'right':
            self.direction_x = 1
            self.direction_y = 0
            self.tank_imgs[0] = self.tank.subsurface((0,48*3),(48,48))
            self.tank_imgs[1] = self.tank.subsurface((48, 48*3), (48, 48))
            pass
        else:
            raise ValueError('Tank class -> direction key error.')
        
        self.tank_img_index = (self.tank_img_index + 1)%2
        self.tank_img = self.tank_imgs[self.tank_img_index]
    
    def move(self, direction,tankGroup, brickGroup, ironGroup, home):
        '''
        direction:
            up
            down
            left
            right
        '''
        self.turn(direction)
        
        self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
        can_move = self._can_move(tankGroup, brickGroup, ironGroup, home)
#        if can_move:
#            self.tank_img_index = (self.tank_img_index + 1)%2
#            self.tank_img = self.tank_imgs[self.tank_img_index]
        if not can_move:
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            min_step = 1
            self.rect = self.rect.move(min_step*self.direction_x, min_step*self.direction_y)
            can_move = self._can_move(tankGroup, brickGroup, ironGroup, home)
            if not can_move:
                self.rect = self.rect.move(min_step*-self.direction_x, min_step*-self.direction_y)
    
    def _can_move(self,tankGroup, brickGroup, ironGroup, home):
        #判断是否到底地图边缘
        if self.rect.top < self.top or self.rect.bottom > self.bottom or self.rect.left < self.left or self.rect.right > self.right:
            return False
        #和墙碰撞
        if pygame.sprite.spritecollide(self,brickGroup,False,None) or pygame.sprite.spritecollide(self,ironGroup,False,None):
            return False
        #和其他坦克碰撞
        if pygame.sprite.spritecollide(self,tankGroup,False,None):
            return False
        #和大本营碰撞
        if pygame.sprite.collide_rect(self,home):
            return False
        return True    

class MyTank():
    def __init__(self,player,basic_map):
        self.player = player
        self.basic_map = basic_map
        self.life = 3
        self.armor_level = 1
        self.speed_level = 1
        self.gun_level = 1
        if player == 1:
            self.tank = Tank(0,basic_map,'./images/myTank/tank_T1_0.png',self.armor_level,self.gun_level,self.speed_level,0,-1,basic_map.birth_point_1_left,basic_map.birth_point_1_top)
        else:
            self.tank = Tank(0,basic_map,'./images/myTank/tank_T2_0.png',self.armor_level,self.gun_level,self.speed_level,0,-1,basic_map.birth_point_2_left,basic_map.birth_point_2_top)
        self.can_move = True
        self.can_shoot = True
        
    def level_up(self,level_kind):
        if (level_kind == 'armor'):
            self.armor_level += 1
        elif (level_kind == 'gun'):
            self.gun_level += 1
        elif (level_kind == 'speed'):
            self.speed_level += 1
        else:
            raise ValueError('MyTank class -> level kind key error.')  
            
        self.reset()
    
    def level_down(self,level_kind):
        if (level_kind == 'armor'):
            if self.armor_level > 1:
                self.armor_level -= 1
        elif (level_kind == 'gun'):
            if self.gun_level > 1:
                self.gun_level -= 1
        elif (level_kind == 'speed'):
            if self.speed_level > 1:
                self.speed_level -= 1
        else:
            raise ValueError('MyTank class -> level kind key error.')
            
        self.reset()
        
    def set_level(self,armor_level,gun_level,speed_level):
        assert armor_level > 0, 'MyTank class -> armor_level must bigger than 0.'
        assert gun_level > 0, 'MyTank class -> gun_level must bigger than 0.'
        assert speed_level > 0, 'MyTank class -> speed_level must bigger than 0.'
        assert armor_level <= 60, 'MyTank class -> armor_level must less than 60.'
        assert gun_level <= 60, 'MyTank class -> gun_level must less than 60.'
        assert speed_level <= 60, 'MyTank class -> speed_level must less than 60.'
        self.armor_level = armor_level
        self.speed_level = speed_level
        self.gun_level = gun_level
        
        self.reset()
            
    def shoot(self):
        if self.can_shoot:
            return self.tank.shoot()
        return None
    
    def shoot_reload(self,deltT):
        self.tank.shoot_reload(deltT)
    
    def be_shooted(self, bullet):
        '''
        返回角色是否死亡
        '''
        destoried = self.tank.be_shooted(bullet)
        if destoried:
            self.life -= 1
            if self.life <= 0:
                return True
            else:
                self.reset()
        return False
    
    def reset(self):
        if self.player == 1:
            self.tank.turn('up')
            self.tank.reset(self.armor_level,self.gun_level,self.speed_level,self.basic_map.birth_point_1_left,self.basic_map.birth_point_1_top)
        else:
            self.tank.turn('up')
            self.tank.reset(self.armor_level,self.gun_level,self.speed_level,self.basic_map.birth_point_2_left,self.basic_map.birth_point_2_top)
        
    def move(self,direction,tankGroup, brickGroup, ironGroup, home):
        if self.can_move:
            self.tank.move(direction,tankGroup, brickGroup, ironGroup, home)


class EnemyTank():
    def __init__(self,basic_map,level,sp_index):
        if level > 4 or level <= 0:
            raise ValueError('EnemyTank class -> level must between 0 and 3')
        if sp_index < 0 or sp_index >= len(basic_map.enemy_points_top):
            raise ValueError('EnemyTank class -> startpoint index must between 0 and {}'.format(len(basic_map.enemy_points_top)))
        self.level = level
        self.tanks1 = ['./images/enemyTank/enemy_1_0.png', './images/enemyTank/enemy_1_1.png', './images/enemyTank/enemy_1_2.png', './images/enemyTank/enemy_1_3.png']
        self.tanks2 = ['./images/enemyTank/enemy_2_0.png', './images/enemyTank/enemy_2_1.png', './images/enemyTank/enemy_2_2.png', './images/enemyTank/enemy_2_3.png']
        self.tanks3 = ['./images/enemyTank/enemy_3_0.png', './images/enemyTank/enemy_3_1.png', './images/enemyTank/enemy_3_2.png', './images/enemyTank/enemy_3_3.png']
        self.tanks4 = ['./images/enemyTank/enemy_4_0.png', './images/enemyTank/enemy_4_1.png', './images/enemyTank/enemy_4_2.png', './images/enemyTank/enemy_4_3.png']
        self.tanks = [self.tanks1, self.tanks2, self.tanks3, self.tanks4]
        img_type = random.randint(0,3)
        if level == 1:
            gun_level = 1
        else:
            gun_level = level*2
        self.tank = Tank(1,basic_map,self.tanks[level-1][img_type],level,gun_level,level,0,1,basic_map.enemy_points_left[sp_index],basic_map.enemy_points_top[sp_index])
        self.with_food = False
        if random.randint(0,9) < 1:
            self.with_food = True
        self.can_move = True
        self.can_shoot = True
        self.last_move = 'down'
        
    def shoot(self):
        '''
        随机射击
        '''
        if self.can_shoot:
            if random.randint(0,9) < 5:
                return self.tank.shoot()
        return None
        
    def shoot_reload(self,deltT):
        self.tank.shoot_reload(deltT)
    
    def be_shooted(self,bullet):
        destoried = self.tank.be_shooted(bullet)
        return destoried

    def move(self,tankGroup, brickGroup, ironGroup, home):
        '''
        随机移动
        '''
        if self.can_move:
            move_direction = ['up','down','left','right']
            direction = random.randint(0,19)
            if (direction < 4):
                self.tank.move(move_direction[direction],tankGroup, brickGroup, ironGroup, home)
                self.last_move = move_direction[direction]
            else:
                self.tank.move(self.last_move,tankGroup, brickGroup, ironGroup, home)



