# misc.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
import ctypes
import os
import queue
import re
import threading
import time
from collections.abc import Iterable
from concurrent.futures.thread import ThreadPoolExecutor

import cv2
import pygame
import requests
from PIL import Image

pg = None
check_disabled = False
all_widgets = []
_scheduled_functions = []
_last_tick = None
_dt = 0
SYNC_FRAME_LOAD_LIMIT = 600
_pending_frame_queues = []


def _update_clock():
	global _last_tick, _dt
	now = time.time()
	if _last_tick is None:
		_dt = 0
	else:
		_dt = now-_last_tick
	_last_tick = now
	_drain_frame_queues()


def _check_update():
	global check_disabled
	if check_disabled: return
	url = "https://raw.githubusercontent.com/PizzaPost/pywidgets/master/info.json"
	try:
		response = requests.get(url)
		response.raise_for_status()
		data = response.json()
		latest_version = data["version"]
		current_version = "26.36"
		if latest_version!=current_version:
			print(
				f"\033[31mAn update is available. Download it now with 'pip install --upgrade easypygamewidgets'\n"
				f"You are currently on: {current_version}\n"
				f"The newest version is: {latest_version}\033[0m"
			)
	except Exception as e:
		print(f"easypygamewidgets: Failed to check for updates: {e}")


def disable_update_check():
	global check_disabled
	check_disabled = True


def _check_linked():
	if not isinstance(pg, pygame.Surface):
		print("Please link a pygame window first:\n    easypygamewidgets.link_pygame_window(window)")
		exit(0)


def _check_pygame_version():
	try:
		import pygame
		if not hasattr(pygame, "IS_CE"): raise ImportError
	except ImportError:
		print(
			"[INFO] easypygamewidgets 26.9+ requires 'pygame-ce'.\n"
			"Existing 'pygame' installation detected. You have four ways to resolve this:\n"
			"1. Update to Python 3.14+ and install pygame-ce:\n"
			"     pip install pygame-ce\n"
			"2. Replace pygame with pygame-ce (recommended):\n"
			"     pip uninstall pygame && pip install pygame-ce\n"
			"3. Isolation: Use a virtual environment (venv) for this project.\n"
			"4. Legacy: Roll back to an older version of this library:\n"
			"     pip install 'easypygamewidgets<=26.8' --force-reinstall"
		)
		exit(1)


def link_pygame_window(window: pygame.Surface, layer=500):
	global pg
	_check_pygame_version()
	_check_update()
	pg = window
	all_widgets.append((pg, layer))


def _add_widget(widget):
	all_widgets.append(widget)
	_resort_layers()


def create_pygame_layer(function, layer):
	all_widgets.append((function, layer))
	_resort_layers()


def _resort_layers():
	all_widgets.sort(key=lambda w: w[1] if isinstance(w, tuple) else w.layer)


def set_appearance_mode(mode):
	hwnd = pygame.display.get_wm_info()["window"]
	tmp = ctypes.c_int(mode)
	ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(tmp), ctypes.sizeof(tmp))


def schedule(function, time_to_execute: int, unit: str = "seconds", fps: float = 60):
	if time_to_execute<1:
		time_to_execute = 1
	if fps<=0:
		fps = 60
	if unit in ("f", "frames"):
		time_to_execute /= fps
	elif unit in ("m", "min", "minutes"):
		time_to_execute *= 60
	elif unit in ("s", "sec", "seconds"):
		...
	else:
		print(f"Invalid time unit: {unit}\nFallback: seconds")
	_scheduled_functions.append([function, time_to_execute])


def _get_offset(widget):
	offset_x = offset_y = 0
	if getattr(widget, "screen", None):
		offset_x = widget.screen.current_offset[0]
		offset_y = widget.screen.current_offset[1]
	if getattr(widget, "parent", None):
		offset_x += widget.parent.x
		offset_y += widget.parent.y
	return offset_x, offset_y


