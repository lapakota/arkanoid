import pygame
from config import CONFIG


class Paddle:
    def __init__(self, width: int, height: int, speed: int, color: str):
        self.width = width
        self.height = height
        self.movement_speed = speed
        self.color = pygame.Color(color)
        bottom_indent = 10
        self.rect = pygame.Rect(CONFIG.GAME_WIDTH // 2 - self.width // 2,
                                CONFIG.GAME_HEIGHT - self.height - bottom_indent,
                                self.width, self.height)

    def draw(self, screen: pygame.surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)
