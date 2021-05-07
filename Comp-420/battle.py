# -*- coding: utf-8 -*-
"""
This file is for the characteristics and options a player has in combat
Code that has a red mark are tempoory
and will be moved to files that are more appropiate or deleted
"""

import random
import skill_library as SL
import time

def Roll(sides):
    """
    sides: int
    rolls a sides sided die
    """
    dice = []
    for i in range(sides):
        dice.append(i+1)
    roll = random.choice(dice)
    return roll
def add_percent(num, percent):
    """
    will increase a number by a percentage
    percent is an in for convinence
    """
    get = num * float(percent)
    return int(get + num)
class Someone:
    def __init__(self, Name, HP, SP, ATK, DEF, MG, SPD):
        self._Name = Name
        self._HP = HP
        self._SP = SP
        self._ATK = ATK
        self._DEF = DEF
        self._MG = MG
        self._SPD = SPD
        self._c_HP = self._HP
        self._c_SP = self._SP
        self._skill = []
    def get_name(self):
        """
        Keep tracks of names that are used in combat and helps access name in the skill library
        """
        return str(self._Name)
    def get_c_HP(self):
        """
        Current Hit Points
        if current HP is less than or equal 0, player/enemy will be defeated
        Cannot exceed HP
        Cannot go below 0
        """
        return int(self._c_HP)
    def get_HP(self):
        """
        Maximum Hit Points
        will increase per level
        """
        return int(self._HP)
    def get_c_SP(self):
        """
        Current Spirit Points
        Cannot exceed SP
        Cannot go below 0
        """
        return int(self._c_SP)
    def get_SP(self):
        """
        Maimum Spirit Points
        Spirit points are used to cast spells
        Will increase per level
        """
        return int(self._SP)
    def get_ATK(self):
        """
        Attack Stat
        the more attack someone has,
        the more HP a target loses
        """
        return int(self._ATK)
    def get_DEF(self):
        """
        Defense Stat
        the more defense someone has,
        the less damage they take
        """
        return int(self._DEF)
    def get_MG(self):
        """
        Magic Stat
        increases the damge of magic spells
        """
        return int(self._MG)
    def get_SPD(self):
        """
        Speed stat
        can be used too see who goes first
        can be used in the future as accuracy
        """
        return int(self._SPD)
    def _adjust(self, damage):
        """
        Damage is an integer that is made by attacks
        if the event that the damage is lower than 0,
        the target reciving damage will gain health instead.
        This is meant to make that number turn it into chip damage
        """
        if damage <= 0:
            damage = Roll(6) + Roll(5)
        return damage
    def Empty_SP(self, cost=0):
        """
        returns a T/F statement that determines if 
        someone is using a spell thats greater than
        what their current SP has
        """
        return self.get_c_SP() <= cost or self.get_c_SP() == 0
    def Low_HP(self, cost=0):
        """
        returns a T/F statement that determines if
        someone is using a physical skill that is greater than
        what their current HP has current HP should not equal the cost as well
        """
        return self.get_c_HP() < cost or self.get_c_HP() == 0
    def SP_Cost(self, cost):
        """
        subtracts SP required for spell and will
        restrict somoene from using it if conditions are not met
        """
        if self.Empty_SP(cost):
            return False
        else:
            self._c_SP = self.get_c_SP() - cost
    def HP_Cost(self, cost):
        """
        subtracts HP required for using a physical skill and will
        restrict someone from using it if conditions are not met
        """
        if self.Low_HP(cost):
            return False
        else:
            self._c_HP = self.get_c_HP() - cost
    def Attack_Melee(self, other):
        """
        Someone's basic attack
        damage is made by Someone's ATK agasint targets DEF
        the targets current health is subtracted by damage
        """
        Damage = self.get_ATK() - other.get_DEF()
        Damage = Damage + Roll(6)
        Damage = self._adjust(Damage)
        other._c_HP = other.get_c_HP() - Damage
        return Damage
    def Is_Dead(self):
        """
        If a players HP hits 0, they are unable to battle, they do not gain
        HP unless the skill is able to revive them 
        """
        if self.get_c_HP() <= 0:
            self._c_HP = 0
            return True
        return False
    def _assign_skill(self):
        """
        Uses Someones name to see if they are in the library
        if true, the player will be able activate them in self._skill
        False entries will result with Someone with no skill set
        """
        if self._skill != []:
            pass
        else:
            size = SL.in_library(self._Name)
            for i in range(len(size) - 1):
                size[i+1] = getattr(SL, size[i+1])
                self._skill.append(size[i + 1])
    def determine_skill(self, choice, target):
        """
        choice is the skill index that is being selected 
        """
        self._assign_skill()
        skill = self._skill[choice]
        if skill.Is_Magic():
            self.SP_Cost(skill.get_cost())
            print("Casting " + skill.get_skill_name() + " on " + target.get_name())
            Damage = (skill.get_base() + self.get_MG()) - target.get_DEF()
            Damage = self._adjust(Damage)
            print(Damage)
            target._c_HP = target.get_c_HP() - Damage
            target.Is_Dead()
        elif skill.Is_Physical():
            if skill.get_skill_name() == "Attack":
                print("Attacking " + target.get_name())
                print(self.Attack_Melee(target))
                target.Is_Dead()
            else:
                self.HP_Cost(skill.get_cost())
                print(skill.get_skill_name() + " on " + target.get_name())
                Damage = (skill.get_base() + self.get_ATK()) - target.get_DEF()
                Damage = self._adjust(Damage)
                print(Damage)
                target._c_HP = target.get_c_HP() - Damage
                target.Is_Dead()
        elif skill.Is_Support():
            if target.get_c_HP() == target.get_HP():
                print("HP is already full!")
            elif target.Is_Dead():
                print("Already dead!")
            else:
                self.SP_Cost(skill.get_cost())
                print("Healing " + target.get_name())
                base = skill.get_base() + Roll(6) + Roll(6)
                print("+ " + str(base))
                target._c_HP = target.get_c_HP() + base
                if target.get_c_HP() >= target.get_HP():
                    target._c_HP = target.get_HP()
    def display_user_skills(self):
        """
        testing purposes only
        display the name and cost of skill
        only text but eventually a pygame visual
        """
        self._assign_skill()
        for i in range(len(self._skill)):
            skill = self._skill[i]
            print(str(i) + " " + skill.get_skill_name() + ":" + str(skill.get_cost()))
        
