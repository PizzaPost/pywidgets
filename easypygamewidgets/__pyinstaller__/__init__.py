# __init__.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""Internally used to allow using PyInstaller without any errors."""

import os


def get_hook_dirs() -> list[str | bytes]:
	"""Tell PyInstaller where to find hook-easypygamewidgets.py."""
	return [os.path.dirname(__file__)]