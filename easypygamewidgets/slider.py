# slider.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import math
from typing import Any

import pygame

from easypygamewidgets import font, misc
from easypygamewidgets.masterWidget import Widget, Tooltipable

pygame.init()


# PERFECTION
# everything private/properties ❌
# basic animations ❌
# cache system ❌
# config suggestions ❌
# optimized set_screen function ❌
# rgba color ❌

class Slider(Widget, Tooltipable):
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 16,
                 text: str = "easypygamewidgets Slider", start: int | float = 0,
                 end: int | float = 100, initial_value: int | None = None, state: str | None = None,
                 top_left_corner_radius: int = 25,
                 top_right_corner_radius: int = 25,
                 bottom_left_corner_radius: int = 25,
                 bottom_right_corner_radius: int = 25,
                 dot_radius: int | None = None,
                 max_extra_dot_radius: int | None = None,
                 move_text_with_dot_radius: bool = False,
                 active_unpressed_text_color: tuple = (255, 255, 255),
                 disabled_unpressed_text_color: tuple = (150, 150, 150),
                 active_hover_text_color: tuple = (255, 255, 255),
                 disabled_hover_text_color: tuple = (150, 150, 150),
                 active_pressed_text_color: tuple = (255, 255, 255),
                 active_unpressed_used_background_color: tuple = (30, 30, 30),
                 disabled_unpressed_used_background_color: tuple = (20, 20, 20),
                 active_hover_used_background_color: tuple = (30, 30, 30),
                 disabled_hover_used_background_color: tuple = (20, 20, 20),
                 active_pressed_used_background_color: tuple = (30, 30, 30),
                 active_unpressed_unused_background_color: tuple = (60, 60, 60),
                 disabled_unpressed_unused_background_color: tuple = (30, 30, 30),
                 active_hover_unused_background_color: tuple = (60, 60, 60),
                 disabled_hover_unused_background_color: tuple = (30, 30, 30),
                 active_pressed_unused_background_color: tuple = (60, 60, 60),
                 active_unpressed_dot_color: tuple = (255, 255, 255),
                 disabled_unpressed_dot_color: tuple = (150, 150, 150),
                 active_hover_dot_color: tuple = (255, 255, 255),
                 disabled_hover_dot_color: tuple = (150, 150, 150),
                 active_pressed_dot_color: tuple = (200, 200, 200),
                 active_unpressed_border_color: tuple = (100, 100, 100),
                 disabled_unpressed_border_color: tuple = (60, 60, 60),
                 active_hover_border_color: tuple = (150, 150, 150),
                 disabled_hover_border_color: tuple = (60, 60, 60),
                 active_pressed_border_color: tuple = (150, 150, 150),
                 active_pressed_display_color: tuple = (190, 190, 190),
                 active_hover_display_color: tuple = (190, 190, 190),
                 active_unpressed_display_color: tuple = (190, 190, 190),
                 disabled_hover_display_color: tuple = (150, 150, 150),
                 disabled_unpressed_display_color: tuple = (150, 150, 150),
                 border_width: int = 2,
                 hide_text: bool = False,
                 hide_used_background: bool = False,
                 hide_unused_background: bool = False,
                 hide_dot: bool = False,
                 hide_border: bool = False,
                 hide_display: bool = False,
                 active_hover_cursor: pygame.Cursor | None = None,
                 disabled_hover_cursor: pygame.Cursor | None = None,
                 active_pressed_cursor: pygame.Cursor | None = None,
                 font: pygame.font.Font | pygame.font.SysFont = font.default_font, alignment: str = "center",
                 alignment_spacing: int = 20, show_value_when_pressed: bool = True,
                 show_value_when_hovered: bool = True, show_value_when_unpressed: bool = False,
                 show_value_when_disabled: bool = False, round_display_value: int = 0,
                 show_full_rounding_of_whole_numbers: bool = False, trigger_hold_delay: int = 150, layer=1000,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, line_spacing: int = 30,
                 min_width: int | None = None, max_width: int | None = None, min_height: int | None = None,
                 max_height: int | None = None, anchor_x: str = "left", anchor_y: str = "top", visible: bool = True,
                 data: Any = None):
        super().__init__()
        if screen:
            screen.add_widget(self)
            self._screen = screen
            if state:
                self._state = state
        else:
            self._screen = None
            self._visible = visible
            if state:
                self._state = state
            else:
                self._state = "enabled"
        self._auto_size = auto_size
        self._width = width
        self._height = height
        if auto_size:
            if min_width:
                self._width = max(width, min_width)
            if max_width:
                self._width = min(width, max_width)
            if min_height:
                self._height = max(height, min_height)
            if max_height:
                self._height = min(height, max_height)
        self._text = text
        self._start = start
        self._start = start
        self._end = end
        self._value = min(max(initial_value or start, start), end)
        self._top_left_corner_radius = top_left_corner_radius
        self._top_right_corner_radius = top_right_corner_radius
        self._bottom_left_corner_radius = bottom_left_corner_radius
        self._bottom_right_corner_radius = bottom_right_corner_radius
        if not dot_radius:
            self._dot_radius = height // 2
        else:
            self._dot_radius = dot_radius
        if not max_extra_dot_radius:
            self._max_extra_dot_radius = self._dot_radius // 5 + 1
        else:
            self._max_extra_dot_radius = max_extra_dot_radius
        self._move_text_with_dot_radius = move_text_with_dot_radius
        self._active_unpressed_text_color = active_unpressed_text_color
        self._disabled_unpressed_text_color = disabled_unpressed_text_color
        self._active_hover_text_color = active_hover_text_color
        self._disabled_hover_text_color = disabled_hover_text_color
        self._active_pressed_text_color = active_pressed_text_color
        self._active_unpressed_used_background_color = active_unpressed_used_background_color
        self._disabled_unpressed_used_background_color = disabled_unpressed_used_background_color
        self._active_hover_used_background_color = active_hover_used_background_color
        self._disabled_hover_used_background_color = disabled_hover_used_background_color
        self._active_pressed_used_background_color = active_pressed_used_background_color
        self._active_unpressed_unused_background_color = active_unpressed_unused_background_color
        self._disabled_unpressed_unused_background_color = disabled_unpressed_unused_background_color
        self._active_hover_unused_background_color = active_hover_unused_background_color
        self._disabled_hover_unused_background_color = disabled_hover_unused_background_color
        self._active_pressed_unused_background_color = active_pressed_unused_background_color
        self._active_unpressed_dot_color = active_unpressed_dot_color
        self._disabled_unpressed_dot_color = disabled_unpressed_dot_color
        self._active_hover_dot_color = active_hover_dot_color
        self._disabled_hover_dot_color = disabled_hover_dot_color
        self._active_pressed_dot_color = active_pressed_dot_color
        self._active_unpressed_border_color = active_unpressed_border_color
        self._disabled_unpressed_border_color = disabled_unpressed_border_color
        self._active_hover_border_color = active_hover_border_color
        self._disabled_hover_border_color = disabled_hover_border_color
        self._active_pressed_border_color = active_pressed_border_color
        self._active_pressed_display_color = active_pressed_display_color
        self._active_hover_display_color = active_hover_display_color
        self._active_unpressed_display_color = active_unpressed_display_color
        self._disabled_hover_display_color = disabled_hover_display_color
        self._disabled_unpressed_display_color = disabled_unpressed_display_color
        self._border_width = border_width
        self._hide_text = hide_text
        self._hide_used_background = hide_used_background
        self._hide_unused_background = hide_unused_background
        self._hide_dot = hide_dot
        self._hide_border = hide_border
        self._hide_display = hide_display
        cursor_input = {
            "active_hover": active_hover_cursor,
            "disabled_hover": disabled_hover_cursor,
            "active_pressed": active_pressed_cursor
        }
        self._cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, pygame.cursors.Cursor):
                self._cursors[name] = cursor
            else:
                if cursor is not None:
                    print(
                        f"No custom cursor is used for the slider {text} because it's not a pygame.Cursor object. ({cursor})")
                self._cursors[name] = None
        self._font = font
        self._alignment = alignment
        self._alignment_spacing = alignment_spacing
        self._show_value_when_pressed = show_value_when_pressed
        self._show_value_when_hovered = show_value_when_hovered
        self._show_value_when_unpressed = show_value_when_unpressed
        self._show_value_when_disabled = show_value_when_disabled
        self._round_display_value = round_display_value
        self._show_full_rounding_of_whole_numbers = show_full_rounding_of_whole_numbers
        self._trigger_hold_delay = trigger_hold_delay
        self._layer = layer
        self._tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self._layer + 1)
            if not tooltip.style:
                tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                                  active_unpressed_background_color=self._active_unpressed_used_background_color,
                                  active_unpressed_border_color=self._active_unpressed_border_color)
        self._line_spacing = line_spacing
        self._min_width = min_width
        self._max_width = max_width
        self._min_height = min_height
        self._max_height = max_height
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self._data = data
        self._x = 0
        self._y = 0
        self._alive = True
        self._pressed = False
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._original_cursor = None
        self._extra_dot_radius = 0
        self._pressed_before = False
        self._last_value_update_time = 0
        self._bindings = {}

        safe_set_linesize(font, line_spacing)

        misc.add_widget(self)

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self.set_screen(value)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def auto_size(self):
        return self._auto_size

    @auto_size.setter
    def auto_size(self, value):
        self._auto_size = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def top_left_corner_radius(self):
        return self._top_left_corner_radius

    @top_left_corner_radius.setter
    def top_left_corner_radius(self, value):
        self._top_left_corner_radius = value

    @property
    def top_right_corner_radius(self):
        return self._top_right_corner_radius

    @top_right_corner_radius.setter
    def top_right_corner_radius(self, value):
        self._top_right_corner_radius = value

    @property
    def bottom_left_corner_radius(self):
        return self._bottom_left_corner_radius

    @bottom_left_corner_radius.setter
    def bottom_left_corner_radius(self, value):
        self._bottom_left_corner_radius = value

    @property
    def bottom_right_corner_radius(self):
        return self._bottom_right_corner_radius

    @bottom_right_corner_radius.setter
    def bottom_right_corner_radius(self, value):
        self._bottom_right_corner_radius = value

    @property
    def dot_radius(self):
        return self._dot_radius

    @dot_radius.setter
    def dot_radius(self, value):
        self._dot_radius = value

    @property
    def max_extra_dot_radius(self):
        return self._max_extra_dot_radius

    @max_extra_dot_radius.setter
    def max_extra_dot_radius(self, value):
        self._max_extra_dot_radius = value

    @property
    def move_text_with_dot_radius(self):
        return self._move_text_with_dot_radius

    @move_text_with_dot_radius.setter
    def move_text_with_dot_radius(self, value):
        self._move_text_with_dot_radius = value

    @property
    def active_unpressed_text_color(self):
        return self._active_unpressed_text_color

    @active_unpressed_text_color.setter
    def active_unpressed_text_color(self, value):
        self._active_unpressed_text_color = value

    @property
    def disabled_unpressed_text_color(self):
        return self._disabled_unpressed_text_color

    @disabled_unpressed_text_color.setter
    def disabled_unpressed_text_color(self, value):
        self._disabled_unpressed_text_color = value

    @property
    def active_hover_text_color(self):
        return self._active_hover_text_color

    @active_hover_text_color.setter
    def active_hover_text_color(self, value):
        self._active_hover_text_color = value

    @property
    def disabled_hover_text_color(self):
        return self._disabled_hover_text_color

    @disabled_hover_text_color.setter
    def disabled_hover_text_color(self, value):
        self._disabled_hover_text_color = value

    @property
    def active_pressed_text_color(self):
        return self._active_pressed_text_color

    @active_pressed_text_color.setter
    def active_pressed_text_color(self, value):
        self._active_pressed_text_color = value

    @property
    def active_unpressed_used_background_color(self):
        return self._active_unpressed_used_background_color

    @active_unpressed_used_background_color.setter
    def active_unpressed_used_background_color(self, value):
        self._active_unpressed_used_background_color = value

    @property
    def disabled_unpressed_used_background_color(self):
        return self._disabled_unpressed_used_background_color

    @disabled_unpressed_used_background_color.setter
    def disabled_unpressed_used_background_color(self, value):
        self._disabled_unpressed_used_background_color = value

    @property
    def active_hover_used_background_color(self):
        return self._active_hover_used_background_color

    @active_hover_used_background_color.setter
    def active_hover_used_background_color(self, value):
        self._active_hover_used_background_color = value

    @property
    def disabled_hover_used_background_color(self):
        return self._disabled_hover_used_background_color

    @disabled_hover_used_background_color.setter
    def disabled_hover_used_background_color(self, value):
        self._disabled_hover_used_background_color = value

    @property
    def active_pressed_used_background_color(self):
        return self._active_pressed_used_background_color

    @active_pressed_used_background_color.setter
    def active_pressed_used_background_color(self, value):
        self._active_pressed_used_background_color = value

    @property
    def active_unpressed_unused_background_color(self):
        return self._active_unpressed_unused_background_color

    @active_unpressed_unused_background_color.setter
    def active_unpressed_unused_background_color(self, value):
        self._active_unpressed_unused_background_color = value

    @property
    def disabled_unpressed_unused_background_color(self):
        return self._disabled_unpressed_unused_background_color

    @disabled_unpressed_unused_background_color.setter
    def disabled_unpressed_unused_background_color(self, value):
        self._disabled_unpressed_unused_background_color = value

    @property
    def active_hover_unused_background_color(self):
        return self._active_hover_unused_background_color

    @active_hover_unused_background_color.setter
    def active_hover_unused_background_color(self, value):
        self._active_hover_unused_background_color = value

    @property
    def disabled_hover_unused_background_color(self):
        return self._disabled_hover_unused_background_color

    @disabled_hover_unused_background_color.setter
    def disabled_hover_unused_background_color(self, value):
        self._disabled_hover_unused_background_color = value

    @property
    def active_pressed_unused_background_color(self):
        return self._active_pressed_unused_background_color

    @active_pressed_unused_background_color.setter
    def active_pressed_unused_background_color(self, value):
        self._active_pressed_unused_background_color = value

    @property
    def active_unpressed_dot_color(self):
        return self._active_unpressed_dot_color

    @active_unpressed_dot_color.setter
    def active_unpressed_dot_color(self, value):
        self._active_unpressed_dot_color = value

    @property
    def disabled_unpressed_dot_color(self):
        return self._disabled_unpressed_dot_color

    @disabled_unpressed_dot_color.setter
    def disabled_unpressed_dot_color(self, value):
        self._disabled_unpressed_dot_color = value

    @property
    def active_hover_dot_color(self):
        return self._active_hover_dot_color

    @active_hover_dot_color.setter
    def active_hover_dot_color(self, value):
        self._active_hover_dot_color = value

    @property
    def disabled_hover_dot_color(self):
        return self._disabled_hover_dot_color

    @disabled_hover_dot_color.setter
    def disabled_hover_dot_color(self, value):
        self._disabled_hover_dot_color = value

    @property
    def active_pressed_dot_color(self):
        return self._active_pressed_dot_color

    @active_pressed_dot_color.setter
    def active_pressed_dot_color(self, value):
        self._active_pressed_dot_color = value

    @property
    def active_unpressed_border_color(self):
        return self._active_unpressed_border_color

    @active_unpressed_border_color.setter
    def active_unpressed_border_color(self, value):
        self._active_unpressed_border_color = value

    @property
    def disabled_unpressed_border_color(self):
        return self._disabled_unpressed_border_color

    @disabled_unpressed_border_color.setter
    def disabled_unpressed_border_color(self, value):
        self._disabled_unpressed_border_color = value

    @property
    def active_hover_border_color(self):
        return self._active_hover_border_color

    @active_hover_border_color.setter
    def active_hover_border_color(self, value):
        self._active_hover_border_color = value

    @property
    def disabled_hover_border_color(self):
        return self._disabled_hover_border_color

    @disabled_hover_border_color.setter
    def disabled_hover_border_color(self, value):
        self._disabled_hover_border_color = value

    @property
    def active_pressed_border_color(self):
        return self._active_pressed_border_color

    @active_pressed_border_color.setter
    def active_pressed_border_color(self, value):
        self._active_pressed_border_color = value

    @property
    def active_pressed_display_color(self):
        return self._active_pressed_display_color

    @active_pressed_display_color.setter
    def active_pressed_display_color(self, value):
        self._active_pressed_display_color = value

    @property
    def active_hover_display_color(self):
        return self._active_hover_display_color

    @active_hover_display_color.setter
    def active_hover_display_color(self, value):
        self._active_hover_display_color = value

    @property
    def active_unpressed_display_color(self):
        return self._active_unpressed_display_color

    @active_unpressed_display_color.setter
    def active_unpressed_display_color(self, value):
        self._active_unpressed_display_color = value

    @property
    def disabled_hover_display_color(self):
        return self._disabled_hover_display_color

    @disabled_hover_display_color.setter
    def disabled_hover_display_color(self, value):
        self._disabled_hover_display_color = value

    @property
    def disabled_unpressed_display_color(self):
        return self._disabled_unpressed_display_color

    @disabled_unpressed_display_color.setter
    def disabled_unpressed_display_color(self, value):
        self._disabled_unpressed_display_color = value

    @property
    def border_width(self):
        return self._border_width

    @border_width.setter
    def border_width(self, value):
        self._border_width = value

    @property
    def hide_text(self):
        return self._hide_text

    @hide_text.setter
    def hide_text(self, value):
        self._hide_text = value

    @property
    def hide_used_background(self):
        return self._hide_used_background

    @hide_used_background.setter
    def hide_used_background(self, value):
        self._hide_used_background = value

    @property
    def hide_unused_background(self):
        return self._hide_unused_background

    @hide_unused_background.setter
    def hide_unused_background(self, value):
        self._hide_unused_background = value

    @property
    def hide_dot(self):
        return self._hide_dot

    @hide_dot.setter
    def hide_dot(self, value):
        self._hide_dot = value

    @property
    def hide_border(self):
        return self._hide_border

    @hide_border.setter
    def hide_border(self, value):
        self._hide_border = value

    @property
    def hide_display(self):
        return self._hide_display

    @hide_display.setter
    def hide_display(self, value):
        self._hide_display = value

    @property
    def active_hover_cursor(self):
        return self._cursors["active_hover"]

    @active_hover_cursor.setter
    def active_hover_cursor(self, value):
        self._cursors["active_hover"] = value

    @property
    def disabled_hover_cursor(self):
        return self._cursors["disabled_hover"]

    @disabled_hover_cursor.setter
    def disabled_hover_cursor(self, value):
        self._cursors["disabled_hover"] = value

    @property
    def active_pressed_cursor(self):
        return self._cursors["active_pressed"]

    @active_pressed_cursor.setter
    def active_pressed_cursor(self, value):
        self._cursors["active_pressed"] = value

    @property
    def cursors(self):
        return self._cursors

    @cursors.setter
    def cursors(self, value):
        self._cursors = value

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value

    @property
    def alignment_spacing(self):
        return self._alignment_spacing

    @alignment_spacing.setter
    def alignment_spacing(self, value):
        self._alignment_spacing = value

    @property
    def show_value_when_pressed(self):
        return self._show_value_when_pressed

    @show_value_when_pressed.setter
    def show_value_when_pressed(self, value):
        self._show_value_when_pressed = value

    @property
    def show_value_when_hovered(self):
        return self._show_value_when_hovered

    @show_value_when_hovered.setter
    def show_value_when_hovered(self, value):
        self._show_value_when_hovered = value

    @property
    def show_value_when_unpressed(self):
        return self._show_value_when_unpressed

    @show_value_when_unpressed.setter
    def show_value_when_unpressed(self, value):
        self._show_value_when_unpressed = value

    @property
    def show_value_when_disabled(self):
        return self._show_value_when_disabled

    @show_value_when_disabled.setter
    def show_value_when_disabled(self, value):
        self._show_value_when_disabled = value

    @property
    def round_display_value(self):
        return self._round_display_value

    @round_display_value.setter
    def round_display_value(self, value):
        self._round_display_value = value

    @property
    def show_full_rounding_of_whole_numbers(self):
        return self._show_full_rounding_of_whole_numbers

    @show_full_rounding_of_whole_numbers.setter
    def show_full_rounding_of_whole_numbers(self, value):
        self._show_full_rounding_of_whole_numbers = value

    @property
    def trigger_hold_delay(self):
        return self._trigger_hold_delay

    @trigger_hold_delay.setter
    def trigger_hold_delay(self, value):
        self._trigger_hold_delay = value

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value
        if self._tooltip:
            self._tooltip.configure(layer=self._layer + 1)
        misc.resort_layers()

    @property
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._tooltip = value

    @property
    def line_spacing(self):
        return self._line_spacing

    @line_spacing.setter
    def line_spacing(self, value):
        self._line_spacing = value

    @property
    def min_width(self):
        return self._min_width

    @min_width.setter
    def min_width(self, value):
        self._min_width = value

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, value):
        self._max_width = value

    @property
    def min_height(self):
        return self._min_height

    @min_height.setter
    def min_height(self, value):
        self._min_height = value

    @property
    def max_height(self):
        return self._max_height

    @max_height.setter
    def max_height(self, value):
        self._max_height = value

    @property
    def anchor_x(self):
        return self._anchor_x

    @anchor_x.setter
    def anchor_x(self, value):
        self._anchor_x = value

    @property
    def anchor_y(self):
        return self._anchor_y

    @anchor_y.setter
    def anchor_y(self, value):
        self._anchor_y = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value

    @property
    def pressed(self):
        return self._pressed

    @pressed.setter
    def pressed(self, value):
        self._pressed = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def original_cursor(self):
        return self._original_cursor

    @original_cursor.setter
    def original_cursor(self, value):
        self._original_cursor = value

    @property
    def extra_dot_radius(self):
        return self._extra_dot_radius

    @extra_dot_radius.setter
    def extra_dot_radius(self, value):
        self._extra_dot_radius = value

    @property
    def pressed_before(self):
        return self._pressed_before

    @pressed_before.setter
    def pressed_before(self, value):
        self._pressed_before = value

    @property
    def last_value_update_time(self):
        return self._last_value_update_time

    @last_value_update_time.setter
    def last_value_update_time(self, value):
        self._last_value_update_time = value

    @property
    def bindings(self):
        return self._bindings

    @bindings.setter
    def bindings(self, value):
        self._bindings = value

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if any(k in kwargs for k in
               ('auto_size', 'x', 'y', 'width', 'height', 'min_width', 'max_width', 'min_height', 'max_height')):
            if self._auto_size:
                if self._min_width:
                    self._width = max(self._width, self._min_width)
                if self._max_width:
                    self._width = min(self._width, self._max_width)
                if self._min_height:
                    self._height = max(self._height, self._min_height)
                if self._max_height:
                    self._height = min(self._height, self._max_height)
            self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        if 'layer' in kwargs:
            misc.resort_layers()
        if 'line_spacing' in kwargs or 'font' in kwargs:
            safe_set_linesize(self._font, self._line_spacing)
        return self

    def config(self, **kwargs):
        self.configure(**kwargs)

    def get(self):
        return self._value

    def set(self, value):
        self._value = min(max(value, self._start), self._end)