Paige = Someone('Paige', 75, 50, 15, 14, 25, 27)
Mobius = Someone('Mobius', 100, 20, 24, 30, 22, 24)
Emma = Someone('Emma', 80, 48, 20, 23, 24, 33)
Flint = Someone('Flint', 95, 35, 26, 26, 20, 18)

Foe = Someone('Foe', 60, 10, 2, 8, 14, 19)
Fiend = Someone('Fiend', 80, 0, 28, 20, 23, 25)
Gaurd = Someone('Gaurd', 35, 15, 23, 18, 5, 10)
Mage = Someone('Mage', 35, 35, 14, 16, 25, 16)
Priest = Someone('Priest', 70, 40, 14, 14, 14, 10)
Warlock = Someone('Warlock', 70, 40, 14, 14, 14, 10)


Heroes = [Paige, Mobius, Emma, Flint]
Villians = [Foe, Fiend, Priest, Mage]


def smart_heal(target):
    """
    This is help to make the AI make better choices
    when healing they will only heal targets that have taken damage
    """
    health = []
    health_order = []
    for i in range(len(target)):
        damage_taken = target[i].get_HP() - target[i].get_c_HP()
        if damage_taken == 0 or damage_taken == target[i].get_HP():
            pass
        else:
            health.append(target[i].get_c_HP())
    i = 0
    j = 0
    while len(health_order) != len(health):
        if health[i] == target[j].get_c_HP():
            health_order.append(target[j])
            j = 0
            i +=1
        else:
            j += 1
    if len(health_order) == 0:
        return None
    return health_order
def smart_choice(group, reverse=False):
    """
    will go through a list and append a new one that will
    only offers targets that are alive
    if reverse is true, then it will return a list of dead people 
    """
    living = []
    dead = []
    for i in range(len(group)):
        if group[i].Is_Dead() == False:
            living.append(group[i])
        elif group[i].Is_Dead():
            dead.append(group[i])
    if reverse == True:
        return dead
    else:
        return living
def legal_move(someone, skill):
    """
    If the player chooses a move that they cannot perform
    legal_move will remian false, this will keep prompting the player
    until they choose the right 
    this might need to be moved into the Someone class
    """
    if skill.Is_Magic() or skill.Is_Support():
        if someone.Empty_SP(skill.get_cost()):
            return False
    elif skill.Is_Physical():
        if someone.Low_HP(skill.get_cost()):
            return False
    return True

def AI(bot, heroes, villians):
    """
    bot is a someone class
    this helps make the AI choose a skill druing battle
    with the help of smart_heal,
    AI will heal the ally with the lowest health and
    it can make another choice if all their allies
    have full health
    """
    bot._assign_skill()
    time.sleep(3)
    legal = False
    while legal == False:
        num_choice = random.randrange(len(bot._skill))
        action = bot._skill[num_choice]
        if legal_move(bot, action) == False:
            pass
        else:
            
            if action.Is_Support():
                target = smart_heal(villians)
                if target == None:
                    num_choice = random.randrange(0, len(bot._skill))
                else:
                    bot.determine_skill(num_choice, target[0])
                    legal = True
            else:
                options = smart_choice(heroes)
                target = options[random.randrange(len(options))]
                bot.determine_skill(num_choice, target)
                legal = True

