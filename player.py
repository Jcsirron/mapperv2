from pygame import sprite, surface, rect, draw, mask
from random import randint
from meat_space_assets import PLAYER_FRAMES
from screen_handler import SCREEN_CENTER
from globals import *


# noinspection PyAttributeOutsideInit
class Player(sprite.Sprite):

    def __init__(self, loading=False):
        sprite.Sprite.__init__(self)
        self.image = surface.Surface((32, 64))
        self.image.fill(BLACK)
        self.ani_frame = 0
        self.ani_timer = 0
        self.ani_fps = 100
        self.facing_direction = (0, 1)
        self.step_count = 0
        self.max_steps = 10
        self.stepped = 0
        if not loading:
            self.flags = {"Red": 9, "Orange": 9, "Blue": 9}
            self.primary_slot = None
            self.secondary_slot = None
            self.image.fill(BLACK)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(SCREEN_CENTER[0] * 1.5, SCREEN_CENTER[1])
            self.movement_speed = 300
            self.set_up_player()

    def load_player(self, **kwargs):
        self.rect, self.movement_speed, self.flags, self.primary_slot, self.secondary_slot = None, None, None, None, None
        for key, value in kwargs.items():
            if key == "rect":
                self.rect = value
            elif key == "movement speed":
                self.movement_speed = value
            elif key == "flags":
                self.flags = value
            elif key == "primary slot":
                self.primary_slot = value
            elif key == "secondary slot":
                self.secondary_slot = value
        self.set_up_player()

    def set_up_player(self):
        self.collide_image = surface.Surface((self.rect.width, self.rect.width))
        self.collide_image.set_colorkey(self.collide_image.get_at((0, 0)))
        draw.rect(self.collide_image, WHITE, self.collide_image.get_rect(), 4, 4)

        self.collision_image = surface.Surface((self.rect.width, self.rect.width))
        self.collision_image.set_colorkey(self.collision_image.get_at((0, 0)))
        draw.circle(self.collision_image, BLACK,
                    (self.collision_image.get_width() / 2, self.collision_image.get_height() / 2), 16)
        self.mask = mask.from_surface(self.collision_image)

        self.collide_rect = rect.Rect(self.rect.left, self.rect.top + self.rect.width, self.rect.width, self.rect.width)
        self.facing_direction = (0, 1)
        self.interact_rect = self.collide_rect.move(0, self.collide_rect.height)

    def update(self, movement, buttons, delta_time):
        if movement[0] != 0 or movement[1] != 0:
            self.change_facing(movement)
            if movement[0] == 0 or movement[1] == 0:
                self.rect = self.rect.move(movement[0] * int(self.movement_speed * delta_time), movement[1] * int(self.movement_speed * delta_time))
            else:
                self.rect = self.rect.move(movement[0] * int(0.71 * self.movement_speed * delta_time), movement[1] * int(0.71 * self.movement_speed * delta_time))
            self.animate_character(delta_time)
            self.collide_rect.bottomleft = self.rect.bottomleft
        else:
            self.ani_timer = 0
            self.ani_frame = 0
            self.animate_character(delta_time)
        if buttons[3]:
            if (self.ani_frame == 0 or self.ani_frame == 4) and (movement[0] != 0 or movement[1] != 0):
                if self.ani_frame != self.stepped and self.step_count != -1:
                    if self.step_count < self.max_steps:
                        self.step_count += 1
                    elif self.step_count > 2 * self.max_steps:
                        self.step_count = -1
                    else:
                        self.step_count += randint(0, int(self.max_steps / 4))
                    self.stepped = self.ani_frame
        else:
            self.step_count = 0
        self.interact_rect.update(self.collide_rect.x + self.collide_rect.width * self.facing_direction[0], self.collide_rect.y + self.collide_rect.height * self.facing_direction[1], self.interact_rect.width, self.interact_rect.height)

    def change_facing(self, movement):
        self.facing_direction = movement

    def animate_character(self, delta_time):
        self.ani_timer += delta_time
        while self.ani_timer > 1:
            self.ani_timer -= 1
        self.ani_frame = int(self.ani_timer * 8)
        if self.facing_direction[0] == 1:
            self.image = PLAYER_FRAMES["PLAYER_RIGHT[" + str(self.ani_frame) + "]"]
        elif self.facing_direction[0] == -1:
            self.image = PLAYER_FRAMES["PLAYER_LEFT[" + str(self.ani_frame) + "]"]
        elif self.facing_direction[1] == -1:
            self.image = PLAYER_FRAMES["PLAYER_UP[" + str(self.ani_frame) + "]"]
        elif self.facing_direction[1] == 1:
            self.image = PLAYER_FRAMES["PLAYER_DOWN[" + str(self.ani_frame) + "]"]

    def export_player(self):
        return {"rect": self.rect, "movement speed": self.movement_speed, "flags": self.flags, "primary slot": self.primary_slot, "secondary slot": self.secondary_slot}
