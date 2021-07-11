from random import randrange
from typing import List, Tuple

import pygame

from ball import Ball
from block import Block, SolidBlock
from config import CONFIG
from handlers import MouseHandler, KeyHandler, GeneralEventsHandler
from paddle import Paddle
from sounds import Sounds


def get_random_rgb_color() -> Tuple[int, int, int]:
    return randrange(30, 256), randrange(30, 256), randrange(30, 256)


class Game:
    def __init__(self):
        self.run = True
        self.lives = CONFIG.LIVES
        self.scores = 0
        self.paddle = Paddle(CONFIG.PADDLE_WIDTH, CONFIG.PADDLE_HEIGHT, CONFIG.PADDLE_SPEED,
                             pygame.Color(CONFIG.PADDLE_COLOR))
        self.ball = Ball(CONFIG.BALL_RADIUS, CONFIG.BALL_SPEED, pygame.Color(CONFIG.BALL_COLOR))
        self.ball.stick_to_the_paddle(self.paddle)
        self.blocks = self._spawn_blocks_map()
        self.mouse_handler = MouseHandler(self.paddle, self.ball)
        self.key_handler = KeyHandler(self.paddle, self.ball)
        self.big_font = pygame.font.SysFont('segou', 140)
        self.small_font = pygame.font.SysFont('comicsans', 34)

    def restart_game(self) -> None:
        self.__init__()
        self.main_loop()

    def main_loop(self) -> None:
        screen = pygame.display.set_mode((CONFIG.GAME_WIDTH, CONFIG.GAME_HEIGHT))
        clock = pygame.time.Clock()
        bg_img = pygame.image.load(CONFIG.BG_PATH).convert()

        while self.run:
            self._listen_restart()
            # drawing
            screen.blit(bg_img, (0, 0))
            self.paddle.draw(screen)
            [block.draw(screen) for block in self.blocks]
            self.ball.draw(screen)
            self._draw_hud(screen)
            # movement
            self.ball.move()
            # loose
            self._handle_loss_life(screen, self.ball, self.paddle)
            # win
            self._handle_win(screen, self.blocks)
            # collisions
            self._ball_with_block_collision(self.ball, self.blocks)
            self.ball.handle_paddle_collision(self.paddle)
            self.ball.handle_walls_collision()
            self.ball.handle_top_collision()
            # controls
            self.mouse_handler.handle_mouse_events()
            self.key_handler.handle_key_pressing()
            # update screen
            pygame.display.flip()
            clock.tick(CONFIG.FPS)

    def _draw_hud(self, screen: pygame.surface) -> None:
        lives_text = self.small_font.render(f'lives: {self.lives}', True, pygame.Color('white'))
        scores_text = self.small_font.render(f'scores: {self.scores}', True, pygame.Color('white'))
        all_text = [lives_text, scores_text]
        left_indent = 10
        down_indent = 35
        width_between_texts = 100
        [screen.blit(text, (left_indent + width_between_texts * i,
                            CONFIG.GAME_HEIGHT - down_indent)) for i, text in enumerate(all_text)]

    def _handle_loss_life(self, screen: pygame.surface, ball: Ball, paddle: Paddle) -> None:
        if ball.is_out_of_bounds():
            self._lose_life()
            ball.respawn(paddle)
            if self._is_dead():
                Sounds.GAME_LOOSE.value.play()
                self.run = False
                self._draw_end_text(screen, "GAME OVER", pygame.Color('red'))
            Sounds.LOOSE_LIFE.value.play()

    def _handle_win(self, screen: pygame.surface, blocks: List[Block]) -> None:
        if len(blocks) == 0:
            Sounds.GAME_WIN.value.play()
            self.run = False
            self._draw_end_text(screen, "YOU WON", pygame.Color('green'))

    @staticmethod
    def _spawn_blocks_map() -> List[Block]:
        columns_count = CONFIG.GAME_WIDTH // CONFIG.BLOCK_WIDTH
        rows_count = CONFIG.GAME_HEIGHT // 2 // CONFIG.BLOCK_HEIGHT - 2
        width_between_blocks = 5
        left_indent = 2
        up_indent = 5
        blocks = [Block(left_indent + (CONFIG.BLOCK_WIDTH + width_between_blocks) * column,
                        up_indent + (CONFIG.BLOCK_HEIGHT + width_between_blocks) * row,
                        CONFIG.BLOCK_WIDTH, CONFIG.BLOCK_HEIGHT, get_random_rgb_color())
                  for column in range(columns_count) for row in range(rows_count)]

        from_upper_blocks = up_indent + (CONFIG.BLOCK_HEIGHT + width_between_blocks) * rows_count
        solid_rows = 1

        solid_blocks = [SolidBlock(left_indent + (CONFIG.BLOCK_WIDTH + width_between_blocks) * column,
                                   from_upper_blocks + (CONFIG.BLOCK_HEIGHT + width_between_blocks) * row,
                                   CONFIG.BLOCK_WIDTH, CONFIG.BLOCK_HEIGHT)
                        for column in range(columns_count) for row in range(solid_rows)]
        blocks.extend(solid_blocks)
        return blocks

    def _draw_end_text(self, screen: pygame.surface, end_text: str, color: pygame.Color) -> None:
        game_over_text = self.big_font.render(end_text, True, color)
        x_indent_from_center = 34 * len(end_text)
        y_indent_from_center = 50
        screen.blit(game_over_text,
                    (CONFIG.GAME_WIDTH // 2 - x_indent_from_center,
                     CONFIG.GAME_HEIGHT // 2 - y_indent_from_center))
        self._draw_hud(screen)
        pygame.display.update()
        while True:
            self._listen_restart()

    def _listen_restart(self) -> None:
        restart = GeneralEventsHandler().handle_general_events()
        if restart:
            self.restart_game()

    def _ball_with_block_collision(self, ball, blocks):
        scores_from_dead_block = ball.handle_block_collision(blocks)
        if scores_from_dead_block:
            self.scores += scores_from_dead_block

    def _lose_life(self) -> None:
        self.lives -= 1

    def _is_dead(self) -> bool:
        return self.lives <= 0
