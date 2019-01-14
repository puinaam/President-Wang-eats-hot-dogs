# -*- coding: utf-8 -*-
#王校长有三条命
#有三个interface，分别为开始页，运行页和结束页
#任何一条热狗落地后扣王校长的命
#热狗死亡有闪烁
#王校长吃热狗（下一功能）

import pygame
import sys
import traceback
import mywsc
import myhotdog
import mysupply

from pygame.locals import *
from myhotdog import BIG,SMALL
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("王思聪吃热狗 -- Prunum")

background = pygame.image.load("sc/background.png").convert()
bar=pygame.image.load("sc/bar.png").convert()

pygame.mixer.music.load("sc/bgm.wav")
pygame.mixer.music.set_volume(0.3)
h1_down_sound = pygame.mixer.Sound("sc/eat.wav")
h1_down_sound.set_volume(0.5)
bomb_sound = pygame.mixer.Sound("sc/use_bomb.wav")
bomb_sound.set_volume(0.5)
aah_sound = pygame.mixer.Sound("sc/aah.wav")
aah_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sc/get_bomb.wav")
get_bomb_sound.set_volume(0.5)

def add_small_hotdog(group1,group2):
    h1=myhotdog.Smallhotdog(bg_size)
    group1.add(h1)
    group2.add(h1)
    
def add_big_hotdog(group1,group2):
    h1=myhotdog.Bighotdog(bg_size)
    group1.add(h1)
    group2.add(h1)
    
def remove_small_hotdog(group1,group2,h1):
    group1.remove(h1)
    group2.remove(h1)
    
def remove_big_hotdog(group1,group2,h1):
    group1.remove(h1)
    group2.remove(h1)

