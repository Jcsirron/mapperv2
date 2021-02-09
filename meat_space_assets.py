#!/usr/bin/env python
from pygame import image, transform
from globals import *
from screen_handler import SCREEN_SIZE
from os import path

FENCES_SHEET = image.load(path.join('Artwork', "Fences.png")).convert()
TREES_SHEET = image.load(path.join("Artwork", "Trees.png")).convert()
ROCKS_SHEET = image.load(path.join("Artwork", "Rocks.png")).convert()
GRASS_SHEET = image.load(path.join("Artwork", "Grass.png")).convert()
WATER_SHEET = image.load(path.join("Artwork", "Water tiles.png")).convert()
MOUNTAIN_SHEET = image.load(path.join("Artwork", "Mountain tiles.png")).convert()
QUEST_BOARD = image.load(path.join("Artwork", "Quest Board.png")).convert()

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

FENCES = [transform.scale(surface_setup(FENCES_SHEET, (32, 32), (0, 0), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (32, 0), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (64, 0), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (96, 0), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (0, 32), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (32, 32), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (64, 32), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (96, 32), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (0, 64), FENCES_SHEET.get_at((0, 0))), (64, 64)),
          transform.scale(surface_setup(FENCES_SHEET, (32, 32), (32, 64), FENCES_SHEET.get_at((0, 0))), (64, 64))]

TREES = [transform.scale(surface_setup(TREES_SHEET, (32, 64), (0, 0), TREES_SHEET.get_at((0, 0))), (64, 128)),      # Tall Pine Tree
         transform.scale(surface_setup(TREES_SHEET, (32, 32), (32, 0), TREES_SHEET.get_at((0, 0))), (64, 64)),
         transform.scale(surface_setup(TREES_SHEET, (64, 64), (64, 0), TREES_SHEET.get_at((0, 0))), (128, 128)),
         transform.scale(surface_setup(TREES_SHEET, (32, 32), (32, 32), TREES_SHEET.get_at((0, 0))), (64, 64)),
         transform.scale(surface_setup(TREES_SHEET, (32, 64), (0, 64), TREES_SHEET.get_at((0, 0))), (64, 128))]

ROCKS = [transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (0, 0), ROCKS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (16, 0), ROCKS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(ROCKS_SHEET, (32, 32), (32, 0), ROCKS_SHEET.get_at((0, 0))), (64, 64)),
         transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (0, 16), ROCKS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (16, 16), ROCKS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (0, 32), ROCKS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (16, 32), ROCKS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (0, 48), ROCKS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(ROCKS_SHEET, (16, 16), (16, 48), ROCKS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(ROCKS_SHEET, (32, 32), (32, 32), ROCKS_SHEET.get_at((0, 0))), (64, 64))]

GRASS = [transform.scale(surface_setup(GRASS_SHEET, (8, 8), (0, 0), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (8, 0), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (16, 0), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (24, 0), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (0, 8), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (8, 8), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (16, 8), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (24, 8), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (0, 16), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (8, 16), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (16, 16), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (24, 16), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (0, 24), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (8, 24), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (16, 24), GRASS_SHEET.get_at((0, 0))), (32, 32)),
         transform.scale(surface_setup(GRASS_SHEET, (8, 8), (24, 24), GRASS_SHEET.get_at((0, 0))), (32, 32))]

WATER = [transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 0), WATER_SHEET.get_at((0, 32))), (128, 128)),                        # 0  Edge at top
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 90),  # 1  Edge at left
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 180), # 2  Edge at bottom
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 270), # 3  Edge at right
         transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 0), WATER_SHEET.get_at((0, 32))), (128, 128)),                       # 4  Horizontal line
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), # 5  Vertical line
         transform.scale(surface_setup(WATER_SHEET, (32, 32), (64, 0), WATER_SHEET.get_at((0, 32))), (128, 128)),                       # 6  Left Top corner
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (64, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), # 7  Left Bottom corner
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (64, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 180),# 8  Right Bottom corner
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (64, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 270),# 9  Right Top corner
         transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 0), WATER_SHEET.get_at((0, 32))), (128, 128)),                       # 10 Right ending
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 90), # 11 Bottom ending
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 180),# 12 Left ending
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 0), WATER_SHEET.get_at((0, 32))), (128, 128)), 270),# 13 Top ending
         transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 32), WATER_SHEET.get_at((0, 32))), (128, 128)),                       # 14 All Enclosed
         transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 64), WATER_SHEET.get_at((0, 32))), (128, 128)),                      # 15 Left Top with corner
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 64), WATER_SHEET.get_at((0, 32))), (128, 128)), 90),# 16 Left Bottom with corner
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 64), WATER_SHEET.get_at((0, 32))), (128, 128)), 180),#17 Right Bottom with corner
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (96, 64), WATER_SHEET.get_at((0, 32))), (128, 128)), 270),#18 Right Top with corner
         transform.scale(surface_setup(WATER_SHEET, (32, 32), (0, 96), WATER_SHEET.get_at((0, 32))), (128, 128)),                       # 19 Just water
         transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 32), WATER_SHEET.get_at((0, 32))), (128, 128)),                      # 20 Left Top corner tip
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 32), WATER_SHEET.get_at((0, 32))), (128, 128)), 90),# 21 Left Bottom corner tip
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 32), WATER_SHEET.get_at((0, 32))), (128, 128)), 180),#22 Right Bottom corner tip
         transform.rotate(transform.scale(surface_setup(WATER_SHEET, (32, 32), (32, 32), WATER_SHEET.get_at((0, 32))), (128, 128)), 270)# 23 Right Top corner tip
         ]

WATERWAYS = {0: {(0, 0): WATER[13], (0, 128): WATER[16], (128, 128): WATER[4], (256, 128): WATER[18], (256, 256): WATER[11]},
             1: {(0, 0): WATER[6], (128, 0): WATER[9], (0, 128): WATER[1], (128, 128): WATER[23], (256, 128): WATER[9],
                 (0, 256): WATER[7], (128, 256): WATER[2], (256, 256): WATER[8]}}

MOUNTAINS = [transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 0), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 32), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 64), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 96), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (0, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (32, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (64, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (96, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (128, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128)),
             transform.scale(surface_setup(MOUNTAIN_SHEET, (32, 32), (160, 128), MOUNTAIN_SHEET.get_at((0, 0))), (128, 128))
             ]

MOUNTAIN_LAYOUTS = {0: {(128, 0): MOUNTAINS[6], (256, 0): MOUNTAINS[3], (384, 0): MOUNTAINS[9],
                        (0, 128): MOUNTAINS[6], (128, 128): MOUNTAINS[14], (384, 128): MOUNTAINS[15], (512, 128): MOUNTAINS[9],
                        (0, 256): MOUNTAINS[7], (128, 256): MOUNTAINS[8], (256, 256): MOUNTAINS[29], (512, 256): MOUNTAINS[29],
                        (0, 384): MOUNTAINS[29], (128, 384): MOUNTAINS[29], (256, 384): MOUNTAINS[29]}}
