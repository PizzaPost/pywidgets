# timekeeper.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import math
import time
from typing import Any

import pygame

from easypygamewidgets import font, misc
from easypygamewidgets.masterWidget import Widget, Tooltipable

pygame.init()


# PERFECTION
# everything private/properties ❌
# basic animations ❌
# free spacing ❌
# cache system ❌
# config suggestions ❌
# optimized set_screen function ❌
# rgba color ❌
# four different corner radii ❌

class Timekeeper(Widget, Tooltipable):
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80, start_at: float | int = 60, end_at: float | int | None = None,
                 show_milliseconds: bool = False, show_seconds: bool = True,
                 show_minutes: bool = False, smart_minutes: bool = True, show_hours: bool = False,
                 smart_hours: bool = True,
                 state: str | None = None,
                 active_unpressed_text_color: tuple = (255, 255, 255),
                 disabled_unpressed_text_color: tuple = (150, 150, 150),
                 active_hover_text_color: tuple = (255, 255, 255),
                 disabled_hover_text_color: tuple = (150, 150, 150),
                 active_pressed_text_color: tuple = (200, 200, 200),
                 active_unpressed_background_color: tuple = (50, 50, 50),
                 disabled_unpressed_background_color: tuple = (30, 30, 30),
                 active_hover_background_color: tuple = (50, 50, 50),
                 disabled_hover_background_color: tuple = (30, 30, 30),
                 active_pressed_background_color: tuple = (40, 40, 40),
                 active_unpressed_border_color: tuple = (100, 100, 100),
                 disabled_unpressed_border_color: tuple = (60, 60, 60),
                 active_hover_border_color: tuple = (100, 100, 100),
                 disabled_hover_border_color: tuple = (60, 60, 60),
                 active_pressed_border_color: tuple = (50, 50, 50),
                 border_thickness: int = 2,
                 hide_text: bool = False,
                 hide_background: bool = False,
                 hide_border: bool = False,
                 active_hover_cursor: pygame.Cursor | None = None,
                 disabled_hover_cursor: pygame.Cursor | None = None,
                 active_pressed_cursor: pygame.Cursor | None = None,
                 font: pygame.font.Font | pygame.font.SysFont = font.default_font, alignment: str = "center",
                 alignment_spacing: int = 20, corner_radius: int = 14, ticking: bool = False,
                 type_order: list[str] = ("h", ":", "m", ":", "s", ".", "ms"), reversed: bool = False, layer=1000,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, min_width: int | None = None,
                 max_width: int | None = None, min_height: int | None = None, max_height: int | None = None,
                 anchor_x: str = "left", anchor_y: str = "top", visible: bool = True, data: Any = None):
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
        self._start_at = start_at
        self._end_at = end_at
        self._show_milliseconds = show_milliseconds
        self._show_seconds = show_seconds
        self._show_minutes = show_minutes
        self._smart_minutes = smart_minutes
        self._show_hours = show_hours
        self._smart_hours = smart_hours
        self._active_unpressed_text_color = active_unpressed_text_color
        self._disabled_unpressed_text_color = disabled_unpressed_text_color
        self._active_hover_text_color = active_hover_text_color
        self._disabled_hover_text_color = disabled_hover_text_color
        self._active_pressed_text_color = active_pressed_text_color
        self._active_unpressed_background_color = active_unpressed_background_color
        self._disabled_unpressed_background_color = disabled_unpressed_background_color
        self._active_hover_background_color = active_hover_background_color
        self._disabled_hover_background_color = disabled_hover_background_color
        self._active_pressed_background_color = active_pressed_background_color
        self._active_unpressed_border_color = active_unpressed_border_color
        self._disabled_unpressed_border_color = disabled_unpressed_border_color
        self._active_hover_border_color = active_hover_border_color
        self._disabled_hover_border_color = disabled_hover_border_color
        self._active_pressed_border_color = active_pressed_border_color
        self._border_thickness = border_thickness
        self._hide_text = hide_text
        self._hide_background = hide_background
        self._hide_border = hide_border
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
                        f"No custom cursor is used for the timekeeper {start_at=}, {end_at=} because it's not a pygame.Cursor object. ({cursor})")
                self._cursors[name] = None
        self._font = font
        self._alignment = alignment
        self._alignment_spacing = alignment_spacing
        self._corner_radius = corner_radius
        self._ticking = ticking
        self._type_order = type_order
        self._reversed = reversed
        self._layer = layer
        self._tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self._layer + 1)
            if not tooltip.style:
                tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                                  active_unpressed_background_color=self._active_unpressed_background_color,
                                  active_unpressed_border_color=self._active_unpressed_border_color)
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
        self._last_updated = None
        self._is_negative = False
        self._bindings = {}

        self._milliseconds = None
        self._seconds = None
        self._minutes = None
        self._hours = None
        split_to_values(self, start_at)

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
    def start_at(self):
        return self._start_at

    @start_at.setter
    def start_at(self, value):
        self._start_at = value

    @property
    def end_at(self):
        return self._end_at

    @end_at.setter
    def end_at(self, value):
        self._end_at = value

    @property
    def show_milliseconds(self):
        return self._show_milliseconds

    @show_milliseconds.setter
    def show_milliseconds(self, value):
        self._show_milliseconds = value

    @property
    def show_seconds(self):
        return self._show_seconds

    @show_seconds.setter
    def show_seconds(self, value):
        self._show_seconds = value

    @property
    def show_minutes(self):
        return self._show_minutes

    @show_minutes.setter
    def show_minutes(self, value):
        self._show_minutes = value

    @property
    def smart_minutes(self):
        return self._smart_minutes

    @smart_minutes.setter
    def smart_minutes(self, value):
        self._smart_minutes = value

    @property
    def show_hours(self):
        return self._show_hours

    @show_hours.setter
    def show_hours(self, value):
        self._show_hours = value

    @property
    def smart_hours(self):
        return self._smart_hours

    @smart_hours.setter
    def smart_hours(self, value):
        self._smart_hours = value

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
    def active_unpressed_background_color(self):
        return self._active_unpressed_background_color

    @active_unpressed_background_color.setter
    def active_unpressed_background_color(self, value):
        self._active_unpressed_background_color = value

    @property
    def disabled_unpressed_background_color(self):
        return self._disabled_unpressed_background_color

    @disabled_unpressed_background_color.setter
    def disabled_unpressed_background_color(self, value):
        self._disabled_unpressed_background_color = value

    @property
    def active_hover_background_color(self):
        return self._active_hover_background_color

    @active_hover_background_color.setter
    def active_hover_background_color(self, value):
        self._active_hover_background_color = value

    @property
    def disabled_hover_background_color(self):
        return self._disabled_hover_background_color

    @disabled_hover_background_color.setter
    def disabled_hover_background_color(self, value):
        self._disabled_hover_background_color = value

    @property
    def active_pressed_background_color(self):
        return self._active_pressed_background_color

    @active_pressed_background_color.setter
    def active_pressed_background_color(self, value):
        self._active_pressed_background_color = value

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
    def border_thickness(self):
        return self._border_thickness

    @border_thickness.setter
    def border_thickness(self, value):
        self._border_thickness = value

    @property
    def hide_text(self):
        return self._hide_text

    @hide_text.setter
    def hide_text(self, value):
        self._hide_text = value

    @property
    def hide_background(self):
        return self._hide_background

    @hide_background.setter
    def hide_background(self, value):
        self._hide_background = value

    @property
    def hide_border(self):
        return self._hide_border

    @hide_border.setter
    def hide_border(self, value):
        self._hide_border = value

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
    def corner_radius(self):
        return self._corner_radius

    @corner_radius.setter
    def corner_radius(self, value):
        self._corner_radius = value

    @property
    def ticking(self):
        return self._ticking

    @ticking.setter
    def ticking(self, value):
        self._ticking = value

    @property
    def type_order(self):
        return self._type_order

    @type_order.setter
    def type_order(self, value):
        self._type_order = value

    @property
    def reversed(self):
        return self._reversed

    @reversed.setter
    def reversed(self, value):
        self._reversed = value

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
        self.set_tooltip(value)

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
    def last_updated(self):
        return self._last_updated

    @last_updated.setter
    def last_updated(self, value):
        self._last_updated = value

    @property
    def is_negative(self):
        return self._is_negative

    @is_negative.setter
    def is_negative(self, value):
        self._is_negative = value

    @property
    def bindings(self):
        return self._bindings

    @bindings.setter
    def bindings(self, value):
        self._bindings = value

    @property
    def milliseconds(self):
        return self._milliseconds

    @milliseconds.setter
    def milliseconds(self, value):
        self._milliseconds = value

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value):
        self._seconds = value

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        self._minutes = value

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        self._hours = value

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        update_size(self)
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
        return self

    def config(self, **kwargs):
        self.configure(**kwargs)

    def get_display_text(self):
        values = {
            "ms": self._milliseconds if self._show_milliseconds else None,
            "s": self._seconds if self._show_seconds else None,
            "m": self._minutes if (self._show_minutes or (self._smart_minutes and self._minutes != 0)) else None,
            "h": self._hours if (self._show_hours or (self._smart_hours and self._hours != 0)) else None,
        }
        parts = []
        pending_sep = None
        for token in self._type_order:
            if token in values:
                value = values[token]
                if value is not None:
                    if pending_sep and parts:
                        parts.append(pending_sep)
                    if token == "ms":
                        ms_int = int(round(value, 4) * 100) % 100
                        parts.append(f"{ms_int:02}")
                    else:
                        parts.append(f"{value:02}")
                    pending_sep = None
            else:
                pending_sep = token
        display_str = "".join(parts)
        if self._is_negative:
            display_str = "-" + display_str
        return display_str

    def set(self, milliseconds=0, seconds=0, minutes=0, hours=0):
        split_to_values(self, hours * 3600 + minutes * 60 + seconds + milliseconds / 1000)
        return self

    def stop(self):
        self._ticking = False
        self._last_updated = None
        return self

    def resume(self):
        self._ticking = True
        self._last_updated = None
        return self

    def start(self):
        self._ticking = True
        self._last_updated = None
        return self

    def reset(self):
        split_to_values(self, self._start_at)
        self._last_updated = None
        return self

    def add(self, amount):
        sign = -1 if self._is_negative else 1
        curr = ((self._hours * 3600) + (self._minutes * 60) + self._seconds + self._milliseconds) * sign
        curr += amount
        split_to_values(self, curr)
        return self

    def subtract(self, amount):
        sign = -1 if self._is_negative else 1
        curr = ((self._hours * 3600) + (self._minutes * 60) + self._seconds + self._milliseconds) * sign
        curr -= amount
        split_to_values(self, curr)
        return self


