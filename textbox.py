from pygame import rect


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def draw_text_to_surface(surface, text, color, font, anti_aliasing=False, background=None):
    size_rect = surface.get_rect()
    y = size_rect.top
    line_spacing = -2

    # get the height of the font
    font_height = font.get_height()

    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + font_height > size_rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < size_rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if background:
            image = font.render(text[:i], 1, color, background)
            image.set_colorkey(background)
        else:
            image = font.render(text[:i], anti_aliasing, color)
        surface.blit(image, (size_rect.left, y))
        y += font_height + line_spacing
        # remove the text we just blitted
        text = text[i:]
    return text


# The intended purpose of this method is to shrink the text size to fit into the number of rows allotted.
def fit_text_lines_to_surface(surface, text, color, max_size_rect, font, rows, anti_aliasing=False, background=None):
    size_rect = rect.Rect(max_size_rect)
    y = size_rect.top
    line_spacing = -2
