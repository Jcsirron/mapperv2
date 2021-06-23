from pygame import surface, rect
from random import choice, randint
from tile import *
from meat_space_assets import *
from screen_handler import SCREEN_SIZE
from pickling_io import *


class MapObject(object):

    def __init__(self):
        self.map_set = {}
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.stored_tiles = []
        self.max_distance_from_center = 2
        self.max_active_tiles = 2 * self.max_distance_from_center * self.max_distance_from_center + 2 * self.max_distance_from_center + 4

    def update_map(self, tiles):
        pass

    def compare_map(self, other_map):
        matching_tiles = []
        for location in other_map.keys():
            if location in self.map_set or location in self.stored_tiles:
                if location in self.stored_tiles:
                    self.unpack_tile(location)
                temp_matches = [location]
                if self.map_set[location].terrain == other_map[location].terrain:
                    temp_matches.append("terrain")
                elif self.map_set[location].improvement == other_map[location].improvement:
                    temp_matches.append("improvement")
                elif self.map_set[location].feature == other_map[location].feature:
                    temp_matches.append("feature")
                matching_tiles.append(temp_matches)
        return matching_tiles

    def get_tile(self, tile_location):
        if tile_location in self.map_set:
            return self.map_set[tile_location]
        else:
            return None

    def get_adjacent_tiles(self, tile_location):
        all_adjacents = []
        x = tile_location[0] - 1
        y = tile_location[1] - 1
        while x <= tile_location[0] + 1:
            while y <= tile_location[1] + 1:
                if (x, y) in self.map_set:
                    all_adjacents.append((x, y))
                y += 1
            y = tile_location[1] - 1
            x += 1
        if tile_location in all_adjacents:
            all_adjacents.remove(tile_location)
        return all_adjacents

    def get_potential_tiles(self, tile_location):
        all_adjacents = []
        x = tile_location[0] - 1
        y = tile_location[1] - 1
        while x <= tile_location[0] + 1:
            while y <= tile_location[1] + 1:
                if (x, y) not in self.map_set:
                    all_adjacents.append((x, y))
                y += 1
            y = tile_location[1] - 1
            x += 1
        if tile_location in all_adjacents:
            all_adjacents.remove(tile_location)
        return all_adjacents

    def update_tile(self, tile_location, terrain=None, improvement=None, feature=None, animal=None, new_surface=None, deplete=None):
        if tile_location in self.map_set:
            self.map_set[tile_location].update_tile(terrain, improvement, feature, animal, new_surface, deplete)

    def add_tile(self, tile_location, size, terrain=None, improvement=None, feature=None, animal=None, depleted=False, objects=None):
        if tile_location not in self.map_set:
            if self.x_max is None:
                self.x_max = tile_location[0]
            elif tile_location[0] > self.x_max:
                self.x_max = tile_location[0]
            if self.x_min is None:
                self.x_min = tile_location[0]
            elif tile_location[0] < self.x_min:
                self.x_min = tile_location[0]
            if self.y_max is None:
                self.y_max = tile_location[1]
            elif tile_location[1] > self.y_max:
                self.y_max = tile_location[1]
            if self.y_min is None:
                self.y_min = tile_location[1]
            elif tile_location[1] < self.y_min:
                self.y_min = tile_location[1]
            self.map_set[tile_location] = Tile(tile_location, size, terrain, improvement, feature, animal, depleted, objects)

    def generate_tile(self, tile_location, tile_size, terrain=None, improvement=None, feature=None, animal=None):
        if terrain is None:
            tiles = self.get_adjacent_tiles(tile_location)
            if len(tiles) > 0:
                adjacents = TERRAIN.copy()
                for tile in tiles:
                    if self.map_set[tile].terrain in TERRAIN:
                        if (abs(tile_location[0] - tile[0]) == 1 and tile_location[1] - tile[1] == 0) or \
                                (tile_location[0] - tile[0] == 0 and abs(tile_location[1] - tile[1]) == 1):
                            adjacents.append(self.map_set[tile].terrain)
                        adjacents.append(self.map_set[tile].terrain)
                terrain = choice(adjacents)
            else:
                terrain = choice(TERRAIN)
        if improvement is None:
            improvement = choice(IMPROVEMENTS)
        if feature is None:
            feature = choice(FEATURES)
        if animal is None:
            animal = choice(ANIMALS)
        self.add_tile(tile_location, tile_size, terrain, improvement, feature, animal)
        self.set_tile_surface(tile_location, tile_size, YELLOW)
        self.generate_objects_for_tile(tile_location, terrain)

    def load_tile(self, tile_location, size, mode, terrain=None, improvement=None, feature=None, animals=None, depleted=False, objects=[]):
        self.add_tile(tile_location, size, terrain, improvement, feature, animals, depleted)
        if mode == "meat":
            self.set_tile_surface(tile_location, size, YELLOW)
        elif mode == "map":
            self.set_tile_surface(tile_location, size, BROWN)
        for decor in objects:
            if decor[0] in DECOR_OBJECTS:
                self.add_object_to_tile(tile_location, decor[1], DECOR_OBJECTS[decor[0]].copy())

    def set_tile_surface(self, tile, surface_size, color=None):
        if tile in self.map_set:
            new_surf = surface.Surface(surface_size)
            if color is not None:
                new_surf.fill(color)
            self.map_set[tile].update_tile(new_surface=new_surf)

    def get_map_size(self):
        return self.get_tile_width(), self.get_tile_height()

    def get_tile_width(self):
        return abs(self.x_min) + self.x_max + 1  # need the plus 1 for (0, 0)

    def get_tile_height(self):
        return abs(self.y_min) + self.y_max + 1  # need the plus 1 for (0, 0)

    def tile_in_map(self, tile):
        if tile in self.map_set or tile in self.stored_tiles:
            return True
        return False

    def add_object_to_tile(self, tile, location, game_object):
        if tile in self.map_set:
            if self.map_set[tile].rect is not None:
                location = (location[0] + self.map_set[tile].rect[0], location[1] + self.map_set[tile].rect[1])
            game_object.rect = game_object.rect.move(location)
            self.map_set[tile].update_objects(game_object)

    # TODO: Create better way to generate tiles, calling generic function to build what's needed.
    def generate_objects_for_tile(self, tile_location, terrain, object_count=24):
        init_loc_list = TILE_SLOTS.copy()
        while len(init_loc_list) > object_count:
            init_loc_list.remove(choice(init_loc_list))
        loc_list = []
        for location in init_loc_list:
            loc_list.append((max(0, min(location[0] + randint(0, 32), int(SCREEN_SIZE[0] * 1.5 / 128 - 1) * 128)), max(0, min(location[1] + randint(0, 32), int(SCREEN_SIZE[1] * 1.5 / 128 - 1) * 128))))

        if terrain == "forest":
            rocks_count = randint(1, int(object_count/10))  # up to 10% can be rocks
            while rocks_count > 0:
                self.add_object_to_tile(tile_location, loc_list.pop(), ROCKS[randint(0, len(ROCKS) - 1)].copy())
                rocks_count -= 1
            grass_count = randint(1, int(object_count/5))  # up to 20% can be grass
            while grass_count > 0:
                self.add_object_to_tile(tile_location, loc_list.pop(), GRASS[randint(0, len(GRASS) - 1)].copy())
                grass_count -= 1
            for location in loc_list:  # The rest are trees
                self.add_object_to_tile(tile_location, location, TREES[randint(0, len(TREES) - 1)].copy())

        # TODO: Change the mountain generation to utilize the tileset (hard code a few layouts for now)
        elif terrain == "mountain":
            loc_list = self.generate_mountain_tile(tile_location, loc_list)
            tree_count = randint(1, int(object_count / 10))  # up to 10% can be trees
            while tree_count > 0:
                self.add_object_to_tile(tile_location, loc_list.pop(), TREES[randint(0, len(TREES) - 1)].copy())
                tree_count -= 1
            grass_count = randint(1, int(object_count / 5))  # up to 20% can be grass
            while grass_count > 0:
                self.add_object_to_tile(tile_location, loc_list.pop(), GRASS[randint(0, len(GRASS) - 1)].copy())
                grass_count -= 1
            for location in loc_list:
                self.add_object_to_tile(tile_location, location, ROCKS[randint(0, len(ROCKS) - 1)].copy())

        elif terrain == "plain":
            tree_count = randint(1, int(object_count / 10))  # up to 10% can be trees
            while tree_count > 0:
                self.add_object_to_tile(tile_location, loc_list.pop(), TREES[randint(0, len(TREES) - 1)].copy())
                tree_count -= 1
            rocks_count = randint(1, int(object_count / 10))  # up to 10% can be rocks
            while rocks_count > 0:
                self.add_object_to_tile(tile_location, loc_list.pop(), ROCKS[randint(0, len(ROCKS) - 1)].copy())
                rocks_count -= 1
            for location in loc_list:
                self.add_object_to_tile(tile_location, location, GRASS[randint(0, len(GRASS) - 1)].copy())

        # TODO: Change the waterway generation to utilize the tileset (hard code a few layouts for now)
        elif terrain == "swamp":
            loc_list = self.generate_water_tile(tile_location, loc_list)
            tree_count = randint(1, int(object_count / 10))  # up to 10% can be trees
            while tree_count > 0:
                self.add_object_to_tile(tile_location, loc_list.pop(), TREES[randint(0, len(TREES) - 1)].copy())
                tree_count -= 1
            rocks_count = randint(1, int(object_count / 10))  # up to 10% can be rocks
            while rocks_count > 0:
                self.add_object_to_tile(tile_location, loc_list.pop(), ROCKS[randint(0, len(ROCKS) - 1)].copy())
                rocks_count -= 1
            for location in loc_list:
                self.add_object_to_tile(tile_location, location, GRASS[randint(0, len(GRASS) - 1)].copy())
        else:
            pass

    def generate_water_tile(self, tile_location, loc_list):
        tile_list = []
        start_tile = (128 * randint(0, 5), 128 * randint(0, 3))
        tileset = choice(WATERWAYS)
        for tile in tileset:
            tileset_location = (tile[0] + start_tile[0], tile[1] + start_tile[1])
            self.add_object_to_tile(tile_location, tileset_location, tileset[tile].copy())
            tile_list.append(tileset_location)
        remove_list = []
        for filled_tile in tile_list:
            for tile in loc_list:
                if filled_tile[0] - 32 <= tile[0] <= filled_tile[0] + 32 and filled_tile[1] - 32 <= tile[1] <= filled_tile[1] + 32:
                    remove_list.append(tile)
        for tile in remove_list:
            loc_list.remove(tile)
        return loc_list

    def trim_tile_set(self, central_tile):
        if len(self.map_set) > self.max_active_tiles:
            stored_tiles = read_in_file("automap.txt", "Saves")
            tiles_to_pack = []
            for tile in self.map_set:
                if abs(central_tile[0] - tile[0]) + abs(central_tile[1] - tile[1]) >= self.max_distance_from_center + 1:
                    if tile not in self.stored_tiles:
                        stored_tiles[tile] = self.pack_tile(tile)
                        self.stored_tiles.append(tile)
                    tiles_to_pack.append(tile)
            for tile in tiles_to_pack:
                del self.map_set[tile]
            save_out_file(stored_tiles, 'automap.txt', "Saves")

    def load_tile_set(self, central_tile, save_file):
        tiles_to_load = []
        start_tile = (central_tile[0] - self.max_distance_from_center, central_tile[1] + self.max_distance_from_center)
        while start_tile[0] <= central_tile[0] + 1:
            while start_tile[1] <= central_tile[1] + 1:
                if start_tile in self.stored_tiles and abs(central_tile[0] - start_tile[0]) + abs(central_tile[1] - start_tile[1]) <= self.max_distance_from_center:
                    tiles_to_load.append(start_tile)
                start_tile = (start_tile[0], start_tile[1] + 1)
            start_tile = (start_tile[0] + 1, central_tile[1] - self.max_distance_from_center + 1)
        if len(tiles_to_load) > 1:
            self.unpack_tiles(tiles_to_load, save_file)
        elif len(tiles_to_load) == 1:
            self.unpack_tile(tiles_to_load[0], save_file)

    def change_max_distance(self, distance):
        self.max_distance_from_center = distance
        self.max_active_tiles = 2 * self.max_distance_from_center * self.max_distance_from_center + 2 * self.max_distance_from_center + 4

    def generate_mountain_tile(self, tile_location, loc_list):
        tile_list = []
        start_tile = (128 * randint(0, 3), 128 * randint(0, 2))
        tileset = choice(MOUNTAIN_LAYOUTS)
        for tile in tileset:
            tileset_location = (tile[0] + start_tile[0], tile[1] + start_tile[1])
            self.add_object_to_tile(tile_location, tileset_location, tileset[tile].copy())
            tile_list.append(tileset_location)
        remove_list = []
        for filled_tile in tile_list:
            for tile in loc_list:
                if filled_tile[0] - 32 <= tile[0] <= filled_tile[0] + 32 and filled_tile[1] - 32 <= tile[1] <= \
                        filled_tile[1] + 32:
                    remove_list.append(tile)
        for tile in remove_list:
            loc_list.remove(tile)
        return loc_list

    def pack_map(self, external_file=None):
        if external_file is not None and path.isfile(path.join('Saves', external_file)):
            pickle_off = open(path.join("Saves", external_file), "rb")
            saved_tiles = pickle.load(pickle_off)
            pickle_off.close()
        else:
            saved_tiles = {}
        export_map = {}
        for tile in self.map_set:
            export_map[tile] = self.pack_tile(tile)
        export_map.update(saved_tiles)
        return export_map

    def pack_tile(self, tile):
        return self.map_set[tile].export_all()

    def unpack_tile(self, tile, save_file):
        if tile in self.stored_tiles:
            saved_tiles = read_in_file(save_file, "Saves")
            if tile in saved_tiles:
                self.load_tile(tile_location=tile, mode="meat", **saved_tiles[tile])
                del saved_tiles[tile]
            self.stored_tiles.remove(tile)
        else:
            return
        save_out_file(saved_tiles, save_file, "Saves")

    def unpack_tiles(self, tiles, save_file):
        saved_tiles = read_in_file(save_file, "Saves")
        for tile in tiles:
            if tile in self.stored_tiles:
                if tile in saved_tiles:
                    if tile not in self.map_set:
                        self.load_tile(tile_location=tile, mode="meat", **saved_tiles[tile])
                    del saved_tiles[tile]
                self.stored_tiles.remove(tile)
        save_out_file(saved_tiles, save_file, "Saves")
