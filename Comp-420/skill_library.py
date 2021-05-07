# -*- coding: utf-8 -*-
"""
Created on Wed May 20 23:59:17 2020

@author: Mikey
"""

class Skill:
    def __init__(self, name, effect, cost, base=0):        
        self._skill = name
        self._type = effect
        self._cost = cost
        self._base = base
    def get_skill_name(self):
        """
        get the name of the skill, for display purposes
        """
        return str(self._skill)
    def get_effect_type(self):
        """
        Skills can vary between the dealing damge, buffs/debuffs and healing
        by getting giving each skill a type, skill design can be arbitary
        """
        return str(self._type)
    def get_cost(self):
        """
        in order to activate a skill, the user must pay SP or a portion
        of their HP
        """
        return int(self._cost)
    def get_base(self):
        """
        Early spells will just use SP and HP to determine damage/healing,
        as spells advance, they will have a starting number along with calculation
        """
        return int(self._base)
    def Is_Magic(self):
        """
        When using a magic attack, the player will do damage based on
        their attack and depending on their max SP
        """
        return self.get_effect_type() == "Magic"
    def Is_Physical(self):
        """
        When using a physical attack, the plauer will do damage based on
        their max HP
        """
        return self.get_effect_type() == "Physical"
    def Is_Support(self):
        """
        As of now, the support effect can only heal
        """
        return self.get_effect_type() == "Support"
def _make_library():
    """
    Helper function to _search_skills
    This does the file reading part
    """
    with open("text_library/user_library.txt", "r") as fd:
        lines = fd.read().splitlines()
    return lines
def _search_skill():
    """
    adjust a single list into a nested list that conatins each user
    """
    old_library = _make_library()
    new_library = []
    user = []
    for i in range(len(old_library)):
        if old_library[i] == '':
            new_library.append(user)
            user = []
        else:
            user.append(old_library[i])
    new_library.append(user)
    return new_library
def in_library(name):
    """
    returns a T/F statement that checks if the user is in the database
    """
    library = _search_skill()
    for i in range(len(library)):
        user = library[i]
        if user[0] == name:
            return library[i]
    return []
### Skills ###
    
### Someone ##
Attack = Skill('Attack', 'Physical', 0)
Guard = Skill('Guard', 'Support', 0)
##############

### Magic ####
Fire = Skill('Fire', 'Magic', 6, 25)
Wind = Skill('Wind', 'Magic', 3, 15)
Thunder = Skill('Thunder', 'Magic', 5, 22)
Water = Skill('Water', 'Magic', 4, 20)
##############

### Support ##
Heal = Skill('Heal', 'Support', 3, 25)
##############

### Physical #
Headbutt = Skill('Headbutt', 'Physical', 10, 15)
Slash = Skill('Slash', 'Physical', 15, 25)
##############
