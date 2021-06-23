import pygame, sys, os
from menu import Menu, end_game
from pygame.locals import *
from globals import *
from input_handler import *
from screen_handler import update_screen, SCREEN_SIZE, buffer_surface, SCREEN_CENTER
from game import game
from button import Button

# Initialize Pygame
pygame.init()
# Initialize the sound module
pygame.mixer.init()
# Initialize the joystick module
pygame.joystick.init()


def main():
    saves_in_directory = os.listdir(".")
    if "Saves" not in saves_in_directory:
        os.mkdir("Saves")
    main_menu = MainMenu()
    cursor = main_menu.menu_list[main_menu.selected_option].get_center()
    while True:
        delta_time = CLOCK.get_time() / 1000
        # Check for quit and do so if needed
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        # Because of course you have to initialize the joysticks every time...
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(JOYPAD_NUMBER)
            joystick.init()
        else:
            joystick = None
        user_inputs = format_inputs(pygame.key.get_pressed(), events, joystick, cursor)
        cursor = main_menu.update(user_inputs[0], user_inputs[1])[1]
        # Draw the cursor....
        pygame.draw.rect(buffer_surface, BLACK, rect.Rect(cursor, (8, 8)))
        update_screen()
        CLOCK.tick(60)


class MainMenu(Menu):
    def __init__(self):
        background = surface.Surface(SCREEN_SIZE)
        background.fill(YELLOW)
        pygame.draw.rect(background, BROWN, rect.Rect(SCREEN_SIZE[0]/4, SCREEN_SIZE[1]/4, SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), 6, 6)
        title_font = font.Font(LOGO_FONT, 72)
        title_font = title_font.render("CartograTour", True, BLACK)
        background.blit(title_font, (SCREEN_SIZE[0]/2 - title_font.get_width()/2, 64))
        buttons = [Button("Play", LOGO_FONT, 36, BLACK, antialias=True, call_function=game, button_color=YELLOW, location=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/4+36)),
                   Button("Quit", LOGO_FONT, 36, BLACK, antialias=True, call_function=end_game, button_color=YELLOW, location=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]*(3/4)-36))]
        Menu.__init__(self, menu_list=buttons, background=background)

    def update(self, movement=None, cursor=(0, 0)):
        return_value, cursor[0] = Menu.update(self, movement, cursor)
        if len(self.menu_list) < 3:
            if os.path.isfile(os.path.join('Saves', 'worldmap.txt')) and os.path.isfile(os.path.join('Saves', 'playermap.txt')) and os.path.isfile(os.path.join('Saves', 'questmenu.txt')):
                self.menu_list.insert(1, Button("Continue", LOGO_FONT, 36, BLACK, antialias=True, call_function=game, button_color=YELLOW, call_args={'player_map': 'playermap.txt', 'world': 'worldmap.txt', 'quests': 'questmenu.txt', 'player': 'player.txt'}, location=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)))
        return return_value, cursor[0]


# Call the Main function to start the program
if __name__ == "__main__":
    main()
