WIDTH = 1100
HEIGHT = 750
FPS = 60

CELL_SIZE = 42
BOARD_SIZE = 10

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

# ===== ПАПЕРОВИЙ СТИЛЬ =====
PAPER_BG = (238, 229, 203)
PAPER_DARK = (84, 70, 50)
PAPER_LINE = (122, 98, 66)
PAPER_LIGHT = (250, 244, 225)

INK = (35, 35, 35)
BLUE_INK = (75, 110, 150)
RED_INK = (160, 60, 50)
GREEN_INK = (90, 130, 90)

SHIP_COLOR = (92, 86, 75)
PREVIEW_GOOD = (110, 160, 110)
PREVIEW_BAD = (180, 70, 70)

# ===== ТУТ МОЖНА ЗМІНИТИ ФОН =====
# Наприклад, можна замінити PAPER_BG на інший колір або картинку.

# ===== ТУТ МОЖНА ДОДАТИ ЗВУК =====
# import pygame
# pygame.mixer.music.load("music.mp3")
# pygame.mixer.music.play(-1)

SHIPS = [
    ("Лінкор", 4, 1),
    ("Крейсер", 3, 2),
    ("Есмінець", 2, 3),
    ("Катер", 1, 4),
]