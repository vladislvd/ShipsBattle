from random import choice, randint
from pyglet.gl import base


class AIgame:
    def __init__(self, ships, shipsDrawer):
        self.ships = ships
        self.drawer_ships = shipsDrawer
        self.target = None
        self.defeated_deck = None
        self.first_deck = True
        self.ships_len = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    def get_probability_map(self, field):
        size = len(field)
        weights = [[0 for _ in range(size)] for _ in range(size)]
        for ship_len in self.ships_len:
            for y in range(size):
                for x in range(size):
                    if ship_len + x <= size:
                        if all(field[y][x + i].type < 2 for i in range(ship_len)):
                            for i in range(ship_len):
                                weights[y][x+i] += 1
                    if ship_len + y <= size:
                        if all(field[y+i][x].type < 2 for i in range(ship_len)):
                            for i in range(ship_len):
                                weights[y+i][x] += 1
        return weights

    def take_move(self, field, ships):
        if self.target is None:
            weights = self.get_probability_map(field)
            best_coords = []
            max_weight = 0
            for y in range(len(field)):
                for x in range(len(field)):
                    if field[y][x].type < 2:
                        if weights[y][x] >= max_weight:
                            max_weight = weights[y][x]
                            best_coords = [(x, y)]
                        elif weights[y][x] == max_weight:
                            best_coords.append((x, y))
            x_from_coord, y_from_coord = self.shoot_on_coord(best_coords, field)
            if field[y_from_coord][x_from_coord].type == 3:
                self.start_hunting(field, ships, x_from_coord, y_from_coord)
                return True
            return False

        elif self.target is not None:
            if not self.hunt_move(field, ships):
                return False
            else:
                if self.drawer_ships.is_kill(self.target, "bool"):
                    self.drawer_ships.tick_cells_around_ship(self.target, field)
                    self.reset_hunt()
                return True

    def start_hunting(self, field, ships, x, y):
        searching_ship = None
        for ship in range(len(ships)):
            for deck in range(len(ships[ship])):
                if ships[ship][deck] == field[y][x]:
                    searching_ship = ships[ship]
        self.target = searching_ship
        self.defeated_deck = field[y][x]
        if self.drawer_ships.is_kill(self.target, "bool"):
            ship_len = len(self.target)
            if ship_len in self.ships_len:
                self.ships_len.remove(ship_len)
            self.drawer_ships.tick_cells_around_ship(self.target, field)
            self.reset_hunt()

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
