import pygame
from settings import *


class Button:
    def __init__(self, x, y, w, h, text, color=PAPER_LIGHT):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, PAPER_LINE, self.rect, 3, border_radius=8)

        text_surface = font.render(self.text, True, INK)
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def draw_text(screen, text, x, y, font, color=INK):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_paper_background(screen):
    screen.fill(PAPER_BG)

    for x in range(0, WIDTH, 45):
        pygame.draw.line(screen, (225, 214, 185), (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, 45):
        pygame.draw.line(screen, (225, 214, 185), (0, y), (WIDTH, y), 1)

    pygame.draw.rect(screen, PAPER_LINE, (25, 25, WIDTH - 50, HEIGHT - 50), 4)