def players_turn(user, heroes, villians):
    """
    This is how the player will act on their turn
    smart heal makes it so you can't allies with max health
    and only offers allies that actaully need healing
    """
    legal = False
    print("Select a skill")
    while legal == False:
        user.display_user_skills()
        choice = correct_input(user._skill)
        action = user._skill[choice]
        if legal_move(user, action) == False:
            print("Choose another skill")
            pass
        else:
            if action.Is_Support():
                options = smart_heal(heroes)
                if options == None:
                    print("choose another skill")
                    pass
                else:
                    print("Select a injured ally")
                    display_targets(options)
                    ally = correct_input(options)
                    user.determine_skill(choice, options[ally])
                    legal = True
            else:
                options = smart_choice(villians)
                display_targets(options)
                target = correct_input(options)
                user.determine_skill(choice, options[target])
                legal = True
def someones_turn(user, heroes, villians):
    """
    will use players_turn or AI depending on the user
    """
    if user in heroes:
        players_turn(user, heroes, villians)
    elif user in villians:
        AI(user, heroes, villians)
def display_targets(people):
    """
    testing purposes only
    display the list of Someones
    you can interact with
    in battle
    eventually a pygame visual
    """
    for i in range(len(people)):
        print(str(i) +" " + people[i].get_name() + ":" + str(people[i].get_c_HP()))
        
def correct_input(index):
    """
    Will prompt the player to select a number and ignore input greater than
    the list offers and have the player insert appropiate input
    """
    wrong = True
    while wrong:
        action = int(input("\n\n"))
        if action < len(index) and action >= 0:
            return action
        elif action == 123:
            return
        print("Incorrect input")

def battle(player, enemy):
    """
    Display purposes only
    this will help show how the combat works
    and show the amount bugs are present, eventually will be in the main file
    to work with the visual file
    """
    select = [player, enemy]
    enemy._assign_skill()
    while player.get_c_HP >= 0 and enemy.get_c_HP >= 0:
        print(player.get_name())
        player.display_user_skills()
        print("Select a skill")
        action = correct_input(player._skill)
        print("select a target")
        display_targets(select)
        target = correct_input(select)
        red = player.determine_skill(action, select[target])
        print('\n')
        print(red)
        if enemy.Is_Dead():
            break
        blue = enemy.determine_skill(random.randrange(0,len(enemy._skill)), player)
        print('\n')
        print(blue)
        if player.Is_Dead():
            break
        print(player.get_c_HP())
        print(enemy.get_c_HP())
    if player.Is_Dead():
        print("You Died")
    elif enemy.Is_Dead():
        print("You Win")
        
def PvP(red, blue):
    """
    player vs player
    """
    select = [red, blue]
    while red.get_c_HP() >= 0 and blue.get_c_HP() >= 0:
        print(red.get_name())
        red.display_user_skills()
        print("Select a skill")
        action = correct_input(red._skill)
        display_targets(select)
        target = correct_input(select)
        red.determine_skill(action, select[target])
        print('\n')
        if blue.Is_Dead():
            break
        print(blue.get_name())
        blue.display_user_skills()
        print("Select a skill")
        action = correct_input(blue._skill)
        display_targets(select)
        target = correct_input(select)
        blue.determine_skill(action, select[target])
        print('\n')
        if red.Is_Dead():
            break
    if red.Is_Dead():
        print(blue.get_name() + " wins!")
    if blue.Is_Dead():
        print(red.get_name() + " wins!")

def team_alive(group):
    """
    this will determine if everyone in a party is able to battle
    """
    death_count = 0
    for i in range(len(group)):
        if group[i].Is_Dead():
            death_count += 1
    if death_count == len(group):
        return False
    else:
        return True
def all_init(group):
    all_speed = []
    turn_order = []
    for i in range(len(group)):
        all_speed.append(group[i].get_SPD())
    all_speed.sort(reverse=True)
    i = 0
    j = 0
    while len(turn_order) != len(all_speed):
        if all_speed[i] == group[j].get_SPD():
            turn_order.append(group[j])
            j = 0
            i +=1
        else:
            j += 1
    return turn_order  
def team_battle(pro, ant):
    """
    Pro and ant are two list that have multiple Someones
    if all of one side is inactive, then the other team will win
    NOTE: 
    Revive spells need to be created to check if people can re enter this
    Turn order will be randomized until initied is establish
    """
    phase = 1
    select = []
    for i in range(len(pro)):
        select.append(pro[i])
    for i in range(len(ant)):
        select.append(ant[i])
    select = all_init(select)
    while team_alive(pro) and team_alive(ant):
        print("Phase " + str(phase))
        print("\n")
        display_targets(select)
        print("\n")
        for i in range(len(select)):
            user = select[i]
            if user.Is_Dead():
                pass
            else:
                print(user.get_name() + "'s turn")
                someones_turn(user, pro, ant)
                print("\n")
                if team_alive(pro) == False or team_alive(ant) == False:
                    break
        phase += 1
    if team_alive(pro) == False:
        print("Game Over")
    else:
        print("You Win!")

#PvP(Mobius, Flint)
#battle(Mobius, Foe)
#team_battle(Heroes, Villians)