# tooltip.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import os
import pathlib
from typing import Any

import pygame

from easypygamewidgets import font, misc
from easypygamewidgets.masterWidget import Widget

pygame.init()


# PERFECTION
# everything private/properties ❌
# basic animations ❌
# free spacing ❌
# cache system ❌
# config suggestions ❌
# rgba color ❌
# four different corner radii ❌

class Tooltip(Widget):
    def __init__(self,
                 widget: "easypygamewidgets.Button | easypygamewidgets.Entry | easypygamewidgets.Label | easypygamewidgets.Slider | easypygamewidgets.Surface | easypygamewidgets.Timekeeper | None" = None,
                 auto_size: bool = True, width: int = 180,
                 height: int = 80,
                 text: str = "easypygamewidgets Tooltip",
                 active_unpressed_text_color: tuple | None = None,
                 active_unpressed_background_color: tuple | None = None,
                 active_unpressed_border_color: tuple | None = None,
                 border_thickness: int = 2,
                 hide_text: bool = False,
                 hide_background: bool = False,
                 hide_border: bool = False,
                 active_hover_cursor: pygame.Cursor | None = None,
                 font: pygame.font.Font | pygame.font.SysFont = font.tooltip_font, alignment: str = "center",
                 alignment_spacing: int = 20, corner_radius: int = 25, layer=1000, style: str | None = None,
                 suppress_icon=False, icon: "pygame.Surface | easypygamewidgets.Surface | None" = None,
                 line_spacing: int = 30, min_width: int | None = None, max_width: int | None = None,
                 min_height: int | None = None, max_height: int | None = None, anchor_x: str = "left",
                 anchor_y: str = "top", visible: bool = False, data: Any = None):
        super().__init__()
        self._bindings = {}
        self._style = style
        self._icon = None
        self._layer = layer
        self._font = font
        self._line_spacing = line_spacing
        if not style:
            self._active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self._active_unpressed_background_color = normalize_color((50, 50, 50, 255))
            self._active_unpressed_border_color = normalize_color((100, 100, 100, 255))
        if widget:
            widget.set_tooltip(self)
        self._auto_size = auto_size
        self._width = width
        self._height = height
        if auto_size:
            temp_surf = font.render(text, True, (0, 0, 0))
            text_w, text_h = temp_surf.get_size()
            self._height = text_h + 20
            icon_offset = self._height if icon and not suppress_icon else 0
            self._width = text_w + (alignment_spacing * 2) + icon_offset
            if min_width:
                self._width = max(self._width, min_width)
            if max_width:
                self._width = min(self._width, max_width)
            if min_height:
                self._height = max(self._height, min_height)
            if max_height:
                self._height = min(self._height, max_height)
        self._text = text
        self._border_thickness = border_thickness
        self._hide_text = hide_text
        self._hide_background = hide_background
        self._hide_border = hide_border
        if style == "info":
            if not icon:
                self._icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                            "assets", "tooltip", "info.png"))
            self._active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self._active_unpressed_background_color = normalize_color((46, 55, 90, 255))
            self._active_unpressed_border_color = normalize_color((39, 78, 194, 255))
        elif style == "warning":
            if not icon:
                self._icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                            "assets", "tooltip", "warning.png"))
            self._active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self._active_unpressed_background_color = normalize_color((111, 100, 34, 255))
            self._active_unpressed_border_color = normalize_color((186, 167, 46, 255))
        elif style == "blocked":
            if not icon:
                self._icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                            "assets", "tooltip", "blocked.png"))
            self._active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self._active_unpressed_background_color = normalize_color((150, 63, 60, 255))
            self._active_unpressed_border_color = normalize_color((188, 46, 41, 255))

        if active_unpressed_text_color:
            self._active_unpressed_text_color = normalize_color(active_unpressed_text_color)
            self._style = "custom"
        if active_unpressed_background_color:
            self._active_unpressed_background_color = normalize_color(active_unpressed_background_color)
            self._style = "custom"
        if active_unpressed_border_color:
            self._active_unpressed_border_color = normalize_color(active_unpressed_border_color)
            self._style = "custom"
        cursor_input = {
            "active_hover": active_hover_cursor
        }
        self._cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, pygame.cursors.Cursor):
                self._cursors[name] = cursor
            else:
                if cursor is not None:
                    print(
                        f"No custom cursor is used for the tooltip {text} because it's not a pygame.Cursor object. ({cursor})")
                self._cursors[name] = None
        self._alignment = alignment
        self._alignment_spacing = alignment_spacing
        self._corner_radius = corner_radius
        self._suppress_icon = suppress_icon
        if icon:
            self._icon = icon
        self._min_width = min_width
        self._max_width = max_width
        self._min_height = min_height
        self._max_height = max_height
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self._data = data
        self._x = 0
        self._y = 0
        self._pressed = False
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._original_cursor = None
        self._visible = visible
        self._needs_redraw = True
        self._cached_surface = None

        safe_set_linesize(font, line_spacing)

        misc.add_widget(self)

    @property
    def bindings(self):
        return self._bindings

    @bindings.setter
    def bindings(self, value):
        self._bindings = value

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style = value
        if value == "info":
            self._icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                        "assets", "tooltip", "info.png"))
            self._active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self._active_unpressed_background_color = normalize_color((46, 55, 90, 255))
            self._active_unpressed_border_color = normalize_color((39, 78, 194, 255))
        elif value == "warning":
            self._icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                        "assets", "tooltip", "warning.png"))
            self._active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self._active_unpressed_background_color = normalize_color((111, 100, 34, 255))
            self._active_unpressed_border_color = normalize_color((186, 167, 46, 255))
        elif value == "blocked":
            self._icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                        "assets", "tooltip", "blocked.png"))
            self._active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self._active_unpressed_background_color = normalize_color((150, 63, 60, 255))
            self._active_unpressed_border_color = normalize_color((188, 46, 41, 255))

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value
        misc.resort_layers()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def line_spacing(self):
        return self._line_spacing

    @line_spacing.setter
    def line_spacing(self, value):
        self._line_spacing = value

    @property
    def active_unpressed_text_color(self):
        return self._active_unpressed_text_color

    @active_unpressed_text_color.setter
    def active_unpressed_text_color(self, value):
        self._active_unpressed_text_color = normalize_color(value)

    @property
    def active_unpressed_background_color(self):
        return self._active_unpressed_background_color

    @active_unpressed_background_color.setter
    def active_unpressed_background_color(self, value):
        self._active_unpressed_background_color = normalize_color(value)

    @property
    def active_unpressed_border_color(self):
        return self._active_unpressed_border_color

    @active_unpressed_border_color.setter
    def active_unpressed_border_color(self, value):
        self._active_unpressed_border_color = normalize_color(value)

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
    def cursors(self):
        return self._cursors

    @cursors.setter
    def cursors(self, value):
        self._cursors = value

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
    def suppress_icon(self):
        return self._suppress_icon

    @suppress_icon.setter
    def suppress_icon(self, value):
        self._suppress_icon = value

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
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def needs_redraw(self):
        return self._needs_redraw

    @needs_redraw.setter
    def needs_redraw(self, value):
        self._needs_redraw = value

    @property
    def cached_surface(self):
        return self._cached_surface

    @cached_surface.setter
    def cached_surface(self, value):
        self._cached_surface = value

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._needs_redraw = True
        if any(k in kwargs for k in
               ('auto_size', 'x', 'y', 'width', 'height', 'min_width', 'max_width', 'min_height', 'max_height', 'text',
                'icon', 'suppress_icon', 'alignment_spacing', 'font')):
            if self._auto_size:
                temp_surf = self._font.render(self._text, True, (0, 0, 0))
                text_w, text_h = temp_surf.get_size()
                self._height = text_h + 20
                icon_offset = self._height if self._icon and not self._suppress_icon else 0
                self._width = text_w + (self._alignment_spacing * 2) + icon_offset
                if self._min_width:
                    self._width = max(self._width, self._min_width)
                if self._max_width:
                    self._width = min(self._width, self._max_width)
                if self._min_height:
                    self._height = max(self._height, self._min_height)
                if self._max_height:
                    self._height = min(self._height, self._max_height)
            self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        if 'widget' in kwargs:
            kwargs["widget"].set_tooltip(self)
        if 'line_spacing' in kwargs or 'font' in kwargs:
            safe_set_linesize(self._font, self._line_spacing)
        return self

    def config(self, **kwargs):
        self.configure(**kwargs)

    def show(self):
        self._visible = True
        self.trigger_event("<SHOW>")
        return self

    def hide(self):
        self._visible = False
        self.trigger_event("<HIDE>")
        return self

    def add_widget(self, widget):
        widget.set_tooltip(self)
        return self

    def remove_widget(self, widget):
        widget.remove_tooltip()
        return self


