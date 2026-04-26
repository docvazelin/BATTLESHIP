import pygame
import random
from settings import *


class Board:
    def __init__(self, x, y, cell_size=CELL_SIZE):
        self.x = x
        self.y = y
        self.cell = cell_size
        self.ships = []
        self.shots = {}  # ← для пострілів

    # =========================
    # МАЛЮВАННЯ ПОЛЯ
    # =========================
    def draw(self, screen, font, show_ships=True):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(
                    self.x + col * self.cell,
                    self.y + row * self.cell,
                    self.cell,
                    self.cell
                )

                pygame.draw.rect(screen, PAPER_LIGHT, rect)
                pygame.draw.rect(screen, PAPER_LINE, rect, 2)

        # літери
        for col, letter in enumerate(LETTERS):
            text = font.render(letter, True, INK)
            screen.blit(
                text,
                (self.x + col * self.cell + 10, self.y - 30)
            )

        # цифри
        for row in range(BOARD_SIZE):
            number = str(BOARD_SIZE - row)
            text = font.render(number, True, INK)
            screen.blit(
                text,
                (self.x - 30, self.y + row * self.cell + 10)
            )

        # кораблі
        if show_ships:
            for ship in self.ships:
                for col, row in ship["cells"]:
                    rect = pygame.Rect(
                        self.x + col * self.cell + 5,
                        self.y + row * self.cell + 5,
                        self.cell - 10,
                        self.cell - 10
                    )
                    pygame.draw.rect(screen, SHIP_COLOR, rect, border_radius=6)

        # постріли
        self.draw_shots(screen)
    def auto_place_all_ships(self):
        self.ships = []
        self.shots = {}

        for name, size, count in SHIPS:
            for _ in range(count):
                placed = False

                while not placed:
                    orientation = random.choice(["H", "V"])
                    col = random.randint(0, BOARD_SIZE - 1)
                    row = random.randint(0, BOARD_SIZE - 1)

                    cells = self.get_ship_cells(col, row, size, orientation)

                    if self.can_place_ship(cells):
                        self.place_ship(name, size, cells)
                        placed = True
    # =========================
    # ПРЕВ'Ю КОРАБЛЯ
    # =========================
    def draw_preview(self, screen, cells, can_place):
        if not cells:
            return

        color = PREVIEW_GOOD if can_place else PREVIEW_BAD

        for col, row in cells:
            if 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE:
                rect = pygame.Rect(
                    self.x + col * self.cell + 4,
                    self.y + row * self.cell + 4,
                    self.cell - 8,
                    self.cell - 8
                )
                pygame.draw.rect(screen, color, rect, border_radius=6)

    # =========================
    # ОТРИМАННЯ КЛІТИНКИ
    # =========================
    def get_cell_from_mouse(self, pos):
        mx, my = pos

        if not (self.x <= mx < self.x + BOARD_SIZE * self.cell):
            return None

        if not (self.y <= my < self.y + BOARD_SIZE * self.cell):
            return None

        col = (mx - self.x) // self.cell
        row = (my - self.y) // self.cell

        return col, row

    # =========================
    # КЛІТИНКИ КОРАБЛЯ
    # =========================
    def get_ship_cells(self, col, row, size, orientation):
        cells = []

        for i in range(size):
            if orientation == "H":
                cells.append((col + i, row))
            else:
                cells.append((col, row + i))

        return cells

    # =========================
    # ПЕРЕВІРКА МОЖЛИВОСТІ РОЗМІЩЕННЯ
    # =========================
    def can_place_ship(self, cells):
        for col, row in cells:
            if col < 0 or col >= BOARD_SIZE or row < 0 or row >= BOARD_SIZE:
                return False

        forbidden = set()

        for ship in self.ships:
            for col, row in ship["cells"]:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        forbidden.add((col + dx, row + dy))

        for cell in cells:
            if cell in forbidden:
                return False

        return True

    # =========================
    # ДОДАТИ КОРАБЕЛЬ
    # =========================
    def place_ship(self, name, size, cells):
        if self.can_place_ship(cells):
            self.ships.append({
                "name": name,
                "size": size,
                "cells": cells
            })
            return True

        return False

    # =========================
    # ВИДАЛИТИ КОРАБЕЛЬ
    # =========================
    def remove_ship_at(self, col, row):
        for ship in self.ships:
            if (col, row) in ship["cells"]:
                self.ships.remove(ship)
                return ship["name"], ship["size"]

        return None

    # =========================
    # ПОСТРІЛ
    # =========================
    def receive_shot(self, col, row):
        if (col, row) in self.shots:
            return "again"

        for ship in self.ships:
            if (col, row) in ship["cells"]:
                self.shots[(col, row)] = "hit"
                return "hit"

        self.shots[(col, row)] = "miss"
        return "miss"

    # =========================
    # МАЛЮВАННЯ ПОСТРІЛІВ
    # =========================
    def draw_shots(self, screen):
        for (col, row), result in self.shots.items():
            cx = self.x + col * self.cell + self.cell // 2
            cy = self.y + row * self.cell + self.cell // 2

            if result == "hit":
                pygame.draw.line(screen, RED_INK, (cx - 10, cy - 10), (cx + 10, cy + 10), 3)
                pygame.draw.line(screen, RED_INK, (cx + 10, cy - 10), (cx - 10, cy + 10), 3)

            elif result == "miss":
                pygame.draw.circle(screen, BLUE_INK, (cx, cy), 6, 2)