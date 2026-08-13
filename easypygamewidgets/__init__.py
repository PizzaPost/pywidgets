# __init__.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

from collections.abc import Callable

import pygame

from .button import Button
from .checkbox import Checkbox
from .dialog import Dialog
from .entry import Entry
from .font import default_font, emoji_font, Font, SysFont, tooltip_font
from .label import Label
from .masterWidgets import Widget
from .misc import (create_frames, create_pygame_layer, disable_update_check, link_pygame_window, schedule,
                   set_appearance_mode)
from .screen import Screen
from .slider import Slider
from .surface import Surface
from .timekeeper import Timekeeper
from .tooltip import Tooltip


def flip():
	if not misc.pg:
		misc._check_linked()
	misc._update_clock()
	for widget in misc.all_widgets:
		if isinstance(widget, tuple):
			if isinstance(widget[0], Callable):
				try:
					widget[0]()
				except TypeError:
					pass
		else:
			if hasattr(widget, "update_animation"):
				widget.update_animation()
			widget.draw(misc.pg)
	pygame.display.flip()


def handle_event(event):
	for widget in misc.all_widgets:
		if hasattr(widget, "react"):
			widget.react(event)


def handle_special_events():
	for func in misc._scheduled_functions[:]:
		func[1] -= misc._dt
		if func[1]<=0:
			func[0]()
			misc._scheduled_functions.remove(func)
	for widget in misc.all_widgets:
		if hasattr(widget, "react"):
			widget.react()