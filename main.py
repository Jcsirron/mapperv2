#!/usr/bin/env python
"""
Main.py program
Version 1.1
Created by Chandler Norris March 18, 2015
Updated by Chandler Norris April 22, 2020

This is the basic format for a pygame main loop.  This has everything needed to initialize a screen and draw to it with
minimal dependencies.
"""

# Import the needed accessory libraries
import pygame
import sys
from pygame.locals import *
from joystick_handler import *
from screen_handler import *
# from music_handler import *
# from sound_handler import *
from map_space import *
from meat_space import *

# Initialize Pygame
pygame.init()
# Initialize the sound module
pygame.mixer.init()
# Initialize the joystick module
pygame.joystick.init()

# Initialize the clock to limit the frames per second
CLOCK = pygame.time.Clock()


def main():
    fps_font = font.Font(FONT, 36)
    # Testing the map_space file
    player_map = MapSpace()
    world = MeatSpace()
    realmode = True
    # The Game Loop
    mouse = [False, pygame.mouse.get_pos()]
    while True:
        mouse[0] = False
        movement = [0, 0, False]
        delta_time = CLOCK.get_time() / 1000
        # Check for quit and do so if needed
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mouse[0] = event.button
            if event.type == KEYUP and event.key == K_SPACE:
                movement[2] = True
        # Get the state of all of the keyboard keys
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            movement[1] -= 1
        elif keys[K_s]:
            movement[1] += 1
        if keys[K_a]:
            movement[0] -= 1
        elif keys[K_d]:
            movement[0] += 1
        # Get the state of the mouse
        # This is where you can call the joystick, if you want to use it.
        # joysticks = get_joysticks()
        mouse[1] = pygame.mouse.get_pos()
        # This is where the "game logic" WILL happen.
        # Put it in a different function.
        if realmode is True:
            update = world.update(movement, mouse, delta_time)
            if update is not None:
                realmode = False
                player_map.active = True
                if type(update) == Quest:
                    player_map.set_quest(update)
                    player_map.set_mode("path")
        else:
            player_map.update(mouse, world.map)
            if not player_map.active:
                realmode = True
        draw_to_buffer([[fps_font.render(str(int(CLOCK.get_fps())), False, BLACK), (0, 0)]])
        update_screen()
        # Limit the frames drawn per second
        CLOCK.tick(60)


# Call the Main function to start the program
if __name__ == "__main__":
    main()
