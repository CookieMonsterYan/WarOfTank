# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 17:41:35 2018

@author: yaj
"""

import pygame
from pygame.locals import *
import scene
import tank
import bullet
import food
import home
import sys
import json
import os
import random
import numpy as np
import math
import levelmark

#用于保存游戏进度中player信息的类
class PlayerInfo():
    def __init__(self,life,armor_level,gun_level,speed_level):
        self.life = life
        self.armor_level = armor_level
        self.gun_level = gun_level
        self.speed_level = speed_level
#        self.score = score

#用于保存游戏进度的类
class GameInfo():
    def __init__(self,num_player):
        self.save_folder = './save/'
        if not os.path.isdir(self.save_folder):
            os.makedirs(self.save_folder)
        self.save_file = os.path.join(self.save_folder,'GameInfo.json')
        self.num_player = num_player
        self.player1 = PlayerInfo(3,1,1,1)
        self.player2 = PlayerInfo(3,1,1,1)
        self.stage = 0
        self.score = 0
        
    def save(self):
        save_dict = {
                'num_player':self.num_player,
                'stage':self.stage,
                'score':self.score,
                'player1_life':self.player1.life,
                'player1_armor':self.player1.armor_level,
                'player1_gun':self.player1.gun_level,
                'player1_speed':self.player1.speed_level,
                'player2_life':self.player2.life,
                'player2_armor':self.player2.armor_level,
                'player2_gun':self.player2.gun_level,
                'player2_speed':self.player2.speed_level,
                }
        with open(self.save_file, 'w') as f:
            json.dump(save_dict,f)
            
    def load(self):
        if not os.path.isfile(self.save_file):
            return False
        with open(self.save_file, 'r') as f:
            save_dict = json.load(f)
        self.num_player = save_dict['num_player']
        self.stage = save_dict['stage']-1
        self.score = save_dict['score']
        self.player1.life = save_dict['player1_life']
        self.player1.armor_level = save_dict['player1_armor']
        self.player1.gun_level = save_dict['player1_gun']
        self.player1.speed_level = save_dict['player1_speed']
        self.player2.life = save_dict['player2_life']
        self.player2.armor_level = save_dict['player2_armor']
        self.player2.gun_level = save_dict['player2_gun']
        self.player2.speed_level = save_dict['player2_speed']
        return True


#开始画面
def show_start(screen, width, height):
    tfont = pygame.font.Font('./font/simkai.ttf', height//4)
    cfont = pygame.font.Font('./font/simkai.ttf', height//20)
    title = tfont.render(u'坦克大战',True,(255,0,0))
    text_1player = cfont.render(u'按1进入单人游戏',True,(0,0,255))
    text_2player = cfont.render(u'按2进入双人游戏',True,(0,0,255))
    text_load = cfont.render(u'按L加载游戏',True,(0,0,255))
    rect_title = title.get_rect()
    rect_title.midtop = (width/2,height/4)
    rect_1player = text_1player.get_rect()
    rect_1player.midtop = (width/2,height/1.8)
    rect_2player = text_2player.get_rect()
    rect_2player.midtop = (width/2,height/1.6)
    rect_load = text_load.get_rect()
    rect_load.midtop = (width/2,height/1.4)
    screen.blit(title,rect_title)
    screen.blit(text_1player,rect_1player)
    screen.blit(text_2player,rect_2player)
    screen.blit(text_load,rect_load)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_l:
                    return 3
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

def show_end(screen, width, height):
    img_bg = pygame.image.load("./images/others/background3.png")
    screen.blit(img_bg,(0,0))
    img_fail = pygame.image.load("./images/others/gameover.png")
    rect_fail = img_fail.get_rect()
    rect_fail.midtop = (width/2,height/2)
    screen.blit(img_fail,rect_fail)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

def show_switch_stage(screen, width, height, game_info):
    game_info.save()
    
    sound_levelup = pygame.mixer.Sound("./audios/levelup.wav")
    sound_levelup.set_volume(1)
    
    p1_armor_mark_group = pygame.sprite.Group()
    p1_fire_mark_group = pygame.sprite.Group()
    p1_speed_mark_group = pygame.sprite.Group()
    p2_armor_mark_group = pygame.sprite.Group()
    p2_fire_mark_group = pygame.sprite.Group()
    p2_speed_mark_group = pygame.sprite.Group()
    
    mark_bottom = height*17/20
    p1_armor_mark_left = width/20*1
    p1_fire_mark_left = width/20*4
    p1_speed_mark_left = width/20*7
    p2_armor_mark_left = width/20*10
    p2_fire_mark_left = width/20*13
    p2_speed_mark_left = width/20*16
    
    font = pygame.font.Font('./font/simkai.ttf', height//20)
    text1 = font.render(u'游戏已保存，按下ESC退出',True,(255,255,0))
    rect_text1 = text1.get_rect()
    rect_text1.midtop = (width/2,height/20)
    text2 = font.render(u'第{}关，按空格键开始战斗'.format(game_info.stage),True,(0,255,0))
    rect_text2 = text2.get_rect()
    rect_text2.midtop = (width/2,height/10)
    sfont = pygame.font.Font('./font/simkai.ttf', height//28)
    sfont2 = pygame.font.Font('./font/simkai.ttf', height//30)
    sfont3 = pygame.font.Font('./font/simkai.ttf', height//40)
    text_p1_a = sfont.render(u'1P装甲等级',True,(255,255,255))
    text_p1_a_rect = text_p1_a.get_rect()
    text_p1_a_rect = (p1_armor_mark_left-width/40,mark_bottom+4)
    text_p1_f = sfont.render(u'1P火炮等级',True,(255,255,255))
    text_p1_f_rect = text_p1_f.get_rect()
    text_p1_f_rect = (p1_fire_mark_left-width/40,mark_bottom+4)
    text_p1_s = sfont.render(u'1P引擎等级',True,(255,255,255))
    text_p1_s_rect = text_p1_s.get_rect()
    text_p1_s_rect = (p1_speed_mark_left-width/40,mark_bottom+4)
    text_p2_a = sfont.render(u'2P装甲等级',True,(255,255,255))
    text_p2_a_rect = text_p2_a.get_rect()
    text_p2_a_rect = (p2_armor_mark_left-width/40,mark_bottom+4)
    text_p2_f = sfont.render(u'2P火炮等级',True,(255,255,255))
    text_p2_f_rect = text_p2_f.get_rect()
    text_p2_f_rect = (p2_fire_mark_left-width/40,mark_bottom+4)
    text_p2_s = sfont.render(u'2P引擎等级',True,(255,255,255))
    text_p2_s_rect = text_p2_s.get_rect()
    text_p2_s_rect = (p2_speed_mark_left-width/40,mark_bottom+4)
    text_p1_a_up = sfont2.render(u'Q键升级1P装甲',True,(255,255,255))
    text_p1_a_up_rect = text_p1_a_up.get_rect()
    text_p1_a_up_rect = (p1_armor_mark_left-width/40,mark_bottom-30*13)
    text_p1_f_up = sfont2.render(u'W键升级1P火炮',True,(255,255,255))
    text_p1_f_up_rect = text_p1_f_up.get_rect()
    text_p1_f_up_rect = (p1_fire_mark_left-width/40,mark_bottom-30*13)
    text_p1_s_up = sfont2.render(u'E键升级1P引擎',True,(255,255,255))
    text_p1_s_up_rect = text_p1_s_up.get_rect()
    text_p1_s_up_rect = (p1_speed_mark_left-width/40,mark_bottom-30*13)
    text_p2_a_up = sfont2.render(u'7键升级2P装甲',True,(255,255,255))
    text_p2_a_up_rect = text_p2_a_up.get_rect()
    text_p2_a_up_rect = (p2_armor_mark_left-width/40,mark_bottom-30*13)
    text_p2_f_up = sfont2.render(u'8键升级2P火炮',True,(255,255,255))
    text_p2_f_up_rect = text_p2_f_up.get_rect()
    text_p2_f_up_rect = (p2_fire_mark_left-width/40,mark_bottom-30*13)
    text_p2_s_up = sfont2.render(u'9键升级2P引擎',True,(255,255,255))
    text_p2_s_up_rect = text_p2_s_up.get_rect()
    text_p2_s_up_rect = (p2_speed_mark_left-width/40,mark_bottom-30*13)
    
    for i in range(1,game_info.player1.armor_level+1):
        p1_armor_mark_group.add(levelmark.Level('armor',p1_armor_mark_left,mark_bottom,i))
    
    for i in range(1,game_info.player1.gun_level+1):
        p1_fire_mark_group.add(levelmark.Level('fire',p1_fire_mark_left,mark_bottom,i))
        
    for i in range(1,game_info.player1.speed_level+1):
        p1_speed_mark_group.add(levelmark.Level('speed',p1_speed_mark_left,mark_bottom,i))
        
    for i in range(1,game_info.player2.armor_level+1):
        p2_armor_mark_group.add(levelmark.Level('armor',p2_armor_mark_left,mark_bottom,i))
    
    for i in range(1,game_info.player2.gun_level+1):
        p2_fire_mark_group.add(levelmark.Level('fire',p2_fire_mark_left,mark_bottom,i))
        
    for i in range(1,game_info.player2.speed_level+1):
        p2_speed_mark_group.add(levelmark.Level('speed',p2_speed_mark_left,mark_bottom,i))
    
    while True:
        img_bg = pygame.image.load("./images/others/background3.png")
        screen.blit(img_bg,(0,0))
                
        screen.blit(text1,rect_text1)        
        screen.blit(text2,rect_text2)
        text_score = font.render(u'SCORES: {}'.format(game_info.score),True,(255,255,255))
        rect_score = text_score.get_rect()
        rect_score.midtop = (width/2,height*19/20-height/40)
        screen.blit(text_score,rect_score)
        
        screen.blit(text_p1_a,text_p1_a_rect)
        screen.blit(text_p1_f,text_p1_f_rect)
        screen.blit(text_p1_s,text_p1_s_rect)
        screen.blit(text_p2_a,text_p2_a_rect)
        screen.blit(text_p2_f,text_p2_f_rect)
        screen.blit(text_p2_s,text_p2_s_rect)
        
        screen.blit(text_p1_a_up,text_p1_a_up_rect)
        screen.blit(text_p1_f_up,text_p1_f_up_rect)
        screen.blit(text_p1_s_up,text_p1_s_up_rect)
        screen.blit(text_p2_a_up,text_p2_a_up_rect)
        screen.blit(text_p2_f_up,text_p2_f_up_rect)
        screen.blit(text_p2_s_up,text_p2_s_up_rect)
        
        text_p1_a_up_s = sfont3.render(u'升级需要{}'.format(game_info.player1.armor_level*1000),True,(255,255,50))
        text_p1_a_up_s_rect = text_p1_a_up_s.get_rect()
        text_p1_a_up_s_rect = (p1_armor_mark_left-width/40,mark_bottom-30*13-height/30)
        text_p1_f_up_s = sfont3.render(u'升级需要{}'.format(game_info.player1.gun_level*1000),True,(255,255,0))
        text_p1_f_up_s_rect = text_p1_f_up_s.get_rect()
        text_p1_f_up_s_rect = (p1_fire_mark_left-width/40,mark_bottom-30*13-height/30)
        text_p1_s_up_s = sfont3.render(u'升级需要{}'.format(game_info.player1.speed_level*1000),True,(255,255,0))
        text_p1_s_up_s_rect = text_p1_s_up_s.get_rect()
        text_p1_s_up_s_rect = (p1_speed_mark_left-width/40,mark_bottom-30*13-height/30)
        text_p2_a_up_s = sfont3.render(u'升级需要{}'.format(game_info.player2.armor_level*1000),True,(255,255,0))
        text_p2_a_up_s_rect = text_p2_a_up_s.get_rect()
        text_p2_a_up_s_rect = (p2_armor_mark_left-width/40,mark_bottom-30*13-height/30)
        text_p2_f_up_s = sfont3.render(u'升级需要{}'.format(game_info.player2.gun_level*1000),True,(255,255,0))
        text_p2_f_up_s_rect = text_p2_f_up_s.get_rect()
        text_p2_f_up_s_rect = (p2_fire_mark_left-width/40,mark_bottom-30*13-height/30)
        text_p2_s_up_s = sfont3.render(u'升级需要{}'.format(game_info.player2.speed_level*1000),True,(255,255,0))
        text_p2_s_up_s_rect = text_p2_s_up_s.get_rect()
        text_p2_s_up_s_rect = (p2_speed_mark_left-width/40,mark_bottom-30*13-height/30)
        screen.blit(text_p1_a_up_s,text_p1_a_up_s_rect)
        screen.blit(text_p1_f_up_s,text_p1_f_up_s_rect)
        screen.blit(text_p1_s_up_s,text_p1_s_up_s_rect)
        screen.blit(text_p2_a_up_s,text_p2_a_up_s_rect)
        screen.blit(text_p2_f_up_s,text_p2_f_up_s_rect)
        screen.blit(text_p2_s_up_s,text_p2_s_up_s_rect)
        
        for mark in p1_armor_mark_group:
            screen.blit(mark.img,mark.rect)
            
        for mark in p1_fire_mark_group:
            screen.blit(mark.img,mark.rect)
            
        for mark in p1_speed_mark_group:
            screen.blit(mark.img,mark.rect)
            
        for mark in p2_armor_mark_group:
            screen.blit(mark.img,mark.rect)
            
        for mark in p2_fire_mark_group:
            screen.blit(mark.img,mark.rect)
            
        for mark in p2_speed_mark_group:
            screen.blit(mark.img,mark.rect)
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_q and game_info.score >= (game_info.player1.armor_level*1000) and game_info.player1.armor_level < 60:                    
                    sound_levelup.play()
                    game_info.score -= game_info.player1.armor_level*1000
                    game_info.player1.armor_level += 1
                    p1_armor_mark_group.add(levelmark.Level('armor',p1_armor_mark_left,mark_bottom,game_info.player1.armor_level))
                elif event.key == pygame.K_w and game_info.score >= (game_info.player1.gun_level*1000) and game_info.player1.gun_level < 60:                    
                    sound_levelup.play()
                    game_info.score -= game_info.player1.gun_level*1000
                    game_info.player1.gun_level += 1
                    p1_fire_mark_group.add(levelmark.Level('fire',p1_fire_mark_left,mark_bottom,game_info.player1.gun_level))
                elif event.key == pygame.K_e and game_info.score >= (game_info.player1.speed_level*1000) and game_info.player1.speed_level < 60:                    
                    sound_levelup.play()
                    game_info.score -= game_info.player1.speed_level*1000
                    game_info.player1.speed_level += 1
                    p1_speed_mark_group.add(levelmark.Level('speed',p1_speed_mark_left,mark_bottom,game_info.player1.speed_level))
                elif event.key == pygame.K_KP7 and game_info.score >= (game_info.player2.armor_level*1000) and game_info.player2.armor_level < 60:                    
                    sound_levelup.play()
                    game_info.score -= game_info.player2.armor_level*1000
                    game_info.player2.armor_level += 1
                    p2_armor_mark_group.add(levelmark.Level('armor',p2_armor_mark_left,mark_bottom,game_info.player2.armor_level))
                elif event.key == pygame.K_KP8 and game_info.score >= (game_info.player2.gun_level*1000) and game_info.player2.gun_level < 60:                    
                    sound_levelup.play()
                    game_info.score -= game_info.player2.gun_level*1000
                    game_info.player2.gun_level += 1
                    p2_fire_mark_group.add(levelmark.Level('fire',p2_fire_mark_left,mark_bottom,game_info.player2.gun_level))
                elif event.key == pygame.K_KP9 and game_info.score >= (game_info.player2.speed_level*1000) and game_info.player2.speed_level < 60:                   
                    sound_levelup.play()
                    game_info.score -= game_info.player2.speed_level*1000
                    game_info.player2.speed_level += 1
                    p2_speed_mark_group.add(levelmark.Level('speed',p2_speed_mark_left,mark_bottom,game_info.player2.speed_level))


def main():
    pygame.init()
    pygame.mixer.init()
    width,height = 924,624
    map_width,map_height = 624,624
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('War of Tanks')
    #字体
    cfont = pygame.font.Font('./font/simkai.ttf', 48)
    #背景图片
    img_bg = pygame.image.load("./images/others/background2.png")
    #加载音效
    sound_add = pygame.mixer.Sound("./audios/add.wav")
    sound_add.set_volume(1)
    sound_bang = pygame.mixer.Sound("./audios/bang.wav")
    sound_bang.set_volume(1)
    sound_blast = pygame.mixer.Sound("./audios/blast.wav")
    sound_blast.set_volume(1)
    sound_fire = pygame.mixer.Sound("./audios/fire.wav")
    sound_fire.set_volume(1)
    sound_Gunfire = pygame.mixer.Sound("./audios/Gunfire.wav")
    sound_Gunfire.set_volume(1)
    sound_hit = pygame.mixer.Sound("./audios/hit.wav")
    sound_hit.set_volume(1)
    sound_start = pygame.mixer.Sound("./audios/start.wav")
    sound_start.set_volume(1)
    sound_win = pygame.mixer.Sound("./audios/win.wav")
    sound_win.set_volume(1)
    #开始画面
    play_mode = show_start(screen,width,height)
    if play_mode != 3:
        num_player = play_mode
        game_info = GameInfo(num_player)
        game_info.save()
    else:
        game_info = GameInfo(1)
        if not game_info.load():
            game_info.save()
    #游戏是否结束
    is_gameover = False
    #时钟
    clock = pygame.time.Clock()
    clock_tick = 60
    #basic map
    basic_map = scene.Basic_Map(map_height,map_width)
    #map
    my_map = scene.Map(basic_map)
    #计分板
    board_player1 = pygame.image.load("./images/myTank/tank_T1_0.png").convert_alpha().subsurface((0,48*3),(48,48))
    board_player1_rect = board_player1.get_rect()
    board_player1_rect.midtop =(map_width + (width-map_width)/3,height/4)
    board_player2 = pygame.image.load("./images/myTank/tank_T2_0.png").convert_alpha().subsurface((0,48*3),(48,48))
    board_player2_rect = board_player2.get_rect()
    board_player2_rect.midtop =(map_width + (width-map_width)/3,height/2)
    #主循环
    while not is_gameover:
        game_info.stage += 1
        show_switch_stage(screen, width, height, game_info)        
        #播放游戏开始音乐
        sound_start.play()
        #关卡难度
        enemy_total = (game_info.stage)*6
        enemy_levels_rate = np.zeros(100)
        enemy_level_1_rate = random.randint(math.ceil(50/game_info.stage),math.ceil(100/game_info.stage))
        enemy_levels_rate[:enemy_level_1_rate] = 1
        if enemy_level_1_rate < 100:
            enemy_level_2_rate = min(100,enemy_level_1_rate+random.randint(1,math.ceil(100/game_info.stage)))
            enemy_levels_rate[enemy_level_1_rate:enemy_level_2_rate] = 2
            if enemy_level_2_rate < 100:
                enemy_level_3_rate = min(100,enemy_level_2_rate+random.randint(1,math.ceil(100/game_info.stage)))
                enemy_levels_rate[enemy_level_2_rate:enemy_level_3_rate] = 3
                if enemy_level_3_rate < 100:
                    enemy_levels_rate[enemy_level_3_rate:] = 4
        enemy_levels_rate = enemy_levels_rate.astype('int')
        enemy_levels_rate = enemy_levels_rate.tolist()
        #地图上可以同时存在的最大地方坦克的数量
        enemy_now_max = 20
        #当前存在的地方坦克数量
        enemy_now = 0
        #精灵组
        tanksGroup = pygame.sprite.Group()
        tanksGroup_my = pygame.sprite.Group()
        bulletsGroup = pygame.sprite.Group()
        foodsGroup = pygame.sprite.Group()
        #坦克组
        mytanks = []
        enemytanks = []
        #自定义事件
        #   生成地方坦克事件
        generate_enemy_event = pygame.constants.USEREVENT + 0
        pygame.time.set_timer(generate_enemy_event, 100)
        #   地方坦克恢复事件
        recover_enemy_event = pygame.constants.USEREVENT + 1
        pygame.time.set_timer(recover_enemy_event, 8000)
        #   我方坦克无敌恢复事件
        unprotect_me_event = pygame.constants.USEREVENT + 2
        pygame.time.set_timer(unprotect_me_event, 8000)        
        #生成关卡地图
        my_map.get_map()
        #我方坦克
        tank_player1 = tank.MyTank(1,basic_map)
        tank_player1.set_level(game_info.player1.armor_level,game_info.player1.gun_level,game_info.player1.speed_level)
        tanksGroup.add(tank_player1.tank)
        tanksGroup_my.add(tank_player1.tank)
        mytanks.append(tank_player1)
        if game_info.num_player > 1:
            tank_player2 = tank.MyTank(2,basic_map)
            tank_player2.set_level(game_info.player2.armor_level,game_info.player2.gun_level,game_info.player2.speed_level)
            tanksGroup.add(tank_player2.tank)
            tanksGroup_my.add(tank_player2.tank)
            mytanks.append(tank_player2)
        #敌方坦克
        for i in range(len(basic_map.enemy_points_left)):
            if enemy_now < enemy_now_max and enemy_total > 0:
                e_level = enemy_levels_rate[random.randint(0,99)]
                enemy_tank = tank.EnemyTank(basic_map,e_level,i)
                if (not (pygame.sprite.spritecollide(enemy_tank.tank,tanksGroup,False,None) or pygame.sprite.spritecollide(enemy_tank.tank,bulletsGroup,False,None))):
                    tanksGroup.add(enemy_tank.tank)
                    enemytanks.append(enemy_tank)
                    enemy_now += 1
                    enemy_total -= 1
        #大本营
        myhome = home.Home(basic_map)
        #出场特效
        appearance_img = pygame.image.load("./images/others/appear.png").convert_alpha()
        appearances = []
        appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
        appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
        appearances.append(appearance_img.subsurface((96, 0), (48, 48)))
        #结束关卡前的倒计时
        before_end_stage = 5000
        #关卡主循环
        while True:
            if is_gameover:
                if before_end_stage <= 0:
                    break
                else:
                    before_end_stage -= clock_tick
                    for t in mytanks:
                        t.can_move = False
                        t.can_shoot = False
                    for t in enemytanks:
                        t.can_move = False
                        t.can_shoot = False
            if enemy_total < 1 and enemy_now < 1:
                is_gameover = False
                sound_win.play()
                if before_end_stage <= 0:
                    break
                else:
                    before_end_stage -= clock_tick
                    for t in mytanks:
                        t.can_move = False
                        t.can_shoot = False
                    for t in enemytanks:
                        t.can_move = False
                        t.can_shoot = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == generate_enemy_event:
                    for i in range(len(basic_map.enemy_points_left)):
                        if enemy_now < enemy_now_max and enemy_total > 0:
                            e_level = enemy_levels_rate[random.randint(0,99)]
                            enemy_tank = tank.EnemyTank(basic_map,e_level,i)
                            if (not (pygame.sprite.spritecollide(enemy_tank.tank,tanksGroup,False,None) or pygame.sprite.spritecollide(enemy_tank.tank,bulletsGroup,False,None))):
                                tanksGroup.add(enemy_tank.tank)
                                enemytanks.append(enemy_tank)
                                enemy_now += 1
                                enemy_total -= 1
                if event.type == recover_enemy_event:
                    for et in enemytanks:
                        et.can_move = True
                if event.type == unprotect_me_event:
                    for mt in mytanks:
                        mt.tank.protected = False
                        
            #检查用户键盘操作
            key_pressed = pygame.key.get_pressed()
            #ESC退出
            if key_pressed[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            # 玩家一
            # WSAD -> 上下左右
            # 空格键射击
            if key_pressed[pygame.K_w]:
                tanksGroup.remove(tank_player1.tank)
                tank_player1.move('up', tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                tanksGroup.add(tank_player1.tank)
            elif key_pressed[pygame.K_s]:
                tanksGroup.remove(tank_player1.tank)
                tank_player1.move('down', tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                tanksGroup.add(tank_player1.tank)
            elif key_pressed[pygame.K_a]:
                tanksGroup.remove(tank_player1.tank)
                tank_player1.move('left', tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                tanksGroup.add(tank_player1.tank)
            elif key_pressed[pygame.K_d]:
                tanksGroup.remove(tank_player1.tank)
                tank_player1.move('right', tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                tanksGroup.add(tank_player1.tank)
            elif key_pressed[pygame.K_SPACE]:
                _bullet = tank_player1.shoot()
                if _bullet != None:
                    bulletsGroup.add(_bullet)
                    sound_fire.play()
            # 玩家二
			# ↑↓←→ -> 上下左右
            # 小键盘0键射击
            if game_info.num_player > 1:
                if key_pressed[pygame.K_UP]:
                    tanksGroup.remove(tank_player2.tank)
                    tank_player2.move('up', tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                    tanksGroup.add(tank_player2.tank)
                elif key_pressed[pygame.K_DOWN]:
                    tanksGroup.remove(tank_player2.tank)
                    tank_player2.move('down', tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                    tanksGroup.add(tank_player2.tank)
                elif key_pressed[pygame.K_LEFT]:
                    tanksGroup.remove(tank_player2.tank)
                    tank_player2.move('left', tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                    tanksGroup.add(tank_player2.tank)
                elif key_pressed[pygame.K_RIGHT]:
                    tanksGroup.remove(tank_player2.tank)
                    tank_player2.move('right', tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                    tanksGroup.add(tank_player2.tank)
                elif key_pressed[pygame.K_KP0]:
                    _bullet = tank_player2.shoot()
                    if _bullet != None:
                        bulletsGroup.add(_bullet)
                        sound_fire.play()            
            #己方坦克吃食物
            for f in foodsGroup:
                if f.being and f.time > 0:
                    if pygame.sprite.spritecollide(f,tanksGroup_my,False,None):
                        f.being = False
                        foodsGroup.remove(f)
                        if f.kind == 0:
                            sound_bang.play()
                            for et in enemytanks:
                                et.tank.being = False
                                tanksGroup.remove(et.tank)
                            enemytanks = []
                            enemy_total -= enemy_now
                            enemy_now = 0
                        elif f.kind == 1:
                            for t in enemytanks:
                                t.can_move = False
                        elif f.kind == 2:
                            sound_add.play()
                            for t in mytanks:
                                t.tank.bullet_stronger = True
                        elif f.kind == 3:
                            my_map.protect_home(True)
                        elif f.kind == 4:
                            sound_add.play()
                            for t in mytanks:
                                t.tank.protected = True
                        elif f.kind == 5:
                            game_info.score += 1000
                        elif f.kind == 6:
                            sound_add.play()
                            for t in mytanks:
                                t.life += 1
                else:
                    f.being = False
                    foodsGroup.remove(f)
            # 敌方坦克行动
            for et in enemytanks:
                if et.can_move and et.tank.being:
                    tanksGroup.remove(et.tank)
                    et.move(tanksGroup,my_map.brickGroup,my_map.ironGroup,myhome)
                    tanksGroup.add(et.tank)
                    _bullet = et.shoot()
                    if _bullet != None:
                        bulletsGroup.add(_bullet)
            #子弹行动
            for b in bulletsGroup:
                if b.being:
                    b.move()
                else:
                    bulletsGroup.remove(b)
            for b in bulletsGroup:
                #子弹之间的碰撞检验
                bulletsGroup.remove(b)
                collide_bullets = pygame.sprite.spritecollide(b,bulletsGroup,False,None)
                if collide_bullets:
                    for cb in collide_bullets:
                        if cb.from_who != b.from_who:
                            b.being = False
                            cb.being = False
                            bulletsGroup.remove(cb)
                    if b.being:
                        bulletsGroup.add(b)
                else:
                    bulletsGroup.add(b)
                #子弹碰到墙
                if b.being:
                    collide_bricks = pygame.sprite.spritecollide(b,my_map.brickGroup,False,None)
                    if collide_bricks:
                        b.being = False
                        bulletsGroup.remove(b)
                        for cb in collide_bricks:
                            cb.being = False
                            my_map.brickGroup.remove(cb)
                #子弹碰到钢墙
                if b.being:
                    collide_irons = pygame.sprite.spritecollide(b,my_map.ironGroup,False,None)
                    if collide_irons:
                        b.being = False
                        bulletsGroup.remove(b)
                        if b.stronger:
                            for ci in collide_irons:
                                ci.being = False
                                my_map.ironGroup.remove(ci)
                #子弹碰到老家
                if b.being:
                    if pygame.sprite.collide_rect(b,myhome):
                        b.being = False
                        bulletsGroup.remove(b)
                        myhome.destory()
                        sound_blast.play()
                        is_gameover = True
                '''
                #子弹碰到坦克
                if b.being:
                    collide_tanks = pygame.sprite.spritecollide(b,tanksGroup,False,None)
                    if collide_tanks:
                        b.being = False
                        bulletsGroup.remove(b)
                        for ct in collide_tanks:
                            is_destoried = ct.be_shooted(b)
                            if is_destoried:
                                if ct.tank.kind == 0:#己方坦克
                                    ct.tank.being = False
                                    
                                    pass
                                else:#敌方坦克
                                    ct.tank.being = False
                                    tanksGroup.remove(ct)
                                    pass
                '''
            #用坦克去碰子弹
            # -> 己方坦克
            for t in mytanks:
                collide_bullets = pygame.sprite.spritecollide(t.tank,bulletsGroup,False,None)
                if collide_bullets:
                    sound_hit.play()
                    game_info.score -= len(collide_bullets)*100
                    if t.be_shooted(collide_bullets):
                        tanksGroup.remove(t.tank)
                        tanksGroup_my.remove(t.tank)
                        mytanks.remove(t)
                    bulletsGroup.remove(collide_bullets)
            if len(mytanks) <= 0:
                sound_blast.play()
                is_gameover = True
            # -> 敌方坦克
            for t in enemytanks:
                collide_bullets = pygame.sprite.spritecollide(t.tank,bulletsGroup,False,None)
                if collide_bullets:
                    sound_hit.play()
                    if t.be_shooted(collide_bullets):
                        sound_bang.play()
                        if t.with_food:
                            foodsGroup.add(food.Food(t.tank.rect.left,t.tank.rect.top))
                        tanksGroup.remove(t.tank)
                        enemytanks.remove(t)
                        enemy_now -= 1
                        game_info.score += t.level*200
                    bulletsGroup.remove(collide_bullets)
            # 绘制场景并更新时间
            # ->背景
            screen.blit(img_bg,(0,0))
            # ->石头墙
            for one in my_map.brickGroup:
                screen.blit(one.wall, one.rect)
            # ->钢墙
            for one in my_map.ironGroup:
                screen.blit(one.wall, one.rect)
            # ->家
            screen.blit(myhome.home, myhome.rect)
            # ->食物
            for one in foodsGroup:
                one.time_out(clock_tick)
                if one.being:
                    screen.blit(one.food, one.rect)
                else:
                    foodsGroup.remove(one)
            # ->子弹
            for one in bulletsGroup:
                screen.blit(one.bullet, one.rect)
            # ->坦克
            for t in tanksGroup:
                t.shoot_reload(clock_tick)
                screen.blit(t.tank_img,t.rect)
            # -> 计分器
            screen.blit(board_player1,board_player1_rect)
            text_player1_life = cfont.render(u'X{}'.format(tank_player1.life),True,(255,255,255))
            rect_player1_life = text_player1_life.get_rect()
            rect_player1_life.midtop = (map_width + (width-map_width)*2/3,height/4)
            screen.blit(text_player1_life,rect_player1_life)
            
            screen.blit(board_player2,board_player2_rect)
            if game_info.num_player > 1:
                text_player2_life = cfont.render(u'X{}'.format(tank_player2.life),True,(255,255,255))
            else:
                text_player2_life = cfont.render(u'X0',True,(255,255,255))
            rect_player2_life = text_player2_life.get_rect()
            rect_player2_life.midtop = (map_width + (width-map_width)*2/3,height/2)
            screen.blit(text_player2_life,rect_player2_life)
            
            text_score = cfont.render(u'SCORES: {}'.format(game_info.score),True,(255,255,255))
            rect_score = text_score.get_rect()
            rect_score.midtop = (map_width + (width-map_width)/2,height*3/4)
            screen.blit(text_score,rect_score)
            ###########
            
            pygame.display.flip()
            clock.tick(clock_tick)
            
        if is_gameover:
            show_end(screen,width,height)
#        else:
#            show_switch_stage(screen,width,height,game_info)



if __name__ == "__main__":
    main()






























