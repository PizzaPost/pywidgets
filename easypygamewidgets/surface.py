# surface.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import time
from typing import Any

import pygame

from easypygamewidgets import misc
from easypygamewidgets.masterWidget import Widget, Tooltipable, Screenable, Deletable

pygame.init()


# PERFECTION
# everything private/properties ❌
# basic animations ✅
# cache system ✅
# config suggestions ❌
# optimized set_screen function ❌

class Surface(Widget, Tooltipable, Screenable, Deletable):
    def __init__(self, surface: pygame.Surface, screen: "easypygamewidgets.Screen | None" = None,
                 state: str | None = None,
                 active_hover_cursor: pygame.Cursor | None = None,
                 disabled_hover_cursor: pygame.Cursor | None = None,
                 active_pressed_cursor: pygame.Cursor | None = None, dragable: bool = False, layer=1000,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, anchor_x: str = "left", anchor_y: str = "top",
                 visible: bool | None = None, data: Any = None):
        super().__init__()
        self._surface = surface
        if screen:
            screen.add_widget(self)
            self._screen = screen
            if state:
                self._state = state
            if visible is not None:
                self._visible = visible
        else:
            self._screen = None
            self._visible = True if visible is None else visible
            if state:
                self._state = state
            else:
                self._state = "enabled"
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
                        f"No custom cursor is used for a surface because it's not a pygame.Cursor object. ({cursor})")
                self._cursors[name] = None
        self._dragable = dragable
        self._layer = layer
        self._tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self._layer + 1)
            if not tooltip.style:
                tooltip.configure(active_unpressed_text_color=(255, 255, 255, 255),
                                  active_unpressed_background_color=(50, 50, 50, 255),
                                  active_unpressed_border_color=(100, 100, 100, 255))
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self._data = data
        self._width = surface.get_width()
        self._height = surface.get_height()
        self._x = 0
        self._y = 0
        self._alive = True
        self._pressed = False
        self._rect = surface.get_rect()
        self._original_cursor = None
        self._drag_offset = None
        self._is_dragging = False
        self._last_checked_dragging = None
        self._bindings = {}
        self._original_surface = surface
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
        self._dialog = None

        misc.add_widget(self)

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value

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
    def dragable(self):
        return self._dragable

    @dragable.setter
    def dragable(self, value):
        self._dragable = value

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
    def original_surface(self):
        return self._original_surface

    @original_surface.setter
    def original_surface(self, value):
        self._original_surface = value

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
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, value):
        self._dialog = value

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'surface' in kwargs:
            self._original_surface = kwargs["surface"]
            self._width = self._original_surface.get_width()
            self._height = self._original_surface.get_height()
            if self._current_scale != 1 or self._current_rotation != 0:
                new_width = int(self._width * self._current_scale)
                new_height = int(self._height * self._current_scale)
                if new_width > 0 and new_height > 0:
                    if self._use_rotozoom:
                        self._surface = pygame.transform.rotozoom(self._original_surface, self._current_rotation,
                                                                  self._current_scale)
                    else:
                        scaled_surface = pygame.transform.smoothscale(self._original_surface, (new_width, new_height))
                        self._surface = pygame.transform.rotate(scaled_surface, self._current_rotation)
            else:
                self._surface = self._original_surface.copy()
        if any(k in kwargs for k in ('x', 'y', 'surface', 'anchor_x', 'anchor_y',)):
            self._rect = self._surface.get_rect(topleft=(self._x, self._y))
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        if 'layer' in kwargs:
            misc.resort_layers()
        return self

    def config(self, **kwargs):
        return self.configure(**kwargs)

    def trigger_event(self, event: str, *args, **kwargs):
        if event in self._bindings:
            binding_data = self._bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            offset_x, offset_y = misc.get_offset(self)
            total_offset_x = offset_x + round(self._current_offset[0])
            total_offset_y = offset_y + round(self._current_offset[1])
            if not require_hover or self._rect.move(total_offset_x, total_offset_y).collidepoint(
                    pygame.mouse.get_pos()):
                command(*args, **kwargs)

    def set_tooltip(self, tooltip):
        self._tooltip = tooltip
        tooltip.configure(layer=self._layer + 1)
        if not tooltip.style:
            tooltip.configure(active_unpressed_text_color=(255, 255, 255, 255),
                              active_unpressed_background_color=(50, 50, 50, 255),
                              active_unpressed_border_color=(100, 100, 100, 255))
        return self

    def scale(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self._target_scale = 1
        else:
            self._target_scale = value
        self._scale_step = (self._target_scale - self._current_scale) / frames_to_finish
        self.update_animation()
        return self

    def rotate(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self._target_rotation = 0
        else:
            self._target_rotation = value
        self._rotation_step = (self._target_rotation - self._current_rotation) / frames_to_finish
        self.update_animation()
        return self

    def rotozoom(self, scale=None, rotation=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self._target_scale = 1 if scale is None else scale
        self._scale_step = (self._target_scale - self._current_scale) / frames_to_finish
        self._target_rotation = 0 if rotation is None else rotation
        self._rotation_step = (self._target_rotation - self._current_rotation) / frames_to_finish
        self._use_rotozoom = True
        self.update_animation()
        return self

    def offset(self, value: tuple[int, int], frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self._target_offset = (0, 0) if value is None else value
        self._offset_step[0] = (self._target_offset[0] - self._current_offset[0]) / frames_to_finish
        self._offset_step[1] = (self._target_offset[1] - self._current_offset[1]) / frames_to_finish
        self.update_animation()
        return self

    def update_animation(self):
        needs_transform = False
        if self._current_scale != self._target_scale:
            if abs(self._current_scale - self._target_scale) <= abs(self._scale_step):
                self._current_scale = self._target_scale
            else:
                self._current_scale += self._scale_step
            needs_transform = True
        if self._current_rotation != self._target_rotation:
            if abs(self._current_rotation - self._target_rotation) <= abs(self._rotation_step):
                self._current_rotation = self._target_rotation
            else:
                self._current_rotation += self._rotation_step
            needs_transform = True
        for x in range(2):
            if self._current_offset[x] != self._target_offset[x]:
                if abs(self._current_offset[x] - self._target_offset[x]) <= abs(self._offset_step[x]):
                    self._current_offset[x] = float(self._target_offset[x])
                else:
                    self._current_offset[x] += self._offset_step[x]
        if needs_transform:
            if self._current_scale != 1 or self._current_rotation != 0:
                new_width = int(self._original_surface.get_width() * self._current_scale)
                new_height = int(self._original_surface.get_height() * self._current_scale)
                if new_width > 0 and new_height > 0:
                    if self._use_rotozoom:
                        self._surface = pygame.transform.rotozoom(self._original_surface, self._current_rotation,
                                                                  self._current_scale)
                    else:
                        scaled_surface = pygame.transform.smoothscale(self._original_surface, (new_width, new_height))
                        self._surface = pygame.transform.rotate(scaled_surface, self._current_rotation)
            else:
                self._surface = self._original_surface.copy()
            old_center = self._rect.center
            self._rect = self._surface.get_rect()
            self._rect.center = old_center
            self._x = self._rect.x
            self._y = self._rect.y

    def draw(self, window: pygame.Surface):
        if not self._alive or not self._visible:
            return
        mouse_pos = pygame.mouse.get_pos()
        offset_x, offset_y = misc.get_offset(self)
        total_offset_x = offset_x + round(self._current_offset[0])
        total_offset_y = offset_y + round(self._current_offset[1])
        interaction_rect = self._rect.move(total_offset_x, total_offset_y)
        is_hovering = interaction_rect.collidepoint(mouse_pos)
        if is_hovering:
            if self._state == "enabled":
                if self._pressed:
                    cursor_key = "active_pressed"
                else:
                    cursor_key = "active_hover"
            else:
                cursor_key = "disabled_hover"
            target_cursor = self._cursors.get(cursor_key)
            if target_cursor:
                current_cursor = pygame.mouse.get_cursor()
                if current_cursor != target_cursor:
                    if self._original_cursor is None:
                        self._original_cursor = current_cursor
                    pygame.mouse.set_cursor(target_cursor)
        else:
            if self._original_cursor:
                pygame.mouse.set_cursor(self._original_cursor)
                self._original_cursor = None

        if is_hovering and not getattr(self, "is_hovered", False):
            self._is_hovered = True
            self.trigger_event("<MOUSE-IN>")
            if self._tooltip:
                self._tooltip.show()
        elif is_hovering and getattr(self, "is_hovered", False):
            self._is_hovered = True
            self.trigger_event("<HOVER>")
        elif not is_hovering and getattr(self, "is_hovered", False):
            self._is_hovered = False
            self.trigger_event("<MOUSE-OUT>")
            if self._tooltip:
                self._tooltip.hide()

        draw_rect = self._rect.move(total_offset_x, total_offset_y)
        window.blit(self._surface, draw_rect)

    def react(self, event=None):
        if self._state != "enabled" or not self._visible:
            self._pressed = False
            return
        mouse_pos = pygame.mouse.get_pos()
        offset_x, offset_y = misc.get_offset(self)
        total_offset_x = offset_x + round(self._current_offset[0])
        total_offset_y = offset_y + round(self._current_offset[1])
        interaction_rect = self._rect.move(total_offset_x, total_offset_y)
        is_inside = interaction_rect.collidepoint(mouse_pos)
        current_time = time.time()
        if not event:
            if pygame.mouse.get_pressed()[0] and is_inside:
                self._pressed = True
                self.trigger_event("<HOLD>")
            elif not pygame.mouse.get_pressed()[0] and is_inside:
                if self._pressed:
                    self._pressed = False
                    self.trigger_event("<RELEASE>")
            elif not pygame.mouse.get_pressed()[0] and not is_inside:
                self._pressed = False
        else:
            if event.type == pygame.MOUSEMOTION:
                if self._pressed and self._dragable:
                    if is_inside or self._is_dragging:
                        self._is_dragging = True
                        self._last_checked_dragging = current_time
                        if self._drag_offset:
                            new_x = mouse_pos[0] - self._drag_offset[0] - total_offset_x
                            new_y = mouse_pos[1] - self._drag_offset[1] - total_offset_y
                            self.place(new_x, new_y, suppress_anchor=True)
            if event.type == pygame.KEYDOWN:
                self.trigger_event("<KEY>")
                if event.unicode:
                    self.trigger_event(event.unicode)
                keyname = pygame.key.name(event.key)
                self.trigger_event(f"<{keyname.upper()}>")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.trigger_event("<PRESS>")
                    if is_inside:
                        self._pressed = True
                        self._drag_offset = (mouse_pos[0] - (self._rect.x + total_offset_x),
                                             mouse_pos[1] - (self._rect.y + total_offset_y))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self._pressed:
                    self.trigger_event("<RELEASE>")
                    self._pressed = False
                    self._is_dragging = False
        if self._last_checked_dragging:
            if current_time - self._last_checked_dragging > 0.2:
                self._is_dragging = False
        if self._pressed and not self._is_dragging:
            self.trigger_event("<HOLD>")
        if self._pressed and self._is_dragging:
            self.trigger_event("<DRAG>")