from pygame import sprite, rect, surface, mask
from globals import *


class Decorator(object):

    def __init__(self, decor_sprite=None, size=(16, 16), collidable=True, **kwargs):
        needs_mask = False
        mask_layer = None
        mask_offset = (0, 0)
        transparent_background = False
        draw_above = False
        draw_below = False
        self.id = None
        if "kwargs" in kwargs:
            self.kwargs = kwargs['kwargs']
        else:
            self.kwargs = kwargs
        for key, item in self.kwargs.items():
            if key == "needs_mask":
                needs_mask = item
            elif key == "mask_layer":
                mask_layer = item
            elif key == "mask_offset":
                mask_offset = item
            elif key == "transparent_background":
                transparent_background = item
            elif key == "draw_above":
                draw_above = item
            elif key == "draw_below":
                draw_below = item
            elif key == "decor_id":
                self.id = item
        self.collidable = collidable
        if decor_sprite is not None:
            self.image = decor_sprite
            size = self.image.get_size()
            if transparent_background:
                self.image.set_colorkey(self.image.get_at((self.image.get_width()-1, self.image.get_height()-1)))
        else:
            self.image = surface.Surface(size)
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        if needs_mask:
            if mask_layer is None:
                if mask_offset != (0, 0):
                    mask_surface = surface.Surface((size[0]-mask_offset[0], size[1]-mask_offset[1]))
                    mask_surface.set_colorkey(self.image.get_at((0, 0)))
                    mask_surface.blit(self.image, (-mask_offset[0], -mask_offset[1]))
                    self.mask = mask.from_surface(mask_surface, 255)
                else:
                    self.mask = mask.from_surface(self.image, 255)
            else:
                self.mask = mask.from_surface(mask_layer, 255)
            self.mask_offset = mask_offset
        else:
            self.mask = None
            self.mask_offset = mask_offset
        if draw_above:
            self.draw_height = 1
        elif draw_below:
            self.draw_height = -1
        else:
            self.draw_height = 0

    def update(self, mouse):
        pass

    def copy(self):
        return Decorator(decor_sprite=self.image, size=self.rect.size, collidable=self.collidable, kwargs=self.kwargs)

    def get_export_values(self, tile_offset):
        return self.id, (self.rect.left - tile_offset[0], self.rect.top - tile_offset[1])
