#!/usr/bin/env python
from pygame import image, transform
from globals import *
from decor import Decorator
from screen_handler import SCREEN_SIZE
from os import path

FENCES_SHEET = image.load(path.join('Artwork', "Fences.png")).convert()
TREES_SHEET = image.load(path.join("Artwork", "Trees.png")).convert()
ROCKS_SHEET = image.load(path.join("Artwork", "Rocks.png")).convert()
GRASS_SHEET = image.load(path.join("Artwork", "Grass.png")).convert()
WATER_SHEET = image.load(path.join("Artwork", "Water tiles.png")).convert()
MOUNTAIN_SHEET = image.load(path.join("Artwork", "Mountain tiles.png")).convert()
QUEST_BOARD = image.load(path.join("Artwork", "Quest Board.png")).convert()
FLAGS_SHEET = image.load(path.join("Artwork", "Flags.png")).convert()
PLAYER_DOWN_SHEET = image.load(path.join("Artwork", "Player Down.png")).convert()
PLAYER_DOWN_SHEET.set_colorkey(PLAYER_DOWN_SHEET.get_at((0, 0)))
PLAYER_UP_SHEET = image.load(path.join("Artwork", "Player Up.png")).convert()
PLAYER_UP_SHEET.set_colorkey(PLAYER_UP_SHEET.get_at((0, 0)))
PLAYER_RIGHT_SHEET = image.load(path.join("Artwork", "Player Right.png")).convert()
PLAYER_RIGHT_SHEET.set_colorkey(PLAYER_RIGHT_SHEET.get_at((0, 0)))
PLAYER_LEFT_SHEET = image.load(path.join("Artwork", "Player Left.png")).convert()
PLAYER_LEFT_SHEET.set_colorkey(PLAYER_LEFT_SHEET.get_at((0, 0)))

MOVE_INSTRUCTIONS = image.load(path.join("Artwork", "Move instructions.png")).convert()
INTERACT_INSTRUCTIONS = image.load(path.join("Artwork", "Interact instructions.png")).convert()

TILE_SLOTS = [(0, 0), (128, 0), (256, 0), (384, 0), (512, 0), (640, 0), (768, 0), (896, 0), (1024, 0), (1152, 0), (1280, 0), (1408, 0),
              (0, 128), (128, 128), (256, 128), (384, 128), (512, 128), (640, 128), (768, 128), (896, 128), (1024, 128), (1152, 128), (1280, 128), (1408, 128),
              (0, 256), (128, 256), (256, 256), (384, 256), (512, 256), (640, 256), (768, 256), (896, 256), (1024, 256), (1152, 256), (1280, 256), (1408, 256),
              (0, 384), (128, 384), (256, 384), (384, 384), (512, 384), (640, 384), (768, 384), (896, 384), (1024, 384), (1152, 384), (1280, 384), (1408, 384),
              (0, 512), (128, 512), (256, 512), (384, 512), (512, 512), (640, 512), (768, 512), (896, 512), (1024, 512), (1152, 512), (1280, 512), (1408, 512),
              (0, 640), (128, 640), (256, 640), (384, 640), (512, 640), (640, 640), (768, 640), (896, 640), (1024, 640), (1152, 640), (1280, 640), (1408, 640),
              (0, 768), (128, 768), (256, 768), (384, 768), (512, 768), (640, 768), (768, 768), (896, 768), (1024, 768), (1152, 768), (1280, 768), (1408, 768),
              (0, 896), (128, 896), (256, 896), (384, 896), (512, 896), (640, 896), (768, 896), (896, 896), (1024, 896), (1152, 896), (1280, 896), (1408, 896),
              (0, 1024), (128, 1024), (256, 1024), (384, 1024), (512, 1024), (640, 1024), (768, 1024), (896, 1024), (1024, 1024), (1152, 1024), (1280, 1024), (1408, 1024)]

# THIS IS THE DYNAMIC TILE SLOT BUILDER.  DO NOT DELETE.
#x, y = 0, 0
#while y <= SCREEN_SIZE[1] * 1.5 - 128:
#    while x <= SCREEN_SIZE[0] * 1.5 - 128:
#        TILE_SLOTS.append((x, y))
#        x += 128
#    x = 0
#    y += 128

