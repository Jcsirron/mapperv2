from pygame import quit
from globals import *
from sys import exit
from screen_handler import draw_to_buffer


def end_game():
    quit()
    exit()


class Menu(object):

    def __init__(self, menu_list, offset=(0, 0), background=None):
        self.menu_list = menu_list
        self.background = background
        self.offset = offset
        self.selected_option = 0
        self.move_toggle = False

    def update(self, movement=None, cursor=(0, 0)):
        return_value = None
        if self.background is not None:
            draw_to_buffer([[self.background, self.offset]])
        for button in self.menu_list:
            if button.rect.collidepoint(cursor[0]):
                button.update(highlight=True)
                if cursor[1]:
                    if isinstance(button.call_function, str):
                        return_value = button.call_function
                    else:
                        button.activate()
            else:
                button.update()
        if movement is not None:
            if movement[1] > 0 and self.move_toggle is False:
                self.move_toggle = True
                if self.selected_option < len(self.menu_list) - 1:
                    self.selected_option += 1
                else:
                    self.selected_option = 0
                cursor[0] = self.menu_list[self.selected_option].get_center()
            elif movement[1] < 0 and self.move_toggle is False:
                self.move_toggle = True
                if self.selected_option > 0:
                    self.selected_option -= 1
                else:
                    self.selected_option = len(self.menu_list) - 1
                cursor[0] = self.menu_list[self.selected_option].get_center()
            elif movement[1] == 0:
                self.move_toggle = False
        return return_value, cursor[0]

