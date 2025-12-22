from .button import Button
from .misc import check_update, link_pygame_window


def flip():
    for b in button.all_buttons:
        button.draw(b, misc.pg)


def handle_event(event):
    if len(button.all_buttons) > 0:
        for b in button.all_buttons:
            button.react(b, event)


def handle_special_events():
    if len(button.all_buttons) > 0:
        for b in button.all_buttons:
            button.react(b)
