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
import sys, os.path
# from music_handler import *
# from sound_handler import *
from map_space import *
from meat_space import *
from input_handler import *
from pickling_io import *
from menu import Menu
import pickle


# TODO: Consolidate all saves and loads into a single file.
def game(player_map=None, world=None, quests=None, player=None):
    fps_font = font.Font(FONT, 36)
    # Testing the map_space file
    if player_map is None:
        player_map = MapSpace()
    else:
        map_import = read_in_file(player_map, "Saves")
        player_map = MapSpace(loading=True)
        for tile in map_import:
            player_map.load_tile(tile=tile, **map_import[tile])
            player_map.update_tile(tile=tile, **map_import[tile])
    if world is None:
        world = MeatSpace()
    else:
        map_import = read_in_file(world, "Saves")
        world = MeatSpace(loading=True)
        for tile in map_import:
            world.load_tile(tile=tile, **map_import[tile])
        if quests is not None:
            quests_import = read_in_file(quests, "Saves")
            for quest in quests_import:
                if quest == "completed":
                    for completed in quests_import[quest]:
                        world.quest_menu.load_quest("completed", **completed)
                elif quest == "active":
                    for active in quests_import[quest]:
                        world.quest_menu.load_quest("active", **active)
                elif quest == "failed":
                    for failed in quests_import[quest]:
                        world.quest_menu.load_quest("failed", **failed)
            world.quest_menu.update_quest_list()
        if player is not None:
            player = read_in_file(player, "Saves")
            world.players[0].load_player(**player)
            world.update_flag_counts()
        world.map.trim_tile_set(world.player_to_tile())
    realmode = True
    # The Game Loop
    cursor = SCREEN_CENTER
    escape_menu = GameMenu()
    esc_menu = False
    while True:
        delta_time = CLOCK.get_time() / 1000
        # Check for quit and do so if needed
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                save_world(world, player_map)
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE or event.type == JOYBUTTONUP and event.button == 7:
                esc_menu = not esc_menu
        # Get the state of all of the keyboard keys
        keys = pygame.key.get_pressed()
        if pygame.joystick.get_count() > 0:
            # Because of course you have to initialize the joysticks every time...
            joystick = pygame.joystick.Joystick(JOYPAD_NUMBER)
            joystick.init()
        else:
            joystick = None
        user_inputs = format_inputs(keys, events, joystick, cursor)
        cursor = user_inputs[1][0]
        # This is where the "game logic" WILL happen.
        # Put it in a different function.
        if realmode is True:
            if esc_menu:
                update = world.update((0, 0), user_inputs[1], user_inputs[2], delta_time)
            else:
                update = world.update(user_inputs[0], user_inputs[1], user_inputs[2], delta_time)
            if update is not None or user_inputs[2][2] is True:
                realmode = False
                player_map.active = True
                cursor = SCREEN_CENTER
                if type(update) == Quest:
                    player_map.set_quest(update)
                    player_map.set_mode("path")
        else:
            if esc_menu:
                player_map.update([user_inputs[1][0], False], [False, False, False, False], world.map)
            else:
                cursor = player_map.update(user_inputs[1], user_inputs[2], world.map)
                if not player_map.active:
                    realmode = True
        if esc_menu:
            menu_choice = escape_menu.update(user_inputs[0], user_inputs[1])
            cursor = menu_choice[1]
            if menu_choice[0] == "save and quit":
                save_world(world, player_map)
                return
            elif menu_choice[0] == "quit":
                if os.path.isfile(os.path.join('Saves', 'automap.txt')):
                    os.remove(os.path.join('Saves', 'automap.txt'))
                return
            elif menu_choice[0] == "continue":
                esc_menu = False
        draw_to_buffer([[fps_font.render(str(int(CLOCK.get_fps())), False, BLACK), (0, 0)]])
        # Draw the cursor....
        draw.rect(buffer_surface, WHITE, rect.Rect(cursor, (8, 8)))
        draw.rect(buffer_surface, BLACK, rect.Rect((cursor[0]+2, cursor[1]+2), (4, 4)))
        update_screen()
        # Limit the frames drawn per second
        CLOCK.tick(60)


class GameMenu(Menu):
    def __init__(self):
        background = surface.Surface((SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
        background.fill(YELLOW)
        draw.rect(background, BROWN, rect.Rect(0, 0, SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), 6, 6)
        title_font = font.Font(LOGO_FONT, 48)
        title_font = title_font.render("CartograTour", True, BLACK)
        background.blit(title_font, (SCREEN_SIZE[0]/4 - title_font.get_width()/2, 36))
        buttons = [Button("Quit To Main Menu", LOGO_FONT, 36, BLACK, antialias=True, call_function="quit", button_color=YELLOW, location=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1] / 2 + 32)),
                   Button("Save & Quit", LOGO_FONT, 36, BLACK, antialias=True, call_function="save and quit", button_color=YELLOW, location=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1] / 2 + 96)),
                   Button("Return to Game", LOGO_FONT, 36, BLACK, antialias=True, call_function="continue", button_color=YELLOW, location=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] * (3 / 4) - 36))]
        Menu.__init__(self, menu_list=buttons, background=background, offset=(SCREEN_SIZE[0]/4, SCREEN_SIZE[1]/4))


def save_world(world, player_map):
    save_out_file(world.map.pack_map("automap.txt"), "worldmap.txt", "Saves")
    save_out_file(world.export_quest_menu(), "questmenu.txt", "Saves")
    save_out_file(player_map.map.pack_map(), "playermap.txt", "Saves")
    save_out_file(world.players[0].export_player(), "player.txt", "Saves")
    if os.path.isfile(os.path.join('Saves', 'automap.txt')):
        os.remove(os.path.join('Saves', 'automap.txt'))
