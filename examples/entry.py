import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

entry = epw.Entry(placeholder_text="This is a placeholder :)")
entry.place(50, 50)

running = True
while running:
    window.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
