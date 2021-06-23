from pygame import  rect, surface
from screen_handler import SCREEN_SIZE
from pygame.locals import *

# Control Variables
MOVE_UP = K_w
MOVE_DOWN = K_s
MOVE_LEFT = K_a
MOVE_RIGHT = K_d
INTERACT = K_SPACE
MAP = K_m
RETURN = K_BACKSPACE
TAB = K_TAB
SELECT = 1

JOYPAD_NUMBER = 0
JOYPAD_SENSITIVITY = 0.1
JOYSPEED = 10
JOYINTERACT = 0
JOYMAP = 3
JOYRETURN = 1
JOYTAB = 2
JOYSELECT = 5


def format_inputs(keys,  key_events=None, joystick=None, cursor_position=(0, 0)):
    movement = [0, 0]
    cursor = [cursor_position, False]
    # key_output = [INTERACT, RETURN, MAP, TAB]
    key_output = [False, False, False, False]
    # Need to handle the joystick given
    if joystick is not None:
        movement[0], movement[1] = joystick.get_hat(0)
        movement[1] = -movement[1]
        x, y = joystick.get_axis(0), joystick.get_axis(1)
        if x < -JOYPAD_SENSITIVITY:
            movement[0] = -1
        elif x > JOYPAD_SENSITIVITY:
            movement[0] = 1
        if -JOYPAD_SENSITIVITY > y:
            movement[1] = -1
        elif y > JOYPAD_SENSITIVITY:
            movement[1] = 1
        point_x, point_y = joystick.get_axis(2), joystick.get_axis(3)
        if JOYPAD_SENSITIVITY < abs(point_x) and JOYPAD_SENSITIVITY < abs(point_y):
            cursor[0] = (max(0, min(SCREEN_SIZE[0] - 8, cursor_position[0] + int(point_x * JOYSPEED))), max(0, min(SCREEN_SIZE[1] - 8, cursor_position[1] + int(point_y * JOYSPEED))))
        elif JOYPAD_SENSITIVITY < abs(point_x):
            cursor[0] = (max(0, min(SCREEN_SIZE[0] - 8, cursor_position[0] + int(point_x * JOYSPEED))), cursor_position[1])
        elif JOYPAD_SENSITIVITY < abs(point_y):
            cursor[0] = (cursor_position[0], max(0, min(SCREEN_SIZE[1] - 8, cursor_position[1] + int(point_y * JOYSPEED))))
    # This area is for where the button needs to be pressed constantly
    if keys[MOVE_DOWN]:
        movement[1] = 1
    elif keys[MOVE_UP]:
        movement[1] = -1
    if keys[MOVE_LEFT]:
        movement[0] = -1
    elif keys[MOVE_RIGHT]:
        movement[0] = 1
    if keys[TAB] or (joystick is not None and joystick.get_button(JOYTAB)):
        key_output[3] = True
    # This area is for where the button needs to be pressed and released once
    for event in key_events:
        if event.type == KEYUP:
            if event.key == INTERACT:
                key_output[0] = True
            elif event.key == RETURN:
                key_output[1] = True
            elif event.key == MAP:
                key_output[2] = True
            elif event.key == TAB:
                key_output[3] = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == SELECT:
                cursor[1] = True
        elif event.type == JOYBUTTONUP:
            if event.button == JOYINTERACT:
                key_output[0] = True
                cursor[1] = True
            elif event.button == JOYRETURN:
                key_output[1] = True
            elif event.button == JOYMAP:
                key_output[2] = True
            elif event.button == JOYTAB:
                key_output[3] = True
            elif event.button == JOYSELECT:
                cursor[1] = True
        elif event.type == MOUSEMOTION:
            cursor[0] = event.pos
    return [movement, cursor, key_output]
