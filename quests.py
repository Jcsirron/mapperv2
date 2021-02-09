from pygame import sprite, rect, surface, draw, mask
from random import choice
from map import TERRAIN, FEATURES, IMPROVEMENTS, ANIMALS
from screen_handler import *
from globals import *
from button import *
from meat_space_assets import QUEST_BOARD

QUEST_DIFFICULTIES = ['easy', 'medium']


# TODO: Create artwork for the quest board
class QuestBoard(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = QUEST_BOARD
        self.image.set_colorkey(self.image.get_at((0, self.image.get_height()-1)))
        self.rect = self.image.get_rect()
        mask_cover = surface.Surface((self.image.get_width(), self.image.get_height()/4))
        mask_cover.blit(self.image, (0, -int(self.image.get_height()*3/4)))
        self.collidable = True
        self.mask = mask.from_surface(mask_cover)
        self.mask_offset = (0, int(self.image.get_height()*3/4))

    def update(self, buttons):
        pass

    def move(self, x, y):
        self.rect = self.rect.move(x, y)


class Quest(object):

    def __init__(self, day, needs, difficulty, expiration=None, avoid=None, adjacent=None, x_offset=None, y_offset=None, index=None, depleting=False):
        self.needs = needs
        self.avoid = avoid
        self.adjacent = adjacent
        self.will_deplete = depleting
        self.created_day = day
        if expiration is not None:
            self.expiration_day = None
        self.difficulty = difficulty
        self.offset = 16
        self.surface = pygame.surface.Surface((int(SCREEN_SIZE[0] * 2 / 3) - self.offset * 2, self.offset * 4))
        self.surface.set_colorkey(self.surface.get_at((0, 0)))
        pygame.draw.rect(self.surface, WHITE, self.surface.get_rect(), border_radius=12)
        text_font = font.Font(FONT, 24)
        quest_text = "I need to visit a "
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
                quest_text = quest_text + " and next to " + str(adjacent) + "s"
        quest_text = quest_text + "."
        text = text_font.render(quest_text, False, BROWN)
        draw_rect = (int((self.surface.get_rect()[2] - text.get_rect()[2])/2), int((self.surface.get_rect()[3] - text.get_rect()[3])/2))
        self.surface.blit(text, draw_rect)
        if self.will_deplete:
            # TODO: Make this more obvious with other assets later
            draw.circle(self.surface, RED, (16, 16), 6)
        self.rect = self.surface.get_rect().move(x_offset + self.offset, y_offset + self.offset * 5 * index)
        self.active = True
        self.completed = False

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


class QuestMenu(object):

    def __init__(self):
        self.is_active = False
        self.surface = surface.Surface((int(SCREEN_SIZE[0] * 2 / 3), int(SCREEN_SIZE[1] * 2 / 3)))
        self.surface.fill(BROWN)
        self.rect = pygame.rect.Rect(int(SCREEN_SIZE[0]/6), int(SCREEN_SIZE[1]/6), self.surface.get_width(), self.surface.get_height())
        font_text = font.Font(FONT, 36)
        title = font_text.render("Quest Board", False, WHITE)
        self.quest_text = font.Font(FONT, 18)
        self.surface.blit(title, (int(self.surface.get_width()/2 - title.get_width()/2), 16))
        self.close_button = Button("Close", FONT, 24)
        self.close_button.update_location(location=(int(SCREEN_CENTER[0] - self.close_button.get_width() / 2), int(SCREEN_SIZE[1] / 6 * 5)))
        self.active_quests = []
        self.failed_quests = []
        self.completed_quests = []
        self.completed_quests_text = self.quest_text.render("Completed Quests: " + str(len(self.completed_quests)), False, WHITE)
        self.completed_quests_rect = (self.rect.left + self.completed_quests_text.get_width()/4, self.rect.bottom - 36)
        self.failed_quests_text = self.quest_text.render("Failed Quests: " + str(len(self.failed_quests)), False, WHITE)
        self.failed_quests_rect = (self.rect.left + int(self.rect.width/2 + title.get_width()/2 + self.failed_quests_text.get_width()/4), self.rect.bottom - 36)
        self.generate_quest('easy deplete')
        self.generate_quest('easy deplete')
        self.generate_quest('medium')
        self.generate_quest('medium2')
        self.generate_quest('medium3')
        self.active = False

    def update(self, mouse, movement):
        if self.active:
            if mouse[0] is not False:
                if not (self.rect.collidepoint(mouse[1])):
                    self.active = False
                for quest in self.active_quests:
                    if quest.rect.collidepoint(mouse[1]):
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
        elif difficulty == "medium":
            avoid_terrain = choice(TERRAIN)
            while avoid_terrain in needs:
                avoid_terrain = choice(TERRAIN)
            avoid.append(avoid_terrain)
        # TODO: Rename difficulty so it makes more sense
        elif difficulty == "medium2":
            adjacent.append(choice(TERRAIN))
        # TODO: Rename difficulty so it makes more sense
        elif difficulty == "medium3":
            need_terrain = choice(TERRAIN)
            while need_terrain in needs:
                need_terrain = choice(TERRAIN)
            needs.append(need_terrain)
        return needs, avoid, adjacent, will_deplete

    def generate_quest(self, difficulty):
        reqs = self.generate_requirements(difficulty)
        self.active_quests.append(Quest(1, reqs[0], difficulty, avoid=reqs[1], adjacent=reqs[2], x_offset=self.rect[0], y_offset=self.rect[1] + 64, index=len(self.active_quests), depleting=reqs[3]))
