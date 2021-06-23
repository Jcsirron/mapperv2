from pygame import font, transform, time, rect, surface
from os import path
from pygame.locals import *

BLACK = (31, 36, 10)
GREY = (146, 126, 106)
BROWN = (104, 76, 60)
WHITE = (239, 216, 161)
BLUE = (60, 159, 156)
DARKBLUE = (24, 63, 57)
GREEN = (57, 87, 28)
GGREEN = (0, 255, 0)
YELLOW = (239, 183, 117)
RED = (239, 58, 12)
FONT = None

game_font = font.match_font('arial')
if game_font is not None:
    FONT = game_font

LOGO_FONT = path.join("Artwork", 'Heehaw.ttf')

TILE_SIZE = (64, 64)

# Initialize the clock to limit the frames per second
CLOCK = time.Clock()


def surface_setup(image, image_size, image_offset=(0, 0), color_key=None, scaling=None):
    return_surface = surface.Surface(image_size)
    return_surface.blit(image, (0, 0), rect.Rect(image_offset, image_size))
    if scaling is not None:
        return_surface = transform.scale(return_surface, (int(image_size[0] * scaling), int(image_size[1] * scaling)))
    if color_key is not None:
        return_surface.set_colorkey(color_key)
    return_surface = return_surface.convert()
    return return_surface



