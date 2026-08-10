# animated_surface.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode(vsync=True)
clock = pygame.time.Clock()
epw.link_pygame_window(window)
epw.set_appearance_mode(2)

screen = epw.Screen(visible=True)
img_surface = epw.Surface(frames=epw.create_frames("ball"), screen=screen, active_hover_cursor=pygame.cursors.tri_left,
                          anchor_x="center", anchor_y="center", playing=True, looping=True)
img_surface.place(x=50, y=50, mode="%")


def draw():
    window.fill((30, 30, 30))


epw.create_pygame_layer(draw, 500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()
    clock.tick(60)
pygame.quit()