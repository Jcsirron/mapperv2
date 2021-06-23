from pygame import sprite, rect, surface, draw, mask
from decor import Decorator
from random import choice
from map import TERRAIN, FEATURES, IMPROVEMENTS, ANIMALS
from screen_handler import *
from globals import *
from button import *
from meat_space_assets import QUEST_BOARD

QUEST_DIFFICULTIES = ['easy', 'easy deplete', 'avoid', 'adjacent', 'multiple']


class Quest(object):

    def __init__(self, day, needs, difficulty, expiration=None, avoid=None, adjacent=None, x_offset=None, y_offset=None, index=None, depleting=False):
        self.needs = needs
        self.avoid = avoid
        self.adjacent = adjacent
        self.will_deplete = depleting
        self.created_day = day
        if expiration is not None:
            self.expiration_day = None
        else:
            self.expiration_day = expiration
        self.difficulty = difficulty
        self.offset = 16
        self.active = True
        self.completed = False
        self.rect = None
        self.__generate_image__()
        self.update_rect(x_offset, y_offset, index)

    def __generate_image__(self):
        self.surface = pygame.surface.Surface((int(SCREEN_SIZE[0] * 2 / 3) - self.offset * 2, self.offset * 4))
        self.surface.set_colorkey(self.surface.get_at((0, 0)))
        pygame.draw.rect(self.surface, WHITE, self.surface.get_rect(), border_radius=12)
        text_font = font.Font(FONT, 24)
        if not self.will_deplete:
            quest_text = "I need to visit a "
        else:
            quest_text = "I need to harvest from a "
        if len(self.needs) > 1:
            for need in self.needs:
                if self.needs.index(need) < len(self.needs) - 1:
                    quest_text = quest_text + str(need) + " and "
                else:
                    quest_text = quest_text + str(need)
        else:
            quest_text = quest_text + str(self.needs[0])
        if len(self.avoid) > 0:
            for avoid in self.avoid:
                quest_text = quest_text + " and avoid " + str(avoid) + "s"
        if len(self.adjacent) > 0:
            for adjacent in self.adjacent:
                quest_text = quest_text + " next to " + str(adjacent) + "s"
        quest_text = quest_text + "."
        text = text_font.render(quest_text, False, BROWN)
        draw_rect = (int((self.surface.get_rect()[2] - text.get_rect()[2])/2), int((self.surface.get_rect()[3] - text.get_rect()[3])/2))
        self.surface.blit(text, draw_rect)
        if self.will_deplete:
            draw.circle(self.surface, RED, (self.surface.get_width() - 16, 16), 6)

    def update_rect(self, x_offset, y_offset, index):
        self.rect = self.surface.get_rect().move(x_offset + self.offset, y_offset + self.offset * 5 * index)

    def __repr__(self):
        return "%s quest: needs: %s avoid: %s" % (self.difficulty, self.needs, self.avoid)

    def update(self):
        pass

    def move_rect(self, x, y, index):
        self.rect = self.surface.get_rect().move(x + self.offset, y + self.offset * 5 * index)

    def check_quest(self, path, world_map, player_map):
        self.active = False
        valid_goal = False
        avoids_all = True
        has_adjacents = False
        goals = self.needs.copy()
        for tile in path:
            if tile in world_map.stored_tiles:
                world_map.unpack_tile(tile, "worldmap.txt")
            if tile in world_map.map_set and len(self.avoid) > 0 and not world_map.map_set[tile].depleted:
                if world_map.map_set[tile].terrain in self.avoid:
                    avoids_all = False
            if tile in world_map.map_set and world_map.map_set[tile].terrain in self.needs and not world_map.map_set[tile].depleted:
                if world_map.map_set[tile].terrain in goals:
                    goals.remove(world_map.map_set[tile].terrain)
                    if self.will_deplete:
                        world_map.update_tile(tile, deplete=True)
                        if tile in player_map.map_set:
                            # This could be a difficulty value to change later
                            player_map.map_set[tile].depleted = True
                if len(goals) == 0:
                    valid_goal = True
                if self.adjacent is not None:
                    all_adjacents = world_map.get_adjacent_tiles(tile)
                    adjacents = self.adjacent.copy()
                    for adjacent in all_adjacents:
                        if world_map.map_set[adjacent].terrain in adjacents:
                            adjacents.remove(world_map.map_set[adjacent].terrain)
                    if len(adjacents) == 0:
                        has_adjacents = True
                else:
                    has_adjacents = True
        self.completed = valid_goal and avoids_all and has_adjacents

    def is_expired(self, current_day):
        if current_day > self.expiration_day:
            return True
        else:
            return False

    def export_quest(self):
        return {'day': self.created_day, 'needs': self.needs, 'difficulty': self.difficulty, 'expiration': self.expiration_day, 'avoid': self.avoid, 'adjacent': self.adjacent,
                'depleting': self.will_deplete}


