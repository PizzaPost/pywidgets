from .button import Button
from .misc import check_update, link_pygame_window
from .slider import Slider


def flip():
    if not misc.pg:
        misc.check_linked()
    for b in button.all_buttons:
        button.draw(b, misc.pg)
    for s in slider.all_sliders:
        slider.draw(s, misc.pg)


def handle_event(event):
    if len(button.all_buttons) > 0:
        for b in button.all_buttons:
            button.react(b, event)
    if len(slider.all_sliders) > 0:
        for s in slider.all_sliders:
            slider.react(s, event)


def handle_special_events():
    if len(button.all_buttons) > 0:
        for b in button.all_buttons:
            button.react(b)
    if len(slider.all_sliders) > 0:
        for s in slider.all_sliders:
            slider.react(s)
