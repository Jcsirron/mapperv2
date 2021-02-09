from pygame import surface, font, sprite, draw
from screen_handler import draw_to_buffer


class Button(sprite.Sprite):

    def __init__(self, button_text=None, input_font=None, font_size=None, font_color=(0, 0, 0), button_image=None, button_color=None, highlight_color=(255, 255, 255), click_color=(0, 0, 0), call_function=None):
        sprite.Sprite.__init__(self)
        self.highlight_color = highlight_color
        self.click_color = click_color
        self.call_function = call_function
        if button_image is not None:
            self.main_surface = surface
        elif button_text is not None and font_size is not None:
            if font is not None:
                draw_font = font.Font(input_font, font_size)
            else:
                draw_font = font.Font(font.match_font('arial'), font_size)
            temp = draw_font.render(button_text, False, font_color)
            self.main_surface = surface.Surface((temp.get_width() + 4, temp.get_height() + 4))
            self.main_surface.set_colorkey(self.main_surface.get_at((0, 0)))
            if button_color is not None:
                draw.rect(self.main_surface, button_color, self.main_surface.get_rect(), border_radius=4)
            self.main_surface.blit(temp, (2, 2))
        self.main_surface.convert()
        self.surface = self.main_surface.copy()
        self.rect = self.surface.get_rect()

    def update(self):
        draw_to_buffer([[self.surface, self.rect]])

    def highlight(self):
        temp_surface = surface.Surface((self.surface.get_width(), self.surface.get_height()))
        temp_surface.convert()
        temp_surface.fill(self.highlight_color)
        temp_surface.set_alpha(64)
        self.surface = self.main_surface.copy()
        self.surface.blit(temp_surface, (0, 0))

    def pressed(self):
        temp_surface = surface.Surface((self.surface.get_width(), self.surface.get_height()))
        temp_surface.convert()
        temp_surface.fill(self.click_color)
        temp_surface.set_alpha(64)
        self.surface = self.main_surface.copy()
        self.surface.blit(temp_surface, (0, 0))

    def default(self):
        self.surface = self.main_surface.copy()

    def update_location(self, location, alignment=None):
        if alignment is None:
            self.rect.topleft = location
        elif alignment == "top right":
            self.rect.topright = location
        elif alignment == "center":
            self.rect.center = location
        elif alignment == "left":
            self.rect.left = location
        elif alignment == "right":
            self.rect.right = location
        elif alignment == "bottom right":
            self.rect.bottomright = location
        elif alignment == "bottom left":
            self.rect.bottomleft = location

    def activate(self):
        if self.call_function is not None:
            self.call_function()

    def set_call_function(self, call_function):
        self.call_function = call_function

    def get_center(self):
        return self.rect.center

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_rect(self):
        return self.rect
