from random import choice

from pyglet.clock import schedule_once


class AIgame:
    def __init__(self, ships, shipsDrawer):
        self.ships = ships
        self.drawer_ships = shipsDrawer
        self.target = None
        self.searching_ship = None
        self.move = 0

    def take_move(self, field, ships, game_scene):
        if self.target is None:
            if self.take_move_on_diagonal(field) is not None:
                x_on_field, y_on_field = self.take_move_on_diagonal(field)
                field[y_on_field][x_on_field].on_mouse_click(
                    x_on_field=x_on_field,
                    y_on_field=y_on_field,
                    field=field
                )
                if field[y_on_field][x_on_field].type == 3:
                    for ship in range(len(ships)):
                        for deck in range(len(ships[ship])):
                            if ships[ship][deck] == field[y_on_field][x_on_field]:
                                self.searching_ship = ships[ship]
                    self.target = self.searching_ship
                    game_scene.turn = 'AI'
                    if self.drawer_ships.is_kill(self.searching_ship, "bool"):
                        self.drawer_ships.tick_cells_around_ship(self.target, field)
                        return False
                    # __import__("time").sleep(1)
                    return True
                return False
            elif self.take_move_on_diagonal(field) is None:
                x_on_field, y_on_field = self.take_random_move(field, len(field))
                field[y_on_field][x_on_field].on_mouse_click(
                    x_on_field=x_on_field,
                    y_on_field=y_on_field,
                    field=field
                )
                if field[y_on_field][x_on_field].type == 3:
                    for ship in range(len(ships)):
                        for deck in range(len(ships[ship])):
                            if ships[ship][deck] == field[y_on_field][x_on_field]:
                                self.searching_ship = ships[ship]
                    self.target = self.searching_ship
                    game_scene.turn = 'AI'
                    if self.drawer_ships.is_kill(self.searching_ship, "bool"):
                        self.drawer_ships.tick_cells_around_ship(self.target, field)
                        return False

                    return True
                return False
        elif self.target is not None:
            self.hunt_move(field)
            if self.drawer_ships.is_kill(self.searching_ship, "bool"):
                self.drawer_ships.tick_cells_around_ship(self.target, field)
                self.target = None
                return False
            return True

    def get_cells(self, field, len_field):
        cells = []
        for y in range(len_field):
            for x in range(len_field):
                if field[y][x].type != 3 and field[y][x].type != 2:
                    cells.append((x, y))
        return cells

    def take_random_move(self, field, len_field):
        cells = []
        for y in range(len_field):
            for x in range(len_field):
                if field[y][x].type != 3 and field[y][x].type != 2:
                    cells.append((x, y))
        x_on_field, y_on_field = choice(cells)
        return x_on_field, y_on_field

    def get_diagonal_cells(self, field, len_field, max_ship_len):
        cells = []
        for y in range(len_field):
            for x in range(len_field):
                if (x % max_ship_len) == (y % max_ship_len) and field[y][x].type != 3 and field[y][x].type != 2:
                    cells.append((x, y))
        return cells

    def take_move_on_diagonal(self, field):
        cells = self.get_diagonal_cells(field, len(field), 4)
        available = []
        for x_on_field, y_on_field in cells:
            if getattr(field[y_on_field][x_on_field], 'type') != 2 and \
                    getattr(field[y_on_field][x_on_field], 'type') != 3:
                available.append((x_on_field, y_on_field))
        if cells:
            x_on_field, y_on_field = choice(cells)
            return x_on_field, y_on_field
        else:
            return None

    def hunt_move(self, field):
        if not self.drawer_ships.is_kill(self.target, "bool"):
            coordinates = self.drawer_ships.is_kill(self.target, "coord")
            x_form_coord, y_form_coord = choice(coordinates)
            field[y_form_coord][x_form_coord].on_mouse_click(
                x_on_field=x_form_coord,
                y_on_field=y_form_coord,
                field=field
            )
