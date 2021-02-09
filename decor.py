from pygame import sprite, rect, surface, mask
from globals import *


# TODO: Add sub-image for collision handling
class Decorator(sprite.Sprite):

    def __init__(self, ext_sprite=None, size=(16, 16), collidable=True, needs_mask=False, mask_layer=None, mask_offset=(0, 0), transparent_background=False):
        sprite.Sprite.__init__(self)
        self.collidable = collidable
        if ext_sprite is not None:
            self.image = ext_sprite
            if transparent_background:
                self.image.set_colorkey(self.image.get_at((self.image.get_width()-1, self.image.get_height()-1)))
        else:
            self.image = surface.Surface(size)
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        if needs_mask:
            if mask_layer is None:
                self.mask = mask.from_surface(self.image, 255)
            else:
                self.mask = mask.from_surface(mask_layer, 255)
            self.mask_offset = mask_offset
        else:
            self.mask = None
            self.mask_offset = mask_offset

    def update(self, mouse):
        pass
