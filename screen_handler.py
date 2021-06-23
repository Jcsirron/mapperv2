#!/usr/bin/env python
"""
screen_handler.py
Created by Chandler Norris April 25, 2020

This is a basic pygame screen handling program to ease the drawing to the screen.  It implements a rudimentary screen
shake capability for creating juice.
"""
import pygame.surface
import pygame.rect
from random import randrange
from os import environ


# Name the window screen
pygame.display.set_caption("CartograTour")
# Set the window icon
pygame.display.set_icon(pygame.surface.Surface((32, 32)))
# Center the window, since that's the nice way to do it.
environ['SDL_VIDEO_CENTERED'] = '1'

# Set the screensize
SCREEN_SIZE = (1024, 768)
SCREEN_CENTER = (int(SCREEN_SIZE[0]/2), int(SCREEN_SIZE[1]/2))
buffer_surface = pygame.Surface(SCREEN_SIZE)
# Initialize a screen to reference later
screen = pygame.display.set_mode(size=SCREEN_SIZE)
buffer_surface.fill((0, 0, 0))
buffer_surface = buffer_surface.convert()
FILL_COLOR = (0, 0, 0)
FULLSCREEN = False


def update_screen(shake=False, shake_distance=15):
    # Draw the BUFFER_SURFACE to the screen
    if shake is not False:
        screen.fill(FILL_COLOR)
        if shake == "horizontal":
            screen.blit(buffer_surface, (0, 0), ((int(randrange(0, shake_distance) - shake_distance / 2), 0),
                                                 SCREEN_SIZE))
        elif shake == "vertical":
            screen.blit(buffer_surface, (0, 0), ((0, int(randrange(0, shake_distance) - shake_distance / 2)),
                                                 SCREEN_SIZE))
        else:
            screen.blit(buffer_surface, (0, 0), ((int(randrange(0, shake_distance) - shake_distance / 2),
                                                  int(randrange(0, shake_distance) - shake_distance / 2)), SCREEN_SIZE))
    else:
        screen.blit(buffer_surface, (0, 0))
    # Update the screen to reflect changes
    pygame.display.update()


# Example on how to draw to the buffer.
# draw_to_buffer([[pygame.Surface((100, 100)), (0, 0)], [pygame.Surface((100, 100)), [555, 155]]])
def draw_to_buffer(surfaces_list):
    for surface in surfaces_list:
        buffer_surface.blit(surface[0], surface[1])


def clear_buffer():
    buffer_surface.fill(FILL_COLOR)


def set_fill_color(color=(0, 0, 0)):
    global FILL_COLOR
    FILL_COLOR = color


def set_screen_mode(resolution=SCREEN_SIZE, full_screen=False):
    global SCREEN_SIZE
    global buffer_surface
    global screen
    global FULLSCREEN
    if resolution != SCREEN_SIZE:
        SCREEN_SIZE = resolution
        screen = pygame.display.set_mode(size=SCREEN_SIZE)
        buffer_surface = pygame.Surface(SCREEN_SIZE)
        buffer_surface.fill(FILL_COLOR)
        buffer_surface = buffer_surface.convert()
    if full_screen is not False and FULLSCREEN is False:
        pygame.display.toggle_fullscreen()
        FULLSCREEN = True
    elif full_screen is False and FULLSCREEN is not False:
        pygame.display.toggle_fullscreen()
        FULLSCREEN = False
