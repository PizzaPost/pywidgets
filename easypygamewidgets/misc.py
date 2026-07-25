# misc.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import ctypes

import pygame
import requests

pg = None
check_disabled = False
all_widgets = []
scheduled_functions = []


def check_update():
    global check_disabled
    if check_disabled: return
    url = "https://raw.githubusercontent.com/PizzaPost/pywidgets/master/info.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        latest_version = data["version"]
        current_version = "26.29.1"
        if latest_version != current_version:
            print(f"An update is available. Download it now with 'pip install --upgrade easypygamewidgets'\n"
                  f"You are currently on: {current_version}\n"
                  f"The newest version is: {latest_version}")
    except Exception as e:
        print(f"easypygamewidgets: Failed to check for updates: {e}")


def disable_update_check():
    global check_disabled
    check_disabled = True


def check_linked():
    if not isinstance(pg, pygame.Surface):
        print("Please link a pygame window first:\n    easypygamewidgets.link_pygame_window(window)")
        exit(0)


def check_pygame_version():
    try:
        import pygame
        if not hasattr(pygame, "IS_CE"): raise ImportError
    except ImportError:
        print("[INFO] easypygamewidgets 26.9+ requires 'pygame-ce'.\n"
              "Existing 'pygame' installation detected. You have four ways to resolve this:\n"
              "1. Update to Python 3.14+ and install pygame-ce:\n"
              "     pip install pygame-ce\n"
              "2. Replace pygame with pygame-ce (recommended):\n"
              "     pip uninstall pygame && pip install pygame-ce\n"
              "3. Isolation: Use a virtual environment (venv) for this project.\n"
              "4. Legacy: Roll back to an older version of this library:\n"
              "     pip install 'easypygamewidgets<=26.8' --force-reinstall")
        exit(1)


def link_pygame_window(window: pygame.Surface, layer=500):
    global pg
    check_pygame_version()
    check_update()
    pg = window
    all_widgets.append((pg, layer))


def add_widget(widget):
    all_widgets.append(widget)
    resort_layers()


def create_pygame_layer(function, layer):
    all_widgets.append((function, layer))
    resort_layers()


def resort_layers():
    all_widgets.sort(key=lambda w: w[1] if isinstance(w, tuple) else w.layer)


def set_appearance_mode(mode):
    hwnd = pygame.display.get_wm_info()["window"]
    tmp = ctypes.c_int(mode)
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(tmp), ctypes.sizeof(tmp))


def schedule(function, frames_to_execute):
    if frames_to_execute < 1:
        frames_to_execute = 1
    scheduled_functions.append([function, frames_to_execute])


def get_offset(widget):
    offset_x = offset_y = 0
    if widget.screen:
        offset_x, offset_y = widget.screen.x, widget.screen.y
    if getattr(widget, "parent", None):
        offset_x += widget.parent.x
        offset_y += widget.parent.y
    return offset_x, offset_y


