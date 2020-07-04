# -*- coding: utf-8 -*-
"""
Created on Sun May 17 01:41:00 2020

@author: Mikey
"""


import sys
import pygame

def main():
    pygame.init()
 
    fps = 60
    fpsClock = pygame.time.Clock()
 
    width, height = 720, 500
    screen = pygame.display.set_mode((width, height))
 
    # Game loop.
    while True:
        screen.fill((31, 13, 185))
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
  
        # Update.
        # Draw.
        pygame.display.flip()
        fpsClock.tick(fps)
        
if __name__ == "__main__":
    print("test")
    main()