from map_space_assets import forest_tile, mountain_tile, waterway_tile, plain_tile, home_tile
from pygame import surface, rect
from globals import *

TERRAIN = ["forest", "plain", "swamp", "mountain"]
IMPROVEMENTS = ["road", "settlement", "ruins", "mine", "home"]
FEATURES = ["glade", "outcropping", "fishing hole"]
ANIMALS = ["small game", "large game", "small predator", "large predator"]


class Tile(object):

    def __init__(self, location, size, terrain=None, improvement=None, feature=None, animal=None, depleted=False, objects=None):
        self.location = location
        self.terrain = terrain
        self.improvement = improvement
        self.feature = feature
        self.animals = animal
        self.surface = surface.Surface(size)
        self.surface.fill(BROWN)
        self.rect = rect.Rect(location[0]*size[0], location[1]*size[1], size[0], size[1])
        self.depleted = depleted
        self.update_tile(terrain, improvement, feature, animal)
        if objects is not None:
            self.objects = objects
        else:
            self.objects = []

    def __repr__(self):
        return "Tile()"

    def __str__(self):
        objects = []
        for i in self.objects:
            objects.append(i.id)
        return "Class " + str(self.__repr__()) + "\tLocation: " + str(self.location) + "\tTerrain: " + \
               str(self.terrain) + "\tImprovement: " + str(self.improvement) + "\tFeature: " + str(self.feature) + \
               "\tObjects: " + str(objects)

    def update_tile(self, terrain=None, improvement=None, feature=None, animal=None, new_surface=None, depleted=None):
        if terrain is not None:
            self.update_terrain(terrain)
            if terrain == "forest":
                self.surface.blit(forest_tile, (0, 0))
            elif terrain == "plain":
                self.surface.blit(plain_tile, (0, 0))
            elif terrain == "swamp":
                self.surface.blit(waterway_tile, (0, 0))
            elif terrain == "mountain":
                self.surface.blit(mountain_tile, (0, 0))
            elif terrain == "town":
                self.surface.blit(home_tile, (0, 0))
            else:
                self.surface.fill(BROWN)
        if improvement is not None:
            self.update_improvement(improvement)
        if feature is not None:
            self.update_feature(feature)
        if animal is not None:
            self.update_animals(animal)
        if new_surface is not None:
            self.update_surface(new_surface)
        if depleted is not None:
            self.depleted = depleted

    def update_terrain(self, terrain):
        if terrain in TERRAIN:
            self.terrain = terrain
        elif terrain == "clear":
            self.terrain = None

    def update_improvement(self, improvement):
        if improvement in IMPROVEMENTS:
            if self.location == (0, 0):
                self.improvement = "home"
            else:
                self.improvement = improvement
        elif improvement == "clear":
            if self.location == (0, 0):
                self.improvement = "home"
            self.improvement = None

    def update_feature(self, feature):
        if feature in FEATURES:
            self.feature = feature
        elif feature == "clear":
            self.feature = None

    def update_animals(self, animal):
        if animal in ANIMALS:
            self.animals = animal
        elif animal == "clear":
            self.animals = None

    def update_objects(self, game_object):
        if game_object not in self.objects:
            x = 0
            for existing_object in self.objects:
                if game_object.rect.centery <= existing_object.rect.centery:
                    break
                x += 1
            self.objects.insert(x, game_object)
        elif game_object == "clear":
            self.objects = []

    def update_surface(self, new_surface, overwrite=True):
        if surface is not None:
            if overwrite:
                self.surface = new_surface
            else:
                self.surface.blit(new_surface, (0, 0))
            self.rect = rect.Rect(self.location[0]*self.surface.get_width(), self.location[1]*self.surface.get_height(), self.surface.get_width(), self.surface.get_height())

    def pop_object(self, game_object):
        return_object = None
        if game_object in self.objects:
            return_object = self.objects.pop(self.objects.index(game_object))
        return return_object

    def set_surface(self, new_surface):
        self.surface = new_surface

    def move_rect(self, distance):
        self.rect = self.rect.move(distance)

    def export_stats(self):
        return {"size": self.surface.get_size(), "terrain": self.terrain, "improvement": self.improvement, "feature": self.feature, "animals": self.animals, "depleted": self.depleted}

    def export_objects(self):
        export_list = []
        for decor_object in self.objects:
            export_list.append(decor_object.get_export_values((self.location[0] * self.surface.get_width(), self.location[1] * self.surface.get_height())))
        return export_list

    def export_all(self):
        export = self.export_stats()
        export['objects'] = self.export_objects()
        return export
