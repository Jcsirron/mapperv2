from map import MapObject, TERRAIN, IMPROVEMENTS, FEATURES, ANIMALS
from pygame import rect
from globals import *
from screen_handler import *
from button import *
from map_space_assets import map_forest_tile, map_mountain_tile, map_waterway_tile, map_plain_tile, map_home_tile
from textbox import *


# noinspection PyAttributeOutsideInit,PyGlobalUndefined
class MapSpace(object):

    def __init__(self):
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
        self.map_sprite = surface.Surface(TILE_SIZE)
        self.add_tile((0, 0), TILE_SIZE, "town", "home")
        self.set_highlight_tile((0, 0))
        self.help_text_location = rect.Rect(16, SCREEN_SIZE[1] - 96, 384, 128)
        self.charting_mode_help_text = surface.Surface((384, 96))
        self.charting_mode_help_text.fill(BLACK)
        draw_text_to_surface(self.charting_mode_help_text, "Left Click to choose tile.  Right Click to create tile.", WHITE, font.Font(FONT, 26), False)

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

    def update(self, mouse, world_map=None):
        global FILL_COLOR
        if FILL_COLOR != BLACK:
            set_fill_color(BLACK)
        clear_buffer()
        self.redraw_map()
        draw_to_buffer([[self.map_sprite, self.map_offset]])
        if self.mode == "selected":
            self.selected_mode(mouse)
        elif self.mode == "path":
            self.path_mode(mouse, world_map)
        else:
            self.charting_mode(mouse)

    def selected_mode(self, mouse):
        if not self.help_text_location.collidepoint(mouse[1]):
            draw_to_buffer([[self.selected_menu_help_text, self.help_text_location]])
        active_tile = self.map.get_tile(self.highlight_tile)
        if active_tile.terrain == "forest":
            draw_to_buffer([[map_forest_tile, self.selected_rect]])
        elif active_tile.terrain == "waterway":
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
        draw.rect(buffer_surface, BROWN, self.selected_rect, 4)

        if self.selected_submenu is None:
            self.terrain_button.update()
            self.improvement_button.update()
            self.feature_button.update()
            self.animal_button.update()
            self.clear_button.update()
            self.depleted_button.update()
            if mouse[0]:
                if self.terrain_button.get_rect().collidepoint(mouse[1]):
                    self.selected_submenu = "terrain"
                elif self.improvement_button.get_rect().collidepoint(mouse[1]):
                    self.selected_submenu = "improvement"
                elif self.feature_button.get_rect().collidepoint(mouse[1]):
                    self.selected_submenu = "feature"
                elif self.animal_button.get_rect().collidepoint(mouse[1]):
                    self.selected_submenu = "animal"
                elif self.clear_button.get_rect().collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, terrain="clear", improvements="clear", features="clear", animals="clear")
                    else:
                        # TODO: Put in an error notification here
                        pass
                elif self.depleted_button.get_rect().collidepoint(mouse[1]):
                    self.update_tile(self.highlight_tile, depleted=not self.map.map_set[self.highlight_tile].depleted)
                elif not self.selected_rect.collidepoint(mouse[1]):
                    self.mode = None

        elif self.selected_submenu == "terrain":
            draw_to_buffer([[self.terrain_button.surface, (self.selected_rect.right + 4, self.selected_rect.top)]])
            self.clear_button.update()
            for button in self.terrain_sub_buttons:
                button.update()
                if mouse[0] and button.rect.collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, button.call_function)
                    else:
                        # TODO: Put in an error notification here
                        pass
            if mouse[0]:
                if self.clear_button.rect.collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, terrain="clear")
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
                if mouse[0] and button.rect.collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, improvements=button.call_function)
                    else:
                        # TODO: Put in an error notification here
                        pass
            if mouse[0]:
                if self.clear_button.rect.collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, improvements="clear")
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
                if mouse[0] and button.rect.collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, features=button.call_function)
                    else:
                        # TODO: Put in an error notification here
                        pass
            if mouse[0]:
                if self.clear_button.rect.collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, features="clear")
                    else:
                        # TODO: Put in an error notification here
                        pass
                self.selected_submenu = None

        elif self.selected_submenu == "animal":
            draw_to_buffer([[self.animal_button.surface, (self.selected_rect.right + 4, self.selected_rect.top)]])
            self.clear_button.update()
            for button in self.animal_sub_buttons:
                button.update()
                if mouse[0] and button.rect.collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, animals=button.call_function)
                    else:
                        # TODO: Put in an error notification here
                        pass
            if mouse[0]:
                if self.clear_button.rect.collidepoint(mouse[1]):
                    if self.highlight_tile != (0, 0):
                        self.update_tile(self.highlight_tile, animals="clear")
                    else:
                        # TODO: Put in an error notification here
                        pass
                self.selected_submenu = None

    def path_mode(self, mouse, world_map=None):
        if not self.help_text_location.collidepoint(mouse[1]):
            draw_to_buffer([[self.path_mode_help_text, self.help_text_location]])
        if (0, 0) not in self.path:
            self.path.insert(0, (0, 0))
        if mouse[0] == 1:
            if self.cancel_button.rect.collidepoint(mouse[1]):
                self.mode = None
                self.active = False
                self.set_quest(None)
                self.path = []
            elif self.done_button.rect.collidepoint(mouse[1]):
                self.mode = None
                self.active = False
                self.quest.check_quest(self.path, world_map, self.map)
                self.set_quest(None)
                self.path = []
            elif self.convert_position_to_tile(mouse[1]) == self.path[-1]:
                # If it matches the last path in the list, remove it.
                self.path.remove(self.convert_position_to_tile(mouse[1]))
            elif self.convert_position_to_tile(mouse[1]) not in self.path:
                new_location = self.convert_position_to_tile(mouse[1])
                if new_location[0] != self.path[-1][0] and new_location[1] != self.path[-1][1]:
                    if abs(self.path[-1][0] - new_location[0]) > abs(self.path[-1][1] - new_location[1]):
                        self.path.append((self.path[-1][0], new_location[1]))
                    else:
                        self.path.append((new_location[0], self.path[-1][1]))
                self.path.append(self.convert_position_to_tile(mouse[1]))
        elif mouse[0] == 3:
            self.set_highlight_tile(self.convert_position_to_tile(mouse[1]))
        for path in self.path:
            if self.path.index(path) + 1 < len(self.path):
                # Draw from current to next
                self.draw_point_to_point(path, self.path[self.path.index(path) + 1])
            else:
                # Draw the circle at the center of the tile
                offset = SCREEN_CENTER[0] - self.highlight_tile[0] * TILE_SIZE[0], SCREEN_CENTER[1] - self.highlight_tile[1] * TILE_SIZE[1]
                draw.circle(buffer_surface, GGREEN, center=(path[0] * TILE_SIZE[0] + offset[0], path[1] * TILE_SIZE[1] + offset[1]), radius=4)
        if self.quest is not None:
            draw_to_buffer([[self.quest.surface, (SCREEN_SIZE[0]/2 - self.quest.rect[2]/2, 8)]])
        draw_to_buffer([[self.cancel_button.surface, self.cancel_button.get_rect()], [self.done_button.surface, self.done_button.get_rect()]])

    def charting_mode(self, mouse):
        if not self.help_text_location.collidepoint(mouse[1]):
            draw_to_buffer([[self.charting_mode_help_text, self.help_text_location]])
        grid_tile = self.snap_position_to_tile(mouse[1])
        draw.rect(buffer_surface, WHITE, (grid_tile, TILE_SIZE), 4)
        # Center testing lines
        draw.rect(buffer_surface, WHITE, self.highlight_rect, 4)
        if mouse[0] == 1:
            if self.done_button.rect.collidepoint(mouse[1]):
                self.active = False
            else:
                grid_tile = self.convert_position_to_tile(mouse[1])
                self.set_highlight_tile(grid_tile)
                if self.map.tile_in_map(self.highlight_tile):
                    self.mode = "selected"
        if mouse[0] == 3:
            grid_tile = self.convert_position_to_tile(mouse[1])
            if not self.map.tile_in_map(grid_tile):
                self.add_tile(grid_tile, TILE_SIZE)
        draw_to_buffer([[self.done_button.surface, self.done_button.rect]])

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
        draw.rect(self.map_sprite, BROWN, rect.Rect(((tile[0] - self.map.x_min) * TILE_SIZE[0], (tile[1] - self.map.y_min) * TILE_SIZE[1]), TILE_SIZE), 1)

    def set_highlight_tile(self, tile):
        self.highlight_tile = tile
        self.update_map_offset()

    def update_map_offset(self):
        self.map_offset = (SCREEN_CENTER[0] - ((self.highlight_tile[0] + abs(self.map.x_min)) * TILE_SIZE[0]) - int(TILE_SIZE[0]/2), SCREEN_CENTER[1] - (self.highlight_tile[1] + abs(self.map.y_min)) * TILE_SIZE[1] - int(TILE_SIZE[1]/2))

    def add_tile(self, tile, size, terrain=None, improvement=None, feature=None, animals=None):
        self.map.add_tile(tile, size, terrain, improvement, feature, animals)

    def update_tile(self, tile, terrain=None, improvements=None, features=None, animals=None,  new_surface=None, depleted=None):
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