FENCES = {0: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (0, 0), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[0]"),
          1: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (32, 0), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[1]"),
          2: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (64, 0), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[2]"),
          3: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (96, 0), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[3]"),
          4: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (0, 32), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[4]"),
          5: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (32, 32), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[5]"),
          6: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (64, 32), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[6]"),
          7: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (96, 32), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[7]"),
          8: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (0, 64), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[8]"),
          9: Decorator(transform.scale(surface_setup(FENCES_SHEET, (32, 32), (32, 64), FENCES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="FENCES[9]")}

TREES = {0: Decorator(transform.scale(surface_setup(TREES_SHEET, (32, 64), (0, 0), TREES_SHEET.get_at((0, 0))), (64, 128)), needs_mask=True, decor_id="TREES[0]", mask_offset=(0, 96)),      # Tall Pine Tree
         1: Decorator(transform.scale(surface_setup(TREES_SHEET, (32, 32), (32, 0), TREES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="TREES[1]", mask_offset=(0, 32)),
         2: Decorator(transform.scale(surface_setup(TREES_SHEET, (64, 64), (64, 0), TREES_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="TREES[2]", mask_offset=(0, 96)),
         3: Decorator(transform.scale(surface_setup(TREES_SHEET, (32, 32), (32, 32), TREES_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="TREES[3]", mask_offset=(0, 32)),
         4: Decorator(transform.scale(surface_setup(TREES_SHEET, (32, 64), (0, 64), TREES_SHEET.get_at((0, 0))), (64, 128)), needs_mask=True, decor_id="TREES[4]", mask_offset=(0, 96))}

ROCKS = {0: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (0, 0), ROCKS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="ROCKS[0]"),
         1: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (16, 0), ROCKS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="ROCKS[1]"),
         2: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (32, 32), (32, 0), ROCKS_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="ROCKS[2]"),
         3: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (0, 16), ROCKS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="ROCKS[3]"),
         4: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (16, 16), ROCKS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="ROCKS[4]"),
         5: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (0, 32), ROCKS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="ROCKS[5]"),
         6: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (16, 32), ROCKS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="ROCKS[6]"),
         7: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (0, 48), ROCKS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="ROCKS[7]"),
         8: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (16, 48), ROCKS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="ROCKS[8]"),
         9: Decorator(transform.scale(surface_setup(ROCKS_SHEET, (32, 32), (32, 32), ROCKS_SHEET.get_at((0, 0))), (64, 64)), needs_mask=True, decor_id="ROCKS[9]")}

GRASS = {0: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (0, 0), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[0]"),
         1: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (8, 0), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[1]"),
         2: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (16, 0), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[2]"),
         3: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (24, 0), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[3]"),
         4: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (0, 8), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[4]"),
         5: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (8, 8), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[5]"),
         6: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (16, 8), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[6]"),
         7: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (24, 8), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[7]"),
         8: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (0, 16), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[8]"),
         9: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (8, 16), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[9]"),
         10: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (16, 16), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[10]"),
         11: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (24, 16), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[11]"),
         12: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (0, 24), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[12]"),
         13: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (8, 24), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[13]"),
         14: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (16, 24), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[14]"),
         15: Decorator(transform.scale(surface_setup(GRASS_SHEET, (8, 8), (24, 24), GRASS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="GRASS[15]")}

WATER = {0: Decorator(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), needs_mask=True, decor_id="WATER[0]"),                            # 0  Edge at top
         1: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), needs_mask=True, decor_id="WATER[1]"),      # 1  Edge at left
         2: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 180), needs_mask=True, decor_id="WATER[2]"),     # 2  Edge at bottom
         3: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 270), needs_mask=True, decor_id="WATER[3]"),     # 3  Edge at right
         4: Decorator(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), needs_mask=True, decor_id="WATER[4]"),                           # 4  Horizontal line
         5: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), needs_mask=True, decor_id="WATER[5]"),     # 5  Vertical line
         6: Decorator(transform.scale(surface_setup(WATER_SHEET, (32, 32), (64, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), needs_mask=True, decor_id="WATER[6]"),                           # 6  Left Top corner
         7: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (64, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), needs_mask=True, decor_id="WATER[7]"),     # 7  Left Bottom corner
         8: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (64, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 180), needs_mask=True, decor_id="WATER[8]"),    # 8  Right Bottom corner
         9: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (64, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 270), needs_mask=True, decor_id="WATER[9]"),    # 9  Right Top corner
         10: Decorator(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), needs_mask=True, decor_id="WATER[10]"),                         # 10 Right ending
         11: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), needs_mask=True, decor_id="WATER[11]"),   # 11 Bottom ending
         12: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 180), needs_mask=True, decor_id="WATER[12]"),  # 12 Left ending
         13: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 270), needs_mask=True, decor_id="WATER[13]"),  # 13 Top ending
         14: Decorator(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 32), WATER_SHEET.get_at((0, 32))), (128, 128)), needs_mask=True, decor_id="WATER[14]"),                         # 14 All Enclosed
         15: Decorator(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 64), WATER_SHEET.get_at((0, 32))), (128, 128)), needs_mask=True, decor_id="WATER[15]"),                        # 15 Left Top with corner
         16: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 64), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), needs_mask=True, decor_id="WATER[16]"),  # 16 Left Bottom with corner
         17: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 64), WATER_SHEET.get_at((0, 32))), (128, 128)), 180), needs_mask=True, decor_id="WATER[17]"), #17 Right Bottom with corner
         18: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 64), WATER_SHEET.get_at((0, 32))), (128, 128)), 270), needs_mask=True, decor_id="WATER[18]"), #18 Right Top with corner
         19: Decorator(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 96), WATER_SHEET.get_at((0, 32))), (128, 128)), needs_mask=True, decor_id="WATER[19]"),                         # 19 Just water
         20: Decorator(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 32), WATER_SHEET.get_at((0, 32))), (128, 128)), needs_mask=True, decor_id="WATER[20]"),                        # 20 Left Top corner tip
         21: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 32), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), needs_mask=True, decor_id="WATER[21]"),  # 21 Left Bottom corner tip
         22: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 32), WATER_SHEET.get_at((0, 32))), (128, 128)), 180), needs_mask=True, decor_id="WATER[22]"), #22 Right Bottom corner tip
         23: Decorator(transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 32), WATER_SHEET.get_at((0, 32))), (128, 128)), 270), needs_mask=True, decor_id="WATER[23]")} # 23 Right Top corner tip

