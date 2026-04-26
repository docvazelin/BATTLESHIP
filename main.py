import pygame
from settings import *
from menus import main_menu
from game import placement_screen, pass_turn_screen, battle_screen

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Морський бій")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 24)
small_font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 42, bold=True)


def main():
    while True:
        result = main_menu(screen, font, big_font)

        if result == "start":

            # ===== ГРАВЕЦЬ 1 =====
            pass_turn_screen(screen, font, big_font, "Гравець 1")

            board_player_1 = placement_screen(
                screen,
                font,
                small_font,
                big_font,
                "Гравець 1"
            )

            if board_player_1 is None:
                continue

            # ===== ГРАВЕЦЬ 2 =====
            pass_turn_screen(screen, font, big_font, "Гравець 2")

            board_player_2 = placement_screen(
                screen,
                font,
                small_font,
                big_font,
                "Гравець 2"
            )

            if board_player_2 is None:
                continue

            battle_screen(
                screen,
                font,
                big_font,
                board_player_1,
                board_player_2
            )

if __name__ == "__main__":
    main()