class QuestMenu(object):

    def __init__(self, loading=False):
        self.is_active = False
        self.surface = surface.Surface((int(SCREEN_SIZE[0] * 2 / 3), int(SCREEN_SIZE[1] * 2 / 3)))
        self.surface.fill(BROWN)
        self.rect = pygame.rect.Rect(int(SCREEN_SIZE[0]/6), int(SCREEN_SIZE[1]/6), self.surface.get_width(), self.surface.get_height())
        font_text = font.Font(FONT, 36)
        title = font_text.render("Quest Board", False, WHITE)
        will_deplete_font = font.Font(FONT, 16)
        will_deplete = will_deplete_font.render("Will deplete area?", False, WHITE)
        self.quest_text = font.Font(FONT, 20)
        self.surface.blit(title, (int(self.surface.get_width()/2 - title.get_width()/2), 16))
        self.surface.blit(will_deplete, (int(self.surface.get_width() - will_deplete.get_width() - 8), 36))
        self.close_button = Button("Close", FONT, 24)
        self.close_button.update_location(location=(int(SCREEN_CENTER[0] - self.close_button.get_width() / 2), int(SCREEN_SIZE[1] / 6 * 5)))
        self.active_quests = []
        self.failed_quests = []
        self.completed_quests = []
        self.completed_quests_text = self.quest_text.render("Completed Quests: " + str(len(self.completed_quests)), False, WHITE)
        self.completed_quests_rect = (self.rect.left + self.completed_quests_text.get_width()/4, self.rect.bottom - 36)
        self.failed_quests_text = self.quest_text.render("Failed Quests: " + str(len(self.failed_quests)), False, WHITE)
        self.failed_quests_rect = (self.rect.left + int(self.rect.width/2 + title.get_width()/2 + self.failed_quests_text.get_width()/4), self.rect.bottom - 36)
        if not loading:
            while len(self.active_quests) < 5:
                self.generate_quest()
        self.active = False

    def update(self, mouse, movement):
        if self.active:
            if mouse[1] is not False:
                if not (self.rect.collidepoint(mouse[0])):
                    self.active = False
                for quest in self.active_quests:
                    if quest.rect.collidepoint(mouse[0]):
                        return quest
            if movement[2]:
                self.active = False
            draw_to_buffer([[self.surface, self.rect], [self.completed_quests_text, self.completed_quests_rect], [self.failed_quests_text, self.failed_quests_rect]])
            self.close_button.update()
            remove_list = []
            for quest in self.active_quests:
                if not quest.active:
                    remove_list.append(quest)
                draw_to_buffer([[quest.surface, quest.rect]])
            for quest in remove_list:
                self.active_quests.remove(quest)
                if quest.completed:
                    self.completed_quests.append(quest)
                else:
                    self.failed_quests.append(quest)
            if len(remove_list) > 0:
                self.update_quest_list()

    def get_active_quests(self):
        return self.active_quests

    def get_failed_quests(self):
        return self.failed_quests

    def get_completed_quests(self):
        return self.completed_quests

    def update_quest_list(self):
        x = 0
        for quest in self.active_quests:
            quest.move_rect(self.rect[0], self.rect[1] + 64, x)
            x += 1
        # TODO: Change how active quests are added to the quest board.
        if len(self.active_quests) < 5:
            self.generate_quest()
        self.completed_quests_text = self.quest_text.render("Completed Quests: " + str(len(self.completed_quests)), False, WHITE)
        self.failed_quests_text = self.quest_text.render("Failed Quests: " + str(len(self.failed_quests)), False, WHITE)

    @staticmethod
    def generate_requirements(difficulty):
        needs = []
        avoid = []
        adjacent = []
        will_deplete = False
        # Default is easy
        needs.append(choice(TERRAIN))
        if difficulty == "easy deplete":
            will_deplete = True
        elif difficulty == "avoid":
            avoid_terrain = choice(TERRAIN)
            while avoid_terrain in needs:
                avoid_terrain = choice(TERRAIN)
            avoid.append(avoid_terrain)
        elif difficulty == "adjacent":
            adjacent.append(choice(TERRAIN))
        elif difficulty == "multiple":
            need_terrain = choice(TERRAIN)
            while need_terrain in needs:
                need_terrain = choice(TERRAIN)
            needs.append(need_terrain)
        return needs, avoid, adjacent, will_deplete

    def generate_quest(self, difficulty=None):
        if difficulty is None:
            reqs = self.generate_requirements(choice(QUEST_DIFFICULTIES))
        else:
            reqs = self.generate_requirements(difficulty)
        self.active_quests.append(Quest(1, reqs[0], difficulty, avoid=reqs[1], adjacent=reqs[2], x_offset=self.rect[0], y_offset=self.rect[1] + 64, index=len(self.active_quests), depleting=reqs[3]))

    def load_quest(self, quest_type, **kwargs):
        day, expiration = 1, None
        needs, difficulty = None, None
        avoid, adjacent, depleting = None, None, False
        for key, value in kwargs.items():
            if key == "day":
                day = value
            elif key == "needs":
                needs = value
            elif key == "difficulty":
                difficulty = value
            elif key == "expiration":
                expiration = value
            elif key == "avoid":
                avoid = value
            elif key == "adjacent":
                adjacent = value
            elif key == "depleting":
                depleting = value
        if quest_type == "completed":
            self.completed_quests.append(Quest(day, needs=needs, difficulty=difficulty, expiration=expiration, avoid=avoid, adjacent=adjacent, x_offset=self.rect[0], y_offset=self.rect[1] + 64, index=len(self.active_quests), depleting=depleting))
        elif quest_type == "active":
            self.active_quests.append(Quest(day, needs=needs, difficulty=difficulty, expiration=expiration, avoid=avoid, adjacent=adjacent, x_offset=self.rect[0], y_offset=self.rect[1] + 64, index=len(self.active_quests), depleting=depleting))
        else:
            self.failed_quests.append(Quest(day, needs=needs, difficulty=difficulty, expiration=expiration, avoid=avoid, adjacent=adjacent, x_offset=self.rect[0], y_offset=self.rect[1] + 64, index=len(self.active_quests), depleting=depleting))

    def export_quest_board(self):
        export = {"completed": [], "failed": [], "active": []}
        for quest in self.completed_quests:
            export["completed"].append(quest.export_quest())
        for quest in self.failed_quests:
            export["failed"].append(quest.export_quest())
        for quest in self.active_quests:
            export["active"].append(quest.export_quest())
        return export
