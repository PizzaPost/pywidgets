import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)
bg = (30, 30, 30)
screen = epw.Screen(id="main")


def change_color():
    global bg
    bg = (120, 20, 20)


button = epw.Button(screen=screen, text="Click Me!", click_command=change_color)
slider = epw.Slider(text="Slide Me!")
screen.add_widget(slider)

hide_button = epw.Button(text="Hide", click_command=screen.hide)
show_button = epw.Button(text="Show", click_command=screen.show)
disable_button = epw.Button(text="Disable", click_command=screen.disable)
enable_button = epw.Button(text="Enable", click_command=screen.enable)

button.place(50, 50)
slider.place(50, 180)
hide_button.place(50, 440)
show_button.place(50, 520)
disable_button.place(200, 440)
enable_button.place(200, 520)

running = True
while running:
    window.fill(bg)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