WATERWAYS = {0: {(0, 0): WATER[13], (0, 128): WATER[16], (128, 128): WATER[4], (256, 128): WATER[18], (256, 256): WATER[11]},
             1: {(0, 0): WATER[6], (128, 0): WATER[9], (0, 128): WATER[1], (128, 128): WATER[23], (256, 128): WATER[9],
                 (0, 256): WATER[7], (128, 256): WATER[2], (256, 256): WATER[8]}}

MOUNTAINS = {0: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[0]"),
             1: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[1]"),
             2: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[2]"),
             3: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[3]"),
             4: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[4]"),
             5: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[5]"),
             6: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[6]"),
             7: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[7]"),
             8: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[8]"),
             9: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[9]"),
             10: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[10]"),
             11: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[11]"),
             12: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[12]"),
             13: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[13]"),
             14: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[14]"),
             15: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[15]"),
             16: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[16]"),
             17: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[17]"),
             18: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[18]"),
             19: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[19]"),
             20: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[20]"),
             21: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[21]"),
             22: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[22]"),
             23: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[23]"),
             24: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[24]"),
             25: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[25]"),
             26: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[26]"),
             27: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[27]"),
             28: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[28]"),
             29: Decorator(transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)), needs_mask=True, decor_id="MOUNTAINS[29]")
             }

MOUNTAIN_LAYOUTS = {0: {(128, 0): MOUNTAINS[6], (256, 0): MOUNTAINS[3], (384, 0): MOUNTAINS[9],
                        (0, 128): MOUNTAINS[6], (128, 128): MOUNTAINS[14], (384, 128): MOUNTAINS[15], (512, 128): MOUNTAINS[9],
                        (0, 256): MOUNTAINS[7], (128, 256): MOUNTAINS[8], (256, 256): MOUNTAINS[29], (512, 256): MOUNTAINS[29],
                        (0, 384): MOUNTAINS[29], (128, 384): MOUNTAINS[29], (256, 384): MOUNTAINS[29]}}

INSTRUCTIONS = {0: Decorator(MOVE_INSTRUCTIONS, collidable=False, transparent_background=True, decor_id="INSTRUCTIONS[0]"),
                1: Decorator(INTERACT_INSTRUCTIONS, collidable=False, transparent_background=True, decor_id="INSTRUCTIONS[1]"),
                2: Decorator(decor_sprite=QUEST_BOARD, collidable=True, transparent_background=True, size=QUEST_BOARD.get_size(), needs_mask=True, mask_offset=(0, int(QUEST_BOARD.get_height()*3/4)), decor_id="QUESTBOARD")
                }

