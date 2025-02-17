import pygame
import game_states_and_settings as gss
import control
import gui
import ai

clock = pygame.time.Clock()

while control.running:

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                control.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                control.left_mouse_click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                control.left_mouse_release(event.pos)

    if (gss.whites_turn and not gss.white_human) or (not gss.whites_turn and not gss.black_human):
        ai.play()

    control.update()

    clock.tick(60)


pygame.quit()
