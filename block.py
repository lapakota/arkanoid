from typing import Tuple

import pygame

GRAY = (169, 169, 169)


class Block:
    def __init__(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.scores = 10
        self.lives = 1

    def is_dead(self) -> bool:
        return self.lives <= 0

    def take_damage(self) -> None:
        self.lives -= 1

    def draw(self, screen: pygame.surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)


class SolidBlock(Block):
    def __init__(self, x: int, y: int, width: int, height: int):
        super(SolidBlock, self).__init__(x, y, width, height, GRAY)
        self.scores = 30
        self.lives = 3

    def take_damage(self) -> None:
        self.lives -= 1
        new_color_value = self.color[0] - 60
        self.color = (new_color_value, new_color_value, new_color_value)
