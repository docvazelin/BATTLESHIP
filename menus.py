import pygame
import sys
from settings import *
from ui import Button, draw_text, draw_paper_background


def main_menu(screen, font, big_font):
    start_btn = Button(410, 280, 280, 65, "Розпочати гру")
    settings_btn = Button(410, 365, 280, 65, "Налаштування")
    exit_btn = Button(410, 450, 280, 65, "Вийти")

    while True:
        draw_paper_background(screen)

        title = big_font.render("Морський бій", True, INK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        draw_text(screen, "паперова версія гри", 430, 215, font, PAPER_DARK)

        for btn in [start_btn, settings_btn, exit_btn]:
            btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_btn.is_clicked(event):
                return "start"

            if settings_btn.is_clicked(event):
                settings_menu(screen, font, big_font)

            if exit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()


def settings_menu(screen, font, big_font):
    back_btn = Button(410, 540, 280, 60, "Назад")

    while True:
        draw_paper_background(screen)

        title = big_font.render("Налаштування", True, INK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 130))

        draw_text(screen, "Тут можна буде змінити фон гри.", 330, 250, font)
        draw_text(screen, "Тут можна буде увімкнути або вимкнути звук.", 330, 295, font)
        draw_text(screen, "Потрібні місця в коді позначені коментарями.", 330, 340, font)

        back_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.is_clicked(event):
                return

        pygame.display.update()