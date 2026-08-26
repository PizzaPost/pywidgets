from typing import NewType

binding = NewType("binding", str)

MOUSE_IN = binding("<MOUSE_IN>")
HOVER = binding("<HOVER>")
MOUSE_OUT = binding("<MOUSE_OUT>")

# TODO: add keys like A, a, SPACE, ...
KEY = binding("<KEY>")

PRESS = binding("<PRESS>")
HOLD = binding("<HOLD>")
RELEASE = binding("<RELEASE>")

CHECK = binding("<CHECK>")
UNCHECK = binding("<UNCHECK>")

FOCUS_IN = binding("<FOCUS_IN>")
FOCUS_OUT = binding("<FOCUS_OUT>")
COPY = binding("<COPY>")
PASTE = binding("<PASTE>")
CUT = binding("<CUT>")
BACKSPACE = binding("<BACKSPACE>")
DELETE = binding("<DELETE>")
TYPING = binding("<TYPING>")
SELECT_ALL = binding("<SELECT_ALL>")

DRAG = binding("<DRAG>")

TICKING = binding("<TICKING>")
FINISHED = binding("<FINISHED>")

# TODO: widget types