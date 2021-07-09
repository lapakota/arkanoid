import pygame

from game import Game


def main():
    game = Game()
    game.main_loop()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Arkanoid')
    main()
