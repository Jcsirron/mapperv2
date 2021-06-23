import pygame
from globals import *
from screen_handler import draw_to_buffer, SCREEN_SIZE


class TimeFilter(object):
    def __init__(self, time_look_up):
        self.surface = pygame.surface.Surface(SCREEN_SIZE)
        self.surface.fill(BLACK)
        self.surface.set_colorkey(WHITE)
        self.opacity = 0
        self.surface.set_alpha(self.opacity)
        self.time_look_up = time_look_up
        self.darkening = True

    def update(self, time_of_day):
        self.look_up_opacity(time_of_day)
        if self.opacity != 0:
            draw_to_buffer([[self.surface, (0, 0)]])
        '''if self.darkening:
            if self.opacity > 200:
                self.darkening = False
            else:
                self.opacity += 1
        else:
            if self.opacity < 0:
                self.darkening = True
            else:
                self.opacity -= 1
        self.surface.set_alpha(self.opacity)
        draw_to_buffer([[self.surface, (0, 0)]])'''

    def add_light(self, light_surface, location):
        self.surface.blit(light_surface, location)

    def fill_darkness(self):
        self.surface.fill(BLACK)

    def look_up_opacity(self, time_of_day):
        if time_of_day in self.time_look_up:
            if self.opacity != self.time_look_up[time_of_day]:
                self.opacity = self.time_look_up[time_of_day]
                self.surface.set_alpha(self.opacity)