def main():
    pygame.mixer.music.play(-1) #play bmg
    clock = pygame.time.Clock()
    interface=0
    
    #value initialize----------------------------------------------------------
    switch_image=True
    delay=100
    score=0
    score_font = pygame.font.Font("sc/Inkfree.ttf", 34)
    time_for_big_one=-7
    level=1
    running=True
    #暂停 ----------------------------------------------------------------------
    paused=False
    pause_nor_image = pygame.image.load("sc/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("sc/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("sc/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("sc/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image
    #文字-----------------------------------------------------------------------
    gameover_font = pygame.font.Font("sc/Inkfree.ttf", 72) 
    gameover_font2 = pygame.font.Font("sc/Inkfree.ttf", 48)      
    gamestart_font = pygame.font.Font("sc/Inkfree.ttf", 24)
    gamestart_text=gamestart_font.render("u can press 'space' 2 eat all hotdogs", True, (255,255,255))
    gamestart_rect=gamestart_text.get_rect()
    #start---------------------------------------------------------------------
    start_image=pygame.image.load("sc/start.png").convert_alpha()
    start_rect=start_image.get_rect()
    start_rect.left, start_rect.top = (width - start_rect.width)//2, (height-start_rect.height)//2-100
    #restart-------------------------------------------------------------------
    restart_image=pygame.image.load("sc/restart.png").convert_alpha()
    restart_rect=restart_image.get_rect()
    restart_rect.left, restart_rect.top = (width - restart_rect.width)//2, (height-restart_rect.height)//2+100
    #创建王校长------------------------------------------------------------------
    me=mywsc.Mywsc(bg_size)
    # 全屏炸弹
    bomb_image = pygame.image.load("sc/100.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("sc/Inkfree.ttf", 48)
    bomb_num = 3
    #创建补给------------------------------------------------------------
    bomb_supply = mysupply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 20 * 1000)
    # 中弹图片索引--------------------------------------------------------------
    h1_destroy_index = 0
    h2_destroy_index = 0
    me_destroy_index = 0 
    # 生成小热狗----------------------------------------------------------------
    hotdog = pygame.sprite.Group()
    
    small_hotdog = pygame.sprite.Group()
    big_hotdog = pygame.sprite.Group()
    add_small_hotdog(small_hotdog,hotdog)
    
    
#主循环----------------------------------------------------------------------------------------------
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos) and interface == 1:
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 20 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and interface == 3:
                    interface=1
                    score=0
                    bomb_num=3
                    for each in hotdog:
                        remove_small_hotdog(hotdog,small_hotdog,each)
                        remove_big_hotdog(hotdog,big_hotdog,each)
                    add_small_hotdog(small_hotdog,hotdog)
                    me.active=True
                    me.lives=3
                    paused=False
                    level=1
                    myhotdog.speed=5
                    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and interface == 0:
                    interface=1
                    
            elif event.type == MOUSEMOTION and interface==1:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                       paused_image = pause_nor_image

            elif event.type == KEYDOWN and interface==1:                                        #bomb
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in hotdog:
                            each.active = False
                            if each.size==SMALL:    
                                score+=1
                            else:
                                score+=3
                            #add_small_hotdog(small_hotdog,hotdog)

            elif event.type == SUPPLY_TIME and interface==1:
                #supply_sound.play()
                bomb_supply.reset()
                #if choice([True, False]):
                #    bomb_supply.reset()
                #else:
                #    bullet_supply.reset()
        #interface_1-----------------------------------------------------------
        if interface==1:
            #画背景-----------------------------------------------------------------
            screen.blit(background, (0, 0))        
            #检测键盘操作------------------------------------------------------------
            if not paused:
                ok_2_move=True
                key_pressed = pygame.key.get_pressed()
                for h in big_hotdog:
                    if h.eating==True:
                        ok_2_move=False
                        
                if ok_2_move:        
                    if key_pressed[K_a] or key_pressed[K_LEFT]:
                        me.moveLeft()
                    if key_pressed[K_d] or key_pressed[K_RIGHT]:
                        me.moveRight()
            
                #检测是否吃到热狗-----------------------------------------------------
                eaten = pygame.sprite.spritecollide(me, hotdog, False, pygame.sprite.collide_mask)
                if eaten:
                   for h in eaten:
                       if h.size==BIG:
                           if h.score_counted==False:
                               score+=3
                               h.score_counted=True
                           h.eating = True
                       if h.size==SMALL:
                           if h.score_counted==False:
                               h.score_counted=True
                               score+=1
                           h.active = False
                       h.attack=False           
                # 创建热狗-----------------------------------------------------------
                if score>150:
                    level=5
                elif score>100:
                    level=4
                elif score>50:
                    level=3
                elif score>30:
                    level=2
                
                if level==1:
                    gap=270
                    myhotdog.speed=5
                elif level==2:
                    gap=250
                    myhotdog.speed=6
                elif level==3:
                    gap=230
                    myhotdog.speed=6
                elif level==4:
                    gap=200
                    myhotdog.speed=7
                elif level==5:
                    gap=170
                    myhotdog.speed=7

                ok_for_new=True
                for i in hotdog:
                    if i.rect.top<gap:
                        ok_for_new=ok_for_new and False
                if ok_for_new:            
                    if time_for_big_one<0:
                        add_small_hotdog(small_hotdog,hotdog)
                        time_for_big_one=time_for_big_one+1
                    else:
                        add_big_hotdog(big_hotdog,hotdog)
                        time_for_big_one=-7
               
                #画小热狗---------------------------------------------------------------
                for each in small_hotdog:
                    if each.active:
                        each.move()
                        screen.blit(each.image, each.rect)
                    else:
                        # 毁灭 active==0
                        if each.attack==True:
                            if me.lives>1:
                                me.lives=me.lives-1
                                aah_sound.play()
                                each.attack=False
                            else:#game over
                                me.lives=0
                                aah_sound.play()
                                me.active=False
                        if not(delay % 3):
                            if h1_destroy_index == 0:
                                h1_down_sound.play()
                            screen.blit(each.destroy_images[h1_destroy_index], each.rect)
                            h1_destroy_index = (h1_destroy_index + 1) % 2
                            if h1_destroy_index == 0:
                                remove_small_hotdog(small_hotdog,hotdog,each)
                #画大热狗-----------------------------------------------------------
                for each in big_hotdog:
                    if each.active:
                        each.move()
                        screen.blit(each.image, each.rect)
                    else:
                        # 毁灭 active==0
                        if each.attack==True:
                            if me.lives>1:
                                me.lives=me.lives-1
                                each.attack=False
                            else:#game over
                                me.lives=0
                                me.active=False
                        if not(delay % 3):
                            if h2_destroy_index == 0:
                                h1_down_sound.play()
                            screen.blit(each.destroy_images[h2_destroy_index], each.rect)
                            h2_destroy_index = (h2_destroy_index + 1) % 4 #4pics
                            if h2_destroy_index == 0:
                                remove_big_hotdog(big_hotdog,hotdog,each)
                #画全屏炸弹 并 检测是否吃到补给------------------------------------------
                if bomb_supply.active:
                    bomb_supply.move()
                    screen.blit(bomb_supply.image, bomb_supply.rect)
                    if pygame.sprite.collide_mask(bomb_supply, me):
                        get_bomb_sound.play()
                        if bomb_num < 3:
                            bomb_num += 1
                        bomb_supply.active = False
                #画王校长---------------------------------------------------------------
                if me.active:
                    if switch_image:
                        screen.blit(me.image1, me.rect)
                    else:
                        screen.blit(me.image2, me.rect)
                else:
                    # 毁灭
                    if not(delay % 3):
                        if me_destroy_index == 0:
                            pass#me_down_sound.play()
                        screen.blit(me.destroy_images[me_destroy_index], me.rect)
                        me_destroy_index = (me_destroy_index + 1) % 4
                        if me_destroy_index == 0:
                            interface = 3
            else:#paused
                for each in small_hotdog:
                    if each.active:
                        screen.blit(each.image, each.rect)
                for each in big_hotdog:
                    if each.active:
                        screen.blit(each.image, each.rect)
                if bomb_supply.active:
                    screen.blit(bomb_supply.image, bomb_supply.rect)
                if me.active:
                    screen.blit(me.image1, me.rect)
            #画状态栏-----------------------------------------------------------
            screen.blit(bar,(0,bg_size[1]-60))
            #生命 左下角
            if me.lives==1:
                screen.blit(me.image_icon,(0,bg_size[1]-60))
            elif me.lives==2:
                screen.blit(me.image_icon,(0,bg_size[1]-60))
                screen.blit(me.image_icon,(60,bg_size[1]-60))
            elif me.lives==3:    
                screen.blit(me.image_icon,(0,bg_size[1]-60))
                screen.blit(me.image_icon,(60,bg_size[1]-60))
                screen.blit(me.image_icon,(120,bg_size[1]-60))
            #道具 右下角
            bomb_text = bomb_font.render("×%d" % bomb_num, True, (255,255,255))
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (width-100, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (width-100 + bomb_rect.width, height - 5 - text_rect.height))
            #分数 左上角
            score_text = score_font.render("Score: %s" % str(score), True, (255,255,255))
            screen.blit(score_text, (10, 5))
            #暂停开始
            screen.blit(paused_image, paused_rect)
            # 切换图片时间控制-------------------------------------------------------
            if not(delay % 5):
                switch_image = not switch_image
            delay -= 1
            if not delay:
                delay = 100
        #interface_3 ----------------------------------------------------------
        if interface==3:
            screen.blit(background, (0, 0))
            gameover_text2=gameover_font2.render("score:%s " % str(score), True, (255,255,255))
            gameover_rect2=gameover_text2.get_rect()
            gameover_text=gameover_font.render("Game Over", True, (255,255,255))
            gameover_rect=gameover_text.get_rect() 
            screen.blit(gameover_text,((width-gameover_rect.width)//2,(height-gameover_rect.height)//2-70))
            screen.blit(gameover_text2,((width-gameover_rect2.width)//2,(height-gameover_rect.height)//2+15))
            screen.blit(restart_image,restart_rect)
            
            #screen.blit(restart_image,(0,0))
        #interface_0----------------------------------------------------------
        if interface==0:
            screen.blit(background, (0, 0))
            screen.blit(start_image,start_rect)
            screen.blit(gamestart_text,((width-gamestart_rect.width)//2,(height-gamestart_rect.height)//2+20))
        
        pygame.display.flip() #刷新---------------------------------------------       
        clock.tick(60) 
        #fps---------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()