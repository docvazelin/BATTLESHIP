import pygame
from settings import *
from menus import main_menu
from game import placement_screen

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Морський бій")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 42, bold=True)


def main():
    while True:
        result = main_menu(screen, font, big_font)

        if result == "start":
            board = placement_screen(screen, font, big_font)

            if board is not None:
                print("Кораблі розставлено!")
                for ship in board.ships:
                    print(ship)


if __name__ == "__main__":
    main()