def safe_set_linesize(font, line_spacing):
    descent = abs(font.get_descent())
    font.set_linesize(line_spacing + descent)


def draw(slider, surface: pygame.Surface):
    if not slider.alive or not slider.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = misc.is_point_over_widget(slider, mouse_pos)
    if slider.state == "enabled":
        if slider.pressed:
            text_color = slider.active_pressed_text_color
            bg_color_used = slider.active_pressed_used_background_color
            bg_color_unused = slider.active_pressed_unused_background_color
            brd_color = slider.active_pressed_border_color
            dot_color = slider.active_pressed_dot_color
            display_color = slider.active_pressed_display_color
        elif is_hovering:
            text_color = slider.active_hover_text_color
            bg_color_used = slider.active_hover_used_background_color
            bg_color_unused = slider.active_hover_unused_background_color
            brd_color = slider.active_hover_border_color
            dot_color = slider.active_hover_dot_color
            display_color = slider.active_hover_display_color
        else:
            text_color = slider.active_unpressed_text_color
            bg_color_used = slider.active_unpressed_used_background_color
            bg_color_unused = slider.active_unpressed_unused_background_color
            brd_color = slider.active_unpressed_border_color
            dot_color = slider.active_unpressed_dot_color
            display_color = slider.active_unpressed_display_color
    else:
        if is_hovering:
            text_color = slider.disabled_hover_text_color
            bg_color_used = slider.disabled_hover_used_background_color
            bg_color_unused = slider.disabled_hover_unused_background_color
            brd_color = slider.disabled_hover_border_color
            dot_color = slider.disabled_hover_dot_color
            display_color = slider.disabled_hover_display_color
        else:
            text_color = slider.disabled_unpressed_text_color
            bg_color_used = slider.disabled_unpressed_used_background_color
            bg_color_unused = slider.disabled_unpressed_unused_background_color
            brd_color = slider.disabled_unpressed_border_color
            dot_color = slider.disabled_unpressed_dot_color
            display_color = slider.disabled_unpressed_display_color

    if is_hovering:
        if slider.state == "enabled":
            if slider.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = slider.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if slider.original_cursor is None:
                    slider.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if slider.original_cursor:
            pygame.mouse.set_cursor(slider.original_cursor)
            slider.original_cursor = None

    if is_hovering and not getattr(slider, "is_hovered", False):
        slider.is_hovered = True
        slider.trigger_event("<MOUSE-IN>")
        if slider.tooltip:
            slider.tooltip.show()
    elif is_hovering and getattr(slider, "is_hovered", False):
        slider.is_hovered = True
        slider.trigger_event("<HOVER>")
    elif not is_hovering and getattr(slider, "is_hovered", False):
        slider.is_hovered = False
        slider.trigger_event("<MOUSE-OUT>")
        if slider.tooltip:
            slider.tooltip.hide()
    if slider.tooltip:
        if slider.tooltip.visible:
            if not slider.pressed and not is_hovering:
                slider.tooltip.hide()

    temp_surf = slider.font.render(slider.text, True, text_color)
    if slider.auto_size:
        slider.width = temp_surf.get_width() + 40 + (slider.alignment_spacing - 20)
        if slider.min_width:
            slider.width = max(slider.width, slider.min_width)
        if slider.max_width:
            slider.width = min(slider.width, slider.max_width)
        if slider.min_height:
            slider.height = max(slider.height, slider.min_height)
        if slider.max_height:
            slider.height = min(slider.height, slider.max_height)
        slider.rect = pygame.Rect(slider.x, slider.y, slider.width, slider.height)

    offset_x, offset_y = misc.get_screen_offset(slider)
    draw_rect = slider.rect.move(offset_x, offset_y)

    text_height = temp_surf.get_height()
    track_y = draw_rect.top + text_height + 10 + slider.height // 2
    track_rect = pygame.Rect(draw_rect.x, track_y - (slider.height // 2), draw_rect.width, slider.height)
    max_radius = min(track_rect.width, track_rect.height) // 2
    tl = min(slider.top_left_corner_radius, max_radius)
    tr = min(slider.top_right_corner_radius, max_radius)
    bl = min(slider.bottom_left_corner_radius, max_radius)
    br = min(slider.bottom_right_corner_radius, max_radius)
    if not slider.hide_unused_background:
        pygame.draw.rect(surface, bg_color_unused, track_rect, border_top_left_radius=tl, border_top_right_radius=tr,
                         border_bottom_left_radius=bl, border_bottom_right_radius=br)
    if slider.end - slider.start != 0:
        pct = (slider.value - slider.start) / (slider.end - slider.start)
    else:
        pct = 0
    pct = max(0, min(1, pct))
    used_width = int(track_rect.width * pct)
    if used_width > 0 and not slider.hide_used_background:
        clip_surf = pygame.Surface(track_rect.size, pygame.SRCALPHA)
        mask_rect = pygame.Rect(0, 0, track_rect.width, track_rect.height)
        pygame.draw.rect(clip_surf, (255, 255, 255), mask_rect, border_top_left_radius=tl,
                         border_bottom_left_radius=bl, border_top_right_radius=tr, border_bottom_right_radius=br)
        used_fill_rect = pygame.Rect(0, 0, used_width, track_rect.height)
        fill_surf = pygame.Surface(track_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(fill_surf, bg_color_used, used_fill_rect)
        clip_surf.blit(fill_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        surface.blit(clip_surf, track_rect.topleft)
    if brd_color and not slider.hide_border:
        pygame.draw.rect(surface, brd_color, track_rect, width=slider.border_width, border_top_left_radius=tl,
                         border_top_right_radius=tr, border_bottom_left_radius=bl, border_bottom_right_radius=br)
    dot_x = track_rect.x + used_width
    dot_x = max(track_rect.left + slider.dot_radius, min(dot_x, track_rect.right - slider.dot_radius))
    if not slider.hide_dot:
        pygame.draw.aacircle(surface, dot_color, (int(dot_x), int(track_rect.centery)),
                             slider.dot_radius + slider.extra_dot_radius)
    if not slider.hide_display:
        if (slider.state == "enabled" or slider.show_value_when_disabled) and (
                slider.show_value_when_pressed and slider.pressed or slider.show_value_when_hovered and is_hovering and not slider.pressed or slider.show_value_when_unpressed):
            if slider.show_full_rounding_of_whole_numbers:
                text_surf = slider.font.render(str(round(slider.value, slider.round_display_value)), True,
                                               display_color)
            elif not slider.show_full_rounding_of_whole_numbers and round(slider.value,
                                                                          slider.round_display_value) % 1 == 0:
                text_surf = slider.font.render(str(round(slider.value, slider.round_display_value)).replace(".0", ""),
                                               True, display_color)
            elif not slider.show_full_rounding_of_whole_numbers:
                text_surf = slider.font.render(str(round(slider.value, slider.round_display_value)), True,
                                               display_color)
            text_rect = text_surf.get_rect()
            if slider.move_text_with_dot_radius:
                text_rect.center = (dot_x, track_rect.centery + 25 + slider.dot_radius + slider.extra_dot_radius)
            else:
                text_rect.center = (dot_x, track_rect.centery + 25 + slider.dot_radius)
            surface.blit(text_surf, text_rect)

    if not slider.hide_text:
        text_surf = slider.font.render(slider.text, True, text_color)
        text_rect = text_surf.get_rect()
        if slider.move_text_with_dot_radius:
            text_y_center = track_rect.centery - 25 - slider.dot_radius - slider.extra_dot_radius
        else:
            text_y_center = track_rect.centery - 25 - slider.dot_radius

        if slider.alignment == "stretched" and len(slider.text) > 1 and not slider.auto_size:
            total_char_width = sum(slider.font.render(char, True, text_color).get_width() for char in slider.text)
            available_width = draw_rect.width - (slider.alignment_spacing * 2)
            if available_width > total_char_width:
                spacing = (available_width - total_char_width) / (len(slider.text) - 1)
                current_x = draw_rect.left + slider.alignment_spacing
                for char in slider.text:
                    char_surf = slider.font.render(char, True, text_color)
                    surface.blit(char_surf, char_surf.get_rect(midleft=(current_x, text_y_center)))
                    current_x += char_surf.get_width() + spacing
            else:
                surface.blit(text_surf, text_surf.get_rect(center=(draw_rect.centerx, text_y_center)))
        else:
            if slider.alignment == "left":
                text_rect.midleft = (draw_rect.left + slider.alignment_spacing, text_y_center)
            elif slider.alignment == "right":
                text_rect.midright = (draw_rect.right - slider.alignment_spacing, text_y_center)
            else:
                text_rect.center = (draw_rect.centerx, text_y_center)
            surface.blit(text_surf, text_rect)


def react(slider, event=None):
    if slider.state != "enabled" or not slider.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    is_inside = misc.is_point_over_widget(slider, mouse_pos)

    def update_value():
        offset_x, offset_y = misc.get_screen_offset(slider)
        draw_rect = slider.rect.move(offset_x, offset_y)

        temp_surf = slider.font.render(slider.text, True, (0, 0, 0))
        text_height = temp_surf.get_height()
        track_y = draw_rect.top + text_height + 10 + slider.height // 2
        track_rect = pygame.Rect(draw_rect.x, track_y - (slider.height // 2), draw_rect.width, slider.height)
        relative_x = mouse_pos[0] - track_rect.x
        pct = relative_x / track_rect.width
        pct = max(0, min(1, pct))
        new_slider_value = slider.start + (pct * (slider.end - slider.start))
        moved = slider.value != new_slider_value
        slider.value = new_slider_value
        current_time = pygame.time.get_ticks()
        if not slider.pressed_before:
            slider.trigger_event("<PRESS>")
            slider.pressed_before = True
        else:
            if moved:
                slider.last_value_update_time = current_time
                slider.trigger_event("<DRAG>")
            else:
                if current_time - slider.last_value_update_time > slider.trigger_hold_delay:
                    slider.trigger_event("<HOLD>")

    if not event:
        if pygame.mouse.get_pressed()[0] and is_inside:
            slider.pressed = True
        if slider.pressed:
            if pygame.mouse.get_pressed()[0]:
                update_value()
            else:
                slider.pressed = False
                slider.pressed_before = False
                slider.trigger_event("<RELEASE>")
    else:
        if event.type == pygame.KEYDOWN:
            slider.trigger_event("<KEY>")
            if event.unicode:
                slider.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            slider.trigger_event(f"<{keyname.upper()}>")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_inside:
                slider.pressed = True
                update_value()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider.pressed = False
                slider.pressed_before = False
                slider.trigger_event("<RELEASE>")
        elif event.type == pygame.MOUSEMOTION:
            if slider.pressed:
                update_value()
    t = pygame.time.get_ticks() * 0.01
    pulse = (1 - math.cos(t * math.pi)) * 0.5
    if slider.pressed:
        slider.extra_dot_radius = min(slider.max_extra_dot_radius, slider.extra_dot_radius + pulse)
    else:
        slider.extra_dot_radius = max(0, slider.extra_dot_radius - pulse)