def update_size(timekeeper):
    if timekeeper.auto_size:
        display_text = timekeeper.get_display_text()
        text_w = timekeeper.font.size(display_text)[0]
        extra_w = text_w + (timekeeper.alignment_spacing * 2)
        timekeeper.width = (extra_w + 39) // 40 * 40
        timekeeper.height = (timekeeper.font.size(display_text)[1] + 39) // 40 * 40
        if timekeeper.min_width:
            timekeeper.width = max(timekeeper.width, timekeeper.min_width)
        if timekeeper.max_width:
            timekeeper.width = min(timekeeper.width, timekeeper.max_width)
        if timekeeper.min_height:
            timekeeper.height = max(timekeeper.height, timekeeper.min_height)
        if timekeeper.max_height:
            timekeeper.height = min(timekeeper.height, timekeeper.max_height)
        timekeeper.rect = pygame.Rect(timekeeper.x, timekeeper.y, timekeeper.width, timekeeper.height)


def split_to_values(widget, total_seconds):
    base_seconds = math.floor(total_seconds)
    widget.is_negative = base_seconds < 0
    abs_secs = abs(base_seconds)
    widget.hours = int(abs_secs // 3600)
    widget.minutes = int((abs_secs % 3600) // 60)
    widget.seconds = int(abs_secs % 60)
    widget.milliseconds = abs(total_seconds) - int(abs(abs_secs))
    update_size(widget)


def draw(timekeeper, surface: pygame.Surface):
    if not timekeeper.alive or not timekeeper.visible:
        return
    offset_x, offset_y = misc.get_screen_offset(timekeeper)
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = misc.is_point_over_widget(timekeeper, mouse_pos)
    if timekeeper.state == "enabled":
        if timekeeper.pressed and is_hovering:
            text_color = timekeeper.active_pressed_text_color
            bg_color = timekeeper.active_pressed_background_color
            brd_color = timekeeper.active_pressed_border_color
        elif is_hovering:
            text_color = timekeeper.active_hover_text_color
            bg_color = timekeeper.active_hover_background_color
            brd_color = timekeeper.active_hover_border_color
        else:
            text_color = timekeeper.active_unpressed_text_color
            bg_color = timekeeper.active_unpressed_background_color
            brd_color = timekeeper.active_unpressed_border_color
    else:
        if is_hovering:
            text_color = timekeeper.disabled_hover_text_color
            bg_color = timekeeper.disabled_hover_background_color
            brd_color = timekeeper.disabled_hover_border_color
        else:
            text_color = timekeeper.disabled_unpressed_text_color
            bg_color = timekeeper.disabled_unpressed_background_color
            brd_color = timekeeper.disabled_unpressed_border_color

    if is_hovering:
        if timekeeper.state == "enabled":
            if timekeeper.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = timekeeper.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if timekeeper.original_cursor is None:
                    timekeeper.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if timekeeper.original_cursor:
            pygame.mouse.set_cursor(timekeeper.original_cursor)
            timekeeper.original_cursor = None

    if is_hovering and not getattr(timekeeper, "is_hovered", False):
        timekeeper.is_hovered = True
        timekeeper.trigger_event("<MOUSE-IN>")
        if timekeeper.tooltip:
            timekeeper.tooltip.show()
    elif is_hovering and getattr(timekeeper, "is_hovered", False):
        timekeeper.is_hovered = True
        timekeeper.trigger_event("<HOVER>")
    elif not is_hovering and getattr(timekeeper, "is_hovered", False):
        timekeeper.is_hovered = False
        timekeeper.trigger_event("<MOUSE-OUT>")
        if timekeeper.tooltip:
            timekeeper.tooltip.hide()

    display_text = timekeeper.get_display_text()
    draw_rect = timekeeper.rect.move(offset_x, offset_y)
    if not timekeeper.hide_background:
        pygame.draw.rect(surface, bg_color, draw_rect, border_radius=timekeeper.corner_radius)
    if timekeeper.border_thickness > 0 and not timekeeper.hide_border:
        pygame.draw.rect(surface, brd_color, draw_rect, width=timekeeper.border_thickness,
                         border_radius=timekeeper.corner_radius)
    old_clip = surface.get_clip()
    clip_rect = draw_rect.inflate(-4, -4)
    surface.set_clip(clip_rect)
    y_pos = draw_rect.centery
    drawn_stretched = False
    if not timekeeper.hide_text:
        if timekeeper.alignment == "stretched" and len(display_text) > 1 and not timekeeper.auto_size:
            total_char_width = sum(timekeeper.font.render(char, True, text_color).get_width() for char in display_text)
            available_width = draw_rect.width - (timekeeper.alignment_spacing * 2)
            if available_width > total_char_width:
                drawn_stretched = True
                spacing = (available_width - total_char_width) / (len(display_text) - 1)
                current_x = draw_rect.left + timekeeper.alignment_spacing
                for char in display_text:
                    char_surf = timekeeper.font.render(char, True, text_color)
                    surface.blit(char_surf, char_surf.get_rect(midleft=(current_x, y_pos)))
                    current_x += char_surf.get_width() + spacing
        if not drawn_stretched:
            text_surf = timekeeper.font.render(display_text, True, text_color)
            text_rect = text_surf.get_rect()
            if timekeeper.alignment == "left":
                text_rect.midleft = (draw_rect.left + timekeeper.alignment_spacing, y_pos)
            elif timekeeper.alignment == "right":
                text_rect.midright = (draw_rect.right - timekeeper.alignment_spacing, y_pos)
            else:
                text_rect.center = draw_rect.center
            surface.blit(text_surf, text_rect)
            timekeeper.last_text_x = text_rect.x
            surface.set_clip(old_clip)


def react(timekeeper, event=None):
    if timekeeper.state != "enabled" or not timekeeper.visible:
        return
    is_inside = misc.is_point_over_widget(timekeeper, pygame.mouse.get_pos())
    if event:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_inside:
            timekeeper.trigger_event("<PRESS>")
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and is_inside:
            timekeeper.trigger_event("<RELEASE>")
        elif event.type == pygame.KEYDOWN:
            timekeeper.trigger_event("<KEY>")
            if event.unicode:
                timekeeper.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            timekeeper.trigger_event(f"<{keyname.upper()}>")
    else:
        if timekeeper.ticking:
            now = time.time()
            if not timekeeper.last_updated:
                timekeeper.last_updated = now
            dt = now - timekeeper.last_updated
            timekeeper.last_updated = now
            sign = -1 if timekeeper.is_negative else 1
            curr = ((timekeeper.hours * 3600) + (
                    timekeeper.minutes * 60) + timekeeper.seconds + timekeeper.milliseconds) * sign
            change = -dt if timekeeper.reversed else dt
            next_value = curr + change
            if timekeeper.end_at is not None:
                reached_limit = False
                if not timekeeper.reversed and next_value >= timekeeper.end_at:
                    reached_limit = True
                elif timekeeper.reversed and next_value <= timekeeper.end_at:
                    reached_limit = True
                if reached_limit:
                    split_to_values(timekeeper, timekeeper.end_at)
                    timekeeper.stop()
                    timekeeper.trigger_event("<FINISHED>")
                    return
            split_to_values(timekeeper, next_value)