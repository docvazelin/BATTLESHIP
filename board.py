import pygame
import random
from settings import *


def load_ship_image(size):
    path = f"assets/ships/ship_{size}.png"

    try:
        image = pygame.image.load(path)
        print(f"Завантажено: {path}")
        return image
    except Exception as error:
        print(f"Не знайдено: {path}", error)
        return None


def load_mark_image(name):
    try:
        return pygame.image.load(f"assets/marks/{name}.png")
    except:
        return None


SHIP_IMAGES = {
    4: load_ship_image(4),
    3: load_ship_image(3),
    2: load_ship_image(2),
    1: load_ship_image(1),
}

MARK_IMAGES = {
    "hit": load_mark_image("hit"),
    "miss": load_mark_image("miss"),
    "miss_auto": load_mark_image("miss"),
}


class Board:
    def __init__(self, x, y, cell_size=CELL_SIZE):
        self.x = x
        self.y = y
        self.cell = cell_size
        self.ships = []
        self.shots = {}

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

        for col, letter in enumerate(LETTERS):
            text = font.render(letter, True, INK)
            screen.blit(text, (self.x + col * self.cell + 10, self.y - 30))

        for row in range(BOARD_SIZE):
            number = str(BOARD_SIZE - row)
            text = font.render(number, True, INK)
            screen.blit(text, (self.x - 30, self.y + row * self.cell + 10))

        if show_ships:
            for ship in self.ships:
                self.draw_ship(screen, ship)

        self.draw_shots(screen)

    def draw_ship(self, screen, ship):
        cells = ship["cells"]
        size = ship["size"]

        min_col = min(cell[0] for cell in cells)
        min_row = min(cell[1] for cell in cells)
        max_row = max(cell[1] for cell in cells)

        x = self.x + min_col * self.cell
        y = self.y + min_row * self.cell

        image = SHIP_IMAGES.get(size)

        if image:
            if min_row == max_row:
                image = pygame.transform.scale(
                    image,
                    (self.cell * size, self.cell)
                )
            else:
                image = pygame.transform.rotate(image, 90)
                image = pygame.transform.scale(
                    image,
                    (self.cell, self.cell * size)
                )

            screen.blit(image, (x, y))

        else:
            for col, row in cells:
                rect = pygame.Rect(
                    self.x + col * self.cell + 5,
                    self.y + row * self.cell + 5,
                    self.cell - 10,
                    self.cell - 10
                )
                pygame.draw.rect(screen, SHIP_COLOR, rect, border_radius=6)

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

    def get_cell_from_mouse(self, pos):
        mx, my = pos

        if not (self.x <= mx < self.x + BOARD_SIZE * self.cell):
            return None

        if not (self.y <= my < self.y + BOARD_SIZE * self.cell):
            return None

        col = (mx - self.x) // self.cell
        row = (my - self.y) // self.cell

        return col, row

    def get_ship_cells(self, col, row, size, orientation):
        cells = []

        for i in range(size):
            if orientation == "H":
                cells.append((col + i, row))
            else:
                cells.append((col, row + i))

        return cells

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

    def place_ship(self, name, size, cells):
        if self.can_place_ship(cells):
            self.ships.append({
                "name": name,
                "size": size,
                "cells": cells
            })
            return True

        return False

    def remove_ship_at(self, col, row):
        for ship in self.ships:
            if (col, row) in ship["cells"]:
                self.ships.remove(ship)
                return ship["name"], ship["size"]

        return None

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

    def receive_shot(self, col, row):
        current_cell = (col, row)

        if current_cell in self.shots:
            if self.shots[current_cell] == "miss_auto":
                return "auto_miss"

            return "again"

        for ship in self.ships:
            if current_cell in ship["cells"]:
                self.shots[current_cell] = "hit"

                if self.is_ship_destroyed(ship):
                    self.mark_around_destroyed_ship(ship)
                    return "destroyed"

                return "hit"

        self.shots[current_cell] = "miss"
        return "miss"

    def is_ship_destroyed(self, ship):
        for cell in ship["cells"]:
            if cell not in self.shots or self.shots[cell] != "hit":
                return False

        return True

    def all_ships_destroyed(self):
        for ship in self.ships:
            for cell in ship["cells"]:
                if cell not in self.shots or self.shots[cell] != "hit":
                    return False

        return True

    def mark_around_destroyed_ship(self, ship):
        for col, row in ship["cells"]:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    new_col = col + dx
                    new_row = row + dy

                    if 0 <= new_col < BOARD_SIZE and 0 <= new_row < BOARD_SIZE:
                        cell = (new_col, new_row)

                        if cell not in self.shots:
                            self.shots[cell] = "miss_auto"

    def draw_shots(self, screen):
        for (col, row), result in self.shots.items():
            x = self.x + col * self.cell
            y = self.y + row * self.cell

            image = MARK_IMAGES.get(result)

            if image:
                image = pygame.transform.scale(
                    image,
                    (self.cell - 8, self.cell - 8)
                )
                screen.blit(image, (x + 4, y + 4))

            else:
                cx = x + self.cell // 2
                cy = y + self.cell // 2

                if result == "hit":
                    pygame.draw.line(screen, RED_INK, (cx - 10, cy - 10), (cx + 10, cy + 10), 3)
                    pygame.draw.line(screen, RED_INK, (cx + 10, cy - 10), (cx - 10, cy + 10), 3)

                elif result == "miss" or result == "miss_auto":
                    pygame.draw.circle(screen, BLUE_INK, (cx, cy), 6, 2)