def is_point_over_widget(widget, point):
    class_name = widget.__class__.__name__
    if class_name == "Entry" or class_name == "Label":
        offset_x, offset_y = get_offset(widget)
        total_offset_x = offset_x + round(widget.current_offset[0])
        total_offset_y = offset_y + round(widget.current_offset[1])
        rect = widget.rect.move(total_offset_x, total_offset_y)
        if not rect.collidepoint(point):
            return False
        x, y = point
        geom_rect = rect
        scale = widget.current_scale
        rotation = widget.current_rotation
        if scale != 1 or rotation != 0:
            cx, cy = rect.center
            if rotation != 0:
                v = pygame.math.Vector2(x - cx, y - cy)
                v = v.rotate(rotation)
                x, y = cx + v.x, cy + v.y
            base_w = widget.width * scale
            base_h = widget.height * scale
            geom_rect = pygame.Rect(0, 0, base_w, base_h)
            geom_rect.center = (cx, cy)
            if not geom_rect.collidepoint((x, y)):
                return False
        tl_r = widget.top_left_corner_radius * scale
        tr_r = widget.top_right_corner_radius * scale
        bl_r = widget.bottom_left_corner_radius * scale
        br_r = widget.bottom_right_corner_radius * scale
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
    elif class_name == "Button":
        offset_x, offset_y = get_offset(widget)
        total_offset_x = offset_x + round(widget.current_offset[0])
        total_offset_y = offset_y + round(widget.current_offset[1])
        rect = widget.rect.move(total_offset_x, total_offset_y)
        if not rect.collidepoint(point):
            return False
        x, y = point
        geom_rect = rect
        scale = widget.current_scale
        rotation = widget.current_rotation
        if scale != 1 or rotation != 0:
            cx, cy = rect.center
            if rotation != 0:
                v = pygame.math.Vector2(x - cx, y - cy)
                v = v.rotate(rotation)
                x, y = cx + v.x, cy + v.y
            base_w = widget.width * scale
            base_h = widget.height * scale
            geom_rect = pygame.Rect(0, 0, base_w, base_h)
            geom_rect.center = (cx, cy)
            if not geom_rect.collidepoint((x, y)):
                return False
        r = widget.corner_radius * scale
        r = min(r, geom_rect.width // 2, geom_rect.height // 2)
        if r <= 0:
            return True
        if (geom_rect.left + r <= x <= geom_rect.right - r) or (geom_rect.top + r <= y <= geom_rect.bottom - r):
            return True
        centers = [
            (geom_rect.left + r, geom_rect.top + r),
            (geom_rect.right - r, geom_rect.top + r),
            (geom_rect.left + r, geom_rect.bottom - r),
            (geom_rect.right - r, geom_rect.bottom - r)
        ]
        for cx, cy in centers:
            if ((x - cx) ** 2 + (y - cy) ** 2) <= r ** 2:
                return True
        return False
    elif class_name == "Dialog":
        offset_x, offset_y = get_offset(widget)
        total_offset_x = offset_x + round(widget.current_offset[0])
        total_offset_y = offset_y + round(widget.current_offset[1])
        rect = widget.rect.move(total_offset_x, total_offset_y)
        if not rect.collidepoint(point):
            return False
        x, y = point
        geom_rect = rect
        scale = widget.current_scale
        rotation = widget.current_rotation
        if scale != 1 or rotation != 0:
            cx, cy = rect.center
            if rotation != 0:
                v = pygame.math.Vector2(x - cx, y - cy)
                v = v.rotate(rotation)
                x, y = cx + v.x, cy + v.y
            base_w = widget.width * scale
            base_h = widget.height * scale
            geom_rect = pygame.Rect(0, 0, base_w, base_h)
            geom_rect.center = (cx, cy)
            if not geom_rect.collidepoint((x, y)):
                return False
        r = widget.corner_radius * scale
        r = min(r, geom_rect.width // 2, geom_rect.height // 2)
        if r <= 0:
            return True
        if (geom_rect.left + r <= x <= geom_rect.right - r) or (geom_rect.top + r <= y <= geom_rect.bottom - r):
            return True
        centers = [(geom_rect.left + r, geom_rect.top + r), (geom_rect.right - r, geom_rect.top + r),
                   (geom_rect.left + r, geom_rect.bottom - r), (geom_rect.right - r, geom_rect.bottom - r)]
        for cx, cy in centers:
            if ((x - cx) ** 2 + (y - cy) ** 2) <= r ** 2:
                return True
        return False
    elif class_name == "Slider":
        offset_x, offset_y = get_offset(widget)
        draw_rect = widget.rect.move(offset_x, offset_y)
        temp_surf = widget.font.render(widget.text, True, (0, 0, 0))
        text_height = temp_surf.get_height()
        track_y = draw_rect.top + text_height + 10 + widget.height // 2
        track_rect = pygame.Rect(draw_rect.x, track_y - (widget.height // 2), draw_rect.width, widget.height)
        x, y = point
        if not track_rect.collidepoint(point):
            return False
        max_radius = min(track_rect.width, track_rect.height) // 2
        tl = min(widget.top_left_corner_radius, max_radius)
        tr = min(widget.top_right_corner_radius, max_radius)
        bl = min(widget.bottom_left_corner_radius, max_radius)
        br = min(widget.bottom_right_corner_radius, max_radius)
        if x < track_rect.left + tl and y < track_rect.top + tl:
            cx, cy = track_rect.left + tl, track_rect.top + tl
            if (x - cx) ** 2 + (y - cy) ** 2 > tl ** 2:
                return False
        elif x > track_rect.right - tr and y < track_rect.top + tr:
            cx, cy = track_rect.right - tr, track_rect.top + tr
            if (x - cx) ** 2 + (y - cy) ** 2 > tr ** 2:
                return False
        elif x < track_rect.left + bl and y > track_rect.bottom - bl:
            cx, cy = track_rect.left + bl, track_rect.bottom - bl
            if (x - cx) ** 2 + (y - cy) ** 2 > bl ** 2:
                return False
        elif x > track_rect.right - br and y > track_rect.bottom - br:
            cx, cy = track_rect.right - br, track_rect.bottom - br
            if (x - cx) ** 2 + (y - cy) ** 2 > br ** 2:
                return False
        return True
    elif class_name == "Tooltip":
        rect = widget.rect.move(point[0], point[1])
        if not rect.collidepoint(point): return False
        r = widget.corner_radius
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
    elif class_name == "Timekeeper":
        offset_x, offset_y = get_offset(widget)
        rect = widget.rect.move(offset_x, offset_y)
        if not rect.collidepoint(point): return False
        r = widget.corner_radius
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


def normalize_color(color):
    if color is None:
        return 0, 0, 0, 0
    if len(color) == 3:
        return *color, 255
    return color