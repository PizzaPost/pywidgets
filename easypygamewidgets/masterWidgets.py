import copy
from typing import Any

import pygame

from easypygamewidgets import misc


class Widget:
    def clone(self):
        copied_widget = copy.deepcopy(self)
        misc.all_widgets.append(copied_widget)
        misc.resort_layers()
        return copied_widget

    def bind(self, event: str, command, require_hover: bool = True, widget_boolean_value=None,
             required_value_for_widget_boolean_value: Any = True):
        if widget_boolean_value and not callable(widget_boolean_value):
            print('Please use this bind function as follows: '
                  'entry.bind("<TAB>", lambda: print(1), widget_boolean_value=lambda: entry.focused)')
        self._bindings[event] = {"command": command, "require_hover": require_hover,
                                 "widget_boolean_value": widget_boolean_value,
                                 "required_value_for_widget_boolean_value": required_value_for_widget_boolean_value}
        return self

    def trigger_event(self, event: str, *args, **kwargs):
        if event in self._bindings:
            binding_data = self._bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            widget_boolean_value = binding_data["widget_boolean_value"]
            required_value_for_widget_boolean_value = binding_data["required_value_for_widget_boolean_value"]
            if not require_hover or misc.is_point_over_widget(self, pygame.mouse.get_pos()):
                value = widget_boolean_value() if callable(widget_boolean_value) else widget_boolean_value
                if value is None or value == required_value_for_widget_boolean_value:
                    try:
                        command(self, *args, **kwargs)
                    except TypeError:
                        command(*args, **kwargs)

    def unbind(self, event: str):
        if event in self._bindings:
            del self._bindings[event]
        return self

    def unbind_all(self):
        self._bindings.clear()
        return self

    def place(self, x: int, y: int, mode: str = "px", suppress_anchor: bool = False):
        if mode == "px":
            self._x = x
            self._y = y
        elif mode in ("%", "percent", "percentage"):
            screen_width = misc.pg.get_width()
            screen_height = misc.pg.get_height()
            self._x = int(x * screen_width / 100)
            self._y = int(y * screen_height / 100)
        else:
            self._x = x
            self._y = y
            print(f"Invalid Mode: {mode}\nFallback: px")
        if not suppress_anchor:
            anchor_offset = [0, 0]
            if self._anchor_x == "left":
                anchor_offset[0] = 0
            elif self._anchor_x == "center":
                anchor_offset[0] = self.width // 2
            elif self._anchor_x == "right":
                anchor_offset[0] = self.width
            if self._anchor_y == "top":
                anchor_offset[1] = 0
            elif self._anchor_y == "center":
                anchor_offset[1] = self.height // 2
            elif self._anchor_y == "bottom":
                anchor_offset[1] = self.height
            self.x -= anchor_offset[0]
            self.y -= anchor_offset[1]
        self._rect = pygame.Rect(self._x, self._y, self.width, self.height)
        self._needs_transform = True
        return self

    def anchor(self, anchor_x: str = "left", anchor_y: str = "top"):
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self.place(self._x, self._y)
        return self

    def grid(self, screen: "easypygamewidgets.Screen", row: int, column: int, rowspan: int = 1, columnspan: int = 1):
        if rowspan < 1:
            rowspan = 1
        if columnspan < 1:
            columnspan = 1
        if hasattr(self, "set_screen"):
            self.set_screen(screen)
        self._grid_row = row
        self._grid_column = column
        self._grid_rowspan = rowspan
        self._grid_columnspan = columnspan
        screen.recalculate_grid()
        return self

    def remove_grid(self):
        if hasattr(self, "_grid_row"):
            del self._grid_row
            del self._grid_column
            del self._grid_rowspan
            del self._grid_columnspan
        screen = getattr(self, "screen", None)
        if screen is not None:
            screen.recalculate_grid()
        return self

    def update_animation(self):
        pass

    def draw(self, surface: pygame.Surface):
        pass

    def react(self, event=None):
        pass


class Tooltipable:
    def set_tooltip(self, tooltip):
        self._tooltip = tooltip
        tooltip.configure(layer=self._layer + 1)
        if not tooltip.style:
            tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                              active_unpressed_background_color=self._active_unpressed_background_color,
                              active_unpressed_border_color=self._active_unpressed_border_color)
        return self

    def remove_tooltip(self):
        if self._tooltip:
            self._tooltip.visible = False
            self._tooltip = None
        return self


class Screenable:
    def set_screen(self, screen):
        if screen is None:
            self._screen = None
            return self
        if self in screen.widgets:
            return self
        self._screen = screen
        screen.add_widget(self)
        return self


class Deletable:
    def delete(self):
        self._alive = False
        if self in misc.all_widgets:
            misc.all_widgets.remove(self)
        if getattr(self, "screen", None) is not None:
            if self in self._screen._widgets:
                self._screen._widgets.remove(self)
            self.set_screen(None)