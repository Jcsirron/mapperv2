from camera import *
from map import *
from player import Player
from weather import *
from quests import *
from screen_handler import SCREEN_SIZE, draw_to_buffer, clear_buffer
from textbox import *


class MeatSpace(object):

    def __init__(self, loading=False, player=None):
        self.map = MapObject()
        self.tile_size = (int(SCREEN_SIZE[0] * 1.5), int(SCREEN_SIZE[1] * 1.5))
        self.map.add_tile((0, 0), self.tile_size, "town", "home")
        self.map.set_tile_surface((0, 0), self.tile_size, YELLOW)
        self.time_filter = TimeFilter(TIME_LOOK_UP_TABLE)
        #filter = surface.Surface((150, 150))
        #filter.fill(BLACK)
        #draw.circle(filter, WHITE, (75, 75), 75)
        #self.time_filter.add_light(filter, (SCREEN_CENTER[0]-75, SCREEN_CENTER[1]-75))
        if not loading:
            self.generate_home_tile()
            self.quest_menu = QuestMenu()
            self.players = [Player()]
        else:
            self.quest_menu = QuestMenu(loading)
            self.players = [Player(loading=True)]
        self.camera = Camera(follow_camera, SCREEN_SIZE[0], SCREEN_SIZE[1])

        self.map_button = Button("Map", FONT, 24, WHITE, button_color=BLACK)
        self.map_button.update_location((SCREEN_SIZE[0] - 16, 16), "top right")
        self.help_text_location = rect.Rect(16, SCREEN_SIZE[1] - 96, 384, 128)
        self.quest_help_text = surface.Surface((384, 96))
        self.quest_help_text.set_colorkey(self.quest_help_text.get_at((0, 0)))
        draw_text_to_surface(self.quest_help_text, "Left Click to choose quest.", BLACK, font.Font(FONT, 26), False)

        red_flag = surface.Surface((FLAGS[0].image.get_size()[0] + 12, FLAGS[0].image.get_size()[1] + 12)).convert()
        red_flag.fill(WHITE)
        draw.rect(red_flag, BROWN, red_flag.get_rect(), 4, 2)
        orange_flag = red_flag.copy()
        blue_flag = red_flag.copy()
        red_flag.blit(FLAGS[1].image, (6, 6))
        orange_flag.blit(FLAGS[2].image, (6, 6))
        blue_flag.blit(FLAGS[0].image, (6, 6))
        self.red_flag_button = Button(button_image=red_flag)
        self.red_flag_button.update_location((SCREEN_CENTER[0] - red_flag.get_width() * 1.25, SCREEN_SIZE[1] - red_flag.get_height()), "center")
        self.red_flag_count = surface.Surface((self.red_flag_button.get_rect()[2], self.red_flag_button.get_rect()[3])).convert()
        self.red_flag_count.fill(WHITE)
        self.red_flag_count.set_colorkey(self.red_flag_count.get_at((0, 0)))
        self.red_flag_count_rect = (self.red_flag_button.rect.centerx - 6, self.red_flag_button.rect.centery - 6)
        self.orange_flag_button = Button(button_image=orange_flag)
        self.orange_flag_button.update_location((SCREEN_CENTER[0], SCREEN_SIZE[1] - orange_flag.get_height()), "center")
        self.orange_flag_count = surface.Surface((self.orange_flag_button.get_rect()[2], self.orange_flag_button.get_rect()[3])).convert()
        self.orange_flag_count.fill(WHITE)
        self.orange_flag_count.set_colorkey(self.orange_flag_count.get_at((0, 0)))
        self.orange_flag_count_rect = (self.orange_flag_button.rect[0] + 12, self.orange_flag_button.rect[1] + 16)
        self.blue_flag_button = Button(button_image=blue_flag)
        self.blue_flag_button.update_location((SCREEN_CENTER[0] + blue_flag.get_width() * 1.25, SCREEN_SIZE[1] - blue_flag.get_height()), "center")
        self.blue_flag_count = surface.Surface((self.blue_flag_button.get_rect()[2], self.blue_flag_button.get_rect()[3])).convert()
        self.blue_flag_count.fill(WHITE)
        self.blue_flag_count.set_colorkey(self.blue_flag_count.get_at((0, 0)))
        self.blue_flag_count_rect = (self.blue_flag_button.rect[0] + 12, self.blue_flag_button.rect[1] + 16)
        if not loading:
            self.update_flag_counts()

    def generate_home_tile(self):
        self.map.add_object_to_tile((0, 0), (self.tile_size[0]/4-48, self.tile_size[1]/4), INSTRUCTIONS[0].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] * 3 / 4 - 64, self.tile_size[1] / 4), INSTRUCTIONS[1].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0]/2, self.tile_size[1]/2), INSTRUCTIONS[2].copy())
        self.map.add_object_to_tile((0, 0), (0, 0), FENCES[0].copy())
        self.map.add_object_to_tile((0, 0), (64, 0), FENCES[3].copy())
        self.map.add_object_to_tile((0, 0), (128, 0), FENCES[6].copy())
        self.map.add_object_to_tile((0, 0), (0, 64), FENCES[7].copy())
        self.map.add_object_to_tile((0, 0), (0, 128), FENCES[8].copy())

        self.map.add_object_to_tile((0, 0), (self.tile_size[0]-64, 0), FENCES[2].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 128, 0), FENCES[3].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 192, 0), FENCES[4].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 64, 64), FENCES[7].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 64, 128), FENCES[8].copy())

        self.map.add_object_to_tile((0, 0), (0, self.tile_size[1]-64), FENCES[4].copy())
        self.map.add_object_to_tile((0, 0), (64, self.tile_size[1] - 64), FENCES[3].copy())
        self.map.add_object_to_tile((0, 0), (128, self.tile_size[1] - 64), FENCES[6].copy())
        self.map.add_object_to_tile((0, 0), (0, self.tile_size[1] - 128), FENCES[7].copy())
        self.map.add_object_to_tile((0, 0), (0, self.tile_size[1] - 192), FENCES[9].copy())

        self.map.add_object_to_tile((0, 0), (self.tile_size[0]-64, self.tile_size[1]-64), FENCES[6].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 128, self.tile_size[1] - 64), FENCES[3].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 192, self.tile_size[1] - 64), FENCES[4].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 64, self.tile_size[1] - 128), FENCES[7].copy())
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 64, self.tile_size[1] - 192), FENCES[9].copy())

    def update(self, movement, cursor, buttons, delta_time):
        self.map.trim_tile_set(self.player_to_tile())
        self.map.load_tile_set(self.player_to_tile(), "automap.txt")
        clear_buffer()
        if self.quest_menu.active:
            movement = [0, 0]
        draw_first, draw_after, active_tiles, collide_objects = self.update_tiles()
        player_draw = self.update_players(movement, cursor, buttons, delta_time, collide_objects, active_tiles)
        self.time_filter.update("6:00")
        draw_to_buffer(draw_first + player_draw + draw_after)
        if self.quest_menu.active:
            update = self.quest_menu.update(cursor, buttons)
            if not self.help_text_location.collidepoint(cursor[0]):
                draw_to_buffer([[self.quest_help_text, self.help_text_location]])
            if update is not None:
                return update
            if buttons[1]:
                self.quest_menu.active = False
        else:
            self.handle_inputs(cursor, buttons, collide_objects)

    def update_flag_counts(self):
        # TODO: Change this if multiple players are put in.
        transparency = surface.Surface((24, 24)).convert()
        transparency.set_colorkey(transparency.get_at((0, 0)))
        draw.rect(transparency, YELLOW, (0, 0, 24, 24), 0, 8)
        for flag in self.players[0].flags:
            if flag == "Red":
                self.red_flag_count.fill(self.red_flag_count.get_at((0, 0)))
                self.red_flag_count.blit(transparency, (0, 0))
                draw_text_to_surface(self.red_flag_count, " " + str(self.players[0].flags[flag]) + "x", BLACK, font.Font(FONT, 16), False)
            elif flag == "Orange":
                self.orange_flag_count.fill(self.orange_flag_count.get_at((0, 0)))
                self.orange_flag_count.blit(transparency, (0, 0))
                draw_text_to_surface(self.orange_flag_count, " " + str(self.players[0].flags[flag]) + "x", BLACK, font.Font(FONT, 16), False)
            elif flag == "Blue":
                self.blue_flag_count.fill(self.blue_flag_count.get_at((0, 0)))
                self.blue_flag_count.blit(transparency, (0, 0))
                draw_text_to_surface(self.blue_flag_count, " " + str(self.players[0].flags[flag]) + "x", BLACK, font.Font(FONT, 16), False)

    def update_tiles(self):
        tiles_to_add = []
        active_tiles = []
        draw_before_player = []
        draw_after_player = []
        collide_objects = []
        for tile in self.map.map_set:
            draw_window = self.camera.apply(self.map.map_set[tile])
            # If the tile is on screen.
            if draw_window.colliderect((0, 0), SCREEN_SIZE):
                draw_before_player.append((self.map.map_set[tile].surface, draw_window, SCREEN_SIZE))
                active_tiles.append(tile)
                for collider in self.map.map_set[tile].objects:
                    if (collider.draw_height == 0 and collider.rect.top + collider.mask_offset[1] <= self.players[0].collide_rect.center[1]) or collider.draw_height == -1:
                        draw_before_player.append((collider.image, self.camera.apply(collider)))
                    else:
                        draw_after_player.append((collider.image, self.camera.apply(collider)))
                    collide_objects.append(collider)
            if draw_window[0] > 0 and (tile[0] - 1, tile[1]) not in self.map.map_set and (tile[0] - 1, tile[1]) not in self.map.stored_tiles:
                tiles_to_add.append((tile[0] - 1, tile[1]))
            if draw_window[0] - SCREEN_SIZE[0] < - draw_window[2] and (tile[0] + 1, tile[1]) not in self.map.map_set and (tile[0] + 1, tile[1]) not in self.map.stored_tiles:
                tiles_to_add.append((tile[0] + 1, tile[1]))
            if draw_window[1] > 0 and (tile[0], tile[1] - 1) not in self.map.map_set and (tile[0], tile[1] - 1) not in self.map.stored_tiles:
                tiles_to_add.append((tile[0], tile[1] - 1))
            if draw_window[1] - SCREEN_SIZE[1] < - draw_window[3] and (tile[0], tile[1] + 1) not in self.map.map_set and (tile[0], tile[1] + 1) not in self.map.stored_tiles:
                tiles_to_add.append((tile[0], tile[1] + 1))
        for add_tile in tiles_to_add:
            self.map.generate_tile(add_tile, self.tile_size)
        return draw_before_player, draw_after_player, active_tiles, collide_objects

    def update_players(self, movement, cursor, buttons, delta_time, collide_objects, active_tiles):
        for player in self.players:
            colliders_to_remove = []
            for collider in collide_objects:
                collider.update(buttons)
                if collider.id == "FLAGS[0]" and player.interact_rect.colliderect(collider.rect) and buttons[0] is True:
                    player.flags["Blue"] += 1
                    self.update_flag_counts()
                    colliders_to_remove.append(collider)
                if collider.id == "FLAGS[1]" and player.interact_rect.colliderect(collider.rect) and buttons[0] is True:
                    player.flags["Red"] += 1
                    self.update_flag_counts()
                    colliders_to_remove.append(collider)
                if collider.id == "FLAGS[2]" and player.interact_rect.colliderect(collider.rect) and buttons[0] is True:
                    player.flags["Orange"] += 1
                    self.update_flag_counts()
                    colliders_to_remove.append(collider)
                if collider.id == "QUESTBOARD" and player.interact_rect.colliderect(collider.rect) and not self.quest_menu.active and buttons[0] is True:
                    self.quest_menu.active = True
                    buttons[1] = False
                    cursor[1] = False
                if collider.collidable is True and player.collide_rect.move(movement[0]*int(player.movement_speed * delta_time), 0).colliderect(collider.rect):
                    if collider.mask is not None:
                        offset = (player.collide_rect.left + (movement[0] * int(player.movement_speed * delta_time)) - (collider.rect.left + collider.mask_offset[0]), player.collide_rect.top - (collider.rect.top + collider.mask_offset[1]))
                        if collider.mask.overlap(player.mask, offset) is not None:
                            player.change_facing(movement.copy())
                            movement[0] = 0
                    else:
                        player.change_facing(movement.copy())
                        movement[0] = 0
                if collider.collidable is True and player.collide_rect.move(0, movement[1]*int(player.movement_speed * delta_time)).colliderect(collider.rect):
                    if collider.mask is not None:
                        offset = (player.collide_rect.left - (collider.rect.left + collider.mask_offset[0]), player.collide_rect.top + (movement[1]*int(player.movement_speed * delta_time)) - (collider.rect.top + collider.mask_offset[1]))
                        if collider.mask.overlap(player.mask, offset) is not None:
                            player.change_facing(movement.copy())
                            movement[1] = 0
                    else:
                        player.change_facing(movement.copy())
                        movement[1] = 0

            for collider in colliders_to_remove:
                for tile in active_tiles:
                    if collider in self.map.map_set[tile].objects:
                        self.map.map_set[tile].objects.remove(collider)

            player.update(movement, buttons, delta_time)
            self.camera.update(player)
            # TODO: Break this function up better to allow for multiple players to be returned (Client side stuff?)
            return [(player.collide_image, self.camera.rect_apply(player.interact_rect)), (player.image, self.camera.rect_apply(player.rect))]

    def handle_inputs(self, cursor, buttons, collide_objects):
        draw_to_buffer(
            [[self.map_button.surface, self.map_button.rect], [self.red_flag_button.surface, self.red_flag_button.rect],
             [self.red_flag_count, self.red_flag_count_rect],
             [self.orange_flag_button.surface, self.orange_flag_button.rect],
             [self.orange_flag_count, self.orange_flag_count_rect],
             [self.blue_flag_button.surface, self.blue_flag_button.rect],
             [self.blue_flag_count, self.blue_flag_count_rect]])
        if cursor[1]:
            if self.map_button.rect.collidepoint(cursor[0]):
                return "map"
            if self.red_flag_button.rect.collidepoint(cursor[0]) and self.players[0].flags["Red"] > 0:
                add = True
                for collider in collide_objects:
                    if self.players[0].interact_rect.colliderect(collider.rect):
                        add = False
                if add:
                    self.players[0].flags["Red"] -= 1
                    self.map.add_object_to_tile(self.player_to_tile(),
                                                self.player_without_offset(self.player_to_tile()), FLAGS[1].copy())
                    self.update_flag_counts()
            if self.orange_flag_button.rect.collidepoint(cursor[0]) and self.players[0].flags["Orange"] > 0:
                add = True
                for collider in collide_objects:
                    if self.players[0].interact_rect.colliderect(collider.rect):
                        add = False
                if add:
                    self.players[0].flags["Orange"] -= 1
                    self.map.add_object_to_tile(self.player_to_tile(),
                                                self.player_without_offset(self.player_to_tile()), FLAGS[2].copy())
                    self.update_flag_counts()
            if self.blue_flag_button.rect.collidepoint(cursor[0]) and self.players[0].flags["Blue"] > 0:
                add = True
                for collider in collide_objects:
                    if self.players[0].interact_rect.colliderect(collider.rect):
                        add = False
                if add:
                    self.players[0].flags["Blue"] -= 1
                    self.map.add_object_to_tile(self.player_to_tile(),
                                                self.player_without_offset(self.player_to_tile()), FLAGS[0].copy())
                    self.update_flag_counts()
        if buttons[3]:
            # Draw the player count above the player
            number_count = font.Font(FONT, 36)
            if self.players[0].step_count == -1:
                number_count = number_count.render("?", True, BLACK)
            else:
                number_count = number_count.render(str(self.players[0].step_count), True, BROWN)
            draw_location = self.camera.rect_apply(
                rect.Rect(self.players[0].rect.left + (self.players[0].rect.width - number_count.get_width()) / 2,
                          self.players[0].rect.top - number_count.get_height() - 4, number_count.get_width(),
                          number_count.get_height()))
            background_rect = surface.Surface((number_count.get_width() + 16, number_count.get_height() + 8))
            background_rect.fill(YELLOW)
            background_rect.set_colorkey(YELLOW)
            draw.rect(background_rect, WHITE, ((4, 4), (number_count.get_width() + 8, number_count.get_height())),
                      border_radius=8)
            draw.rect(background_rect, BROWN, ((4, 4), (number_count.get_width() + 8, number_count.get_height())), 2,
                      border_radius=8)
            draw_to_buffer([[background_rect, (draw_location[0] - 8, draw_location[1] - 4)],
                            [number_count, (draw_location[0], draw_location[1])]])

    def player_to_tile(self):
        location = (int(self.players[0].collide_rect[0] // self.tile_size[0]), int(self.players[0].collide_rect[1] // self.tile_size[1]))
        return location

    def player_without_offset(self, tile):
        location = (int(self.players[0].interact_rect[0] - self.tile_size[0] * tile[0]), int(self.players[0].interact_rect[1] - self.tile_size[1] * tile[1]))
        return location

    def load_tile(self, tile, size, terrain=None, improvement=None, feature=None, animals=None, depleted=False, objects=None):
        self.map.load_tile(tile, size, "meat", terrain, improvement, feature, animals, depleted, objects)

    def export_quest_menu(self):
        return self.quest_menu.export_quest_board()
