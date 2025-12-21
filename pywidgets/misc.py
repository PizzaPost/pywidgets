import pygame
import requests

pg = None


def check_update():
    url = "https://raw.githubusercontent.com/PizzaPost/pywidgets/master/info.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        latest_version = data["version"]
        if latest_version == "0.1.0":
            print("pywidgets is on the latest version")
        else:
            print("An update is available. Download it now with 'pip install --upgrade pywidgets'")
    except Exception as e:
        print(f"pywidgets: Failed to check for updates: {e}")


def check_linked():
    if not type(pg) == pygame.Surface:
        print("Please link a pygame window first:\n    pywidgets.link_pygame_window(window)")
        exit(0)


def link_pygame_window(window: pygame.Surface):
    global pg
    check_update()
    pg = window
