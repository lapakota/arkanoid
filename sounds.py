import pygame
from enum import Enum

from config import CONFIG

pygame.mixer.init()


class Sounds(Enum):
    BALL_BONK = pygame.mixer.Sound(CONFIG.BONK_SOUND)
    BLOCK_CRASH = pygame.mixer.Sound(CONFIG.CRASH_SOUND)
    LOOSE_LIFE = pygame.mixer.Sound(CONFIG.LIFE_SOUND)
    GAME_LOOSE = pygame.mixer.Sound(CONFIG.LOOSE_SOUND)
    GAME_WIN = pygame.mixer.Sound(CONFIG.WIN_SOUND)


[sound.value.set_volume(0.2) for sound in Sounds]
