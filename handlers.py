from typing import Union

import pygame

from ball import Ball
from config import CONFIG
from paddle import Paddle


def handle_sticking(ball: Ball, paddle: Paddle) -> None:
    if ball.is_stopped():
        ball.stick_to_the_paddle(paddle)


class KeyHandler:
    def __init__(self, paddle: Paddle, ball: Ball):
        self.paddle = paddle
        self.ball = ball

    def handle_key_pressing(self) -> None:
        left_buttons = (pygame.K_a, pygame.K_LEFT)
        right_buttons = (pygame.K_d, pygame.K_RIGHT)
        key = pygame.key.get_pressed()

        if (key[left_buttons[0]] or key[left_buttons[1]]) \
                and self.paddle.rect.left > 0:
            self.paddle.rect.left -= self.paddle.movement_speed
            handle_sticking(self.ball, self.paddle)
        elif (key[right_buttons[0]] or key[right_buttons[1]]) \
                and self.paddle.rect.right < CONFIG.GAME_WIDTH:
            self.paddle.rect.right += self.paddle.movement_speed
            handle_sticking(self.ball, self.paddle)
        elif key[pygame.K_e]:
            if self.ball.is_stopped():
                self.ball.start_moving()

        # cheats
        else:
            growth_rate = 5
            if key[pygame.K_z]:
                if self.paddle.width < CONFIG.GAME_WIDTH:
                    self.paddle.rect.w += growth_rate
                    self.paddle.width += growth_rate
            elif key[pygame.K_x]:
                smallest_width = 35
                if self.paddle.width > smallest_width:
                    self.paddle.rect.w -= growth_rate
                    self.paddle.width -= growth_rate
            elif key[pygame.K_c]:
                self.ball.movement_speed += 1
            elif key[pygame.K_v]:
                if self.ball.movement_speed > 0:
                    self.ball.movement_speed -= 1


class MouseHandler:
    def __init__(self, paddle: Paddle, ball: Ball):
        self.paddle = paddle
        self.ball = ball

    def handle_mouse_events(self) -> None:
        mouse_x, _ = pygame.mouse.get_pos()
        is_left_button_pressed, _, is_right_button_pressed = pygame.mouse.get_pressed(3)

        if self.ball.is_stopped() and is_right_button_pressed:
            self.ball.start_moving()

        if is_left_button_pressed:
            handle_sticking(self.ball, self.paddle)

            if mouse_x - self.paddle.width // 2 > 0 and mouse_x + self.paddle.width // 2 < CONFIG.GAME_WIDTH:
                self.paddle.rect.left = mouse_x - self.paddle.width // 2
            # For correct processing at the edges
            if mouse_x - self.paddle.width // 2 <= 0:
                self.paddle.rect.left = 0
            elif mouse_x + self.paddle.width // 2 >= CONFIG.GAME_WIDTH:
                self.paddle.rect.right = CONFIG.GAME_WIDTH


class GeneralEventsHandler:
    @staticmethod
    def handle_general_events() -> Union[None, bool]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_SPACE:
                    restart = True
                    return restart
