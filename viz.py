# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:35:15 2020
visuals folder this will
animate the battle sequence
@author: Mikey
"""

import sys
import time
import pygame
import battle as BT
from pygame.locals import *

width, height = 1200, 600
PURPLE = (100,50,200)
MAROON = (75, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
NAVY = (0,0,75)
WHITE = (255,255,255)
FONT = "freesansbold.ttf"

pygame.init()

team = [BT.Paige, BT.Mobius, BT.Emma, BT.Flint]
other = [BT.Foe, BT.Fiend, BT.Gaurd, BT.Mage, BT.Priest]

def adjust(w, h):
    """
    No matter what size the screen gets changed,
    it's going to help fix the previous positions
    """
    new_w = width - (width - w)
    new_h = height - (height - h)
    return new_w, new_h    

leader_l, leader_w = adjust(25, 325)
A_top_l, A_top_w = adjust(150, 150) 
A_mid_l, A_mid_w = adjust(225, 325)
A_bot_l, A_bot_w = adjust(150, 500)

center_l = width / 2
center_w = height / 2

c_len = [leader_l, A_top_l, A_mid_l, A_bot_l]
c_wid = [leader_w, A_top_w, A_mid_w, A_bot_w]

e_1_len, e_1_wid = adjust(1000, 325)
e_2_len, e_2_wid = adjust(1000, 225)
e_3_len, e_3_wid = adjust(1000, 425)
e_4_len, e_4_wid = adjust(800, 325)
e_5_len, e_5_wid = adjust(800, 225)
e_6_len, e_6_wid = adjust(880, 425)

e_c_len = [e_1_len, e_2_len, e_3_len, e_4_len, e_5_len, e_6_len]
e_c_wid = [e_1_wid, e_2_wid, e_3_wid, e_4_wid, e_5_wid, e_6_wid]


def text_object(text, font=FONT, color=WHITE):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_diplay(text, loc, size, font=FONT, temp=False):
    message = pygame.font.Font(font, size)
    TextSurf, Textrect = text_object(text, message)
    Textrect.center = loc
    screen.blit(TextSurf, Textrect)
    if temp:
        pygame.display.update()
        time.sleep(1)

def health_bar(HP, c_HP, length, width, enemy=False):
    """
    Displays the amount of HP a person has
    near the person
    if the enemy is true then it will not display
    the exact number
    """
    percent = float(c_HP) / float(HP)
    pygame.draw.rect(screen, MAROON, (length,width, 100, 15))
    pygame.draw.rect(screen, RED, (length, width, percent * 100, 15))
    hp_bar = str(c_HP) + "/" + str(HP)
    if not enemy:
        message_diplay(hp_bar, (length + 19, width + 8), 10)
    
def mana_bar(MP, c_MP, length, width):
    """
    Displays the amount of HP a person has
    near the person
    this is only displayed for party members not enimes
    """
    percent = float(c_MP) / float(MP)
    pygame.draw.rect(screen, NAVY, (length,width + 15, 100, 15))
    pygame.draw.rect(screen, BLUE, (length, width + 15, percent * 100, 15))
    mp_bar = str(c_MP) + "/" + str(MP)
    message_diplay(mp_bar, (length + 19, width + 25), 10)

def spend_mana(MP, c_MP, cost, length, width):
    """
    animate the MP bar when using magic
    you can't over spend mana so other precautions have been measured
    """
    for i in range(cost):
        pygame.display.update()
        game_state(team, other)
        current = c_MP - i
        mana_bar(MP, current, length, width)
        time.sleep(0.02)
def game_state(heroes, other):
    for i in range(len(heroes)):
        HP = heroes[i].get_HP()
        c_HP = heroes[i].get_c_HP()
        MP = heroes[i].get_SP()
        c_MP = heroes[i].get_c_SP()
        message_diplay(heroes[i].get_name(), (c_len[i] + 8,c_wid[i] - 20), 15)
        health_bar(HP, c_HP, c_len[i], c_wid[i])
        mana_bar(MP, c_MP, c_len[i], c_wid[i])
    for j in range(len(other)):
        e_HP = other[i].get_HP()
        e_c_HP = other[i].get_c_HP()
        message_diplay(other[j].get_name(), (e_c_len[j] + 8, e_c_wid[j] - 20), 15)
        health_bar(e_HP, e_c_HP, e_c_len[j], e_c_wid[j], True)
def damage_taken(damage, HP, c_HP, length, width, enemy=False):
    """
    Animates the amount of damge someone takes
    """
    for i in range(damage):
        pygame.display.update()
        game_state(team, other)
        current = c_HP - i
        if current < 0:
            current = 0
        health_bar(HP, current, length, width, enemy)
        time.sleep(0.02)

def animate_choice(select, length=center_l, width=center_w, size=20):
    down = 30
    for i in range(len(select)):
        new_w = width + (down * i)
        word = str(i) + " : " + str(select[i])
        message_diplay(word, (length, new_w), size)
        
def skill_list(select, length=center_l, width=center_w, size=20):
    new_list = []
    for i in range(len(select)):
        skill = select[i]
        cost_econ = " HP"
        if not skill.Is_Physical():
            cost_econ = " MP"
        if skill.get_cost() == 0:
            resource = ""
        else:
            resource = ": " + str(skill.get_cost()) + cost_econ 
        new_list.append(skill.get_skill_name() + resource)
    animate_choice(new_list, length, width, size)
    return 
def somoene_list(select, length=center_l, width=center_w, size=20):
    pass
def select_choice(select, length=center_l, width=center_w, size=20):
    """
    should be able to aniamte a list of choices and have the
    player be able to select something from them.
    """
    new_l = length - 100
    locs = []
    deciding = True
    num = 0
    for i in range(len(select)):
        new_w = width + (20 * i)
        locs.append(new_w)
    game_state(team, other)
    while deciding:
        pygame.display.update()
        animate_choice(select)
        game_state(team, other)
        try:
            for i in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_0] == 1:
                    num = 0
                elif pygame.key.get_pressed()[pygame.K_1] == 1:
                    num = 1
                elif pygame.key.get_pressed()[pygame.K_2] == 1:
                    num = 2
                elif pygame.key.get_pressed()[pygame.K_3] == 1:
                    num = 3
                elif pygame.key.get_pressed()[pygame.K_4] == 1:
                    num = 4
                elif pygame.key.get_pressed()[pygame.K_5] == 1:
                    num = 5
                elif pygame.key.get_pressed()[pygame.K_6] == 1:
                    num = 6
                if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
                    game_state(team, other)
                    deciding = 0
                if i.type == QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.draw.rect(screen, PURPLE, (new_l, locs[num], 10, 10))
        except IndexError:
            pass
    return num

def aniamte_player_turn(user, team, other):
    """
    since the player phases uses a lot of print
    the function had to get moved to voz in order to
    display it
    """
    legal = False
    message_diplay("select a skill", (center_l, 15),  25)
    while legal == False:
        user._assign_skill()
        action = select_choice(skill_list(user._skill))
        pygame.display.update()
        skill = user._skill[action]
        if BT.legal_move(user, skill) == False:
            pygame.display.update()
            game_state(team, other)
            animate_choice(user._skill)
            message_diplay("select another skill", (15, center_w),  25)
        else:
            if skill.Is_Support():
                options = BT.smart_heal(team)
                pygame.display.update()
                if options == None:
                    pygame.display.update()
                    game_state(team, other)
                    message_diplay("select another skill", (15, center_w),  25)
                else:
                    game_state(team, other)
                    pygame.display.update()
                    user.determine_skill(action, select_choice(options))
                    legal = True
            else:
                pygame.display.update()
                game_state(team, other)
                options = BT.smart_choice(other)
                user.determine_skill(action, select_choice(options))
                legal = True
    game_state(team, other)

fps = 60
fpsClock = pygame.time.Clock()

oof = ["cat", "dog", "fish"]

screen = pygame.display.set_mode((width, height))
# Game loop.
while True:
  pygame.font.init()
  screen.fill((0, 0, 0))
  full_health = 200
  damage = 45
  #damage_taken(200, 200, damage, leader_l, leader_w)
  #spend_mana(BT.Paige.get_SP(), BT.Paige.get_c_SP(), 30, leader_l, leader_w)
  #game_state(team, other)
  aniamte_player_turn(BT.Paige, team, other)
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  # Update.
  
  # Draw.
  
  pygame.display.flip()
  fpsClock.tick(fps)