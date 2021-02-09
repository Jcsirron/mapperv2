from map import *
from globals import *
from camera import *
from quests import *
from player import Player
from screen_handler import SCREEN_SIZE, draw_to_buffer, clear_buffer
from pygame import surface
from textbox import *


class MeatSpace(object):

    def __init__(self):
        self.map = MapObject()
        self.tile_size = (int(SCREEN_SIZE[0] * 1.5), int(SCREEN_SIZE[1] * 1.5))
        self.map.add_tile((0, 0), self.tile_size, "town", "home")
        self.map.set_tile_surface((0, 0), self.tile_size, YELLOW)
        self.generate_home_tile()
        self.map.generate_tile((0, -1), self.tile_size, "mountain")
        self.map.generate_tile((1, -1), self.tile_size, "waterway")
        self.players = [Player()]
        self.camera = Camera(follow_camera, SCREEN_SIZE[0], SCREEN_SIZE[1])
        self.quest_menu = QuestMenu()
        self.map_button = Button("Map", FONT, 24, WHITE, button_color=BLACK)
        self.map_button.update_location((SCREEN_SIZE[0] - 16, 16), "top right")
        self.help_text_location = rect.Rect(16, SCREEN_SIZE[1] - 96, 384, 128)
        self.quest_help_text = surface.Surface((384, 96))
        self.quest_help_text.set_colorkey(self.quest_help_text.get_at((0, 0)))
        draw_text_to_surface(self.quest_help_text, "Left Click to choose quest.", BLACK, font.Font(FONT, 26), False)

    def generate_home_tile(self):
        self.map.add_object_to_tile((0, 0), (self.tile_size[0]/4-48, self.tile_size[1]/4), Decorator(MOVE_INSTRUCTIONS, collidable=False, transparent_background=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] * 3 / 4 - 64, self.tile_size[1] / 4), Decorator(INTERACT_INSTRUCTIONS, collidable=False, transparent_background=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0]/2, self.tile_size[1]/2), QuestBoard())
        self.map.add_object_to_tile((0, 0), (0, 0), Decorator(FENCES[0], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (64, 0), Decorator(FENCES[3], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (128, 0), Decorator(FENCES[6], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (0, 64), Decorator(FENCES[7], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (0, 128), Decorator(FENCES[8], needs_mask=True))

        self.map.add_object_to_tile((0, 0), (self.tile_size[0]-64, 0), Decorator(FENCES[2], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 128, 0), Decorator(FENCES[3], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 192, 0), Decorator(FENCES[4], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 64, 64), Decorator(FENCES[7], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 64, 128), Decorator(FENCES[8], needs_mask=True))

        self.map.add_object_to_tile((0, 0), (0, self.tile_size[1]-64), Decorator(FENCES[4], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (64, self.tile_size[1] - 64), Decorator(FENCES[3], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (128, self.tile_size[1] - 64), Decorator(FENCES[6], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (0, self.tile_size[1] - 128), Decorator(FENCES[7], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (0, self.tile_size[1] - 192), Decorator(FENCES[9], needs_mask=True))

        self.map.add_object_to_tile((0, 0), (self.tile_size[0]-64, self.tile_size[1]-64), Decorator(FENCES[6], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 128, self.tile_size[1] - 64), Decorator(FENCES[3], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 192, self.tile_size[1] - 64), Decorator(FENCES[4], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 64, self.tile_size[1] - 128), Decorator(FENCES[7], needs_mask=True))
        self.map.add_object_to_tile((0, 0), (self.tile_size[0] - 64, self.tile_size[1] - 192), Decorator(FENCES[9], needs_mask=True))

    def update(self, movement, buttons, delta_time):
        clear_buffer()
        tiles_to_add = []
        collide_objects = []
        draw_to_buffer([[FENCES[0], self.camera.rect_apply(rect.Rect((150, 150, 64, 64)))]])
        draw_after_player = []
        for tile in self.map.map_set:
            # TODO: Create sorting where colliders/decor with centers below the player are blitted after the player
            draw_window = self.camera.apply(self.map.map_set[tile])
            # If the tile is on screen.
            if draw_window.colliderect((0, 0), SCREEN_SIZE):
                draw_to_buffer([[self.map.map_set[tile].surface, draw_window, SCREEN_SIZE]])
                for collider in self.map.map_set[tile].objects:
                    if collider.rect.top + collider.rect.y <= self.players[0].rect.top + self.players[0].rect.y:
                        draw_to_buffer([[collider.image, self.camera.apply(collider)]])
                    else:
                        draw_after_player.append(collider)
                    collide_objects.append(collider)
            if draw_window[0] > 0 and (tile[0] - 1, tile[1]) not in self.map.map_set:
                tiles_to_add.append((tile[0] - 1, tile[1]))
            if draw_window[0] - SCREEN_SIZE[0] < - draw_window[2] and (tile[0] + 1, tile[1]) not in self.map.map_set:
                tiles_to_add.append((tile[0] + 1, tile[1]))
            if draw_window[1] > 0 and (tile[0], tile[1] - 1) not in self.map.map_set:
                tiles_to_add.append((tile[0], tile[1] - 1))
            if draw_window[1] - SCREEN_SIZE[1] < - draw_window[3] and (tile[0], tile[1] + 1) not in self.map.map_set:
                tiles_to_add.append((tile[0], tile[1] + 1))
        for add_tile in tiles_to_add:
            self.map.generate_tile(add_tile, self.tile_size)
        for player in self.players:
            for collider in collide_objects:
                collider.update(buttons)
                if type(collider) == QuestBoard and player.interact_rect.colliderect(collider.rect) and not self.quest_menu.active and movement[2] is True:
                    self.quest_menu.active = True
                    movement[2] = False
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
            player.update(movement, buttons, delta_time)
            self.camera.update(player)
            draw_to_buffer([[player.image, self.camera.rect_apply(player.rect)], [player.collide_image, self.camera.rect_apply(player.interact_rect)]])
        for collider in draw_after_player:
            draw_to_buffer([[collider.image, self.camera.apply_old(collider)]])
        if self.quest_menu.active:
            update = self.quest_menu.update(buttons, movement)
            if not self.help_text_location.collidepoint(buttons[1]):
                draw_to_buffer([[self.quest_help_text, self.help_text_location]])
            if update is not None:
                return update
        else:
            draw_to_buffer([[self.map_button.surface, self.map_button.rect]])
            if buttons[0]:
                if self.map_button.rect.collidepoint(buttons[1]):
                    return "map"
