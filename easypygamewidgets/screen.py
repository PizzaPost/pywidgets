# screen.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

from typing import Any

import pygame

from easypygamewidgets import misc
from easypygamewidgets.masterWidget import Widget, Deletable

pygame.init()


# PERFECTION
# cursors (next update) ❌
# bindings (next update) ❌
# missing three animations ❔

class Screen(Widget, Deletable):
    def __init__(self, auto_size: bool = True, width: int | None = None, height: int | None = None,
                 min_width: int | None = None, max_width: int | None = None, min_height: int | None = None,
                 max_height: int | None = None, active_hover_cursor: pygame.Cursor | None = None,
                 disabled_hover_cursor: pygame.Cursor | None = None,
                 active_pressed_cursor: pygame.Cursor | None = None,
                 widgets: "list[easypygamewidgets.Button | easypygamewidgets.Entry | easypygamewidget.Label | easypygamewidgets.Slider | easypygamewidgets.Surface | easypygamewidgets.Timekeeper | easypygamewidgets.Tooltip]" = None,
                 darken_background_with_alpha: int = 0, anchor_x: str = "left", anchor_y: str = "top",
                 visible: bool = False, enabled: bool = True, x: int = 0,
                 y: int = 0, layer=1000, ignore_empty_cells: bool = False, row_spacing: int = 10,
                 column_spacing: int = 10, data: Any = None):
        super().__init__()
        self._bindings = {}
        self._row_spacing = row_spacing
        self._column_spacing = column_spacing
        self._auto_size = auto_size
        if auto_size:
            self._width = 0
            self._height = 0
        else:
            self._width = width if width is not None else (misc.pg.get_width())
            self._height = height if height is not None else (misc.pg.get_height())
        self._min_width = min_width
        self._max_width = max_width
        self._min_height = min_height
        self._max_height = max_height
        cursor_input = {
            "active_hover": active_hover_cursor,
            "disabled_hover": disabled_hover_cursor,
            "active_pressed": active_pressed_cursor
        }
        self._cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, pygame.Cursor):
                self._cursors[name] = cursor
            else:
                if cursor is not None:
                    print(f"No custom cursor is used for a grid because it's not a pygame.Cursor object. ({cursor})")
                self._cursors[name] = None
        self._widgets = widgets if widgets is not None else []
        self._darken_background_with_alpha = max(min(darken_background_with_alpha, 255), 0)
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self._visible = visible
        self._enabled = enabled
        self._x = x
        self._y = y
        self._layer = layer
        self._ignore_empty_cells = ignore_empty_cells
        self._data = data
        self._fill_width = width is None
        self._fill_height = height is None
        self._last_pg_size = None
        self._alive = True
        self._pressed = False
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._original_cursor = None
        self._is_hovered = False
        self._target_offset = (0, 0)
        self._current_offset = [0, 0]
        self._offset_step = [0, 0]

        misc.add_widget(self)

        self.update_widget_state(True, True)

    @property
    def bindings(self):
        return self._bindings

    @bindings.setter
    def bindings(self, value):
        self._bindings = value

    @property
    def auto_size(self):
        return self._auto_size

    @auto_size.setter
    def auto_size(self, value):
        self._auto_size = value
        self.recalculate_grid()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._fill_width = value is None
        self._width = value if value is not None else (misc.pg.get_width())
        if not self._auto_size:
            self.recalculate_grid()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._fill_height = value is None
        self._height = value if value is not None else (misc.pg.get_height())
        if not self._auto_size:
            self.recalculate_grid()

    @property
    def row_spacing(self):
        return self._row_spacing

    @row_spacing.setter
    def row_spacing(self, value):
        self._row_spacing = value
        self.recalculate_grid()

    @property
    def column_spacing(self):
        return self._column_spacing

    @column_spacing.setter
    def column_spacing(self, value):
        self._column_spacing = value
        self.recalculate_grid()

    @property
    def min_width(self):
        return self._min_width

    @min_width.setter
    def min_width(self, value):
        self._min_width = value
        self.recalculate_grid()

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, value):
        self._max_width = value
        self.recalculate_grid()

    @property
    def min_height(self):
        return self._min_height

    @min_height.setter
    def min_height(self, value):
        self._min_height = value
        self.recalculate_grid()

    @property
    def max_height(self):
        return self._max_height

    @max_height.setter
    def max_height(self, value):
        self._max_height = value
        self.recalculate_grid()

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
    def ignore_empty_cells(self):
        return self._ignore_empty_cells

    @ignore_empty_cells.setter
    def ignore_empty_cells(self, value):
        self._ignore_empty_cells = value
        self.recalculate_grid()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

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
        self.recalculate_grid()

    @property
    def original_cursor(self):
        return self._original_cursor

    @original_cursor.setter
    def original_cursor(self, value):
        self._original_cursor = value

    @property
    def is_hovered(self):
        return self._is_hovered

    @is_hovered.setter
    def is_hovered(self, value):
        self._is_hovered = value

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

    def offset(self, value: tuple[int, int], frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self._target_offset = (0, 0) if value is None else value
        self._offset_step[0] = (self._target_offset[0] - self._current_offset[0]) / frames_to_finish
        self._offset_step[1] = (self._target_offset[1] - self._current_offset[1]) / frames_to_finish
        self.update_animation()
        return self

    def update_animation(self):
        for x in range(2):
            if self._current_offset[x] != self._target_offset[x]:
                if abs(self._current_offset[x] - self._target_offset[x]) <= abs(self._offset_step[x]):
                    self._current_offset[x] = float(self._target_offset[x])
                else:
                    self._current_offset[x] += self._offset_step[x]

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
        if hasattr(widget, "_grid_row"):
            self.recalculate_grid()
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

    def delete(self):
        if self in misc.all_widgets:
            misc.all_widgets.remove(self)
        for widget in self._widgets:
            widget.set_screen(None)
            widget.delete()
        self.widgets.clear()

    def recalculate_grid(self):
        grid_widgets = [w for w in self._widgets if hasattr(w, "_grid_row")]
        if not grid_widgets: return
        occupied_rows = []
        occupied_cols = []
        for w in grid_widgets:
            occupied_rows.extend(range(w._grid_row, w._grid_row + w._grid_rowspan))
            occupied_cols.extend(range(w._grid_column, w._grid_column + w._grid_columnspan))
        sorted_rows = sorted(occupied_rows)
        sorted_cols = sorted(occupied_cols)
        max_row = sorted_rows[-1] + 1
        max_col = sorted_cols[-1] + 1
        if self._ignore_empty_cells:
            row_map = {orig: i for i, orig in enumerate(sorted_rows)}
            col_map = {orig: i for i, orig in enumerate(sorted_cols)}
            num_rows = len(sorted_rows)
            num_cols = len(sorted_cols)
        else:
            row_map = {i: i for i in range(max_row)}
            col_map = {i: i for i in range(max_col)}
            num_rows = max_row
            num_cols = max_col
        if num_rows == 0 or num_cols == 0: return
        if self._auto_size:
            col_widths = [0] * num_cols
            row_heights = [0] * num_rows
            for w in grid_widgets:
                if w._grid_columnspan == 1:
                    c = col_map.get(w._grid_column)
                    if c is not None:
                        col_widths[c] = max(col_widths[c], w.width)
                if w._grid_rowspan == 1:
                    r = row_map.get(w._grid_row)
                    if r is not None:
                        row_heights[r] = max(row_heights[r], w.height)
            for w in grid_widgets:
                if w._grid_columnspan > 1:
                    cols = [col_map[c] for c in range(w._grid_column, w._grid_column + w._grid_columnspan) if
                            c in col_map]
                    if cols:
                        current = sum(col_widths[c] for c in cols) + self._column_spacing * (len(cols) - 1)
                        if w.width > current:
                            share = (w.width - current) / len(cols)
                            for c in cols:
                                col_widths[c] += share
                if w._grid_rowspan > 1:
                    rows = [row_map[r] for r in range(w._grid_row, w._grid_row + w._grid_rowspan) if r in row_map]
                    if rows:
                        current = sum(row_heights[r] for r in rows) + self._row_spacing * (len(rows) - 1)
                        if w.height > current:
                            share = (w.height - current) / len(rows)
                            for r in rows:
                                row_heights[r] += share
            self._width = int(sum(col_widths) + self._column_spacing * (num_cols - 1))
            self._height = int(sum(row_heights) + self._row_spacing * (num_rows - 1))
            if self._min_width:
                self._width = max(self._width, self._min_width)
            if self._max_width:
                self._width = min(self._width, self._max_width)
            if self._min_height:
                self._height = max(self._height, self._min_height)
            if self._max_height:
                self._height = min(self._height, self._max_height)
        else:
            available_width = misc.pg.get_width() if self._fill_width else self._width
            available_height = misc.pg.get_height() if self._fill_height else self._height
            self._width = available_width
            self._height = available_height
            col_width = (available_width - self._column_spacing * (num_cols - 1)) / num_cols
            row_height = (available_height - self._row_spacing * (num_rows - 1)) / num_rows
            col_widths = [col_width] * num_cols
            row_heights = [row_height] * num_rows
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        col_x = [0.0] * num_cols
        for i in range(1, num_cols):
            col_x[i] = col_x[i - 1] + col_widths[i - 1] + self._column_spacing
        row_y = [0.0] * num_rows
        for i in range(1, num_rows):
            row_y[i] = row_y[i - 1] + row_heights[i - 1] + self._row_spacing
        for w in grid_widgets:
            mapped_c = col_map.get(w._grid_column)
            mapped_r = row_map.get(w._grid_row)
            if mapped_c is None or mapped_r is None:
                continue
            end_c = min(mapped_c + w._grid_columnspan - 1, num_cols - 1)
            end_r = min(mapped_r + w._grid_rowspan - 1, num_rows - 1)
            cell_x = col_x[mapped_c]
            cell_y = row_y[mapped_r]
            cell_w = col_x[end_c] + col_widths[end_c] - cell_x
            cell_h = row_y[end_r] + row_heights[end_r] - cell_y
            offset_x = (cell_w - w.width) / 2
            offset_y = (cell_h - w.height) / 2
            target_x = int(self._x + cell_x + offset_x)
            target_y = int(self._y + cell_y + offset_y)
            w.place(target_x, target_y, suppress_anchor=True)

    def draw(self, surface: pygame.Surface):
        current_pg_size = misc.pg.get_size()
        if current_pg_size != self._last_pg_size:
            self._last_pg_size = current_pg_size
            self.recalculate_grid()
        if self.darken_background_with_alpha and self.visible:
            background_surf = pygame.Surface(surface.get_size())
            background_surf.fill((0, 0, 0))
            background_surf.set_alpha(self.darken_background_with_alpha)
            surface.blit(background_surf, (0, 0))