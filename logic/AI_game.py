from random import choice, randint

from pyglet.gl.lib import t


class AIgame:
    def __init__(self, ships, shipsDrawer):
        self.ships = ships
        self.drawer_ships = shipsDrawer
        self.target = None
        self.defeated_deck = None
        self.first_deck = True
        #”ƒ¿À»“‹!!!
        self.move = 0
        #”ƒ¿À»“‹!!!

    def take_move(self, field, ships):
        if self.target is None:
            if self.take_move_on_diagonal(field) is not None:
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
                    self.target = searching_ship
                    self.defeated_deck = field[y_on_field][x_on_field]
                    if self.drawer_ships.is_kill(self.target, "bool"):
                        self.drawer_ships.tick_cells_around_ship(self.target, field)
                        return False
                    return True
                return False
            elif self.take_move_on_diagonal(field) is None:
                x_on_field, y_on_field = self.take_random_move(field, len(field))
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
                    self.target = searching_ship
                    self.defeated_deck = field[y_on_field][x_on_field]
                    if self.drawer_ships.is_kill(self.target, "bool"):
                        self.drawer_ships.tick_cells_around_ship(self.target, field)
                        return False
                    return True
                return False
        elif self.target is not None:
            if not self.hunt_move(field, ships):
                return False
            else:
                if self.drawer_ships.is_kill(self.target, "bool"):
                    self.drawer_ships.tick_cells_around_ship(self.target, field)
                    self.reset_hunt()
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

    def shoot_on_coord(self, coordinates, field):
        x_from_coord, y_from_coord = choice(coordinates)
        field[y_from_coord][x_from_coord].on_mouse_click(
            x_on_field=x_from_coord,
            y_on_field=y_from_coord,
            field=field
        )
        return x_from_coord, y_from_coord

    def reset_hunt(self):
        self.target = None
        self.defeated_deck = None
        self.first_deck = True


    def hunt_move(self, field, ships):
        if not self.drawer_ships.is_kill(self.target, "bool"):
            if not self.first_deck:
                coordinates = self.drawer_ships.is_kill(self.target, "coord")
                x_from_coord, y_from_coord = self.shoot_on_coord(coordinates, field)
                self.defeated_deck = field[y_from_coord][x_from_coord]
                self.first_deck = False
                return True
            elif self.first_deck:
                chance = randint(1, 100)
                if chance <= 25:
                    coordinates = self.drawer_ships.is_kill(self.target, "coord")
                    x_from_coord, y_from_coord = self.shoot_on_coord(coordinates, field)
                    self.defeated_deck = field[y_from_coord][x_from_coord]
                    self.first_deck = False
                    return True
                if chance > 25:
                    coordinates = []
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    for x, y in directions:
                        new_x = self.defeated_deck.x_on_field + x
                        new_y = self.defeated_deck.y_on_field + y
                        if 0 <= new_x <= 9 and 0 <= new_y <= 9 and field[new_y][new_x].type == 0:
                            coordinates.append((new_x, new_y))
                    if coordinates:
                        x_from_coord, y_from_coord = self.shoot_on_coord(coordinates, field)
                        #self.defeated_deck = field[y_from_coord][x_from_coord]
                        self.first_deck = True
                        return False
                    else:
                        coordinates = self.drawer_ships.is_kill(self.target, "coord")
                        x_from_coord, y_from_coord = self.shoot_on_coord(coordinates, field)
                        self.defeated_deck = field[y_from_coord][x_from_coord]
                        self.first_deck = False
                        return True
        else:
            self.reset_hunt()
            self.take_move(field, ships)
