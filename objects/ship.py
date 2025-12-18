from itertools import product

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

    def is_kill(self, ship):
        killed_decks = 0
        for deck in range(len(ship)):
            if ship[deck].type == 3:
                killed_decks += 1
        if killed_decks != len(ship):
            return False
        else:
            return True

    def tick_cells_around_ship(self, ship, field, double_field):
        for deck in range(len(ship)):
            for x, y in product([-1, 0, 1], repeat=2):
                x_on_field = ship[deck].x_on_field
                y_on_field = ship[deck].y_on_field
                if 0 <= y_on_field + y < len(field) and 0 <= x_on_field + x < len(field[0]):
                    if field[y_on_field + y][x_on_field + x].type != 3:
                        field[y_on_field + y][x_on_field + x].set_type(2)
                        double_field[y_on_field + y][x_on_field + x].delete()
