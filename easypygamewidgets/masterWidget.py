import copy

import pygame

from easypygamewidgets import misc


class Widget:
    def clone(self):
        copied_widget = copy.deepcopy(self)
        misc.all_widgets.append(copied_widget)
        misc.resort_layers()
        return copied_widget

    def delete(self):
        self._alive = False
        if self in misc.all_widgets:
            misc.all_widgets.remove(self)

    def bind(self, event: str, command, require_hover: bool = True):
        self._bindings[event] = {"command": command, "require_hover": require_hover}
        return self

    def trigger_event(self, event: str, *args, **kwargs):
        if event in self._bindings:
            binding_data = self._bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            if not require_hover or misc.is_point_over_widget(self, pygame.mouse.get_pos()):
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
                anchor_offset[0] = self._width // 2
            elif self._anchor_x == "right":
                anchor_offset[0] = self._width
            if self._anchor_y == "top":
                anchor_offset[1] = 0
            elif self._anchor_y == "center":
                anchor_offset[1] = self._height // 2
            elif self._anchor_y == "bottom":
                anchor_offset[1] = self._height
            self.x -= anchor_offset[0]
            self.y -= anchor_offset[1]
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._needs_transform = True
        return self

    def anchor(self, anchor_x: str = "left", anchor_y: str = "top"):
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self.place(self._x, self._y)
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
        if self in screen.widgets:
            return self
        self._screen = screen
        screen.add_widget(self)
        return self