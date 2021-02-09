#!/usr/bin/env python
from pygame import image, transform
from globals import *
from os import path


# TODO: Create tiling for adjacent tiling, making the map space more cohesive
FOREST_TILES = image.load(path.join('Artwork', "Forest tile.png"))
MOUNTAIN_TILES = image.load(path.join('Artwork', "Mountains tile.png"))
WATERWAY_TILES = image.load(path.join('Artwork', "Water tile.png"))
PLAIN_TILES = image.load(path.join('Artwork', "Plain tile.png"))
HOME_TILES = image.load(path.join("Artwork", "Home tile.png"))


forest_tile = surface_setup(FOREST_TILES, (64, 64))
map_forest_tile = transform.scale(forest_tile.copy(), (512, 512))

map_mountain_tile = surface_setup(MOUNTAIN_TILES, (512, 512))
mountain_tile = transform.scale(map_mountain_tile.copy(), TILE_SIZE)

waterway_tile = surface_setup(WATERWAY_TILES, (64, 64))
map_waterway_tile = transform.scale(waterway_tile.copy(), (512, 512))

plain_tile = surface_setup(PLAIN_TILES, (64, 64))
map_plain_tile = transform.scale(plain_tile.copy(), (512, 512))

home_tile = surface_setup(HOME_TILES, (64, 64))
map_home_tile = transform.scale(home_tile.copy(), (512, 512))