FLAGS = {0: Decorator(transform.scale(surface_setup(FLAGS_SHEET, (32, 32), (0, 0), FLAGS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="FLAGS[0]"),
         1: Decorator(transform.scale(surface_setup(FLAGS_SHEET, (32, 32), (32, 0), FLAGS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="FLAGS[1]"),
         2: Decorator(transform.scale(surface_setup(FLAGS_SHEET, (32, 32), (64, 0), FLAGS_SHEET.get_at((0, 0))), (32, 32)), collidable=False, decor_id="FLAGS[2]")
         }

PLAYER_FRAMES = {"PLAYER_DOWN[0]": PLAYER_DOWN_SHEET.subsurface((0, 0, 32, 64)), "PLAYER_DOWN[1]": PLAYER_DOWN_SHEET.subsurface((32, 0, 32, 64)), "PLAYER_DOWN[2]": PLAYER_DOWN_SHEET.subsurface((64, 0, 32, 64)), "PLAYER_DOWN[3]": PLAYER_DOWN_SHEET.subsurface((96, 0, 32, 64)), "PLAYER_DOWN[4]": PLAYER_DOWN_SHEET.subsurface((128, 0, 32, 64)), "PLAYER_DOWN[5]": PLAYER_DOWN_SHEET.subsurface((160, 0, 32, 64)), "PLAYER_DOWN[6]": PLAYER_DOWN_SHEET.subsurface((192, 0, 32, 64)), "PLAYER_DOWN[7]": PLAYER_DOWN_SHEET.subsurface((224, 0, 32, 64)),
                 "PLAYER_UP[0]": PLAYER_UP_SHEET.subsurface((0, 0, 32, 64)), "PLAYER_UP[1]": PLAYER_UP_SHEET.subsurface((32, 0, 32, 64)), "PLAYER_UP[2]": PLAYER_UP_SHEET.subsurface((64, 0, 32, 64)), "PLAYER_UP[3]": PLAYER_UP_SHEET.subsurface((96, 0, 32, 64)), "PLAYER_UP[4]": PLAYER_UP_SHEET.subsurface((128, 0, 32, 64)), "PLAYER_UP[5]": PLAYER_UP_SHEET.subsurface((160, 0, 32, 64)), "PLAYER_UP[6]": PLAYER_UP_SHEET.subsurface((192, 0, 32, 64)), "PLAYER_UP[7]": PLAYER_UP_SHEET.subsurface((224, 0, 32, 64)),
                 "PLAYER_RIGHT[0]": PLAYER_RIGHT_SHEET.subsurface((0, 0, 32, 64)), "PLAYER_RIGHT[1]": PLAYER_RIGHT_SHEET.subsurface((32, 0, 32, 64)), "PLAYER_RIGHT[2]": PLAYER_RIGHT_SHEET.subsurface((64, 0, 32, 64)), "PLAYER_RIGHT[3]": PLAYER_RIGHT_SHEET.subsurface((96, 0, 32, 64)), "PLAYER_RIGHT[4]": PLAYER_RIGHT_SHEET.subsurface((128, 0, 32, 64)), "PLAYER_RIGHT[5]": PLAYER_RIGHT_SHEET.subsurface((160, 0, 32, 64)), "PLAYER_RIGHT[6]": PLAYER_RIGHT_SHEET.subsurface((192, 0, 32, 64)), "PLAYER_RIGHT[7]": PLAYER_RIGHT_SHEET.subsurface((224, 0, 32, 64)),
                 "PLAYER_LEFT[0]": PLAYER_LEFT_SHEET.subsurface((0, 0, 32, 64)), "PLAYER_LEFT[1]": PLAYER_LEFT_SHEET.subsurface((32, 0, 32, 64)), "PLAYER_LEFT[2]": PLAYER_LEFT_SHEET.subsurface((64, 0, 32, 64)), "PLAYER_LEFT[3]": PLAYER_LEFT_SHEET.subsurface((96, 0, 32, 64)), "PLAYER_LEFT[4]": PLAYER_LEFT_SHEET.subsurface((128, 0, 32, 64)), "PLAYER_LEFT[5]": PLAYER_LEFT_SHEET.subsurface((160, 0, 32, 64)), "PLAYER_LEFT[6]": PLAYER_LEFT_SHEET.subsurface((192, 0, 32, 64)), "PLAYER_LEFT[7]": PLAYER_LEFT_SHEET.subsurface((224, 0, 32, 64))}

DECOR_OBJECTS = {"FENCES[0]": FENCES[0], 'FENCES[1]': FENCES[1], 'FENCES[2]': FENCES[2], 'FENCES[3]': FENCES[3], 'FENCES[4]': FENCES[4], 'FENCES[5]': FENCES[5], 'FENCES[6]': FENCES[6], 'FENCES[7]': FENCES[7], 'FENCES[8]': FENCES[8], 'FENCES[9]': FENCES[9],
                 'TREES[0]': TREES[0], 'TREES[1]': TREES[1], 'TREES[2]': TREES[2], 'TREES[3]': TREES[3], 'TREES[4]': TREES[4],
                 'ROCKS[0]': ROCKS[0], 'ROCKS[1]': ROCKS[1], 'ROCKS[2]': ROCKS[2], 'ROCKS[3]': ROCKS[3], 'ROCKS[4]': ROCKS[4], 'ROCKS[5]': ROCKS[5], 'ROCKS[6]': ROCKS[6], 'ROCKS[7]': ROCKS[7], 'ROCKS[8]': ROCKS[8], 'ROCKS[9]': ROCKS[9],
                 'GRASS[0]': GRASS[0], 'GRASS[1]': GRASS[1], 'GRASS[2]': GRASS[2], 'GRASS[3]': GRASS[3], 'GRASS[4]': GRASS[4], 'GRASS[5]': GRASS[5], 'GRASS[6]': GRASS[6], 'GRASS[7]': GRASS[7], 'GRASS[8]': GRASS[8], 'GRASS[9]': GRASS[9], 'GRASS[10]': GRASS[10], 'GRASS[11]': GRASS[11], 'GRASS[12]': GRASS[12], 'GRASS[13]': GRASS[13], 'GRASS[14]': GRASS[14], 'GRASS[15]': GRASS[15],
                 'WATER[0]': WATER[0], 'WATER[1]': WATER[1], 'WATER[2]': WATER[2], 'WATER[3]': WATER[3], 'WATER[4]': WATER[4], 'WATER[5]': WATER[5], 'WATER[6]': WATER[6], 'WATER[7]': WATER[7], 'WATER[8]': WATER[8], 'WATER[9]': WATER[9], 'WATER[10]': WATER[10], 'WATER[11]': WATER[11], 'WATER[12]': WATER[12], 'WATER[13]': WATER[13], 'WATER[14]': WATER[14], 'WATER[15]': WATER[15],
                 'WATER[16]': WATER[16], 'WATER[17]': WATER[17], 'WATER[18]': WATER[18], 'WATER[19]': WATER[19], 'WATER[20]': WATER[20], 'WATER[21]': WATER[21], 'WATER[22]': WATER[22], 'WATER[23]': WATER[23],
                 'MOUNTAINS[0]': MOUNTAINS[0], 'MOUNTAINS[1]': MOUNTAINS[1], 'MOUNTAINS[2]': MOUNTAINS[2], 'MOUNTAINS[3]': MOUNTAINS[3], 'MOUNTAINS[4]': MOUNTAINS[4], 'MOUNTAINS[5]': MOUNTAINS[5], 'MOUNTAINS[6]': MOUNTAINS[6], 'MOUNTAINS[7]': MOUNTAINS[7], 'MOUNTAINS[8]': MOUNTAINS[8], 'MOUNTAINS[9]': MOUNTAINS[9], 'MOUNTAINS[10]': MOUNTAINS[10], 'MOUNTAINS[11]': MOUNTAINS[11], 'MOUNTAINS[12]': MOUNTAINS[12], 'MOUNTAINS[13]': MOUNTAINS[13], 'MOUNTAINS[14]': MOUNTAINS[14], 'MOUNTAINS[15]': MOUNTAINS[15],
                 'MOUNTAINS[16]': MOUNTAINS[16], 'MOUNTAINS[17]': MOUNTAINS[17], 'MOUNTAINS[18]': MOUNTAINS[18], 'MOUNTAINS[19]': MOUNTAINS[19], 'MOUNTAINS[20]': MOUNTAINS[20], 'MOUNTAINS[21]': MOUNTAINS[21], 'MOUNTAINS[22]': MOUNTAINS[22], 'MOUNTAINS[23]': MOUNTAINS[23], 'MOUNTAINS[24]': MOUNTAINS[24], 'MOUNTAINS[25]': MOUNTAINS[25], 'MOUNTAINS[26]': MOUNTAINS[26], 'MOUNTAINS[27]': MOUNTAINS[27], 'MOUNTAINS[28]': MOUNTAINS[28], 'MOUNTAINS[29]': MOUNTAINS[29],
                 "INSTRUCTIONS[0]": INSTRUCTIONS[0], "INSTRUCTIONS[1]": INSTRUCTIONS[1], "QUESTBOARD": INSTRUCTIONS[2], "FLAGS[0]": FLAGS[0], "FLAGS[1]": FLAGS[1], "FLAGS[2]": FLAGS[2]}

TIME_LOOK_UP_TABLE = {"6:00": 75, "7:00": 50, "8:00": 25, "9:00": 0, "18:00": 25, "19:00": 50, "20:00": 100, "21:00": 125, "22:00": 200}