def safe_set_linesize(font, line_spacing):
    descent = abs(font.get_descent())
    font.set_linesize(line_spacing + descent)


def normalize_color(color):
    if color is None:
        return (0, 0, 0, 0)
    if len(color) == 3:
        return (*color, 255)
    return color


def render_tooltip_surface(tooltip):
    text_color = tooltip.active_unpressed_text_color
    bg_color = tooltip.active_unpressed_background_color
    brd_color = tooltip.active_unpressed_border_color
    if tooltip.auto_size:
        temp_surf = tooltip.font.render(tooltip.text, True, (0, 0, 0))
        text_w, text_h = temp_surf.get_size()
        tooltip.height = text_h + 20
        icon_offset = tooltip.height if tooltip.icon and not tooltip.suppress_icon else 0
        tooltip.width = text_w + (tooltip.alignment_spacing * 2) + icon_offset
        if tooltip.min_width:
            tooltip.width = max(tooltip.width, tooltip.min_width)
        if tooltip.max_width:
            tooltip.width = min(tooltip.width, tooltip.max_width)
        if tooltip.min_height:
            tooltip.height = max(tooltip.height, tooltip.min_height)
        if tooltip.max_height:
            tooltip.height = min(tooltip.height, tooltip.max_height)
        tooltip.rect = pygame.Rect(tooltip.x, tooltip.y, tooltip.width, tooltip.height)
    cached = pygame.Surface((tooltip.width, tooltip.height), pygame.SRCALPHA)
    local_rect = pygame.Rect(0, 0, tooltip.width, tooltip.height)
    if not tooltip.hide_background:
        tmp = pygame.Surface(pygame.Rect(local_rect).size, pygame.SRCALPHA)
        pygame.draw.rect(tmp, bg_color, tmp.get_rect(), border_radius=tooltip.corner_radius)
        cached.blit(tmp, local_rect)
    icon_offset = local_rect.height if tooltip.icon and not tooltip.suppress_icon else 0
    text_area_left = icon_offset
    text_area_width = local_rect.width - icon_offset
    if tooltip.icon and not tooltip.suppress_icon:
        scaled_icon = pygame.transform.smoothscale(tooltip.icon if isinstance(tooltip.icon, pygame.Surface)
                                                   else tooltip.icon.surface, (local_rect.height,
                                                                               local_rect.height))
        cached.blit(scaled_icon, (0, 0))
    if not tooltip.hide_border and brd_color:
        tmp = pygame.Surface(pygame.Rect(local_rect).size, pygame.SRCALPHA)
        pygame.draw.rect(tmp, brd_color, tmp.get_rect(), width=tooltip.border_thickness,
                         border_radius=tooltip.corner_radius)
        cached.blit(tmp, local_rect)
    if not tooltip.hide_text:
        descent = abs(tooltip.font.get_descent())
        if tooltip.alignment == "stretched" and len(tooltip.text) > 1 and not tooltip.auto_size:
            total_char_width = sum(tooltip.font.render(char, True, text_color).get_width() for char in tooltip.text)
            available_width = text_area_width - (tooltip.alignment_spacing * 2)
            if available_width > total_char_width:
                spacing = (available_width - total_char_width) / (len(tooltip.text) - 1)
                current_x = text_area_left + tooltip.alignment_spacing
                for char in tooltip.text:
                    char_surf = tooltip.font.render(char, True, text_color)
                    char_surf.set_alpha(text_color[3])
                    cached.blit(char_surf, char_surf.get_rect(midleft=(current_x, local_rect.centery)))
                    current_x += char_surf.get_width() + spacing
            else:
                text_surf = tooltip.font.render(tooltip.text, True, text_color)
                text_surf.set_alpha(text_color[3])
                cached.blit(text_surf,
                            text_surf.get_rect(
                                center=(text_area_left + text_area_width // 2, local_rect.centery)))
        else:
            text_surf = tooltip.font.render(tooltip.text, True, text_color)
            text_surf.set_alpha(text_color[3])
            text_rect = text_surf.get_rect()
            text_rect.centery = local_rect.centery
            if tooltip.alignment == "left":
                text_rect.left = text_area_left + tooltip.alignment_spacing
            elif tooltip.alignment == "right":
                text_rect.right = local_rect.right - tooltip.alignment_spacing
            else:
                text_rect.centerx = text_area_left + (text_area_width // 2)
            cached.blit(text_surf, text_rect)
    tooltip.cached_surface = cached
    tooltip.needs_redraw = False


def draw(tooltip, surface: pygame.Surface):
    if not tooltip._visible:
        return
    safe_set_linesize(tooltip.font, tooltip.line_spacing)
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = misc.is_point_over_widget(tooltip, mouse_pos)
    if tooltip.needs_redraw or tooltip.cached_surface is None:
        render_tooltip_surface(tooltip)
    if is_hovering:
        cursor_key = "active_hover"
        target_cursor = tooltip.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if tooltip.original_cursor is None:
                    tooltip.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if tooltip.original_cursor:
            pygame.mouse.set_cursor(tooltip.original_cursor)
            tooltip.original_cursor = None

    if is_hovering and not getattr(tooltip, "is_hovered", False):
        tooltip.is_hovered = True
        tooltip.trigger_event("<SHOW>")
    elif is_hovering and getattr(tooltip, "is_hovered", False):
        tooltip.is_hovered = True
        tooltip.trigger_event("<HOVER>")
    elif not is_hovering and getattr(tooltip, "is_hovered", False):
        tooltip.is_hovered = False
        tooltip.trigger_event("<HIDE>")

    draw_rect = tooltip.rect.move(mouse_pos[0], mouse_pos[1])
    if tooltip.visible:
        surface.blit(tooltip.cached_surface, draw_rect)


def react(tooltip, event=None): pass