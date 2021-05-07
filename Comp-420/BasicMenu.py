# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 22:51:39 2021

@author: Mikey
"""
import pygame, sys
import battle as BT
import time
import glob
import random
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('COMP-420')
screen = pygame.display.set_mode((1000, 700),0,32)

class Character:
    """
    The Character class is the data type that
    helps render each seperate character while also
    keeping track of their stats
    
    someone: Takes in the Someone() data type from battle.py
    
    x, and y is thier inital position
    
    pathname: file location to load the characters images
    
    leader: a boolean that would allow the character switch places
    with someone if True (Right now their is no advantatge 
    in being leader or not)
    
    image: the index of the list of images that each character has
    image starts at 0 which is their idle image
    """
    def __init__(self, someone, x, y, pathname, leader):
        self._someone = someone
        self._x = x
        self._y = y
        self._pathname = pathname
        self._leader = leader
        self._image = 0
    def get_pos(self):
        return (int(self._x), int(self._y))
    def get_pathname(self):
        return str(self._pathname)
    def change_image  (self, i):
        """The images in the file are named only with numbers 
        this makes it easy to switch between other images
        switches when the character is attacking or is out of HP"""
        self._image = i
    def load_image(self):
        """gets the images loaded while also scaling
        it down to fit in the screen"""
        pic_loc = str(self.get_pathname() + "/" + str(self._image) + ".png")
        pic = pygame.transform.scale(pygame.image.load(pic_loc),(100,100))
        return pic
    def show_image(self):
        """uses the laoded image and the pos
        to display the image on the screen"""
        pygame.Surface.blit(screen, self.load_image(), self.get_pos())
    def is_leader(self):
        """Only leader gets the option to switch pos
        with someone else. This Boolean keeps
        from people accessing it during their turn"""
        return self._leader
    def change_pos(self, (ex, why)):
        """
        updates the pos with a new set of pos
        """
        self._x = ex
        self._y = why
    def change_leader(self, teamate):
        """
        If someone is leader, they can
        change positions with someone else
        in order to make them leader
        """
        tx = int(teamate._x)
        ty = int(teamate._y)
        teamate.change_pos(self.get_pos())
        self.change_pos((tx, ty))
        self._leader = not self.is_leader()
        teamate._leader = not teamate.is_leader()
def load_all(people):
    """ People is a list of characters
    this is a quick way to load all the images whe the program start"""
    for i in range(len(people)):
        people[i].load_image()
    
def update_all(people):
    """people is a list of characters
    this is to update any of the images that change
    during combat"""
    for i in range(len(people)):
        people[i].show_image()
def just_someone(everyone):
    """
    Takes in a list of Character()s and
    extracts the Someone() type in order
    to run the code in battle.py
    """
    people = []
    for i in range(len(everyone)):
        people.append(everyone[i]._someone)
    return people

### The list of playable characters and enemies ###
Paige = Character(BT.Paige, 50, 200, "images/characters/Paige", leader=True)    
Mobius = Character(BT.Mobius, 145, 75, "images/characters/Mobius", False)
Emma = Character(BT.Emma, 225, 200, "images/characters/Emma", leader=False)
Flint = Character(BT.Flint, 145, 375, "images/characters/Flint", leader=False)

Foe = Character(BT.Foe, 600, 100, "images/enemies", leader=False)
Fiend = Character(BT.Fiend, 600, 300, "images/enemies", leader=False)
Gaurd = Character(BT.Gaurd, 600, 500, "images/enemies", leader=False)
Mage = Character(BT.Mage, 800, 300, "images/enemies", leader=False)
Priest = Character(BT.Priest, 800, 100, "images/enemies", leader=False)
Warlock = Character(BT.Warlock, 800, 500, "images/enemies", leader=False)

people = [Paige, Mobius, Emma, Flint]
bad_people = [Foe, Fiend, Gaurd, Mage, Priest, Warlock]
everyone = people + bad_people

class Menus:
    """The Building blocks in order to create
    a new menuscreen. plugs in a lot of repetive varribles in order
    to use pygame effectivly"""
    def __init__(self):
        self._running = True
    def is_running(self):
        """"Self._running is running true until Someone() has declared a move"""
        return self._running == True
    def longblock(self, x, y):
        """Creates the basic block that would be used outside of combot"""
        button = pygame.Rect(x, y, 200, 50)
        return button
    def shortblock(self, x, y):
        """Creates the smaller blocks that will be used to target people
        in combat"""
        button = pygame.Rect(x, y, 25, 25)
        return button
    def custom(self, x, y, w, h):
        """ Create a block of any size for other purposes"""
        button = pygame.Rect(x, y, w, h)
        return button
    def highlight_short(self, x, y):
        """The yellow square to indicated which choice you are selecting"""
        button = pygame.Rect(x, y, 35, 35)
        return button
    def highlight_back(self, x, y):
        """This is for the highlighter for the back/K_0 button"""
        button = pygame.Rect(x, y, 105, 25)
        return button
    def draw(self, rect):
        """Displays the blocks onto the screen"""
        global screen
        pygame.draw.rect(screen, (7, 54, 66), rect)
    def draw_color(self, rect, color):
        """Draws the shape but in any color"""
        global screen
        pygame.draw.rect(screen, color, rect)
    def draw_highlight(self, rect):
        """Draws blocks specfically yellow as the indicatior"""
        global screen
        pygame.draw.rect(screen, (181, 137, 0), rect)
    def text(self, text, x, y, size=True):
        """Displays text onto the screen 
        If size=False, then the text will be smaller than the standard"""
        global screen
        current_text_color = (133, 153, 0)
        font = pygame.font.SysFont(None, 20)
        small_font = pygame.font.SysFont(None, 15)
        textobj = font.render(text, 1, current_text_color)
        if size == False:
            textobj = small_font.render(text, 1, current_text_color)
        if size == True:
            textobj = font.render(text, 1, current_text_color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        screen.blit(textobj, textrect)
    def screen_wipe(self):
        """Fills the screen by the background"""
        screen.fill((0,43,54))
    
def display_stats(people):
    """ Uses Menus to show the stats of the main characters"""
    menu = Menus()
    HUD = menu.custom(10 , 500, 460, 460)
    HUD_boarder = menu.custom(0, 500, 480, 480)
 
    menu.draw_color(HUD_boarder,(137, 207, 240))
    menu.draw(HUD)
    for i in range(len(people)):
        person = people[i]
        c_hp = person._someone.get_c_HP()
        c_sp = person._someone.get_c_SP()
        hp = person._someone.get_HP()
        sp = person._someone.get_SP()
        x = i * 100
        percent = float(c_hp) / float(hp)
        percent_sp = float(c_sp) / float(sp)
        menu.text(person._someone.get_name(), 20 + x, 580)
        
        health = menu.custom(20 + x, 600, 75, 25)
        Mana = menu.custom(20 + x, 635, 75, 25)
        
        c_health = menu.custom(20 + x, 600, percent * 75, 25)
        c_mana = menu.custom(20 + x, 635, percent_sp * 75, 25)
        
        menu.draw_color(health, (80, 25, 25))
        menu.draw_color(Mana, (25, 25, 90))
        menu.draw_color(c_health, (128, 0, 31))
        menu.draw_color(c_mana, (137, 207, 240))

def display_enemies(bad_people):
    """Only displays the enemies health using Menus"""
    menu = Menus()
    for i in range(len(bad_people)):
        person = bad_people[i]
        c_hp = person._someone.get_c_HP()
        hp = person._someone.get_HP()
        percent = float(c_hp) / float(hp)
        y = i * 200
        if i < 3:
            menu.text(person._someone.get_name(), 600, 100 + y)
            health = menu.custom(600, 200 + y , 75, 25)
            c_health = menu.custom(600, 200 + y, percent * 75, 25)
            menu.draw_color(health, (80, 25, 25))
            menu.draw_color(c_health, (128, 0, 31))
        if i >= 3:
            menu.text(person._someone.get_name(), 800, 100 + y - 600)
            health = menu.custom(800, 200 + y - 600 , 75, 25)
            c_health = menu.custom(800, 200 + y - 600, percent * 75, 25)
            menu.draw_color(health, (80, 25, 25))
            menu.draw_color(c_health, (128, 0, 31))

def update_world():
    """Combines all the visuals
    in order to layer it correctly"""
    menu = Menus()
    menu.screen_wipe()
    update_all(everyone)
    display_enemies(bad_people)
    display_stats(people)
    
class Event:
    """
    Event is recording a single event that happens
    while the program is running
    This class also ignores unessecary events so
    only Keydown, Mouse_POS, and Clicks get taken in
    
    _event is the non None Type 
    that comes from the pygame.event.get() 
    
    _mx, _my are the Mouse_POS to trigger
    specific events
    """
    def __init__(self):
        event = pygame.event.wait()
        que = pygame.event.get()
        if que != []:
            event = que.pop(0)
        self._event = event
        self._mx, self._my = pygame.mouse.get_pos()          
    def get_event(self):
        return self._event
    def get_type(self):
        return self._event.type
    def click(self):
        """
        Confirms the event is a Mouse click
        """
        return self.get_type() == MOUSEBUTTONDOWN
    def wait(self):
        """
        Forces the queue to wait until
        an important event was made
        it helped slowed traffic to catch
        problems and is more important
        if sound was added to the program
        """
        pygame.event.wait()
    def keydown(self):
        """Confirms the event is when the keyboard is used"""
        return self.get_type() == KEYDOWN
    def motion(self):
        """Confirms when the mouse is moving"""
        return self.get_type() == MOUSEMOTION
    def what_key(self):
        """Returns the value of the keypress"""
        if self.keydown():
            return int(self._event.key)
    def kill(self):
        """checks to see if the user is trying to close the program"""
        if self.get_type() == QUIT:
            pygame.quit()
            sys.exit()
    def valid_keys(self, numbers):
        """This takes in a list of keys that are valid
        to use when dealing with certain menus for needed"""
        key = 1000
        if self.keydown() and not self.motion() and not self.click():
            key = self.what_key()
        if key in numbers and key != None:
            return self.what_key()
    def sleep(self, x):
        """Makes the program wait for x amount of seconds"""
        time.sleep(x)
    def update(self):
        pygame.display.update()
    def tik(self):
        mainClock.tick(60)
    def refreash(self):
        """This makes sure the program is refreashing every frame"""
        self.update()
        self.tik()

class Event_Manager:
    """Event_Manager Combines the Menus and Event class
    with this, it's possble to make buttons for the user to 
    interact with as well as other design choices"""
    def __init__(self):
        self._event = Event()
        self._Menu = Menus()
        self._loc = 1000
    def valid_collide(self, button):
        """ takes in an existing button that's created from menus
        and checks if the mouse location is within that button"""
        return button.collidepoint((self._event._mx, self._event._my))
    def valid_click(self, button):
        """After confirming that the mouse is within the rectangle, it
        will result in true if a click was followed yo"""
        if self.valid_collide(button):
            button.inflate(5, 5)
            return self._event.click()
    def highlight_combat_cross(self, x, y, yellow_button):
        """This is a helper function to change the location of the
        rectangle that indicates which square is being read"""
        loc = self._event.valid_keys([258, 260, 262, 264])
        if loc == 264:
            #moves yellow button to top square. 
            yellow_button = self._Menu.highlight_short(x - 15, y - 55)
        if loc == 260:
            #moves yellow button to the left
            yellow_button = self._Menu.highlight_short(x - 55, y - 14)
        if loc == 258:
            #moves yellow button down
            yellow_button = self._Menu.highlight_short(x - 15, y + 27)
        if loc == 262:
            #moves square to the right
            yellow_button = self._Menu.highlight_short(x + 25, y - 14)
        self._loc = loc
        return yellow_button
    def highlight_skills(self, x, y, yellow_button):
        """This is a helper function to change the location of the
        rectangle that indicates which square is being read"""
        loc = self._event.valid_keys([256,257,258,259,260,262,263,264,265])
        if loc == 256:
            #moves yellow button to 0 button
            yellow_button = self._Menu.highlight_back(x - 47, y + 70)
        if loc == 257:
            #moves yellow button to bottom left
            yellow_button = self._Menu.highlight_short(x - 55, y + 27)
        if loc == 258:
            #moves yellow button down
            yellow_button = self._Menu.highlight_short(x - 15, y + 27)
        if loc == 259:
            #moves yellow to bottom right
            yellow_button = self._Menu.highlight_short(x + 25, y + 27)
        if loc == 260:
            #moves yellow button to the left
            yellow_button = self._Menu.highlight_short(x - 55, y - 14)
        if loc == 262:
            #moves square to the right
            yellow_button = self._Menu.highlight_short(x + 25, y - 14)
        if loc == 263:
            #moves yellow to top left
            yellow_button = self._Menu.highlight_short(x - 55, y - 55)
        if loc == 264:
            #moves yellow button to top square. 
            yellow_button = self._Menu.highlight_short(x - 15, y - 55)
        if loc == 265:
            #moves yellow to top right
            yellow_button = self._Menu.highlight_short(x + 25, y - 55)
        self._loc = loc
        return yellow_button
    def highlight_leader(self, yellow_button):
        """This is a helper function to change the location of the
        rectangle that indicates which square is being read"""
        loc = self._event.valid_keys([256, 257, 260, 263])
        if loc == 256:
            #still appears under character
            yellow_button = self._Menu.highlight_back(33, 295)
        if loc == 257:
            #appears infront of the character below
            yellow_button = self._Menu.highlight_back(230 , 386)
        if loc == 260:
            #appears infront of the middle character
            yellow_button = self._Menu.highlight_back(310, 211)
        if loc == 263:
            #appears infront of the character above
            yellow_button = self._Menu.highlight_back(230, 86)
        self._loc = loc
        return yellow_button
    def highlight_attack(self, x, y, yellow_button):
        """This is a helper function to change the location of the
        rectangle that indicates which square is being read"""
        loc = self._event.valid_keys([256, 257, 260, 263, 261, 258, 264])
        if loc == 256:
            #backs out
            yellow_button = self._Menu.highlight_back(x - 17, y + 95)
        if loc == 257:
            #attacks bottom left enemy
            yellow_button = self._Menu.highlight_short(595, 495)
        if loc == 260:
            #attacks center enemy
            yellow_button = self._Menu.highlight_short(595, 295)
        if loc == 263:
            #attacjs top left
            yellow_button = self._Menu.highlight_short(595, 95)
        if loc == 258:
            #attacks bottom right
            yellow_button = self._Menu.highlight_short(795, 495)
        if loc == 261:
            #attacks center back
            yellow_button = self._Menu.highlight_short(795, 295)
        if loc == 264:
            #attacks top right
            yellow_button = self._Menu.highlight_short(795, 95)
        self._loc = loc
        return yellow_button
    def show_loc(self):
        """ keep track of the loc for the highlight helpers"""
        return self._loc
    

def main_menu():   
    """
    Main Menu is starting screen when the program starts
    In a future version, it this screen would a more interactive
    settings for color and sound
    """
    
    while True:
        tool = Event_Manager()
        tool._Menu.screen_wipe()
        tool._Menu.text("Main Menu", 20, 20)
        
        button_1 = tool._Menu.longblock(350, 300)
         
        if tool.valid_click(button_1):
            Demo()
        tool._Menu.draw(button_1)
        tool._Menu.text("Demo", 430, 320)
        
        tool._event.kill()
        tool._event.refreash()

def Demo():
    """
    Demo runs one encounter for a turn based RPG
    The order is just the four party members versus six
    enemies
    
    anyone out of HP will switched into an image instead
    of their normal idle image
    
    The menu is mapped to the keypad, Use 5 to confirm choices
    when selecting an enemy for an attack, use 6 instead
    
    Press 0 then the confirm button in order to go back a menu
    
    First team to lose all of their HP loses
    
    you can track the enemies turns in the console incase it
    appears that the program is not responding
    """
    running = True
    load_all(everyone)
    update_world()
    order = everyone
    party = just_someone(people)
    enemies = just_someone(bad_people)
    while running:
        tool = Event_Manager()
        update_world()
        for i in range(len(order)):
            person = order[i]
            if not person._someone.Is_Dead():
                if person in people:
                    tool._Menu.text(person._someone.get_name() + "'s Turn", 20, 20)
                    combat_menu(person._x, person._y, tool._Menu, person, people)
                    tool._Menu._running = True
                    update_world()
                if person in bad_people:
                    update_world()
                    tool._Menu.text(person._someone.get_name() + "'s Turn", 20, 20)
                    BT.AI(order[i]._someone, party, enemies)
            if person._someone.Is_Dead():
                person.change_image(1)
                update_world()
        update_world()
        if BT.team_alive(party) == False or BT.team_alive(enemies) == False:
            running = False
    if not BT.team_alive(party):
        print("Game Over")
    else:
        print("You Win")
        tool._event.kill()
        tool._event.refreash()

def combat_menu(x, y, menu, someone, people):
    """
    The first menu that pops up for players
    Leader is not an option if the character is not leader
    gaurd increases the users defense until the start of their next turn
    
    use 5 to confirm your choices in this menu
    """
    running = True
    c_button = 1001
    orginal_def = 0
    update_world()
    while running:
        tool = Event_Manager()
        up_button = tool._Menu.shortblock(x+23, y-50)
        down_button = tool._Menu.shortblock(x+23, y + 35)
        left_button = tool._Menu.shortblock(x - 17, y - 7)
        right_button = tool._Menu.shortblock(x + 63, y - 7)
        if tool._event.what_key() == 261:
            tool._Menu.screen_wipe()
            if c_button == 264:
                skill_menu(x, y, someone, bad_people, menu)
            if c_button == 262:
                attack_menu(someone, bad_people, menu)
            if c_button == 260:
                leader_menu(someone, people, menu)
            if c_button == 258:
                orginal_def = someone._someone._DEF
                someone._someone._DEF = someone._someone._DEF + 10
                menu._running = False
        if orginal_def != 0 and orginal_def != someone._someone._DEF:
            someone._someone._DEF = someone._someone._DEF - 10
        if not menu.is_running():
            running = False
        yellow_button = tool.highlight_combat_cross(x + 35, y+3, up_button)
        if tool._event.keydown():
            c_button = tool.show_loc()
            update_world()
        tool._Menu.draw_highlight(yellow_button)
        tool._Menu.draw(up_button)
        tool._Menu.draw(down_button)
        tool._Menu.draw(left_button)
        tool._Menu.draw(right_button)
        
        tool._Menu.text("Skills", x+23, y - 45, False)
        tool._Menu.text("Gaurd", x+23, y + 35, False)
        tool._Menu.text("Leader", x-22, y - 7, False)
        tool._Menu.text("Attack", x+68, y - 7, False)
        
        tool._event.kill()
        tool._event.refreash()
        
def leader_menu(someone, people, menu):
    """
    Availble to the current leader
    right now you can only change the location, but still
    counts as their turn.
    """
    running = True
    c_button = 1001
    update_world()
    while running:
        if not someone.is_leader():
            running = False
        tool = Event_Manager()
        upleft_button = tool._Menu.shortblock(230, 86)
        left_button = tool._Menu.shortblock(310, 211)
        downleft_button = tool._Menu.shortblock(230 , 386)
        back_button = tool._Menu.shortblock(33, 295)
        
        if tool._event.what_key() == 261:
            if c_button == 256:
                running = False
            if c_button == 257:
                someone.change_leader(people[3])
                menu._running = False
            if c_button == 260:
                someone.change_leader(people[2])
                print("Mid")
                menu._running = False
            if c_button == 263:
                someone.change_leader(people[1])
                print("High")
                menu._running = False
        yellow_button = tool.highlight_leader(left_button)
        
        if not menu.is_running():
            running = False
        if tool._event.keydown():
            c_button = tool.show_loc()
            update_world()
        
        tool._Menu.draw_highlight(yellow_button)
        tool._Menu.draw(upleft_button)
        tool._Menu.draw(left_button)
        tool._Menu.draw(downleft_button)
        tool._Menu.draw(back_button)
        
        if c_button == 257:
            tool._Menu.text(str(people[3]._someone.get_name()), 235, 368)
        if c_button == 260:
            tool._Menu.text(str(people[2]._someone.get_name()), 315, 198)
        if c_button == 263:
            tool._Menu.text(str(people[1]._someone.get_name()), 235, 72)
        
        
        tool._event.kill()
        tool._event.refreash()
        
        
def attack_menu(person, bad_people, menu, melee=True, skill=0):
    """Attack Menu is how you target enemies for attacks.
    Melee is False when the character is using a skill instead
    skill is the index of their list of available skills"""
    running = True
    c_button = 1001
    person.change_image(2)
    update_world()
    person._someone._assign_skill()
    skills = person._someone._skill
    someones = just_someone(bad_people)
    while running:
        tool = Event_Manager()
        topleft = tool._Menu.shortblock(600, 100)
        center = tool._Menu.shortblock(600, 300)
        bottomleft = tool._Menu.shortblock(600, 500)
        topright = tool._Menu.shortblock(800, 100)
        centerback = tool._Menu.shortblock(800, 300)
        bottomright = tool._Menu.shortblock(800, 500)
        back_button = tool._Menu.shortblock(person._x - 17, person._y + 95)
        if tool._event.what_key() == 262: 
            if c_button == 256:
                running = False
            if c_button == 257:
                print("bottom left")
                if melee:
                    person._someone.Attack_Melee(bad_people[2]._someone)
                if not melee:
                    person._someone.determine_skill(skill, someones[2])
                menu._running = False
            if c_button == 260:
                if melee:
                    person._someone.Attack_Melee(bad_people[1]._someone)
                if not melee:
                    person._someone.determine_skill(skill, someones[1])
                menu._running = False
            if c_button == 263:
                if melee:
                    person._someone.Attack_Melee(bad_people[0]._someone)
                if not melee:
                    person._someone.determine_skill(skill, someones[0])
                menu._running = False
            if c_button == 258:
                if melee:
                    person._someone.Attack_Melee(bad_people[5]._someone)
                if not melee:
                    person._someone.determine_skill(skill, someones[5])
                menu._running = False
            if c_button == 261:
                if melee:
                    person._someone.Attack_Melee(bad_people[4]._someone)
                if not melee:
                    person._someone.determine_skill(skill, someones[4])
                menu._running = False
            if c_button == 264:
                if melee:
                    person._someone.Attack_Melee(bad_people[3]._someone)
                if not melee:
                    person._someone.determine_skill(skill, someones[3])
                menu._running = False
            person.change_image(0)
        yellow_button = tool.highlight_attack(person._x, person._y, topleft)
        if not menu.is_running():
            running = False
        if tool._event.keydown():
            c_button = tool.show_loc()
            update_world()
        
        tool._Menu.draw_highlight(yellow_button)
        tool._Menu.draw(back_button)
        tool._Menu.draw(topleft)
        tool._Menu.draw(center)
        tool._Menu.draw(bottomleft)
        tool._Menu.draw(topright)
        tool._Menu.draw(centerback)
        tool._Menu.draw(bottomright)
        
        tool._event.kill()
        tool._event.refreash()
        
def skill_menu(x, y, person, people, menu):
    """
    The list of skills presented by the character
    right now, the characters do not have access to Healing
    skills because their is not support menu at the momment
    also characters have the max amount of skills to prevent index errors
    currently. since enemies don't need this interface,
    they are able to heal themselves
    
    once the selected skill has been verified by pressing 5
    Attack Menu will open to select the target
    """
    running = True
    c_button = 1001
    update_world()
    person._someone._assign_skill()
    skills = person._someone._skill
    while running:
        tool = Event_Manager()
        
        up_button = tool._Menu.shortblock(x+23, y-50)
        down_button = tool._Menu.shortblock(x+23, y + 35)
        left_button = tool._Menu.shortblock(x - 17, y - 7)
        right_button = tool._Menu.shortblock(x + 63, y - 7)

        upright_button = tool._Menu.shortblock(x + 63, y - 50)
        upleft_button = tool._Menu.shortblock(x - 17, y - 50)
        downright_button = tool._Menu.shortblock(x + 63, y + 35)
        downleft_button = tool._Menu.shortblock(x - 17, y + 35)
        back_button = tool._Menu.shortblock(x - 17, y + 70)
        
        if tool._event.what_key() == 261:
            if c_button == 256:
                running = False
            if c_button == 257:
                attack_menu(person, bad_people, menu, False, 1)
            if c_button == 258:
                attack_menu(person, bad_people, menu, False, 2)
            if c_button == 259:
                attack_menu(person, bad_people, menu, False, 3)
            if c_button == 260:
                attack_menu(person, bad_people, menu, False, 4)
            if c_button == 262:
                attack_menu(person, bad_people, menu, False, 5)
            if c_button == 263:
                attack_menu(person, bad_people, menu, False, 6)
            if c_button == 264:
                attack_menu(person, bad_people, menu, False, 7)
            if c_button == 265:
                attack_menu(person, bad_people, menu, False, 8)
        
        yellow_button = tool.highlight_skills(x + 30, y, up_button)
        
        if not menu.is_running():
            running = False
        if tool._event.keydown():
            c_button = tool.show_loc()
            update_world()   
        tool._Menu.draw_highlight(yellow_button)   
        tool._Menu.draw(up_button)
        tool._Menu.draw(down_button)
        tool._Menu.draw(left_button)
        tool._Menu.draw(right_button)
        tool._Menu.draw(back_button)
        tool._Menu.draw(upright_button)
        tool._Menu.draw(downright_button)
        tool._Menu.draw(upleft_button)
        tool._Menu.draw(downleft_button)
        
        tool._Menu.text(skills[1].get_skill_name(), x-17, y+35, False)
        tool._Menu.text(skills[2].get_skill_name(), x+23, y+35, False)
        tool._Menu.text(skills[3].get_skill_name(), x+63, y+35, False)
        tool._Menu.text(skills[4].get_skill_name(), x-17, y-7, False)
        tool._Menu.text(skills[5].get_skill_name(), x+63, y-7, False)
        tool._Menu.text(skills[6].get_skill_name(), x-17, y-50, False)
        tool._Menu.text(skills[7].get_skill_name(), x+23, y-50, False)
        tool._Menu.text(skills[8].get_skill_name(), x+63, y-50, False)
        tool._event.kill()
        tool._event.refreash()
    