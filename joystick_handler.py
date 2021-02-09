import pygame.joystick


def get_joysticks(joystick_number=None):
    # Get the state of all the joystick
    joystick_count = pygame.joystick.get_count()
    return_joystick_status = {}
    if joystick_number is not None and joystick_count >= joystick_number:
        joystick = pygame.joystick.Joystick(joystick_number)
        joystick.init()
        return_joystick_status[str(joystick_number)] = {}

        joystick_hats = joystick.get_numhats()
        for hat in range(joystick_hats):
            return_joystick_status[str(joystick_number)]["hat " + str(hat)] = joystick.get_hat(hat)

        joystick_buttons = joystick.get_numbuttons()
        return_joystick_status[str(joystick_number)]["buttons"] = [0] * joystick_buttons
        for button in range(joystick_buttons):
            return_joystick_status[str(joystick_number)]["buttons"][button] = joystick.get_button(button)

        joystick_axes = joystick.get_numaxes()
        for axis in range(joystick_axes):
            return_joystick_status[str(joystick_number)]["axis " + str(axis)] = round(joystick.get_axis(axis), 3)
    elif joystick_number is None:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            return_joystick_status[str(i)] = {}

            joystick_hats = joystick.get_numhats()
            for hat in range(joystick_hats):
                return_joystick_status[str(i)]["hat " + str(hat)] = joystick.get_hat(hat)

            joystick_buttons = joystick.get_numbuttons()
            return_joystick_status[str(i)]["buttons"] = [0] * joystick_buttons
            for button in range(joystick_buttons):
                return_joystick_status[str(i)]["buttons"][button] = joystick.get_button(button)

            joystick_axes = joystick.get_numaxes()
            for axis in range(joystick_axes):
                return_joystick_status[str(i)]["axis " + str(axis)] = round(joystick.get_axis(axis), 3)
    return return_joystick_status
