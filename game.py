import pygame
import sys
from settings import *
from ui import Button, draw_text, draw_paper_background
from board import Board


# =========================
# ЕКРАН ПЕРЕДАЧІ ХОДУ
# =========================
def pass_turn_screen(screen, font, big_font, player_name):
    continue_btn = Button(410, 430, 280, 60, "Продовжити")

    while True:
        draw_paper_background(screen)

        draw_text(screen, "Передача ходу", 400, 180, big_font)
        draw_text(screen, "Попросіть попереднього гравця відійти.", 300, 270, font)
        draw_text(screen, f"Хід: {player_name}", 420, 320, font)

        continue_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if continue_btn.is_clicked(event):
                return  # ← ВАЖЛИВО! НЕ sys.exit()

        pygame.display.update()


# =========================
# СТВОРЕННЯ СПИСКУ КОРАБЛІВ
# =========================
def create_ship_list():
    ships = []

    for name, size, count in SHIPS:
        ships.append({
            "name": name,
            "size": size,
            "left": count
        })

    return ships


# =========================
# ЕКРАН РОЗСТАНОВКИ
# =========================
def placement_screen(screen, font, small_font, big_font, player_name):
    board = Board(500, 150)
    ships = create_ship_list()

    selected_index = None
    orientation = "H"

    ready_btn = Button(850, 630, 180, 55, "Готово")
    back_btn = Button(70, 630, 180, 55, "Назад")

    while True:
        draw_paper_background(screen)

        # ===== ЗАГОЛОВОК =====
        draw_text(screen, f"{player_name}: розміщення кораблів", 300, 50, big_font)

        # ===== ПАНЕЛЬ ІНСТРУКЦІЇ =====
        panel_rect = pygame.Rect(40, 90, 360, 250)
        pygame.draw.rect(screen, PAPER_LIGHT, panel_rect, border_radius=14)
        pygame.draw.rect(screen, PAPER_LINE, panel_rect, 4, border_radius=14)

        draw_text(screen, "ІНСТРУКЦІЯ:", 70, 115, font, PAPER_DARK)

        draw_text(screen, "1. Обери корабель", 70, 155, small_font)
        draw_text(screen, "2. Наведи на поле", 70, 185, small_font)

        draw_text(screen, "ЛКМ — поставити корабель", 70, 220, small_font)
        draw_text(screen, "ЛКМ по кораблю — перемістити", 70, 250, small_font)

        draw_text(screen, "ПКМ по кораблю — видалити", 70, 285, small_font)

        draw_text(screen, "R — змінити напрямок", 70, 320, small_font)
        
        # ===== ДОШКА =====
        board.draw(screen, font)

        # ===== КНОПКИ КОРАБЛІВ =====
        ship_buttons = []
        y = 360

        for i, ship in enumerate(ships):
            text = f"{ship['name']} ({ship['size']}) x{ship['left']}"

            color = (220, 210, 180)

            if selected_index == i:
                color = (200, 180, 130)

            if ship["left"] <= 0:
                color = (180, 170, 150)

            btn = Button(70, y, 260, 45, text, color)
            btn.draw(screen, font)

            ship_buttons.append((btn, i))
            y += 55

        # ===== ПРЕВ'Ю =====
        mouse_cell = board.get_cell_from_mouse(pygame.mouse.get_pos())
        preview_cells = []
        can_place = False

        if selected_index is not None and mouse_cell:
            ship = ships[selected_index]

            if ship["left"] > 0:
                col, row = mouse_cell

                preview_cells = board.get_ship_cells(
                    col,
                    row,
                    ship["size"],
                    orientation
                )

                can_place = board.can_place_ship(preview_cells)

                board.draw_preview(screen, preview_cells, can_place)

        # ===== СТАН =====
        if selected_index is not None:
            ship = ships[selected_index]
            draw_text(
                screen,
                f"Обрано: {ship['name']} ({'горизонтально' if orientation == 'H' else 'вертикально'})",
                400,
                620,
                font,
                BLUE_INK
            )

        all_placed = all(ship["left"] == 0 for ship in ships)

        if all_placed:
            ready_btn.draw(screen, font)

        back_btn.draw(screen, font)

        # ===== ОБРОБКА ПОДІЙ =====
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

                # --- ЛІВА КНОПКА МИШІ (ЛКМ) ---
                if event.button == 1:

                    # Кнопки інтерфейсу працюють тільки на ЛКМ
                    if back_btn.is_clicked(event):
                        return None

                    if all_placed and ready_btn.is_clicked(event):
                        return board

                    clicked_menu = False

                    # Вибір типу корабля зліва
                    for btn, index in ship_buttons:
                        if btn.is_clicked(event):
                            clicked_menu = True

                            if ships[index]["left"] > 0:
                                selected_index = index

                    # Якщо клікнули не по меню
                    if not clicked_menu:
                        cell = board.get_cell_from_mouse(event.pos)

                        if cell:
                            col, row = cell

                            # Якщо корабель обрано — ставимо його
                            if selected_index is not None:
                                selected_ship = ships[selected_index]

                                if selected_ship["left"] > 0:
                                    cells = board.get_ship_cells(
                                        col,
                                        row,
                                        selected_ship["size"],
                                        orientation
                                    )

                                    if board.can_place_ship(cells):
                                        if board.place_ship(
                                            selected_ship["name"],
                                            selected_ship["size"],
                                            cells
                                        ):
                                            selected_ship["left"] -= 1

                                            if selected_ship["left"] == 0:
                                                selected_index = None

                            # Якщо нічого не обрано — піднімаємо корабель для переміщення
                            else:
                                removed = board.remove_ship_at(col, row)

                                if removed:
                                    removed_name, removed_size = removed

                                    for i, ship in enumerate(ships):
                                        if ship["name"] == removed_name and ship["size"] == removed_size:
                                            ship["left"] += 1
                                            selected_index = i
                                            break

                # --- ПРАВА КНОПКА МИШІ (ПКМ) ---
                elif event.button == 3:

                    # ПКМ видаляє корабель тільки якщо зараз нічого не обрано
                    if selected_index is None:
                        cell = board.get_cell_from_mouse(event.pos)

                        if cell:
                            col, row = cell
                            removed = board.remove_ship_at(col, row)

                            if removed:
                                removed_name, removed_size = removed

                                for ship in ships:
                                    if ship["name"] == removed_name and ship["size"] == removed_size:
                                        ship["left"] += 1
                                        break

        pygame.display.update() 