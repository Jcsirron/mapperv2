from pygame import sprite, surface, rect, draw, mask
from screen_handler import SCREEN_CENTER
from globals import *


class Player(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = surface.Surface((32, 64))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(SCREEN_CENTER[0] * 1.5, SCREEN_CENTER[1])
        self.collide_image = surface.Surface((32, 32))
        self.collide_image.set_colorkey(self.collide_image.get_at((0, 0)))
        draw.rect(self.collide_image, WHITE, self.collide_image.get_rect(), 4, 4)

        self.collision_image = surface.Surface((32, 32))
        self.collision_image.set_colorkey(self.collision_image.get_at((0, 0)))
        draw.circle(self.collision_image, BLACK, (self.collision_image.get_width()/2, self.collision_image.get_height()/2), 16)
        self.mask = mask.from_surface(self.collision_image)

        self.collide_rect = rect.Rect(self.rect.left, self.rect.top+32, self.rect.width, self.rect.width)
        self.movement_speed = 200
        self.facing_direction = (0, 1)
        self.interact_rect = self.collide_rect.move(0, self.collide_rect.height)

    # TODO: Create the player animation
    def update(self, movement, buttons, delta_time):
        if movement[0] != 0 or movement[1] != 0:
            self.change_facing(movement)
            self.rect = self.rect.move(movement[0] * int(self.movement_speed * delta_time), movement[1] * int(self.movement_speed * delta_time))
            self.collide_rect.bottomleft = self.rect.bottomleft
        self.interact_rect.update(self.collide_rect.x + self.collide_rect.width * self.facing_direction[0], self.collide_rect.y + self.collide_rect.height * self.facing_direction[1], self.interact_rect.width, self.interact_rect.height)

    def change_facing(self, movement):
        self.facing_direction = movement
