# __hook-easypygamewidgets.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""Internally used to allow using PyInstaller without any errors."""

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("easypygamewidgets", subdir="assets")