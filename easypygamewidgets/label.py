# label.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import time
from typing import Unpack, Any

import pygame

from easypygamewidgets import font, misc
from .assets import TypeHints

pygame.init()


# PERFECTION
# everything private/properties ✅
# basic animations ✅
# free spacing ✅
# cache system ✅
# config suggestions ✅
# optimized set_screen function ✅
# rgba color ✅
# four different corner radius ✅

class Label:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80,
                 text: str = "easypygamewidgets Label", state="enabled",
                 active_hover_text_color: tuple | None = (255, 255, 255, 255),
                 active_hover_shadow_color: tuple | None = (50, 50, 50, 200),
                 active_hover_background_color: tuple | None = None,
                 active_hover_underline_color: tuple | None = None,
                 active_hover_strikethrough_color: tuple | None = None,
                 active_hover_border_color: tuple | None = None,
                 active_pressed_text_color: tuple | None = (255, 255, 255, 255),
                 active_pressed_shadow_color: tuple | None = (50, 50, 50, 200),
                 active_pressed_background_color: tuple | None = None,
                 active_pressed_underline_color: tuple | None = None,
                 active_pressed_strikethrough_color: tuple | None = None,
                 active_pressed_border_color: tuple | None = None,
                 active_unpressed_text_color: tuple | None = (255, 255, 255, 255),
                 active_unpressed_shadow_color: tuple | None = (50, 50, 50, 200),
                 active_unpressed_background_color: tuple | None = None,
                 active_unpressed_underline_color: tuple | None = None,
                 active_unpressed_strikethrough_color: tuple | None = None,
                 active_unpressed_border_color: tuple | None = None,
                 disabled_hover_text_color: tuple | None = (150, 150, 150, 255),
                 disabled_hover_shadow_color: tuple | None = (50, 50, 50, 200),
                 disabled_hover_background_color: tuple | None = None,
                 disabled_hover_underline_color: tuple | None = None,
                 disabled_hover_strikethrough_color: tuple | None = None,
                 disabled_hover_border_color: tuple | None = None,
                 disabled_unpressed_text_color: tuple | None = (150, 150, 150, 255),
                 disabled_unpressed_shadow_color: tuple | None = (50, 50, 50, 200),
                 disabled_unpressed_background_color: tuple | None = None,
                 disabled_unpressed_underline_color: tuple | None = None,
                 disabled_unpressed_strikethrough_color: tuple | None = None,
                 disabled_unpressed_border_color: tuple | None = None,
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor | None = None,
                 disabled_hover_cursor: pygame.Cursor | None = None,
                 active_pressed_cursor: pygame.Cursor | None = None,
                 font: pygame.font.Font = font.default_font, alignment: str = "center",
                 alignment_spacing: int = 40, dragable: bool = False, top_left_corner_radius: int = 25,
                 top_right_corner_radius: int = 25, bottom_left_corner_radius: int = 25,
                 bottom_right_corner_radius: int = 25, layer=1000, line_spacing=30,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, min_width: int | None = None,
                 max_width: int | None = None, min_height: int | None = None, max_height: int | None = None,
                 anchor_x: str = "left", anchor_y: str = "top", data: Any = None):
        safe_set_linesize(font, line_spacing)
        lines = str(text).split("\n")
        if lines == [""]:
            lines = [" "]
        max_w = max((font.render(line, True, (255, 255, 255)).get_width() for line in lines), default=0)
        total_h = sum(font.render(line, True, (255, 255, 255)).get_height() for line in lines)
        if screen:
            screen.add_widget(self)
            self._screen = screen
        else:
            self._screen = None
            self._visible = True
            self._state = state
        self._strikethrough = False
        self._underline = False
        self._auto_size = auto_size
        if auto_size:
            self._width = max_w + alignment_spacing * 2
            if min_width:
                self._width = max(max_w + alignment_spacing * 2, min_width)
            if max_width:
                self._width = min(max_w + alignment_spacing * 2, max_width)
            self._height = total_h + 20
            if min_height:
                self._height = max(total_h + 20, min_height)
            if max_height:
                self._height = min(total_h + 20, max_height)
        else:
            self._width = width
            self._height = height
        self._text = text

        self._active_hover_text_color = normalize_color(active_hover_text_color)
        self._active_hover_shadow_color = normalize_color(active_hover_shadow_color)
        self._active_hover_background_color = normalize_color(active_hover_background_color)
        if active_hover_underline_color:
            self._active_hover_underline_color = normalize_color(active_hover_underline_color)
            self._underline = True
        else:
            self._active_hover_underline_color = self._active_hover_text_color
        if active_hover_strikethrough_color:
            self._active_hover_strikethrough_color = normalize_color(active_hover_strikethrough_color)
            self._strikethrough = True
        else:
            self._active_hover_strikethrough_color = self._active_hover_text_color
        self._active_hover_border_color = normalize_color(active_hover_border_color)

        self._active_pressed_text_color = normalize_color(active_pressed_text_color)
        self._active_pressed_shadow_color = normalize_color(active_pressed_shadow_color)
        self._active_pressed_background_color = normalize_color(active_pressed_background_color)
        if active_pressed_underline_color:
            self._active_pressed_underline_color = normalize_color(active_pressed_underline_color)
            self._underline = True
        else:
            self._active_pressed_underline_color = self._active_pressed_text_color
        if active_pressed_strikethrough_color:
            self._active_pressed_strikethrough_color = normalize_color(active_pressed_strikethrough_color)
            self._strikethrough = True
        else:
            self._active_pressed_strikethrough_color = self._active_pressed_text_color
        self._active_pressed_border_color = normalize_color(active_pressed_border_color)

        self._active_unpressed_text_color = normalize_color(active_unpressed_text_color)
        self._active_unpressed_shadow_color = normalize_color(active_unpressed_shadow_color)
        self._active_unpressed_background_color = normalize_color(active_unpressed_background_color)
        if active_unpressed_underline_color:
            self._active_unpressed_underline_color = normalize_color(active_unpressed_underline_color)
            self._underline = True
        else:
            self._active_unpressed_underline_color = self._active_unpressed_text_color
        if active_unpressed_strikethrough_color:
            self._active_unpressed_strikethrough_color = normalize_color(active_unpressed_strikethrough_color)
            self._strikethrough = True
        else:
            self._active_unpressed_strikethrough_color = self._active_unpressed_text_color
        self._active_unpressed_border_color = normalize_color(active_unpressed_border_color)

        self._disabled_hover_text_color = normalize_color(disabled_hover_text_color)
        self._disabled_hover_shadow_color = normalize_color(disabled_hover_shadow_color)
        self._disabled_hover_background_color = normalize_color(disabled_hover_background_color)
        if disabled_hover_underline_color:
            self._disabled_hover_underline_color = normalize_color(disabled_hover_underline_color)
            self._underline = True
        else:
            self._disabled_hover_underline_color = self._disabled_hover_text_color
        if disabled_hover_strikethrough_color:
            self._disabled_hover_strikethrough_color = normalize_color(disabled_hover_strikethrough_color)
            self._strikethrough = True
        else:
            self._disabled_hover_strikethrough_color = self._disabled_hover_text_color
        self._disabled_hover_border_color = normalize_color(disabled_hover_border_color)

        self._disabled_unpressed_text_color = normalize_color(disabled_unpressed_text_color)
        self._disabled_unpressed_shadow_color = normalize_color(disabled_unpressed_shadow_color)
        self._disabled_unpressed_background_color = normalize_color(disabled_unpressed_background_color)
        if disabled_unpressed_underline_color:
            self._disabled_unpressed_underline_color = normalize_color(disabled_unpressed_underline_color)
            self._underline = True
        else:
            self._disabled_unpressed_underline_color = self._disabled_unpressed_text_color
        if disabled_unpressed_strikethrough_color:
            self._disabled_unpressed_strikethrough_color = normalize_color(disabled_unpressed_strikethrough_color)
            self._strikethrough = True
        else:
            self._disabled_unpressed_strikethrough_color = self._disabled_unpressed_text_color
        self._disabled_unpressed_border_color = normalize_color(disabled_unpressed_border_color)

        self._border_thickness = border_thickness
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
                        f"No custom cursor is used for the label {self._text} because it's not a pygame.Cursor object. ({cursor})")
                self._cursors[name] = None
        self._font = font
        self._alignment = alignment
        self._alignment_spacing = alignment_spacing
        self._dragable = dragable
        self._top_left_corner_radius = top_left_corner_radius
        self._top_right_corner_radius = top_right_corner_radius
        self._bottom_left_corner_radius = bottom_left_corner_radius
        self._bottom_right_corner_radius = bottom_right_corner_radius
        self._layer = layer
        self._tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self._layer + 1)
            if not tooltip.style:
                if not self._active_unpressed_background_color:
                    bg_color = (50, 50, 50, 255)
                if not self._active_unpressed_border_color:
                    bd_color = (100, 100, 100, 255)
                tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                                  active_unpressed_background_color=self._active_unpressed_background_color if self._active_unpressed_background_color else bg_color,
                                  active_unpressed_border_color=self._active_unpressed_border_color if self._active_unpressed_border_color else bd_color)
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
        self._drag_offset = None
        self._is_dragging = False
        self._last_checked_dragging = None
        self._bindings = {}
        self._needs_redraw = True
        self._needs_transform = True
        self._last_visual_state = None
        self._original_surface = pygame.Surface((1, 1))
        self._cached_surface = None
        self._target_scale = 1
        self._current_scale = 1
        self._scale_step = 0
        self._target_rotation = 0
        self._current_rotation = 0
        self._rotation_step = 0
        self._target_offset = (0, 0)
        self._current_offset = [0, 0]
        self._offset_step = [0, 0]
        self._use_rotozoom = False
        self._scheduled_functions = []
        self._is_hovered = False

        misc.add_widget(self)

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self._set_screen(value)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def strikethrough(self):
        return self._strikethrough

    @strikethrough.setter
    def strikethrough(self, value):
        self._strikethrough = value

    @property
    def underline(self):
        return self._underline

    @underline.setter
    def underline(self, value):
        self._underline = value

    @property
    def auto_size(self):
        return self._auto_size

    @auto_size.setter
    def auto_size(self, value):
        self._auto_size = value

    @property
    def width(self):
        return int(self._width * self._current_scale)

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return int(self._height * self._current_scale)

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
    def active_hover_text_color(self):
        return self._active_hover_text_color

    @active_hover_text_color.setter
    def active_hover_text_color(self, value):
        self._active_hover_text_color = normalize_color(value)

    @property
    def active_hover_shadow_color(self):
        return self._active_hover_shadow_color

    @active_hover_shadow_color.setter
    def active_hover_shadow_color(self, value):
        self._active_hover_shadow_color = normalize_color(value)

    @property
    def active_hover_background_color(self):
        return self._active_hover_background_color

    @active_hover_background_color.setter
    def active_hover_background_color(self, value):
        self._active_hover_background_color = normalize_color(value)

    @property
    def active_hover_underline_color(self):
        return self._active_hover_underline_color

    @active_hover_underline_color.setter
    def active_hover_underline_color(self, value):
        self._active_hover_underline_color = normalize_color(value)

    @property
    def active_hover_strikethrough_color(self):
        return self._active_hover_strikethrough_color

    @active_hover_strikethrough_color.setter
    def active_hover_strikethrough_color(self, value):
        self._active_hover_strikethrough_color = normalize_color(value)

    @property
    def active_hover_border_color(self):
        return self._active_hover_border_color

    @active_hover_border_color.setter
    def active_hover_border_color(self, value):
        self._active_hover_border_color = normalize_color(value)

    @property
    def active_pressed_text_color(self):
        return self._active_pressed_text_color

    @active_pressed_text_color.setter
    def active_pressed_text_color(self, value):
        self._active_pressed_text_color = normalize_color(value)

    @property
    def active_pressed_shadow_color(self):
        return self._active_pressed_shadow_color

    @active_pressed_shadow_color.setter
    def active_pressed_shadow_color(self, value):
        self._active_pressed_shadow_color = normalize_color(value)

    @property
    def active_pressed_background_color(self):
        return self._active_pressed_background_color

    @active_pressed_background_color.setter
    def active_pressed_background_color(self, value):
        self._active_pressed_background_color = normalize_color(value)

    @property
    def active_pressed_underline_color(self):
        return self._active_pressed_underline_color

    @active_pressed_underline_color.setter
    def active_pressed_underline_color(self, value):
        self._active_pressed_underline_color = normalize_color(value)

    @property
    def active_pressed_strikethrough_color(self):
        return self._active_pressed_strikethrough_color

    @active_pressed_strikethrough_color.setter
    def active_pressed_strikethrough_color(self, value):
        self._active_pressed_strikethrough_color = normalize_color(value)

    @property
    def active_pressed_border_color(self):
        return self._active_pressed_border_color

    @active_pressed_border_color.setter
    def active_pressed_border_color(self, value):
        self._active_pressed_border_color = normalize_color(value)

    @property
    def active_unpressed_text_color(self):
        return self._active_unpressed_text_color

    @active_unpressed_text_color.setter
    def active_unpressed_text_color(self, value):
        self._active_unpressed_text_color = normalize_color(value)

    @property
    def active_unpressed_shadow_color(self):
        return self._active_unpressed_shadow_color

    @active_unpressed_shadow_color.setter
    def active_unpressed_shadow_color(self, value):
        self._active_unpressed_shadow_color = normalize_color(value)

    @property
    def active_unpressed_background_color(self):
        return self._active_unpressed_background_color

    @active_unpressed_background_color.setter
    def active_unpressed_background_color(self, value):
        self._active_unpressed_background_color = normalize_color(value)

    @property
    def active_unpressed_underline_color(self):
        return self._active_unpressed_underline_color

    @active_unpressed_underline_color.setter
    def active_unpressed_underline_color(self, value):
        self._active_unpressed_underline_color = normalize_color(value)

    @property
    def active_unpressed_strikethrough_color(self):
        return self._active_unpressed_strikethrough_color

    @active_unpressed_strikethrough_color.setter
    def active_unpressed_strikethrough_color(self, value):
        self._active_unpressed_strikethrough_color = normalize_color(value)

    @property
    def active_unpressed_border_color(self):
        return self._active_unpressed_border_color

    @active_unpressed_border_color.setter
    def active_unpressed_border_color(self, value):
        self._active_unpressed_border_color = normalize_color(value)

    @property
    def disabled_hover_text_color(self):
        return self._disabled_hover_text_color

    @disabled_hover_text_color.setter
    def disabled_hover_text_color(self, value):
        self._disabled_hover_text_color = normalize_color(value)

    @property
    def disabled_hover_shadow_color(self):
        return self._disabled_hover_shadow_color

    @disabled_hover_shadow_color.setter
    def disabled_hover_shadow_color(self, value):
        self._disabled_hover_shadow_color = normalize_color(value)

    @property
    def disabled_hover_background_color(self):
        return self._disabled_hover_background_color

    @disabled_hover_background_color.setter
    def disabled_hover_background_color(self, value):
        self._disabled_hover_background_color = normalize_color(value)

    @property
    def disabled_hover_underline_color(self):
        return self._disabled_hover_underline_color

    @disabled_hover_underline_color.setter
    def disabled_hover_underline_color(self, value):
        self._disabled_hover_underline_color = normalize_color(value)

    @property
    def disabled_hover_strikethrough_color(self):
        return self._disabled_hover_strikethrough_color

    @disabled_hover_strikethrough_color.setter
    def disabled_hover_strikethrough_color(self, value):
        self._disabled_hover_strikethrough_color = normalize_color(value)

    @property
    def disabled_hover_border_color(self):
        return self._disabled_hover_border_color

    @disabled_hover_border_color.setter
    def disabled_hover_border_color(self, value):
        self._disabled_hover_border_color = normalize_color(value)

    @property
    def disabled_unpressed_text_color(self):
        return self._disabled_unpressed_text_color

    @disabled_unpressed_text_color.setter
    def disabled_unpressed_text_color(self, value):
        self._disabled_unpressed_text_color = normalize_color(value)

    @property
    def disabled_unpressed_shadow_color(self):
        return self._disabled_unpressed_shadow_color

    @disabled_unpressed_shadow_color.setter
    def disabled_unpressed_shadow_color(self, value):
        self._disabled_unpressed_shadow_color = normalize_color(value)

    @property
    def disabled_unpressed_background_color(self):
        return self._disabled_unpressed_background_color

    @disabled_unpressed_background_color.setter
    def disabled_unpressed_background_color(self, value):
        self._disabled_unpressed_background_color = normalize_color(value)

    @property
    def disabled_unpressed_underline_color(self):
        return self._disabled_unpressed_underline_color

    @disabled_unpressed_underline_color.setter
    def disabled_unpressed_underline_color(self, value):
        self._disabled_unpressed_underline_color = normalize_color(value)

    @property
    def disabled_unpressed_strikethrough_color(self):
        return self._disabled_unpressed_strikethrough_color

    @disabled_unpressed_strikethrough_color.setter
    def disabled_unpressed_strikethrough_color(self, value):
        self._disabled_unpressed_strikethrough_color = normalize_color(value)

    @property
    def disabled_unpressed_border_color(self):
        return self._disabled_unpressed_border_color

    @disabled_unpressed_border_color.setter
    def disabled_unpressed_border_color(self, value):
        self._disabled_unpressed_border_color = normalize_color(value)

    @property
    def border_thickness(self):
        return self._border_thickness

    @border_thickness.setter
    def border_thickness(self, value):
        self._border_thickness = value

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
    def dragable(self):
        return self._dragable

    @dragable.setter
    def dragable(self, value):
        self._dragable = value

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
        self._set_tooltip(value)

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
    def drag_offset(self):
        return self._drag_offset

    @drag_offset.setter
    def drag_offset(self, value):
        self._drag_offset = value

    @property
    def is_dragging(self):
        return self._is_dragging

    @is_dragging.setter
    def is_dragging(self, value):
        self._is_dragging = value

    @property
    def last_checked_dragging(self):
        return self._last_checked_dragging

    @last_checked_dragging.setter
    def last_checked_dragging(self, value):
        self._last_checked_dragging = value

    @property
    def bindings(self):
        return self._bindings

    @bindings.setter
    def bindings(self, value):
        self._bindings = value

    @property
    def needs_redraw(self):
        return self._needs_redraw

    @needs_redraw.setter
    def needs_redraw(self, value):
        self._needs_redraw = value

    @property
    def needs_transform(self):
        return self._needs_transform

    @needs_transform.setter
    def needs_transform(self, value):
        self._needs_transform = value

    @property
    def last_visual_state(self):
        return self._last_visual_state

    @last_visual_state.setter
    def last_visual_state(self, value):
        self._last_visual_state = value

    @property
    def original_surface(self):
        return self._original_surface

    @original_surface.setter
    def original_surface(self, value):
        self._original_surface = value

    @property
    def cached_surface(self):
        return self._cached_surface

    @cached_surface.setter
    def cached_surface(self, value):
        self._cached_surface = value

    @property
    def target_scale(self):
        return self._target_scale

    @target_scale.setter
    def target_scale(self, value):
        self._target_scale = value

    @property
    def current_scale(self):
        return self._current_scale

    @current_scale.setter
    def current_scale(self, value):
        self._current_scale = value

    @property
    def scale_step(self):
        return self._scale_step

    @scale_step.setter
    def scale_step(self, value):
        self._scale_step = value

    @property
    def target_rotation(self):
        return self._target_rotation

    @target_rotation.setter
    def target_rotation(self, value):
        self._target_rotation = value

    @property
    def current_rotation(self):
        return self._current_rotation

    @current_rotation.setter
    def current_rotation(self, value):
        self._current_rotation = value

    @property
    def rotation_step(self):
        return self._rotation_step

    @rotation_step.setter
    def rotation_step(self, value):
        self._rotation_step = value

    @property
    def target_offset(self):
        return self._target_offset

    @target_offset.setter
    def target_offset(self, value):
        self._target_offset = value

    @property
    def current_offset(self):
        return self._current_offset

    @current_offset.setter
    def current_offset(self, value):
        self._current_offset = value

    @property
    def offset_step(self):
        return self._offset_step

    @offset_step.setter
    def offset_step(self, value):
        self._offset_step = value

    @property
    def use_rotozoom(self):
        return self._use_rotozoom

    @use_rotozoom.setter
    def use_rotozoom(self, value):
        self._use_rotozoom = value

    @property
    def scheduled_functions(self):
        return self._scheduled_functions

    @scheduled_functions.setter
    def scheduled_functions(self, value):
        self._scheduled_functions = value

    @property
    def is_hovered(self):
        return self._is_hovered

    @is_hovered.setter
    def is_hovered(self, value):
        self._is_hovered = value

    def _configure(self, **kwargs: Unpack[TypeHints.ButtonConfig]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._needs_redraw = True
        layout_keys = ('auto_size', 'x', 'y', 'width', 'height', 'text', 'line_spacing', 'font', 'alignment_spacing',
                       'max_width', 'min_width', 'max_height', 'min_height')
        if any(k in kwargs for k in layout_keys):
            safe_set_linesize(self._font, self._line_spacing)
            lines = str(self._text).split("\n")
            max_w = max((self._font.render(line, True, (255, 255, 255)).get_width() for line in lines),
                        default=0) + self._alignment_spacing
            total_h = sum(self._font.render(line, True, (255, 255, 255)).get_height() for line in lines)
            if self._auto_size:
                self._width = max_w + self._alignment_spacing * 2
                if self._min_width:
                    self._width = max(max_w + self._alignment_spacing * 2, self._min_width)
                if self._max_width:
                    self._width = min(max_w + self._alignment_spacing * 2, self._max_width)
                self._height = total_h + 20
                if self._min_height:
                    self._height = max(total_h + 20, self._min_height)
                if self._max_height:
                    self._height = min(total_h + 20, self._max_height)
            self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        if 'screen' in kwargs:
            self._set_screen(kwargs["screen"])
        if 'layer' in kwargs:
            misc.resort_layers()
        if 'line_spacing' in kwargs:
            safe_set_linesize(self._font, self._line_spacing)
        return self

    def _delete(self):
        self._alive = False
        if self in misc.all_widgets:
            misc.all_widgets.remove(self)

    def _place(self, x: int, y: int, mode: str = "px"):
        anchor_offset = [0, 0]
        if self._anchor_x == "left":
            anchor_offset[0] = 0
        elif self._anchor_x == "center":
            anchor_offset[0] = self._width // 2
        elif self._anchor_x == "right":
            anchor_offset[0] = self._width
        if self._anchor_y == "top":
            anchor_offset[1] = 0
        elif self._anchor_y == "center":
            anchor_offset[1] = self._height // 2
        elif self._anchor_y == "bottom":
            anchor_offset[1] = self._height
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
        self.x -= anchor_offset[0]
        self.y -= anchor_offset[1]
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._needs_transform = True
        return self

    def _anchor(self, anchor_x: str = "left", anchor_y: str = "top"):
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self._place(self._x, self._y)
        return self

    def _bind(self, event: str, command, require_hover: bool = True):
        self._bindings[event] = {"command": command, "require_hover": require_hover}
        return self

    def _trigger_event(self, event: str, *args, **kwargs):
        if event in self._bindings:
            binding_data = self._bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            if not require_hover or is_point_in_rounded_rect(self, pygame.mouse.get_pos()):
                command(*args, **kwargs)

    def _set_screen(self, screen):
        if self in screen.widgets:
            return self
        self._screen = screen
        screen.add_widget(self)
        return self

    def _set_strikethrough(self, value: bool):
        self._strikethrough = value
        self._needs_redraw = True
        return self

    def _set_underline(self, value: bool):
        self._underline = value
        self._needs_redraw = True
        return self

    def _unbind(self, event: str):
        if event in self._bindings:
            del self._bindings[event]
        return self

    def _unbind_all(self):
        self._bindings.clear()
        return self

    def _set_tooltip(self, tooltip):
        self._tooltip = tooltip
        tooltip.configure(layer=self._layer + 1)
        if not tooltip.style:
            if not self._active_unpressed_background_color:
                bg_color = (50, 50, 50)
            if not self._active_unpressed_border_color:
                bd_color = (100, 100, 100)
            tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                              active_unpressed_background_color=self._active_unpressed_background_color if self._active_unpressed_background_color else bg_color,
                              active_unpressed_border_color=self._active_unpressed_border_color if self._active_unpressed_border_color else bd_color)
        return self

    def _remove_tooltip(self):
        if self._tooltip:
            self._tooltip.visible = False
            self._tooltip = None
        return self

    def _scale(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self._target_scale = 1
        else:
            self._target_scale = value
        self._scale_step = (self._target_scale - self._current_scale) / frames_to_finish
        update_animation(self)
        return self

    def _rotate(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self._target_rotation = 0
        else:
            self._target_rotation = value
        self._rotation_step = (self._target_rotation - self._current_rotation) / frames_to_finish
        update_animation(self)
        return self

    def _rotozoom(self, scale=None, rotation=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self._target_scale = 1 if scale is None else scale
        self._scale_step = (self._target_scale - self._current_scale) / frames_to_finish
        self._target_rotation = 0 if rotation is None else rotation
        self._rotation_step = (self._target_rotation - self._current_rotation) / frames_to_finish
        self._use_rotozoom = True
        update_animation(self)
        return self

    def _offset(self, value: tuple[int, int], frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self._target_offset = (0, 0)
        else:
            self._target_offset = value
        self._offset_step[0] = (self._target_offset[0] - self._current_offset[0]) / frames_to_finish
        self._offset_step[1] = (self._target_offset[1] - self._current_offset[1]) / frames_to_finish
        update_animation(self)
        return self

    def _schedule(self, function, frames_to_execute):
        if frames_to_execute < 1:
            frames_to_execute = 1
        self._scheduled_functions.append([function, frames_to_execute])
        return self

    @property
    def configure(self):
        return self._configure

    @property
    def config(self):
        return self._configure

    @property
    def delete(self):
        return self._delete

    @property
    def place(self):
        return self._place

    @property
    def anchor(self):
        return self._anchor

    @property
    def bind(self):
        return self._bind

    @property
    def trigger_event(self):
        return self._trigger_event

    @property
    def set_screen(self):
        return self._set_screen

    @property
    def set_strikethrough(self):
        return self._set_strikethrough

    @property
    def set_underline(self):
        return self._set_underline

    @property
    def unbind(self):
        return self._unbind

    @property
    def unbind_all(self):
        return self._unbind_all

    @property
    def set_tooltip(self):
        return self._set_tooltip

    @property
    def remove_tooltip(self):
        return self._remove_tooltip

    @property
    def scale(self):
        return self._scale

    @property
    def rotate(self):
        return self._rotate

    @property
    def rotozoom(self):
        return self._rotozoom

    @property
    def offset(self):
        return self._offset

    @property
    def schedule(self):
        return self._schedule


def update_animation(label):
    scale_changed = False
    rotation_changed = False
    if label.current_scale != label.target_scale:
        if abs(label.current_scale - label.target_scale) <= abs(label.scale_step):
            label.current_scale = label.target_scale
        else:
            label.current_scale += label.scale_step
        scale_changed = True
    if label.current_rotation != label.target_rotation:
        if abs(label.current_rotation - label.target_rotation) <= abs(label.rotation_step):
            label.current_rotation = label.target_rotation
        else:
            label.current_rotation += label.rotation_step
        rotation_changed = True
    for x in range(2):
        if label.current_offset[x] != label.target_offset[x]:
            if abs(label.current_offset[x] - label.target_offset[x]) <= abs(label.offset_step[x]):
                label.current_offset[x] = float(label.target_offset[x])
            else:
                label.current_offset[x] += label.offset_step[x]

    if scale_changed or rotation_changed:
        label.needs_transform = True


def normalize_color(color):
    if color is None:
        return (0, 0, 0, 0)
    if len(color) == 3:
        return (*color, 255)
    return color


def safe_set_linesize(font, line_spacing):
    try:
        descent = abs(font.get_descent())
    except Exception:
        descent = 0
    font.set_linesize(line_spacing + descent)


def get_screen_offset(widget):
    if widget.screen:
        return widget.screen.x, widget.screen.y
    return 0, 0


def render_base_surface(label, is_hovering):
    if label.state == "enabled":
        if label.pressed:
            text_color = label.active_pressed_text_color
            bg_color = label.active_pressed_background_color
            shadow_color = label.active_pressed_shadow_color
            underline_color = label.active_pressed_underline_color
            strikethrough_color = label.active_pressed_strikethrough_color
            brd_color = label.active_pressed_border_color
        elif is_hovering:
            text_color = label.active_hover_text_color
            bg_color = label.active_hover_background_color
            shadow_color = label.active_hover_shadow_color
            underline_color = label.active_hover_underline_color
            strikethrough_color = label.active_hover_strikethrough_color
            brd_color = label.active_hover_border_color
        else:
            text_color = label.active_unpressed_text_color
            bg_color = label.active_unpressed_background_color
            shadow_color = label.active_unpressed_shadow_color
            underline_color = label.active_unpressed_underline_color
            strikethrough_color = label.active_unpressed_strikethrough_color
            brd_color = label.active_unpressed_border_color
    else:
        if is_hovering:
            text_color = label.disabled_hover_text_color
            bg_color = label.disabled_hover_background_color
            shadow_color = label.disabled_hover_shadow_color
            underline_color = label.disabled_hover_underline_color
            strikethrough_color = label.disabled_hover_strikethrough_color
            brd_color = label.disabled_hover_border_color
        else:
            text_color = label.disabled_unpressed_text_color
            bg_color = label.disabled_unpressed_background_color
            shadow_color = label.disabled_unpressed_shadow_color
            underline_color = label.disabled_unpressed_underline_color
            strikethrough_color = label.disabled_unpressed_strikethrough_color
            brd_color = label.disabled_unpressed_border_color

    if label.auto_size:
        safe_set_linesize(label.font, label.line_spacing)
        lines = str(label.text).split("\n")
        if lines == [""]:
            lines = [" "]
        max_w = max((label.font.render(line, True, text_color).get_width() for line in lines), default=0)
        total_h = sum(label.font.render(line, True, text_color).get_height() for line in lines)
        label._width = max_w + label.alignment_spacing * 2
        if label.min_width:
            label._width = max(max_w + label.alignment_spacing * 2, label.min_width)
        if label.max_width:
            label._width = min(max_w + label.alignment_spacing * 2, label.max_width)
        label._height = total_h + 20
        if label.min_height:
            label._height = max(total_h + 20, label.min_height)
        if label.max_height:
            label._height = min(total_h + 20, label.max_height)
        label.rect = pygame.Rect(label.x, label.y, label._width, label._height)
    label.original_surface = pygame.Surface((label._width, label._height), pygame.SRCALPHA)
    draw_req_rect = pygame.Rect(0, 0, label._width, label._height)
    if bg_color:
        shape_surf = pygame.Surface((label._width, label._height), pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, bg_color, draw_req_rect,
                         border_top_left_radius=label.top_left_corner_radius,
                         border_top_right_radius=label.top_right_corner_radius,
                         border_bottom_left_radius=label.bottom_left_corner_radius,
                         border_bottom_right_radius=label.bottom_right_corner_radius)
        shape_surf.set_alpha(bg_color[3])
        label.original_surface.blit(shape_surf, (0, 0))
    if brd_color:
        shape_surf = pygame.Surface((label._width, label._height), pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, brd_color, draw_req_rect, width=label.border_thickness,
                         border_top_left_radius=label.top_left_corner_radius,
                         border_top_right_radius=label.top_right_corner_radius,
                         border_bottom_left_radius=label.bottom_left_corner_radius,
                         border_bottom_right_radius=label.bottom_right_corner_radius)
        shape_surf.set_alpha(brd_color[3])
        label.original_surface.blit(shape_surf, (0, 0))

    def render_text_line(txt, color, rect_ref, offset=(0, 0)):
        lines = str(txt).split("\n")
        if not lines: return None
        total_height = sum(label.font.render(line, True, color).get_height() for line in lines)
        current_y = rect_ref.centery - total_height // 2 + offset[1]
        union_rect = None
        for line in lines:
            line_surf = label.font.render(line, True, color)
            line_h = line_surf.get_height()
            cx, cy = rect_ref.centerx + offset[0], current_y + line_h // 2
            if label.alignment == "stretched" and len(line) > 1:
                total_char_width = sum(label.font.render(char, True, color).get_width() for char in line)
                available_width = rect_ref.width - (label.alignment_spacing * 2)
                if available_width > total_char_width:
                    spacing = (available_width - total_char_width) / (len(line) - 1)
                    curr_x = rect_ref.left + label.alignment_spacing + offset[0]
                    line_rect = None
                    for char in line:
                        char_s = label.font.render(char, True, color)
                        char_s.set_alpha(color[3])
                        char_r = char_s.get_rect(midleft=(curr_x, cy))
                        label.original_surface.blit(char_s, char_r)
                        curr_x += char_s.get_width() + spacing
                        if line_rect is None:
                            line_rect = char_r.copy()
                        else:
                            line_rect.union_ip(char_r)
                    if union_rect is None:
                        union_rect = line_rect
                    else:
                        union_rect.union_ip(line_rect)
                    current_y += line_h
                    continue
            txt_rect = line_surf.get_rect()
            if label.alignment == "left":
                txt_rect.midleft = (rect_ref.left + label.alignment_spacing + offset[0], cy)
            elif label.alignment == "right":
                txt_rect.midright = (rect_ref.right - label.alignment_spacing + offset[0], cy)
            else:
                txt_rect.center = (cx, cy)
            line_surf.set_alpha(color[3])
            label.original_surface.blit(line_surf, txt_rect)
            if union_rect is None:
                union_rect = txt_rect.copy()
            else:
                union_rect.union_ip(txt_rect)
            current_y += line_h
        return union_rect

    surface_rect = label.original_surface.get_rect()
    if shadow_color and shadow_color[3] > 0:
        render_text_line(label.text, shadow_color, surface_rect, offset=(2, 2))
    final_text_rect = render_text_line(label.text, text_color, surface_rect)
    if final_text_rect:
        if underline_color and label.underline:
            shape_surf = pygame.Surface(final_text_rect.size, pygame.SRCALPHA)
            shape_surf_rect = shape_surf.get_rect()
            start_pos = (shape_surf_rect.left, shape_surf_rect.bottom - 2)
            end_pos = (shape_surf_rect.right, shape_surf_rect.bottom - 2)
            shape_surf.set_alpha(underline_color[3])
            pygame.draw.line(shape_surf, underline_color, start_pos, end_pos, 2)
            label.original_surface.blit(shape_surf, final_text_rect)
        if strikethrough_color and label.strikethrough:
            shape_surf = pygame.Surface(final_text_rect.size, pygame.SRCALPHA)
            shape_surf_rect = shape_surf.get_rect()
            start_pos = (shape_surf_rect.left, shape_surf_rect.centery)
            end_pos = (shape_surf_rect.right, shape_surf_rect.centery)
            shape_surf.set_alpha(strikethrough_color[3])
            pygame.draw.line(shape_surf, strikethrough_color, start_pos, end_pos, 2)
            label.original_surface.blit(shape_surf, final_text_rect)
    label.last_visual_state = (is_hovering)
    label.needs_redraw = False
    label.needs_transform = True
    label.cached_surface = label.original_surface


def draw(label, surface: pygame.Surface):
    if not label.alive or not label.visible:
        return
    offset_x, offset_y = get_screen_offset(label)
    total_offset_x = offset_x + round(label.current_offset[0])
    total_offset_y = offset_y + round(label.current_offset[1])
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(label, mouse_pos)
    current_visual_state = (is_hovering)
    if label.needs_redraw or current_visual_state != label.last_visual_state:
        render_base_surface(label, is_hovering)
    if label.needs_transform:
        if label.current_scale != 1 or label.current_rotation != 0:
            new_width = int(label.original_surface.get_width() * label.current_scale)
            new_height = int(label.original_surface.get_height() * label.current_scale)
            if new_width > 0 and new_height > 0:
                if label.use_rotozoom:
                    label.cached_surface = pygame.transform.rotozoom(label.original_surface, label.current_rotation,
                                                                     label.current_scale)
                else:
                    scaled_surface = pygame.transform.smoothscale(label.original_surface, (new_width, new_height))
                    label.cached_surface = pygame.transform.rotate(scaled_surface, label.current_rotation)
            else:
                label.cached_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        else:
            label.cached_surface = label.original_surface.copy()
        base_rect = pygame.Rect(label.x, label.y, label._width, label._height)
        old_center = base_rect.center
        label.rect = label.cached_surface.get_rect()
        label.rect.center = old_center
        label.needs_transform = False
    draw_rect = label.rect.move(total_offset_x, total_offset_y)
    surface.blit(label.cached_surface, draw_rect)
    if is_hovering:
        if label.state == "enabled":
            if label.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = label.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if label.original_cursor is None:
                    label.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if label.original_cursor:
            pygame.mouse.set_cursor(label.original_cursor)
            label.original_cursor = None
    if is_hovering and not label.is_hovered:
        label.is_hovered = True
        label.trigger_event("<MOUSE-IN>")
        if label.tooltip:
            label.tooltip.show()
    elif is_hovering and label.is_hovered:
        label.is_hovered = True
        label.trigger_event("<HOVER>")
    elif not is_hovering and label.is_hovered:
        label.is_hovered = False
        label.trigger_event("<MOUSE-OUT>")
        if label.tooltip:
            label.tooltip.hide()


def is_point_in_rounded_rect(label, point):
    offset_x, offset_y = get_screen_offset(label)
    total_offset_x = offset_x + round(label.current_offset[0])
    total_offset_y = offset_y + round(label.current_offset[1])
    rect = label.rect.move(total_offset_x, total_offset_y)
    if not rect.collidepoint(point):
        return False
    x, y = point
    geom_rect = rect
    scale = label.current_scale
    rotation = label.current_rotation
    if scale != 1 or rotation != 0:
        cx, cy = rect.center
        if rotation != 0:
            v = pygame.math.Vector2(x - cx, y - cy)
            v = v.rotate(rotation)
            x, y = cx + v.x, cy + v.y
        base_w = label._width * scale
        base_h = label._height * scale
        geom_rect = pygame.Rect(0, 0, base_w, base_h)
        geom_rect.center = (cx, cy)
        if not geom_rect.collidepoint((x, y)):
            return False
    tl_r = label.top_left_corner_radius * scale
    tr_r = label.top_right_corner_radius * scale
    bl_r = label.bottom_left_corner_radius * scale
    br_r = label.bottom_right_corner_radius * scale
    max_r = max(tl_r, tr_r, bl_r, br_r)
    if (geom_rect.left + max_r <= x <= geom_rect.right - max_r) or \
            (geom_rect.top + max_r <= y <= geom_rect.bottom - max_r):
        return True
    if x < geom_rect.left + tl_r and y < geom_rect.top + tl_r:
        cx, cy = geom_rect.left + tl_r, geom_rect.top + tl_r
        return (x - cx) ** 2 + (y - cy) ** 2 <= tl_r ** 2
    if x > geom_rect.right - tr_r and y < geom_rect.top + tr_r:
        cx, cy = geom_rect.right - tr_r, geom_rect.top + tr_r
        return (x - cx) ** 2 + (y - cy) ** 2 <= tr_r ** 2
    if x < geom_rect.left + bl_r and y > geom_rect.bottom - bl_r:
        cx, cy = geom_rect.left + bl_r, geom_rect.bottom - bl_r
        return (x - cx) ** 2 + (y - cy) ** 2 <= bl_r ** 2
    if x > geom_rect.right - br_r and y > geom_rect.bottom - br_r:
        cx, cy = geom_rect.right - br_r, geom_rect.bottom - br_r
        return (x - cx) ** 2 + (y - cy) ** 2 <= br_r ** 2
    return True


def react(label, event=None):
    for func in label.scheduled_functions[:]:
        func[1] -= 1
        if func[1] <= 0:
            func[0]()
            label.scheduled_functions.remove(func)
    if label.state != "enabled" or not label.visible:
        label.pressed = False
        return
    current_time = time.time()
    mouse_pos = pygame.mouse.get_pos()
    is_inside = is_point_in_rounded_rect(label, mouse_pos)
    screen_off_x, screen_off_y = get_screen_offset(label)
    total_offset_x = screen_off_x + round(label.current_offset[0])
    total_offset_y = screen_off_y + round(label.current_offset[1])
    if event:
        if event.type == pygame.KEYDOWN:
            label.trigger_event("<KEY>")
            if event.unicode:
                label.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            label.trigger_event(f"<{keyname.upper()}>")
        if event.type == pygame.MOUSEMOTION:
            if label.pressed and label.dragable:
                if is_inside or label.is_dragging:
                    label.is_dragging = True
                    label.last_checked_dragging = current_time
                    if label.drag_offset:
                        new_x = mouse_pos[0] - label.drag_offset[0] - total_offset_x
                        new_y = mouse_pos[1] - label.drag_offset[1] - total_offset_y
                        label.place(new_x, new_y)
        elif event.type == pygame.MOUSEBUTTONDOWN and is_inside:
            if event.button == 1:
                label.pressed = True
                label.drag_offset = (mouse_pos[0] - (label.x + total_offset_x),
                                     mouse_pos[1] - (label.y + total_offset_y))
                label.trigger_event("<PRESS>")
        elif event.type == pygame.MOUSEBUTTONUP and is_inside:
            if event.button == 1:
                label.pressed = False
                label.is_dragging = False
                label.trigger_event("<RELEASE>")
    if label.last_checked_dragging:
        if current_time - label.last_checked_dragging > 0.2:
            label.is_dragging = False
    if label.pressed and not label.is_dragging:
        label.trigger_event("<HOLD>")
    if label.pressed and label.is_dragging:
        label.trigger_event("<DRAG>")