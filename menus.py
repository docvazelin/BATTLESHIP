import pygame
import sys
from settings import *
from ui import Button, draw_text, draw_paper_background


def splash_screen(screen):
    splash = pygame.image.load("assets/start_screen.png")
    splash = pygame.transform.scale(splash, (WIDTH, HEIGHT))

    while True:
        screen.blit(splash, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.clear()
                return

            if event.type == pygame.KEYDOWN:
                pygame.event.clear()
                return


def main_menu(screen, font, big_font):
    start_btn = Button(410, 280, 280, 65, "Розпочати гру")
    settings_btn = Button(410, 365, 280, 65, "Налаштування")
    exit_btn = Button(410, 450, 280, 65, "Вийти")

    while True:
        draw_paper_background(screen)

        title = big_font.render("Морський бій", True, INK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        draw_text(screen, "паперова версія гри", 430, 215, font, PAPER_DARK)

        start_btn.draw(screen, font)
        settings_btn.draw(screen, font)
        exit_btn.draw(screen, font)

        pygame.display.update()

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

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.is_clicked(event):
                return