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

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and continue_btn.rect.collidepoint(event.pos):
                    pygame.event.clear()
                    return


# =========================
# СПИСОК КОРАБЛІВ
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

        draw_text(screen, f"{player_name}: розміщення кораблів", 300, 50, big_font)

        # панель інструкції
        panel_rect = pygame.Rect(40, 90, 360, 280)
        pygame.draw.rect(screen, PAPER_LIGHT, panel_rect, border_radius=14)
        pygame.draw.rect(screen, PAPER_LINE, panel_rect, 4, border_radius=14)

        draw_text(screen, "ІНСТРУКЦІЯ:", 70, 115, font, PAPER_DARK)
        draw_text(screen, "1. Обери корабель", 70, 155, small_font)
        draw_text(screen, "2. Наведи на поле", 70, 185, small_font)
        draw_text(screen, "ЛКМ — поставити корабель", 70, 220, small_font)
        draw_text(screen, "ЛКМ по кораблю — перемістити", 70, 250, small_font)
        draw_text(screen, "ПКМ по кораблю — видалити", 70, 285, small_font)
        draw_text(screen, "R — змінити напрямок", 70, 320, small_font)

        board.draw(screen, font)

        # кнопки кораблів
        ship_buttons = []
        y = 395

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

        # прев'ю
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

        # статус
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

        # події
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    orientation = "V" if orientation == "H" else "H"

            if event.type == pygame.MOUSEBUTTONDOWN:

                # ЛКМ
                if event.button == 1:
                    if back_btn.is_clicked(event):
                        return None

                    if all_placed and ready_btn.is_clicked(event):
                        return board

                    clicked_menu = False

                    for btn, index in ship_buttons:
                        if btn.is_clicked(event):
                            clicked_menu = True

                            if ships[index]["left"] > 0:
                                selected_index = index

                    if not clicked_menu:
                        cell = board.get_cell_from_mouse(event.pos)

                        if cell:
                            col, row = cell

                            if selected_index is not None:
                                ship = ships[selected_index]

                                if ship["left"] > 0:
                                    cells = board.get_ship_cells(
                                        col,
                                        row,
                                        ship["size"],
                                        orientation
                                    )

                                    if board.can_place_ship(cells):
                                        if board.place_ship(ship["name"], ship["size"], cells):
                                            ship["left"] -= 1

                                            if ship["left"] == 0:
                                                selected_index = None

                            else:
                                removed = board.remove_ship_at(col, row)

                                if removed:
                                    name, size = removed

                                    for i, ship in enumerate(ships):
                                        if ship["name"] == name and ship["size"] == size:
                                            ship["left"] += 1
                                            selected_index = i
                                            break

                # ПКМ
                elif event.button == 3:
                    if selected_index is None:
                        cell = board.get_cell_from_mouse(event.pos)

                        if cell:
                            col, row = cell
                            removed = board.remove_ship_at(col, row)

                            if removed:
                                name, size = removed

                                for ship in ships:
                                    if ship["name"] == name and ship["size"] == size:
                                        ship["left"] += 1
                                        break

        pygame.display.update()


# =========================
# БОЙОВИЙ ЕКРАН
# =========================
def battle_screen(screen, font, big_font, board_player_1, board_player_2):
    current_player = 1
    message = "Гравець 1, зробіть постріл!"

    while True:
        draw_paper_background(screen)

        draw_text(screen, "Бій", 515, 40, big_font)

        if current_player == 1:
            own_data = board_player_1
            enemy_data = board_player_2
            player_text = "Хід гравця 1"
        else:
            own_data = board_player_2
            enemy_data = board_player_1
            player_text = "Хід гравця 2"

        own_board = Board(80, 170, 36)
        enemy_board = Board(620, 170, 36)

        own_board.ships = own_data.ships
        own_board.shots = own_data.shots

        enemy_board.ships = enemy_data.ships
        enemy_board.shots = enemy_data.shots

        draw_text(screen, player_text, 455, 95, font)
        draw_text(screen, "Ваше поле", 160, 130, font)
        draw_text(screen, "Поле суперника", 650, 130, font)

        own_board.draw(screen, font, show_ships=True)
        enemy_board.draw(screen, font, show_ships=False)

        draw_text(screen, message, 380, 620, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = enemy_board.get_cell_from_mouse(event.pos)

                if cell:
                    col, row = cell

                    result = enemy_data.receive_shot(col, row)

                    if result == "again":
                        message = "Ти вже сюди стріляв"

                    elif result == "hit":
                        message = "Влучив!"

                    elif result == "miss":
                        message = "Мимо:("

                        pygame.display.update()
                        pygame.time.delay(800)
                        pygame.event.clear()

                        current_player = 2 if current_player == 1 else 1

                        pass_turn_screen(
                            screen,
                            font,
                            big_font,
                            f"Гравець {current_player}"
                        )

                        message = f"Гравець {current_player}, зробіть постріл!"

        pygame.display.update()