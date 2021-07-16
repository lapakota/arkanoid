import random
from typing import List

from block import Block
from paddle import Paddle
from sounds import *


class Ball:
    def __init__(self, radius: int, speed: int, color: pygame.Color):
        self.dx = 0
        self.dy = 0
        self.radius = radius
        self.movement_speed = speed
        self.color = color
        y_offset_from_center = 250
        rect_side = int(self.radius * 2 ** 0.5)  # side of the inscribed square
        self.rect = pygame.Rect(CONFIG.GAME_WIDTH // 2 - self.radius, CONFIG.GAME_HEIGHT // 2 + y_offset_from_center,
                                rect_side, rect_side)
        self._bounce_combo = 0

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

        epsilon = 7
        # collision with angle of rect
        if abs(delta_x - delta_y) < epsilon:
            self.dx, self.dy = -self.dx, -self.dy
        # collision with horizontal side
        elif delta_x > delta_y:
            self.dy *= -1
        # collision with vertical side
        elif delta_x < delta_y:
            self.dx *= -1

    def is_out_of_bounds(self) -> bool:
        return self.rect.y > CONFIG.GAME_HEIGHT + self.rect.height

    def is_stopped(self) -> bool:
        return self.dx == 0 and self.dy == 0

    def is_walls_collision(self) -> bool:
        return self.rect.centerx < self.radius \
               or self.rect.centerx > CONFIG.GAME_WIDTH - self.radius

    def is_top_collision(self) -> bool:
        return self.rect.centery < self.radius

    def is_paddle_collision(self, paddle: Paddle) -> bool:
        return self.rect.colliderect(paddle.rect) and self.dy > 0

    def is_block_collision(self, blocks: List[Block]) -> bool:
        return self.rect.collidelist(blocks) != -1

    def move(self) -> None:
        self.rect.x += self.movement_speed * self.dx
        self.rect.y += self.movement_speed * self.dy

    def start_moving(self) -> None:
        self.dx = random.choice([1, -1])  # move right or left
        self.dy = -1

    def stick_to_the_paddle(self, paddle: Paddle) -> None:
        self.rect.centerx = paddle.rect.centerx
        self.rect.centery = paddle.rect.centery - CONFIG.PADDLE_HEIGHT // 2 - self.radius

    def respawn(self, paddle: Paddle) -> None:
        self.__init__(self.radius, self.movement_speed, self.color)
        self.stick_to_the_paddle(paddle)

    def draw(self, screen: pygame.surface) -> None:
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def speed_up(self) -> None:
        self._bounce_combo += 1
        if self._bounce_combo % CONFIG.DAMAGED_FOR_SPEEDUP == 0:
            self.movement_speed += 1
            self._bounce_combo = 0

    def _draw_rect(self, screen: pygame.surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)
