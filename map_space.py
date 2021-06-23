from map import MapObject, TERRAIN, IMPROVEMENTS, FEATURES, ANIMALS
from pygame import rect
from globals import *
from screen_handler import *
from button import *
from map_space_assets import map_forest_tile, map_mountain_tile, map_waterway_tile, map_plain_tile, map_home_tile, EDIT_ICON
from meat_space_assets import FLAGS, DECOR_OBJECTS
from textbox import *


# noinspection PyAttributeOutsideInit,PyGlobalUndefined
class MapSpace(object):

    def __init__(self, loading=False):
        self.map = MapObject()
        self.highlight_tile = (0, 0)
        self.highlight_rect = pygame.rect.Rect(SCREEN_CENTER[0] - int(TILE_SIZE[0] / 2), SCREEN_CENTER[1] - int(TILE_SIZE[1] / 2), TILE_SIZE[0], TILE_SIZE[1])
        self.map_offset = None
        self.mode = None
        self.quest = None
        self.active = False
        self.__set_up_selected_menu__()
        self.__set_up_selected_submenus__()
        self.__set_up_path_mode__()
        self.__set_up_charting_mode__()
        self.map_sprite = surface.Surface(TILE_SIZE)
        if not loading:
            self.add_tile((0, 0), TILE_SIZE, "town", "home")
            self.set_highlight_tile((0, 0))
        self.help_text_location = rect.Rect(16, SCREEN_SIZE[1] - 96, 384, 128)

    def __set_up_selected_menu__(self):
        self.selected_rect = pygame.rect.Rect(SCREEN_CENTER[0] - 256, SCREEN_CENTER[1] - 256, 512, 512)
        self.terrain_button = Button("Change Terrain", FONT, 24, WHITE, button_color=BROWN)
        self.terrain_button.update_location((self.selected_rect.right + 4, self.selected_rect.top))
        self.improvement_button = Button("Change Improvement", FONT, 24, WHITE, button_color=BROWN)
        self.improvement_button.update_location((self.selected_rect.right + 4, self.selected_rect.top + int(self.terrain_button.get_height() * 1.5)))
        self.feature_button = Button("Change Feature", FONT, 24, WHITE, button_color=BROWN)
        self.feature_button.update_location((self.selected_rect.right + 4, self.selected_rect.top + int(self.terrain_button.get_height() * 3)))
        self.animal_button = Button("Change Animal", FONT, 24, WHITE, button_color=BROWN)
        self.animal_button.update_location((self.selected_rect.right + 4, self.selected_rect.top + int(self.terrain_button.get_height() * 4.5)))
        self.clear_button = Button("Clear", FONT, 18, WHITE, button_color=BROWN)
        self.clear_button.update_location((self.selected_rect.right + 16, self.selected_rect.bottom - self.clear_button.surface.get_height()))
        self.depleted_button = Button("Toggle Depleted", FONT, 24, WHITE, button_color=BROWN)
        self.depleted_button.update_location((self.clear_button.get_rect().x, self.clear_button.get_rect().y - (self.depleted_button.get_height() * 2)))
        text = font.Font(FONT, 36)
        text = text.render("THIS AREA IS DEPLETED!", False, WHITE)
        self.depleted_text = surface.Surface(text.get_size())
        self.depleted_text.set_colorkey(self.depleted_text.get_at((0, 0)))
        draw.rect(self.depleted_text, BLACK, self.depleted_text.get_rect(), border_radius=4)
        self.depleted_text.blit(text, (0, 0))
        self.selected_menu_help_text = surface.Surface((384, 96))
        self.selected_menu_help_text.fill(BLACK)
        draw_text_to_surface(self.selected_menu_help_text, "Left Click to choose feature type.  Click outside selected tile to return.", WHITE, font.Font(FONT, 26), False)

    def __set_up_selected_submenus__(self):
        self.selected_submenu = None
        self.last_edited = None
        self.terrain_sub_buttons = []
        self.improvement_sub_buttons = []
        self.feature_sub_buttons = []
        self.animal_sub_buttons = []
        iterator = 1
        for terrain in TERRAIN:
            button = Button(terrain, FONT, 18, WHITE, button_color=BROWN, call_function=terrain)
            button.update_location((self.selected_rect.right + 16, self.selected_rect.top + int(button.surface.get_height() * 2 * iterator)))
            self.terrain_sub_buttons.append(button)
            iterator += 1
        iterator = 1
        for improvement in IMPROVEMENTS:
            button = Button(improvement, FONT, 18, WHITE, button_color=BROWN, call_function=improvement)
            button.update_location((self.selected_rect.right + 16, self.selected_rect.top + int(button.surface.get_height() * 2 * iterator)))
            self.improvement_sub_buttons.append(button)
            iterator += 1
        iterator = 1
        for feature in FEATURES:
            button = Button(feature, FONT, 18, WHITE, button_color=BROWN, call_function=feature)
            button.update_location((self.selected_rect.right + 16, self.selected_rect.top + int(button.surface.get_height() * 2 * iterator)))
            self.feature_sub_buttons.append(button)
            iterator += 1
        iterator = 1
        for animal in ANIMALS:
            button = Button(animal, FONT, 18, WHITE, button_color=BROWN, call_function=animal)
            button.update_location((self.selected_rect.right + 16, self.selected_rect.top + int(button.surface.get_height() * 2 * iterator)))
            self.animal_sub_buttons.append(button)
            iterator += 1

    def __set_up_path_mode__(self):
        self.path = []
        self.done_button = Button("Done", FONT, 24, WHITE, button_color=BROWN)
        self.done_button.update_location((SCREEN_SIZE[0]-16, SCREEN_SIZE[1]-16), "bottom right")
        self.cancel_button = Button("Cancel", FONT, 24, WHITE, button_color=BROWN)
        self.cancel_button.update_location((self.done_button.rect.left-16, SCREEN_SIZE[1]-16), "bottom right")
        self.path_mode_help_text = surface.Surface((384, 96))
        self.path_mode_help_text.fill(BLACK)
        draw_text_to_surface(self.path_mode_help_text, "Left Click to set destination. Right Click to move camera.  Left Click on end node to remove it.", WHITE, font.Font(FONT, 26), False)

    def __set_up_charting_mode__(self):
        self.selected_flag = None
        red_flag = surface.Surface((FLAGS[0].image.get_size()[0] + 12, FLAGS[0].image.get_size()[1] + 12)).convert()
        red_flag.fill(WHITE)
        draw.rect(red_flag, BROWN, red_flag.get_rect(), 4, 2)
        orange_flag = red_flag.copy()
        blue_flag = red_flag.copy()
        remove_flag = red_flag.copy()
        red_flag.blit(FLAGS[1].image, (6, 6))
        orange_flag.blit(FLAGS[2].image, (6, 6))
        blue_flag.blit(FLAGS[0].image, (6, 6))
        draw.circle(remove_flag, RED, (remove_flag.get_width()/2, remove_flag.get_height()/2), remove_flag.get_width() / 3, 4)
        draw.line(remove_flag, RED, (8, remove_flag.get_height() - 8), (remove_flag.get_width() - 8, 8), 4)
        self.red_flag_button = Button(button_image=red_flag)
        self.red_flag_button.update_location((SCREEN_CENTER[0] - red_flag.get_width() * 1.8, SCREEN_SIZE[1] - red_flag.get_height()), "center")
        self.orange_flag_button = Button(button_image=orange_flag)
        self.orange_flag_button.update_location((SCREEN_CENTER[0] - orange_flag.get_width() * 0.6, SCREEN_SIZE[1] - orange_flag.get_height()), "center")
        self.blue_flag_button = Button(button_image=blue_flag)
        self.blue_flag_button.update_location((SCREEN_CENTER[0] + blue_flag.get_width() * 0.6, SCREEN_SIZE[1] - blue_flag.get_height()), "center")
        self.remove_flag_button = Button(button_image=remove_flag)
        self.remove_flag_button.update_location((SCREEN_CENTER[0] + blue_flag.get_width() * 1.8, SCREEN_SIZE[1] - blue_flag.get_height()), "center")
        self.charting_mode_help_text = surface.Surface((384, 96))
        self.charting_mode_help_text.fill(BLACK)
        draw_text_to_surface(self.charting_mode_help_text, "Left Click to choose tile.", WHITE, font.Font(FONT, 26), False)

    def update(self, cursor, buttons, world_map=None):
        global FILL_COLOR
        if FILL_COLOR != BLACK:
            set_fill_color(BLACK)
        clear_buffer()
        self.redraw_map()
        draw_to_buffer([[self.map_sprite, self.map_offset]])
        if self.mode == "selected":
            self.selected_mode(cursor, buttons)
        elif self.mode == "path":
            cursor = self.path_mode(cursor, world_map)
        else:
            cursor = self.charting_mode(cursor)
        if buttons[2] is True and self.mode != "path":
            self.mode = None
            self.active = False
        if buttons[1] is True and self.mode == "path":
            self.end_path_mode()
            self.mode = None
        draw.rect(buffer_surface, WHITE, rect.Rect(cursor[0], (4, 4)))
        return cursor[0]

    def selected_mode(self, cursor, buttons):
        if self.selected_submenu is None and buttons[1]:
            self.mode = None
            cursor[0] = SCREEN_CENTER
        elif self.selected_submenu is not None and buttons[1]:
            if self.selected_submenu == "terrain":
                cursor[0] = self.terrain_button.get_center()
            elif self.selected_submenu == "improvement":
                cursor[0] = self.improvement_button.get_center()
            elif self.selected_submenu == "feature":
                cursor[0] = self.feature_button.get_center()
            elif self.selected_submenu == "animal":
                cursor[0] = self.animal_button.get_center()
            self.selected_submenu = None
        if not self.help_text_location.collidepoint(cursor[0]):
            draw_to_buffer([[self.selected_menu_help_text, self.help_text_location]])
        active_tile = self.map.get_tile(self.highlight_tile)
        if active_tile.terrain == "forest":
            draw_to_buffer([[map_forest_tile, self.selected_rect]])
        elif active_tile.terrain == "swamp":
            draw_to_buffer([[map_waterway_tile, self.selected_rect]])
        elif active_tile.terrain == "plain":
            draw_to_buffer([[map_plain_tile, self.selected_rect]])
        elif active_tile.terrain == "mountain":
            draw_to_buffer([[map_mountain_tile, self.selected_rect]])
        elif active_tile.terrain == "town":
            draw_to_buffer([[map_home_tile, self.selected_rect]])
        else:
            draw.rect(buffer_surface, BROWN, self.selected_rect)
        if active_tile.depleted:
            buffer_surface.blit(self.depleted_text, (buffer_surface.get_width()/2-self.depleted_text.get_width()/2, buffer_surface.get_height()/2-self.depleted_text.get_height()/2))
        for improvement in self.improvement_sub_buttons:
            if active_tile.improvement == improvement.call_function:
                draw_to_buffer([[improvement.surface, (self.selected_rect.left + 4, self.selected_rect.top)]])
        for feature in self.feature_sub_buttons:
            if active_tile.feature == feature.call_function:
                draw_to_buffer([[feature.surface, (self.selected_rect.left + 4, self.selected_rect.top + feature.surface.get_height() * 1.5)]])
        for animal in self.animal_sub_buttons:
            if active_tile.animals == animal.call_function:
                draw_to_buffer([[animal.surface, (self.selected_rect.left + 4, self.selected_rect.top + animal.surface.get_height() * 3)]])
        draw.rect(buffer_surface, WHITE, self.selected_rect, 6)

        if self.selected_submenu is None:
            self.terrain_button.update()
            self.improvement_button.update()
            self.feature_button.update()
            self.animal_button.update()
            self.clear_button.update()
            self.depleted_button.update()
            if cursor[1]:
                if self.terrain_button.get_rect().collidepoint(cursor[0]):
                    self.selected_submenu = "terrain"
                elif self.improvement_button.get_rect().collidepoint(cursor[0]):
                    self.selected_submenu = "improvement"
                elif self.feature_button.get_rect().collidepoint(cursor[0]):
                    self.selected_submenu = "feature"
                elif self.animal_button.get_rect().collidepoint(cursor[0]):
                    self.selected_submenu = "animal"
                elif self.clear_button.get_rect().collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, terrain="clear", improvements="clear", features="clear", animals="clear")
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
                elif self.depleted_button.get_rect().collidepoint(cursor[0]):
                    self.update_tile(self.highlight_tile, depleted=not self.map.map_set[self.highlight_tile].depleted)
                    self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                    self.last_edited = self.highlight_tile
                elif not self.selected_rect.collidepoint(cursor[0]):
                    self.mode = None

        elif self.selected_submenu == "terrain":
            draw_to_buffer([[self.terrain_button.surface, (self.selected_rect.right + 4, self.selected_rect.top)]])
            self.clear_button.update()
            for button in self.terrain_sub_buttons:
                button.update()
                if cursor[1] and button.rect.collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, terrain=button.call_function)
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
            if cursor[1]:
                if self.clear_button.rect.collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, terrain="clear")
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
                else:
                    self.selected_submenu = None

        elif self.selected_submenu == "improvement":
            draw_to_buffer([[self.improvement_button.surface, (self.selected_rect.right + 4, self.selected_rect.top)]])
            self.clear_button.update()
            for button in self.improvement_sub_buttons:
                button.update()
                if cursor[1] and button.rect.collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, improvements=button.call_function)
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
            if cursor[1]:
                if self.clear_button.rect.collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, improvements="clear")
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
                else:
                    self.selected_submenu = None

        elif self.selected_submenu == "feature":
            draw_to_buffer([[self.feature_button.surface, (self.selected_rect.right + 4, self.selected_rect.top)]])
            self.clear_button.update()
            for button in self.feature_sub_buttons:
                button.update()
                if cursor[1] and button.rect.collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, features=button.call_function)
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
            if cursor[1]:
                if self.clear_button.rect.collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, features="clear")
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
                self.selected_submenu = None

        elif self.selected_submenu == "animal":
            draw_to_buffer([[self.animal_button.surface, (self.selected_rect.right + 4, self.selected_rect.top)]])
            self.clear_button.update()
            for button in self.animal_sub_buttons:
                button.update()
                if cursor[1] and button.rect.collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, animals=button.call_function)
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
            if cursor[1]:
                if self.clear_button.rect.collidepoint(cursor[0]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, animals="clear")
                        self.add_buffer_tiles(self.highlight_tile, TILE_SIZE)
                        self.last_edited = self.highlight_tile
                    else:
                        # TODO: Put in an error notification here
                        pass
                self.selected_submenu = None

    def path_mode(self, cursor, world_map=None):
        if not self.help_text_location.collidepoint(cursor[0]):
            draw_to_buffer([[self.path_mode_help_text, self.help_text_location]])
        if (0, 0) not in self.path:
            self.path.insert(0, (0, 0))
        if cursor[1] == 1:
            if self.cancel_button.rect.collidepoint(cursor[0]):
                self.end_path_mode()
            elif self.done_button.rect.collidepoint(cursor[0]):
                self.end_path_mode(world_map)
            elif self.convert_position_to_tile(cursor[0]) == self.path[-1]:
                # If it matches the last path in the list, remove it.
                self.path.remove(self.convert_position_to_tile(cursor[0]))
            elif self.convert_position_to_tile(cursor[0]) not in self.path:
                new_location = self.convert_position_to_tile(cursor[0])
                if new_location[0] != self.path[-1][0] and new_location[1] != self.path[-1][1]:
                    if abs(self.path[-1][0] - new_location[0]) > abs(self.path[-1][1] - new_location[1]):
                        self.path.append((self.path[-1][0], new_location[1]))
                    else:
                        self.path.append((new_location[0], self.path[-1][1]))
                self.path.append(self.convert_position_to_tile(cursor[0]))
        elif cursor[1] == 3:
            self.set_highlight_tile(self.convert_position_to_tile(cursor[0]))
        for path_point in self.path:
            if self.path.index(path_point) + 1 < len(self.path):
                # Draw from current to next
                self.draw_point_to_point(path_point, self.path[self.path.index(path_point) + 1])
            else:
                # Draw the circle at the center of the tile
                offset = SCREEN_CENTER[0] - self.highlight_tile[0] * TILE_SIZE[0], SCREEN_CENTER[1] - self.highlight_tile[1] * TILE_SIZE[1]
                draw.circle(buffer_surface, GGREEN, center=(path_point[0] * TILE_SIZE[0] + offset[0], path_point[1] * TILE_SIZE[1] + offset[1]), radius=4)
        if self.quest is not None:
            draw_to_buffer([[self.quest.surface, (SCREEN_SIZE[0]/2 - self.quest.rect[2]/2, 8)]])
        self.cancel_button.update()
        self.done_button.update()
        return cursor

    def end_path_mode(self, world_map=None):
        self.mode = None
        self.active = False
        if world_map is not None:
            self.quest.check_quest(self.path, world_map, self.map)
        self.set_quest(None)
        self.path = []

    def charting_mode(self, cursor):
        if not self.help_text_location.collidepoint(cursor[0]):
            draw_to_buffer([[self.charting_mode_help_text, self.help_text_location]])
        draw.rect(buffer_surface, WHITE, self.highlight_rect, 4)
        if not self.red_flag_button.rect.collidepoint(cursor[0]) and not self.orange_flag_button.rect.collidepoint(cursor[0]) and not self.blue_flag_button.rect.collidepoint(cursor[0]):
            grid_tile = self.snap_position_to_tile(cursor[0])
            draw.rect(buffer_surface, WHITE, (grid_tile, TILE_SIZE), 4)
        if cursor[1] == 1:
            if self.done_button.rect.collidepoint(cursor[0]):
                self.active = False
            elif self.red_flag_button.rect.collidepoint(cursor[0]):
                if self.selected_flag != "red":
                    self.selected_flag = "red"
                else:
                    self.selected_flag = None
            elif self.orange_flag_button.rect.collidepoint(cursor[0]):
                if self.selected_flag != "orange":
                    self.selected_flag = "orange"
                else:
                    self.selected_flag = None
            elif self.blue_flag_button.rect.collidepoint(cursor[0]):
                if self.selected_flag != "blue":
                    self.selected_flag = "blue"
                else:
                    self.selected_flag = None
            elif self.remove_flag_button.rect.collidepoint(cursor[0]):
                if self.selected_flag != "remove":
                    self.selected_flag = "remove"
                else:
                    self.selected_flag = None
            else:
                grid_tile = self.convert_position_to_tile(cursor[0])
                if self.selected_flag is not None and self.map.tile_in_map(grid_tile):
                    active_flags = []
                    for flag in self.map.map_set[grid_tile].objects:
                        active_flags.append(flag.id)
                    draw_object = None
                    if self.selected_flag == "red":
                        if "FLAGS[1]" in active_flags:
                            self.map.map_set[grid_tile].objects.pop(active_flags.index("FLAGS[1]"))
                        else:
                            draw_object = FLAGS[1]
                    elif self.selected_flag == "orange":
                        if "FLAGS[2]" in active_flags:
                            self.map.map_set[grid_tile].objects.pop(active_flags.index("FLAGS[2]"))
                        else:
                            draw_object = FLAGS[2]
                    elif self.selected_flag == "blue":
                        if "FLAGS[0]" in active_flags:
                            self.map.map_set[grid_tile].objects.pop(active_flags.index("FLAGS[0]"))
                        else:
                            draw_object = FLAGS[0]
                    elif self.selected_flag == "remove":
                        self.map.map_set[grid_tile].objects.clear()
                        self.selected_flag = None
                    if draw_object is not None:
                        self.map.add_object_to_tile(grid_tile, (0, TILE_SIZE[1]/4), draw_object)
                elif self.selected_flag is not None and not self.map.tile_in_map(grid_tile):
                    self.selected_flag = None
                else:
                    self.set_highlight_tile(grid_tile)
                    if self.map.tile_in_map(self.highlight_tile):
                        self.mode = "selected"
                        cursor[0] = self.terrain_button.get_center()
        self.done_button.update()
        self.red_flag_button.update()
        self.orange_flag_button.update()
        self.blue_flag_button.update()
        self.remove_flag_button.update()
        if self.selected_flag == "red":
            draw.rect(buffer_surface, WHITE, self.red_flag_button.get_rect(), 8, 4)
        elif self.selected_flag == "orange":
            draw.rect(buffer_surface, WHITE, self.orange_flag_button.get_rect(), 8, 4)
        elif self.selected_flag == "blue":
            draw.rect(buffer_surface, WHITE, self.blue_flag_button.get_rect(), 8, 4)
        elif self.selected_flag == "remove":
            draw.rect(buffer_surface, WHITE, self.remove_flag_button.get_rect(), 8, 4)
        if self.last_edited is not None:
            edit_offset = self.get_tile_position(self.last_edited)
            edit_offset = edit_offset[0] + TILE_SIZE[0] / 2, edit_offset[1]
            draw_to_buffer([[EDIT_ICON, edit_offset]])
        return cursor

    def convert_position_to_tile(self, position):
        x_tile = int((position[0] - self.map_offset[0]) // TILE_SIZE[0]) + self.map.x_min
        y_tile = int((position[1] - self.map_offset[1]) // TILE_SIZE[1]) + self.map.y_min
        return x_tile, y_tile

    @staticmethod
    def snap_position_to_tile(position):
        # Have to add the offset to the position and then subtract it after the fact
        x_tile_location = int(int(((position[0] + TILE_SIZE[0]/2) // TILE_SIZE[0])) * TILE_SIZE[0] - TILE_SIZE[0] / 2)
        y_tile_location = int(int(((position[1] + TILE_SIZE[1]/2) // TILE_SIZE[1])) * TILE_SIZE[1] - TILE_SIZE[1] / 2)
        return x_tile_location, y_tile_location

    def get_tile_position(self, tile):
        return self.highlight_rect[0] + (tile[0] - self.highlight_tile[0]) * TILE_SIZE[0], self.highlight_rect[1] + (tile[1] - self.highlight_tile[1]) * TILE_SIZE[1]

    def get_highlighted(self):
        return self.highlight_tile

    def redraw_map(self):
        if self.map_sprite.get_width() < self.map.get_tile_width() * TILE_SIZE[0] or self.map_sprite.get_height() < self.map.get_tile_height() * TILE_SIZE[1]:
            self.map_sprite = surface.Surface((self.map.get_tile_width() * TILE_SIZE[0], self.map.get_tile_height() * TILE_SIZE[1]))
        self.map_sprite.fill(BLACK)
        for tile in self.map.map_set:
            self.redraw_tile(tile)
        self.update_map_offset()

    def set_quest(self, quest):
        self.quest = quest

    def set_mode(self, mode):
        self.mode = mode

    def redraw_tile(self, tile):
        self.map_sprite.blit(self.map.map_set[tile].surface, rect.Rect(((tile[0] - self.map.x_min) * TILE_SIZE[0], (tile[1] - self.map.y_min) * TILE_SIZE[1]), TILE_SIZE))
        for object in self.map.map_set[tile].objects:
            new_surface = surface.Surface((16, 16))
            new_surface.set_colorkey(new_surface.get_at((0, 0)))
            if object.id == "FLAGS[0]":
                transform.scale(FLAGS[0].image, (16, 16), new_surface)
                self.map_sprite.blit(new_surface, rect.Rect(((tile[0] - self.map.x_min) * TILE_SIZE[0] + TILE_SIZE[0] / 4, (tile[1] - self.map.y_min) * TILE_SIZE[1] + TILE_SIZE[1] * 3 / 5), TILE_SIZE))
            elif object.id == "FLAGS[1]":
                transform.scale(FLAGS[1].image, (16, 16), new_surface)
                self.map_sprite.blit(new_surface, rect.Rect(((tile[0] - self.map.x_min) * TILE_SIZE[0] + TILE_SIZE[0] * 2 / 3, (tile[1] - self.map.y_min) * TILE_SIZE[1] + TILE_SIZE[1] / 2), TILE_SIZE))
            elif object.id == "FLAGS[2]":
                transform.scale(FLAGS[2].image, (16, 16), new_surface)
                self.map_sprite.blit(new_surface, rect.Rect(((tile[0] - self.map.x_min) * TILE_SIZE[0] + TILE_SIZE[0] / 3, (tile[1] - self.map.y_min) * TILE_SIZE[1] + TILE_SIZE[1] / 3), TILE_SIZE))
        draw.rect(self.map_sprite, BROWN, rect.Rect(((tile[0] - self.map.x_min) * TILE_SIZE[0], (tile[1] - self.map.y_min) * TILE_SIZE[1]), TILE_SIZE), 1)

    def set_highlight_tile(self, tile):
        self.highlight_tile = tile
        self.update_map_offset()

    def update_map_offset(self):
        self.map_offset = (SCREEN_CENTER[0] - ((self.highlight_tile[0] + abs(self.map.x_min)) * TILE_SIZE[0]) - int(TILE_SIZE[0]/2), SCREEN_CENTER[1] - (self.highlight_tile[1] + abs(self.map.y_min)) * TILE_SIZE[1] - int(TILE_SIZE[1]/2))

    def add_tile(self, tile, size, terrain=None, improvement=None, feature=None, animals=None, depleted=False):
        self.map.add_tile(tile, size, terrain, improvement, feature, animals, depleted)
        self.add_buffer_tiles(tile, size)

    def add_buffer_tiles(self, tile, size):
        if self.map.map_set[tile].terrain is not None:
            adjacents = self.map.get_potential_tiles(tile)
            for tile in adjacents:
                if tile not in self.map.map_set:
                    self.map.add_tile(tile, size)

    def update_tile(self, tile, **kwargs):
        terrain, improvements, features, animals, new_surface, depleted = None, None, None, None, None, None
        for key, value in kwargs.items():
            if key == "terrain":
                terrain = value
            elif key == "improvements":
                improvements = value
            elif key == "features":
                features = value
            elif key == "animals":
                animals = value
            elif key == "new_surface":
                new_surface = value
            elif key == "depleted":
                depleted = value
        self.map.update_tile(tile, terrain, improvements, features, animals, new_surface, depleted)
        self.redraw_tile(tile)

    def draw_point_to_point(self, point_a, point_b):
        offset = SCREEN_CENTER[0] - self.highlight_tile[0] * TILE_SIZE[0], SCREEN_CENTER[1] - self.highlight_tile[1] * TILE_SIZE[1]
        draw.circle(buffer_surface, GGREEN, center=(point_a[0]*TILE_SIZE[0]+offset[0], point_a[1]*TILE_SIZE[1]+offset[1]), radius=4)
        if point_a[0] == point_b[0]:
            self.draw_vertical_line(point_a, point_b, offset)
        else:
            self.draw_horizontal_line(point_a, point_b, offset)

    @staticmethod
    def draw_vertical_line(point_a, point_b, offset):
        if point_a[1] < point_b[1]:
            starting_point = point_a[1] * TILE_SIZE[1] + offset[1]
        else:
            starting_point = point_b[1] * TILE_SIZE[1] + offset[1]
        length = abs(point_a[1] - point_b[1]) * TILE_SIZE[1]
        starting_point = (point_a[0] * TILE_SIZE[0] + offset[0] - 2, starting_point)
        draw.rect(buffer_surface, GGREEN, pygame.rect.Rect(starting_point, (4, length)))

    @staticmethod
    def draw_horizontal_line(point_a, point_b, offset):
        if point_a[0] < point_b[0]:
            starting_point = point_a[0] * TILE_SIZE[0] + offset[0]
        else:
            starting_point = point_b[0] * TILE_SIZE[0] + offset[0]
        length = abs(point_a[0] - point_b[0]) * TILE_SIZE[0]
        starting_point = (starting_point, point_a[1] * TILE_SIZE[1] + offset[1] - 2)
        draw.rect(buffer_surface, GGREEN, pygame.rect.Rect(starting_point, (length, 4)))

    @staticmethod
    def calculate_all_tiles_along_path(path):
        tiles_to_add = []
        for tile in path:
            if path.index(tile) + 1 < len(path):
                next_tile = path.index(tile) + 1
                if tile[0] == path[next_tile][0]:
                    if abs(tile[1] - path[next_tile][1]) > 1:
                        if tile[1] > path[next_tile][1]:
                            diff = tile[1] - path[next_tile][1] - 1
                            while diff >= 1:
                                tiles_to_add.append((path.index(tile) + len(tiles_to_add) + 1, (tile[0], diff - path[next_tile][1])))
                                diff -= 1
                        else:
                            diff = path[next_tile][1] - tile[1] - 1
                            while diff >= 1:
                                tiles_to_add.append((path.index(tile) + len(tiles_to_add) + 1, (tile[0], path[next_tile][1] - diff)))
                                diff -= 1
                else:
                    if abs(tile[0] - path[next_tile][0]) > 1:
                        if tile[0] > path[next_tile][0]:
                            diff = tile[0] - path[next_tile][0] - 1
                            while diff >= 0:
                                tiles_to_add.append((path.index(tile) + len(tiles_to_add) + 1, (diff - path[next_tile][0], tile[1])))
                                diff -= 1
                        else:
                            diff = path[next_tile][0] - tile[0] - 1
                            while diff >= 1:
                                tiles_to_add.append((path.index(tile) + len(tiles_to_add) + 1, (path[next_tile][0] - diff, tile[1])))
                                diff -= 1
        return_path = path.copy()
        for tile in tiles_to_add:
            return_path.insert(tile[0], tile[1])
        return return_path

    def load_tile(self, tile, size, terrain=None, improvement=None, feature=None, animals=None, depleted=False, objects=None):
        self.map.load_tile(tile, size, "map", terrain, improvement, feature, animals, depleted, objects)
