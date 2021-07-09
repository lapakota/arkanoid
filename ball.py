from random import randrange
from typing import List, Union

from block import Block
from paddle import Paddle
from sounds import *


class Ball:
    def __init__(self, radius, speed, color):
        self.dx = 1
        self.dy = -1
        self.radius = radius
        self.movement_speed = speed
        self.color = pygame.Color(color)
        self.rect_side = int(self.radius * 2 ** 0.5)  # side of the inscribed square
        self._position = randrange(self.rect_side, CONFIG.GAME_WIDTH - self.rect_side)
        y_offset_from_center = 100
        self.rect = pygame.Rect(self._position, CONFIG.GAME_HEIGHT // 2 + y_offset_from_center,
                                self.rect_side, self.rect_side)
        self._damaged_combo = 0

    def bounce_from_collided_rect(self, rect: pygame.Rect) -> None:
        """The function changes the dx, dy of the ball,
         depending on the side of the rectangle that the ball hit"""
        if self.dx > 0:
            delta_x = self.rect.right - rect.left
        else:
            delta_x = rect.right - self.rect.left
        if self.dy > 0:
            delta_y = self.rect.bottom - rect.top
        else:
            delta_y = rect.bottom - self.rect.top

        epsilon = 5
        # collision with angle of rect
        if abs(delta_x - delta_y) < epsilon:
            self.dx, self.dy = -self.dx, -self.dy
        # collision with horizontal side
        elif delta_x > delta_y:
            self.dy *= -1
        # collision with vertical side
        elif delta_y > delta_x:
            self.dx *= -1

    def is_out_of_bounds(self) -> bool:
        return self.rect.y > CONFIG.GAME_HEIGHT

    def handle_walls_collision(self) -> None:
        if self.rect.centerx < self.radius or self.rect.centerx > CONFIG.GAME_WIDTH - self.radius:
            self.dx *= -1

    def handle_top_collision(self) -> None:
        if self.rect.centery < self.radius:
            self.dy *= -1

    def handle_paddle_collision(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect) and self.dy > 0:
            self.bounce_from_collided_rect(paddle.rect)
            Sounds.BALL_BONK.value.play()

    def handle_block_collision(self, blocks: List[Block]) -> Union[None, int]:
        damage_index = self.rect.collidelist(blocks)
        if damage_index != -1:
            damaged_block = blocks[damage_index]
            self.bounce_from_collided_rect(damaged_block.rect)
            damaged_block.take_damage()
            self._damaged_combo += 1
            self._speed_up()
            Sounds.BLOCK_CRASH.value.play()
            if damaged_block.is_dead():
                blocks.pop(damage_index)
                return damaged_block.scores

    def move(self) -> None:
        self.rect.x += self.movement_speed * self.dx
        self.rect.y += self.movement_speed * self.dy

    def respawn(self) -> None:
        new_ball = Ball(self.radius, self.movement_speed, self.color)
        self.dx = new_ball.dx
        self.dy = new_ball.dy
        self._position = new_ball._position
        self.rect = new_ball.rect

    def draw(self, screen: pygame.surface) -> None:
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def draw_rect(self, screen: pygame.surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)

    def _speed_up(self) -> None:
        if self._damaged_combo % CONFIG.DAMAGED_FOR_SPEEDUP == 0:
            self.movement_speed += 1
            self._damaged_combo = 0
