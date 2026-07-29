# screen.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

from typing import Any

import pygame

from easypygamewidgets import misc
from easypygamewidgets.masterWidget import Deletable

pygame.init()


# PERFECTION
# everything private/properties ❌
# animations ❌

class Screen(Deletable):
    def __init__(self,
                 widgets: "list[easypygamewidgets.Button | easypygamewidgets.Entry | easypygamewidget.Label | easypygamewidgets.Slider | easypygamewidgets.Surface | easypygamewidgets.Timekeeper | easypygamewidgets.Tooltip]" = None,
                 darken_background_with_alpha: int = 0, visible: bool = False, enabled: bool = True, x: int = 0,
                 y: int = 0, layer=1000, data: Any = None):
        super().__init__()
        self._widgets = widgets if widgets is not None else []
        self._darken_background_with_alpha = max(min(darken_background_with_alpha, 255), 0)
        self._visible = visible
        self._enabled = enabled
        self._x = x
        self._y = y
        self._layer = layer
        self._data = data

        misc.add_widget(self)

        self.update_widget_state(True, True)

    @property
    def widgets(self):
        return self._widgets

    @widgets.setter
    def widgets(self, value):
        self._widgets = value

    @property
    def darken_background_with_alpha(self):
        return self._darken_background_with_alpha

    @darken_background_with_alpha.setter
    def darken_background_with_alpha(self, value):
        self._darken_background_with_alpha = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

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
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


    def add_widget(self, widget):
        if widget in self.widgets:
            widget.screen.remove_widget(widget)
        self.widgets.append(widget)
        widget.screen = self
        widget.visible = self.visible
        widget.state = "enabled" if self.enabled else "disabled"
        return self

    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
        return self

    def show(self):
        self.visible = True
        self.update_widget_state(True, False)
        return self

    def hide(self):
        self.visible = False
        self.update_widget_state(True, False)
        return self

    def enable(self):
        self.enabled = True
        self.update_widget_state(False, True)
        return self

    def disable(self):
        self.enabled = False
        self.update_widget_state(False, True)
        return self

    def update_widget_state(self, update_visibility: bool = True, update_state: bool = True):
        for widget in self.widgets:
            if update_visibility:
                if self.visible:
                    widget.configure(visible=True)
                else:
                    widget.configure(visible=False)
            if update_state:
                if self.enabled:
                    widget.configure(state="enabled")
                else:
                    widget.configure(state="disabled")

    def place(self, x: int, y: int, mode: str = "px"):
        if mode == "px":
            self.x = x
            self.y = y
        elif mode in ("%", "percent", "percentage"):
            screen_width = misc.pg.get_width()
            screen_height = misc.pg.get_height()
            self.x = int(x * screen_width / 100)
            self.y = int(y * screen_height / 100)
        else:
            self.x = x
            self.y = y
            print(f"Invalid Mode: {mode}\nFallback: px")
        return self

    def delete(self):
        if self in misc.all_widgets:
            misc.all_widgets.remove(self)
        for widget in self._widgets:
            widget.set_screen(None)
            widget.delete()
        self.widgets.clear()

    def draw(self, surface: pygame.Surface):
        if self.darken_background_with_alpha and self.visible:
            background_surf = pygame.Surface(surface.get_size())
            background_surf.fill((0, 0, 0))
            background_surf.set_alpha(self.darken_background_with_alpha)
            surface.blit(background_surf, (0, 0))