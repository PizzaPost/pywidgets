import math

import pygame

pygame.init()

all_sliders = []


class Slider:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 16,
                 text: str = "easypygamewidgets Slider", start: int | float = 0,
                 end: int | float = 100, initial_value: int = None, state: str = "enabled",
                 top_left_corner_radius: int = 25,
                 top_right_corner_radius: int = 25,
                 bottom_left_corner_radius: int = 25,
                 bottom_right_corner_radius: int = 25,
                 dot_radius: int = 5,
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
                 click_sound: str | pygame.mixer.Sound = None,
                 active_hover_cursor: pygame.cursors = None,
                 disabled_hover_cursor: pygame.cursors = None,
                 active_pressed_cursor: pygame.cursors = None,
                 font: pygame.font.Font = pygame.font.Font(None, 38), alignment: str = "center",
                 alignment_spacing: int = 20, command=None, show_value_when_pressed: bool = True,
                 show_value_when_hovered: bool = True, show_value_when_unpressed: bool = False,
                 show_value_when_disabled: bool = False,
                 round_display_value: int = 0, show_full_rounding_of_whole_numbers: bool = False):
        if screen:
            screen.add_widget(self)
        self.auto_size = auto_size
        self.width = width
        self.height = height
        self.text = text
        self.start = start
        self.end = end
        self.state = state
        self.start = start
        self.end = end
        self.value = min(max(initial_value or start, start), end)
        self.top_left_corner_radius = top_left_corner_radius
        self.top_right_corner_radius = top_right_corner_radius
        self.bottom_left_corner_radius = bottom_left_corner_radius
        self.bottom_right_corner_radius = bottom_right_corner_radius
        self.dot_radius = dot_radius
        self.active_unpressed_text_color = active_unpressed_text_color
        self.disabled_unpressed_text_color = disabled_unpressed_text_color
        self.active_hover_text_color = active_hover_text_color
        self.disabled_hover_text_color = disabled_hover_text_color
        self.active_pressed_text_color = active_pressed_text_color
        self.active_unpressed_used_background_color = active_unpressed_used_background_color
        self.disabled_unpressed_used_background_color = disabled_unpressed_used_background_color
        self.active_hover_used_background_color = active_hover_used_background_color
        self.disabled_hover_used_background_color = disabled_hover_used_background_color
        self.active_pressed_used_background_color = active_pressed_used_background_color
        self.active_unpressed_unused_background_color = active_unpressed_unused_background_color
        self.disabled_unpressed_unused_background_color = disabled_unpressed_unused_background_color
        self.active_hover_unused_background_color = active_hover_unused_background_color
        self.disabled_hover_unused_background_color = disabled_hover_unused_background_color
        self.active_pressed_unused_background_color = active_pressed_unused_background_color
        self.active_unpressed_dot_color = active_unpressed_dot_color
        self.disabled_unpressed_dot_color = disabled_unpressed_dot_color
        self.active_hover_dot_color = active_hover_dot_color
        self.disabled_hover_dot_color = disabled_hover_dot_color
        self.active_pressed_dot_color = active_pressed_dot_color
        self.active_unpressed_border_color = active_unpressed_border_color
        self.disabled_unpressed_border_color = disabled_unpressed_border_color
        self.active_hover_border_color = active_hover_border_color
        self.disabled_hover_border_color = disabled_hover_border_color
        self.active_pressed_border_color = active_pressed_border_color
        self.active_pressed_display_color = active_pressed_display_color
        self.active_hover_display_color = active_hover_display_color
        self.active_unpressed_display_color = active_unpressed_display_color
        self.disabled_hover_display_color = disabled_hover_display_color
        self.disabled_unpressed_display_color = disabled_unpressed_display_color
        if click_sound:
            if isinstance(click_sound, pygame.mixer.Sound):
                self.click_sound = click_sound
            self.click_sound = pygame.mixer.Sound(click_sound)
        else:
            self.click_sound = None
        cursor_input = {
            "active_hover": active_hover_cursor,
            "disabled_hover": disabled_hover_cursor,
            "active_pressed": active_pressed_cursor
        }
        self.cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, pygame.cursors.Cursor):
                self.cursors[name] = cursor
            else:
                if cursor is not None:
                    print(
                        f"No custom cursor is used for the slider {self.text} because it's not a pygame.cursors.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.font = font
        self.alignment = alignment
        self.alignment_spacing = alignment_spacing
        self.command = command
        self.show_value_when_pressed = show_value_when_pressed
        self.show_value_when_hovered = show_value_when_hovered
        self.show_value_when_unpressed = show_value_when_unpressed
        self.show_value_when_disabled = show_value_when_disabled
        self.round_display_value = round_display_value
        self.show_full_rounding_of_whole_numbers = show_full_rounding_of_whole_numbers
        self.x = 0
        self.y = font.render(text, True, (255, 255, 255)).get_height()
        self.alive = True
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, 60)
        self.original_cursor = None
        self.extra_dot_radius = 0
        self.max_extra_dot_radius = dot_radius + 1
        self.visible = True

        all_sliders.append(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'width' in kwargs:
            self.rect = pygame.Rect(self.x, self.y, self.width, 60)

    def config(self, **kwargs):
        self.configure(**kwargs)

    def delete(self):
        self.alive = False
        if self in all_sliders:
            all_sliders.remove(self)

    def place(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, 60)
        return self

    def execute(self):
        if self.command:
            self.command()
        return self

    def get(self):
        return self.value

    def set(self, value):
        self.value = min(max(value, self.start), self.end)


def draw(slider, surface: pygame.Surface):
    if not slider.alive or not slider.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(slider, mouse_pos)
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

    if slider.auto_size:
        temp_surf = slider.font.render(slider.text, True, text_color)
        slider.width = temp_surf.get_width() + 40 + (slider.alignment_spacing - 20)
        slider.rect = pygame.Rect(slider.x, slider.y, slider.width, slider.height)

    track_y = slider.rect.centery + 5
    track_rect = pygame.Rect(slider.rect.x, track_y - (slider.height // 2), slider.rect.width, slider.height)
    max_radius = min(track_rect.width, track_rect.height) // 2
    tl = min(slider.top_left_corner_radius, max_radius)
    tr = min(slider.top_right_corner_radius, max_radius)
    bl = min(slider.bottom_left_corner_radius, max_radius)
    br = min(slider.bottom_right_corner_radius, max_radius)
    pygame.draw.rect(surface, bg_color_unused, track_rect, border_top_left_radius=tl, border_top_right_radius=tr,
                     border_bottom_left_radius=bl, border_bottom_right_radius=br)
    if slider.end - slider.start != 0:
        pct = (slider.value - slider.start) / (slider.end - slider.start)
    else:
        pct = 0
    pct = max(0, min(1, pct))
    used_width = int(track_rect.width * pct)
    if used_width > 0:
        used_rect = pygame.Rect(track_rect.x, track_rect.y, used_width, track_rect.height)
        fill_max_radius = min(used_rect.width, used_rect.height) // 2
        fill_tl = min(tl, fill_max_radius)
        fill_bl = min(bl, fill_max_radius)
        fill_tr = min(tr, fill_max_radius) if pct >= 0.99 else 0
        fill_br = min(br, fill_max_radius) if pct >= 0.99 else 0
        pygame.draw.rect(surface, bg_color_used, used_rect, border_top_left_radius=fill_tl,
                         border_bottom_left_radius=fill_bl, border_top_right_radius=fill_tr,
                         border_bottom_right_radius=fill_br)
    if brd_color:
        pygame.draw.rect(surface, brd_color, track_rect, width=2, border_top_left_radius=tl,
                         border_top_right_radius=tr, border_bottom_left_radius=bl,
                         border_bottom_right_radius=br)
    dot_x = track_rect.x + used_width
    dot_x = max(track_rect.left + slider.dot_radius, min(dot_x, track_rect.right - slider.dot_radius))
    pygame.draw.circle(surface, dot_color, (int(dot_x), int(track_rect.centery)),
                       slider.dot_radius + slider.extra_dot_radius)
    if (slider.state == "enabled" or slider.show_value_when_disabled) and (
            slider.show_value_when_pressed and slider.pressed or slider.show_value_when_hovered and is_hovering and not slider.pressed or slider.show_value_when_unpressed):
        if slider.show_full_rounding_of_whole_numbers:
            text_surf = slider.font.render(str(round(slider.value, slider.round_display_value)), True, display_color)
        elif not slider.show_full_rounding_of_whole_numbers and slider.value % 1 == 0:
            text_surf = slider.font.render(str(round(slider.value, slider.round_display_value)).replace(".0", ""), True,
                                           display_color)
        elif not slider.show_full_rounding_of_whole_numbers:
            text_surf = slider.font.render(str(round(slider.value)), True, display_color)
        text_rect = text_surf.get_rect()
        text_rect.center = (dot_x, track_rect.bottom + slider.dot_radius + 17)
        surface.blit(text_surf, text_rect)

    text_surf = slider.font.render(slider.text, True, text_color)
    text_rect = text_surf.get_rect()
    text_y_center = track_rect.top - 17 - slider.dot_radius

    if slider.alignment == "stretched" and len(slider.text) > 1 and not slider.auto_size:
        total_char_width = sum(slider.font.render(char, True, text_color).get_width() for char in slider.text)
        available_width = slider.rect.width - (slider.alignment_spacing * 2)
        if available_width > total_char_width:
            spacing = (available_width - total_char_width) / (len(slider.text) - 1)
            current_x = slider.rect.left + slider.alignment_spacing
            for char in slider.text:
                char_surf = slider.font.render(char, True, text_color)
                surface.blit(char_surf, char_surf.get_rect(midleft=(current_x, text_y_center)))
                current_x += char_surf.get_width() + spacing
        else:
            surface.blit(text_surf, text_surf.get_rect(center=(slider.rect.centerx, text_y_center)))
    else:
        if slider.alignment == "left":
            text_rect.midleft = (slider.rect.left + slider.alignment_spacing, text_y_center)
        elif slider.alignment == "right":
            text_rect.midright = (slider.rect.right - slider.alignment_spacing, text_y_center)
        else:
            text_rect.center = (slider.rect.centerx, text_y_center)
        surface.blit(text_surf, text_rect)


def is_point_in_rounded_rect(slider, point):
    if not slider.rect.collidepoint(point): return False
    rect = slider.rect
    r = max(slider.top_left_corner_radius, slider.top_right_corner_radius,
            slider.bottom_left_corner_radius, slider.bottom_right_corner_radius)
    r = min(r, rect.width // 2, rect.height // 2)
    if r <= 0: return True
    x, y = point
    if (rect.left + r <= x <= rect.right - r) or (rect.top + r <= y <= rect.bottom - r):
        return True
    centers = [(rect.left + r, rect.top + r), (rect.right - r, rect.top + r),
               (rect.left + r, rect.bottom - r), (rect.right - r, rect.bottom - r)]
    for cx, cy in centers:
        if ((x - cx) ** 2 + (y - cy) ** 2) <= r ** 2: return True
    return False


def react(slider, event=None):
    if slider.state != "enabled" or not slider.visible:
        slider.pressed = False
        return
    mouse_pos = pygame.mouse.get_pos()
    is_inside = is_point_in_rounded_rect(slider, mouse_pos)

    def update_value():
        relative_x = mouse_pos[0] - slider.rect.x
        pct = relative_x / slider.rect.width
        pct = max(0, min(1, pct))
        slider.value = slider.start + (pct * (slider.end - slider.start))
        if slider.command:
            slider.command()

    if not event:
        if pygame.mouse.get_pressed()[0] and is_inside:
            slider.pressed = True
        if slider.pressed:
            if pygame.mouse.get_pressed()[0]:
                update_value()
            else:
                slider.pressed = False
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_inside:
                slider.pressed = True
                update_value()
                if slider.click_sound: slider.click_sound.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider.pressed = False
        elif event.type == pygame.MOUSEMOTION:
            if slider.pressed:
                update_value()
    t = pygame.time.get_ticks() * 0.01
    pulse = math.sin(t) * 0.5 + 0.5
    if slider.pressed:
        slider.extra_dot_radius = min(slider.max_extra_dot_radius, slider.extra_dot_radius + pulse)
    else:
        slider.extra_dot_radius = max(0, slider.extra_dot_radius - pulse)
