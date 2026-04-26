import pygame
import sys
from settings import *
from ui import Button, draw_text, draw_paper_background
from board import Board


def create_ship_list():
    result = []

    for name, size, count in SHIPS:
        result.append({
            "name": name,
            "size": size,
            "left": count
        })

    return result


def placement_screen(screen, font, big_font):
    board = Board(480, 150)
    ships = create_ship_list()

    selected_index = None
    orientation = "H"

    ready_btn = Button(850, 630, 180, 55, "Готово")
    back_btn = Button(70, 630, 180, 55, "Назад")

    while True:
        draw_paper_background(screen)

        # Заголовок по центру
        draw_text(screen, "Розміщення кораблів", 380, 40, big_font)

        # ===== ЛІВА ПАНЕЛЬ ПІДКАЗОК =====
        panel_rect = pygame.Rect(40, 90, 300, 200)
        pygame.draw.rect(screen, PAPER_LIGHT, panel_rect, border_radius=10)
        pygame.draw.rect(screen, PAPER_LINE, panel_rect, 3, border_radius=10)

        draw_text(screen, "ІНСТРУКЦІЯ:", 60, 105, font, PAPER_DARK)
        draw_text(screen, "1. Обери корабель", 60, 135, font)
        draw_text(screen, "2. Наведи на поле", 60, 165, font)
        draw_text(screen, "3. ЛКМ — поставити", 60, 195, font)
        draw_text(screen, "R — повернути", 60, 225, font)
        draw_text(screen, "Клік по кораблю — прибрати", 60, 255, font)
        board.draw(screen, font)

        ship_buttons = []

        y = 310
        for i, ship in enumerate(ships):
            text = f"{ship['name']} ({ship['size']}) x{ship['left']}"

            color = (220, 210, 180)

            if selected_index == i:
                color = (205, 190, 145)

            if ship["left"] <= 0:
                color = (190, 180, 160)

            btn = Button(70, y, 260, 45, text, color)
            btn.draw(screen, font)

            ship_buttons.append((btn, i))
            y += 58

        mouse_cell = board.get_cell_from_mouse(pygame.mouse.get_pos())

        preview_cells = []
        can_place = False

        if selected_index is not None and mouse_cell:
            selected_ship = ships[selected_index]

            if selected_ship["left"] > 0:
                col, row = mouse_cell
                preview_cells = board.get_ship_cells(
                    col,
                    row,
                    selected_ship["size"],
                    orientation
                )
                can_place = board.can_place_ship(preview_cells)
                board.draw_preview(screen, preview_cells, can_place)

        if selected_index is not None:
            ship = ships[selected_index]
            draw_text(
                screen,
                f"Обрано: {ship['name']}, напрямок: {'горизонтально' if orientation == 'H' else 'вертикально'}",
                390,
                610,
                font,
                BLUE_INK
            )

        all_placed = all(ship["left"] == 0 for ship in ships)

        if all_placed:
            ready_btn.draw(screen, font)

        back_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.is_clicked(event):
                return None

            if all_placed and ready_btn.is_clicked(event):
                return board

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    orientation = "V" if orientation == "H" else "H"

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn, index in ship_buttons:
                    if btn.is_clicked(event):
                        if ships[index]["left"] > 0:
                            selected_index = index

                cell = board.get_cell_from_mouse(event.pos)

                if cell:
                    col, row = cell

                    removed = board.remove_ship_at(col, row)

                    if removed:
                        removed_name, removed_size = removed

                        for ship in ships:
                            if ship["name"] == removed_name and ship["size"] == removed_size:
                                ship["left"] += 1
                                selected_index = ships.index(ship)
                                break

                    elif selected_index is not None:
                        selected_ship = ships[selected_index]

                        if selected_ship["left"] > 0:
                            cells = board.get_ship_cells(
                                col,
                                row,
                                selected_ship["size"],
                                orientation
                            )

                            if board.place_ship(
                                selected_ship["name"],
                                selected_ship["size"],
                                cells
                            ):
                                selected_ship["left"] -= 1

                                if selected_ship["left"] == 0:
                                    selected_index = None

        pygame.display.update()