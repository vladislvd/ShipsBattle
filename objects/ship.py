from itertools import product
from operator import le
from re import S

from pyglet.text import decode_attributed

import objects
import config


class ShipsDrawer:
    def __init__(self, max_long, batch, start_x, start_y):
        self.ships = []
        self.start_x = start_x
        self.start_y = start_y
        for long in range(1, max_long+1):
            x_for_ships_in_row = self.start_x
            for ship_num in range(max_long-long+1):
                ship = []
                for deck_num in range(long):
                    deck = objects.Cell(
                        x=x_for_ships_in_row + deck_num*(config.CELL_SIZE+config.BORDER_SIZE),
                        y=self.start_y,
                        type=1,
                        batch=batch
                    )
                    ship.append(deck)
                self.ships.append(ship)
                if long == 1:
                    x_for_ships_in_row = self.ships[-1][-1].x + 3*(config.CELL_SIZE + config.BORDER_SIZE)
                if long == 2:
                    x_for_ships_in_row = self.ships[-1][-1].x + 2*(config.CELL_SIZE + config.BORDER_SIZE)
                if long == 3:
                    x_for_ships_in_row = self.ships[-1][-1].x + 4*(config.CELL_SIZE + config.BORDER_SIZE)
            self.start_y -= config.CELL_SIZE + config.BORDER_SIZE

    def is_kill(self, ship, return_type):
        killed_decks = 0
        for deck in range(len(ship)):
            if ship[deck].type == 3:
                killed_decks += 1
        if return_type == "bool":
            return killed_decks == len(ship)
        elif return_type == "coord":
            coordinates = []
            for deck in range(len(ship)):
                if ship[deck].type == 1:
                    coordinates.append([ship[deck].x_on_field, ship[deck].y_on_field])
            return coordinates
        elif return_type == "killed_decks":
            return killed_decks

    def tick_cells_around_ship(self, ship, field, double_field=None):
        for deck in range(len(ship)):
            for x, y in product([-1, 0, 1], repeat=2):
                x_on_field = ship[deck].x_on_field
                y_on_field = ship[deck].y_on_field
                if 0 <= y_on_field + y < len(field) and 0 <= x_on_field + x < len(field[0]):
                    if field[y_on_field + y][x_on_field + x].type != 3:
                        field[y_on_field + y][x_on_field + x].set_type(2)
                        if double_field is not None:
                            double_field[y_on_field + y][x_on_field + x].delete()

    def find_ship(self, ships, field, x_on_field, y_on_field):
        for ship in range(len(ships)):
            for deck in range(len(ships[ship])):
                if ships[ship][deck] == field[y_on_field][x_on_field]:
                    return ships[ship]

    def check_around(self, ship_len, x_on_field, y_on_field, rotate, size, field, for_pl = False):
        if not for_pl:
            for cell in range(ship_len):
                cx = x_on_field + (cell if rotate == 'x' else 0)
                cy = y_on_field + (cell if rotate == 'y' else 0)
                if not (0 <= cx < size and 0 <= cy < size):
                    return False
                for x, y in product([-1, 0, 1], repeat=2):
                    dx, dy = cx + x, cy + y
                    if 0 <= dx < size and 0 <= dy < size:
                        if field[dy][dx].type == 1:
                            return False
            return True
        else:
            ship_cells = set()
            for cell in range(ship_len):
                cx = x_on_field + (cell if rotate == 'x' else 0)
                cy = y_on_field + (cell if rotate == 'y' else 0)
                ship_cells.add((cx,cy))
                
            for cx, cy in ship_cells:
                if not (0 <= cx < size and 0 <= cy < size):
                    return False
                for x, y in product([-1, 0, 1], repeat=2):
                    dx, dy = cx + x, cy + y
                    if (dx, dy) in ship_cells:
                        continue
                    if 0 <= dx < size and 0 <= dy < size:
                        if field[dy][dx].type == 1:
                            return False
            return True

    def check_rotate(self):
        for ship in self.ships:
            if all(deck.x == ship[0].x for deck in ship):
                for deck in ship:
                    deck.rotate = "y"
            elif all(deck.y == ship[0].y for deck in ship):
                for deck in ship:
                    deck.rotate = "x"

    def change_rotate(self, ship, rotate, mouse_x, mouse_y):
        if ship[0].rotate == rotate:
            return False
        for i, deck in enumerate(ship):
            deck.rotate = rotate
            step = i * (config.CELL_SIZE + config.BORDER_SIZE)
            if rotate == 'x':
                deck.x = mouse_x + step
                deck.y = mouse_y
            else:
                deck.x = mouse_x
                deck.y = mouse_y + step
