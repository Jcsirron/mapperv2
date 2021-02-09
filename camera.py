import pygame
from screen_handler import SCREEN_SIZE, SCREEN_CENTER


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.rect.Rect(0, 0, width, height)
        self.old_state = pygame.rect.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def rect_apply(self, target_rect):
        return target_rect.move(self.state.topleft)

    def apply_old(self, target):
        return target.rect.move(self.old_state.topleft)

    def update(self, target):
        self.old_state = self.state.copy()
        self.state = self.camera_func(self.state, target.rect)


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect  # l = left,  t = top
    _, _, w, h = camera      # w = width, h = height
    return pygame.rect.Rect(-l+SCREEN_SIZE[0], -t+SCREEN_SIZE[1], w, h)


def complex_camera(camera, target_rect):
    # we want to center target_rect
    x = -target_rect.center[0] + SCREEN_CENTER[0]
    y = -target_rect.center[1] + SCREEN_CENTER[1]
    # move the camera. Let's use some vectors so we can easily substract/multiply
    camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft)) * 0.02  # add some smoothness coolness
    # set max/min x/y so we don't see stuff outside the world
    camera.x = max(-(camera.width-SCREEN_SIZE[0]), min(0, camera.x))
    camera.y = max(-(camera.height-SCREEN_SIZE[1]), min(0, camera.y))

    return camera


def follow_camera(camera, target_rect):
    # we want to center target_rect
    x = -target_rect.center[0] + SCREEN_CENTER[0]
    y = -target_rect.center[1] + SCREEN_CENTER[1]
    # move the camera. Let's use some vectors so we can easily substract/multiply
    camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft)) * 0.1  # add some smoothness coolness
    return camera