def _is_point_over_widget(widget, point):
	class_name = widget.__class__.__name__
	if class_name=="Entry" or class_name=="Label":
		offset_x, offset_y = _get_offset(widget)
		total_offset_x = offset_x+round(widget.current_offset[0])
		total_offset_y = offset_y+round(widget.current_offset[1])
		rect = widget.rect.move(total_offset_x, total_offset_y)
		if not rect.collidepoint(point):
			return False
		x, y = point
		geom_rect = rect
		scale = widget.current_scale
		rotation = widget.current_rotation
		if scale!=1 or rotation!=0:
			cx, cy = rect.center
			if rotation!=0:
				v = pygame.math.Vector2(x-cx, y-cy)
				v = v.rotate(rotation)
				x, y = cx+v.x, cy+v.y
			base_w = widget.width*scale
			base_h = widget.height*scale
			geom_rect = pygame.Rect(0, 0, base_w, base_h)
			geom_rect.center = (cx, cy)
			if not geom_rect.collidepoint((x, y)):
				return False
		tl_r = widget.top_left_corner_radius*scale
		tr_r = widget.top_right_corner_radius*scale
		bl_r = widget.bottom_left_corner_radius*scale
		br_r = widget.bottom_right_corner_radius*scale
		max_r = max(tl_r, tr_r, bl_r, br_r)
		if (geom_rect.left+max_r<=x<=geom_rect.right-max_r) or \
				(geom_rect.top+max_r<=y<=geom_rect.bottom-max_r):
			return True
		if x<geom_rect.left+tl_r and y<geom_rect.top+tl_r:
			cx, cy = geom_rect.left+tl_r, geom_rect.top+tl_r
			return (x-cx)**2+(y-cy)**2<=tl_r**2
		if x>geom_rect.right-tr_r and y<geom_rect.top+tr_r:
			cx, cy = geom_rect.right-tr_r, geom_rect.top+tr_r
			return (x-cx)**2+(y-cy)**2<=tr_r**2
		if x<geom_rect.left+bl_r and y>geom_rect.bottom-bl_r:
			cx, cy = geom_rect.left+bl_r, geom_rect.bottom-bl_r
			return (x-cx)**2+(y-cy)**2<=bl_r**2
		if x>geom_rect.right-br_r and y>geom_rect.bottom-br_r:
			cx, cy = geom_rect.right-br_r, geom_rect.bottom-br_r
			return (x-cx)**2+(y-cy)**2<=br_r**2
		return True
	elif class_name=="Button" or class_name=="Checkbox":
		offset_x, offset_y = _get_offset(widget)
		total_offset_x = offset_x+round(widget.current_offset[0])
		total_offset_y = offset_y+round(widget.current_offset[1])
		rect = widget.rect.move(total_offset_x, total_offset_y)
		if not rect.collidepoint(point):
			return False
		x, y = point
		geom_rect = rect
		scale = widget.current_scale
		rotation = widget.current_rotation
		if scale!=1 or rotation!=0:
			cx, cy = rect.center
			if rotation!=0:
				v = pygame.math.Vector2(x-cx, y-cy)
				v = v.rotate(rotation)
				x, y = cx+v.x, cy+v.y
			base_w = widget.width*scale
			base_h = widget.height*scale
			geom_rect = pygame.Rect(0, 0, base_w, base_h)
			geom_rect.center = (cx, cy)
			if not geom_rect.collidepoint((x, y)):
				return False
		r = widget.corner_radius*scale
		r = min(r, geom_rect.width//2, geom_rect.height//2)
		if r<=0:
			return True
		if (geom_rect.left+r<=x<=geom_rect.right-r) or (geom_rect.top+r<=y<=geom_rect.bottom-r):
			return True
		centers = [
			(geom_rect.left+r, geom_rect.top+r),
			(geom_rect.right-r, geom_rect.top+r),
			(geom_rect.left+r, geom_rect.bottom-r),
			(geom_rect.right-r, geom_rect.bottom-r)
		]
		for cx, cy in centers:
			if ((x-cx)**2+(y-cy)**2)<=r**2:
				return True
		return False
	elif class_name=="Dialog":
		offset_x, offset_y = _get_offset(widget)
		total_offset_x = offset_x+round(widget.current_offset[0])
		total_offset_y = offset_y+round(widget.current_offset[1])
		rect = widget.rect.move(total_offset_x, total_offset_y)
		if not rect.collidepoint(point):
			return False
		x, y = point
		geom_rect = rect
		scale = widget.current_scale
		rotation = widget.current_rotation
		if scale!=1 or rotation!=0:
			cx, cy = rect.center
			if rotation!=0:
				v = pygame.math.Vector2(x-cx, y-cy)
				v = v.rotate(rotation)
				x, y = cx+v.x, cy+v.y
			base_w = widget.width*scale
			base_h = widget.height*scale
			geom_rect = pygame.Rect(0, 0, base_w, base_h)
			geom_rect.center = (cx, cy)
			if not geom_rect.collidepoint((x, y)):
				return False
		r = widget.corner_radius*scale
		r = min(r, geom_rect.width//2, geom_rect.height//2)
		if r<=0:
			return True
		if (geom_rect.left+r<=x<=geom_rect.right-r) or (geom_rect.top+r<=y<=geom_rect.bottom-r):
			return True
		centers = [
			(geom_rect.left+r, geom_rect.top+r), (geom_rect.right-r, geom_rect.top+r),
			(geom_rect.left+r, geom_rect.bottom-r), (geom_rect.right-r, geom_rect.bottom-r)
		]
		for cx, cy in centers:
			if ((x-cx)**2+(y-cy)**2)<=r**2:
				return True
		return False
	elif class_name=="Slider":
		offset_x, offset_y = _get_offset(widget)
		total_offset_x = offset_x+round(widget.current_offset[0])
		total_offset_y = offset_y+round(widget.current_offset[1])
		draw_rect = widget.rect.move(total_offset_x, total_offset_y)
		x, y = point
		scale = widget.current_scale
		rotation = widget.current_rotation
		cx, cy = draw_rect.center
		if rotation!=0:
			v = pygame.math.Vector2(x-cx, y-cy)
			v = v.rotate(rotation)
			x, y = cx+v.x, cy+v.y
		if scale!=1 and scale!=0:
			x = cx+(x-cx)/scale
			y = cy+(y-cy)/scale
		orig_rect = widget.original_surface.get_rect(center=(cx, cy))
		if not orig_rect.collidepoint((x, y)):
			return False
		temp_surf = widget.font.render(widget.text, True, (0, 0, 0))
		text_height = temp_surf.get_height()
		track_y = orig_rect.top+text_height+10+widget._height//2
		extra_dot = widget.dot_radius+widget.max_extra_dot_radius
		track_y = max(track_y, orig_rect.top+extra_dot)
		widest_magnitude = max(abs(widget.start), abs(widget.end))
		integer_digits = len(str(int(widest_magnitude)))
		decimal_digits = widget.round_display_value if widget.round_display_value>0 else 0
		widest_value_str = "9"*integer_digits+("."+"9"*decimal_digits if decimal_digits else "")
		if widget.start<0 or widget.end<0:
			widest_value_str = "-"+widest_value_str
		side_margin = widget.max_extra_dot_radius+widget.font.size(widest_value_str)[0]//2
		track_rect = pygame.Rect(
			orig_rect.x+side_margin, track_y-(widget._height//2),
			orig_rect.width-side_margin*2, widget._height
		)
		if not track_rect.collidepoint((x, y)):
			return False
		max_radius = min(track_rect.width, track_rect.height)//2
		tl = min(widget.top_left_corner_radius, max_radius)
		tr = min(widget.top_right_corner_radius, max_radius)
		bl = min(widget.bottom_left_corner_radius, max_radius)
		br = min(widget.bottom_right_corner_radius, max_radius)
		if x<track_rect.left+tl and y<track_rect.top+tl:
			cxc, cyc = track_rect.left+tl, track_rect.top+tl
			if (x-cxc)**2+(y-cyc)**2>tl**2: return False
		elif x>track_rect.right-tr and y<track_rect.top+tr:
			cxc, cyc = track_rect.right-tr, track_rect.top+tr
			if (x-cxc)**2+(y-cyc)**2>tr**2: return False
		elif x<track_rect.left+bl and y>track_rect.bottom-bl:
			cxc, cyc = track_rect.left+bl, track_rect.bottom-bl
			if (x-cxc)**2+(y-cyc)**2>bl**2: return False
		elif x>track_rect.right-br and y>track_rect.bottom-br:
			cxc, cyc = track_rect.right-br, track_rect.bottom-br
			if (x-cxc)**2+(y-cyc)**2>br**2: return False
		return True
	elif class_name=="Screen":
		offset_x, offset_y = _get_offset(widget)
		total_offset_x = offset_x+round(widget.current_offset[0])
		total_offset_y = offset_y+round(widget.current_offset[1])
		rect = widget.rect.move(total_offset_x, total_offset_y)
		if not rect.collidepoint(point): return False
		return True
	elif class_name=="Tooltip":
		rect = widget.rect.move(point[0], point[1])
		if not rect.collidepoint(point): return False
		r = widget.corner_radius
		r = min(r, rect.width//2, rect.height//2)
		if r<=0: return True
		x, y = point
		if (rect.left+r<=x<=rect.right-r) or (rect.top+r<=y<=rect.bottom-r):
			return True
		centers = [
			(rect.left+r, rect.top+r), (rect.right-r, rect.top+r),
			(rect.left+r, rect.bottom-r), (rect.right-r, rect.bottom-r)
		]
		for cx, cy in centers:
			if ((x-cx)**2+(y-cy)**2)<=r**2: return True
		return False
	elif class_name=="Timekeeper":
		offset_x, offset_y = _get_offset(widget)
		rect = widget.rect.move(offset_x, offset_y)
		if not rect.collidepoint(point): return False
		r = widget.corner_radius
		r = min(r, rect.width//2, rect.height//2)
		if r<=0: return True
		x, y = point
		if (rect.left+r<=x<=rect.right-r) or (rect.top+r<=y<=rect.bottom-r):
			return True
		centers = [
			(rect.left+r, rect.top+r), (rect.right-r, rect.top+r),
			(rect.left+r, rect.bottom-r), (rect.right-r, rect.bottom-r)
		]
		for cx, cy in centers:
			if ((x-cx)**2+(y-cy)**2)<=r**2: return True
		return False


def normalize_color(color: tuple[int, int, int]|tuple[int, int, int, int]|str|None):
	if color is None:
		return 0, 0, 0, 0
	# rgb
	if len(color)==3:
		return *color, 255
	# rgba
	if len(color)==4:
		return color
	# #hex or hex
	if len(color)==7 and len(color.removeprefix("#"))==6 or len(color)==6 and len(color.removeprefix("#"))==6:
		color = color.removeprefix("#")
		return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255
	raise ValueError("Invalid color format. Supported formats: (r, g, b), (r, g, b, a), #hex, hex")


def _natural_key(s):
	return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


def _load_image(full_path):
	return pygame.image.load(full_path)


def _decode_image_worker(full_paths, raw_queue, worker_count):
	def _decode(full_path):
		with Image.open(full_path) as img:
			img = img.convert("RGBA")
			return full_path, img.size, img.tobytes()

	with ThreadPoolExecutor(max_workers=worker_count) as pool:
		for full_path, size, data in pool.map(_decode, full_paths):
			raw_queue.put(("image", size, data))
	raw_queue.put(None)


def _read_video_bytes_worker(vidcap, raw_queue):
	continue_grabbing, frame = vidcap.read()
	while continue_grabbing:
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		width = frame.shape[1]
		height = frame.shape[0]
		raw_queue.put(("video", (width, height), frame.tobytes()))
		continue_grabbing, frame = vidcap.read()
	vidcap.release()
	raw_queue.put(None)


def _drain_frame_queues():
	if not _pending_frame_queues: return
	for raw_queue, frames_list in _pending_frame_queues[:]:
		while True:
			try:
				item = raw_queue.get_nowait()
			except queue.Empty:
				break
			if item is None:
				_pending_frame_queues.remove((raw_queue, frames_list))
				break
			kind, (width, height), data = item
			if kind=="image":
				frames_list.append(pygame.image.frombuffer(data, (width, height), "RGBA"))
			else:
				frames_list.append(pygame.image.frombuffer(data, (width, height), "RGB"))


def create_frames(path: str|os.PathLike) -> Iterable[pygame.Surface]:
	if os.path.isdir(path):
		filenames = sorted(os.listdir(path), key=_natural_key)
		full_paths = [os.path.join(path, filename) for filename in filenames]
		worker_count = min(32, (os.cpu_count() or 4)*4)
		sync_paths = full_paths[:SYNC_FRAME_LOAD_LIMIT]
		async_paths = full_paths[SYNC_FRAME_LOAD_LIMIT:]
		with ThreadPoolExecutor(max_workers=worker_count) as pool:
			frames_list = list(pool.map(_load_image, sync_paths))
		if async_paths:
			raw_queue = queue.Queue(maxsize=64)
			reader_thread = threading.Thread(
				target=_decode_image_worker,
				args=(async_paths, raw_queue, worker_count), daemon=True
			)
			reader_thread.start()
			_pending_frame_queues.append((raw_queue, frames_list))
		return frames_list
	elif isinstance(path, str) and path.endswith((".mov", ".mp4", ".webm")):
		frames_list = []
		vidcap = cv2.VideoCapture(path)
		continue_grabbing, frame = vidcap.read()
		while continue_grabbing and len(frames_list)<SYNC_FRAME_LOAD_LIMIT:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			width = frame.shape[1]
			height = frame.shape[0]
			frames_list.append(pygame.image.frombuffer(frame.tobytes(), (width, height), "RGB"))
			continue_grabbing, frame = vidcap.read()
		if continue_grabbing:
			raw_queue = queue.Queue(maxsize=64)
			reader_thread = threading.Thread(target=_read_video_bytes_worker, args=(vidcap, raw_queue), daemon=True)
			reader_thread.start()
			_pending_frame_queues.append((raw_queue, frames_list))
		else:
			vidcap.release()
		return frames_list
	elif isinstance(path, pygame.Surface):
		return [pygame.image.load(path)]
	else:
		raise ValueError("Invalid path format. Please provide a directory, video file path, or image file path.")