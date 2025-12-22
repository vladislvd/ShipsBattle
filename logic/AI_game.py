from random import randint, randrange, choice
from functools import lru_cache
import config


class AIgame:
    def __init__(self, turn, ships, shipsDrawer):
        self.turn = turn
        self.ships = ships
        self.drawer_ships = shipsDrawer

    def take_move(self, field, ships):
        x_on_field, y_on_field = self.take_move_on_diagonal(field)
        field[y_on_field][x_on_field].on_mouse_click(
            x_on_field=x_on_field,
            y_on_field=y_on_field,
            field=field
        )
        searching_ship = None
        if field[y_on_field][x_on_field].type == 3:
            for ship in range(len(ships)):
                for deck in range(len(ships[ship])):
                    if ships[ship][deck] == field[y_on_field][x_on_field]:
                        searching_ship = ships[ship]
                        # print(ships[ship][deck].x_on_field, ships[ship][deck].y_on_field)
            if self.drawer_ships.is_kill(searching_ship, "bool") == False:
                coordinates = self.drawer_ships.is_kill(searching_ship, "coord")
                x_form_coord, y_form_coord = choice(coordinates)
                # x, y = self.hunt_move(x_form_coord, y_form_coord, field)
                # x_on_field, y_on_field = x, y
                field[y_form_coord][x_form_coord].on_mouse_click(
                    x_on_field=x_form_coord,
                    y_on_field=y_form_coord,
                    field=field
                )

    def take_random_move(self, field):
        x_on_field = randint(0, 9)
        y_on_field = randint(0, 9)
        return x_on_field, y_on_field

    # @lru_cache(None)
    def get_diagonal_cells(self, len_field, max_ship_len):
        cells = []
        for y in range(len_field):
            for x in range(len_field):
                if (x % max_ship_len) == (y % max_ship_len):
                    cells.append((x, y))
        return cells

    def take_move_on_diagonal(self, field):
        cells = self.get_diagonal_cells(len(field), 4)
        available = []
        for x_on_field, y_on_field in cells:
            if getattr(field[y_on_field][x_on_field], 'type') != 2:
                available.append((x_on_field, y_on_field))
        if available:
            x_on_field, y_on_field = choice(available)
            return x_on_field, y_on_field

    def hunt_move(self, x_on_field, y_on_field, field):
        target_cells = [(x_on_field+1, y_on_field), (x_on_field-1, y_on_field),
                        (x_on_field, y_on_field+1), (x_on_field, y_on_field-1)]
        for coord in range(len(target_cells)):
            if 0 <= target_cells[coord][0] <= 9 and 0 <= target_cells[coord][1] <= 9:
                if field[target_cells[coord][1]][target_cells[coord][0]].type == 1:
                    return target_cells[coord][0], target_cells[coord][1]



