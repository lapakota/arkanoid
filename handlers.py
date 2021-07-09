import pygame

from config import CONFIG
from paddle import Paddle


def key_handler(paddle: Paddle) -> None:
    left_buttons = (pygame.K_a, pygame.K_LEFT)
    right_buttons = (pygame.K_d, pygame.K_RIGHT)
    key = pygame.key.get_pressed()

    if (key[left_buttons[0]] or key[left_buttons[1]]) \
            and paddle.rect.left > 0:
        paddle.rect.left -= paddle.movement_speed
    elif (key[right_buttons[0]] or key[right_buttons[1]]) \
            and paddle.rect.right < CONFIG.GAME_WIDTH:
        paddle.rect.right += paddle.movement_speed
    # cheats
    else:
        growth_rate = 5
        if key[pygame.K_z]:
            if paddle.width < CONFIG.GAME_WIDTH - growth_rate:
                paddle.rect.w += growth_rate
                paddle.width += growth_rate
        elif key[pygame.K_x]:
            smallest_width = 30 + growth_rate
            if paddle.width >= smallest_width:
                paddle.rect.w -= 5
                paddle.width -= 5


def mouse_handler(paddle: Paddle) -> None:
    mouse_x, _ = pygame.mouse.get_pos()
    is_left_button_pressed, _, _ = pygame.mouse.get_pressed(3)

    if is_left_button_pressed \
            and mouse_x - paddle.width // 2 > 0 \
            and mouse_x + paddle.width // 2 < CONFIG.GAME_WIDTH:
        paddle.rect.left = mouse_x - paddle.width // 2
    # For correct processing at the edges
    if is_left_button_pressed and mouse_x - paddle.width // 2 <= 0:
        paddle.rect.left = 0
    elif is_left_button_pressed and mouse_x + paddle.width // 2 >= CONFIG.GAME_WIDTH:
        paddle.rect.right = CONFIG.GAME_WIDTH


def events_handler() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            elif event.key == pygame.K_SPACE:
                restart = True
                return restart
