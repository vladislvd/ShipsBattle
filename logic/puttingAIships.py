import random
import config
from itertools import product
from operator import itemgetter


class PuttingAIShips:
    def __init__(self, field, ships, filedDrawer):
        self.field = field
        self.ships = ships
        self.filedDrawer = filedDrawer
        self.max_attempts = 100
        self.ships_len = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.put_ai_ships(ships)


    def check_around(self, decks, x_on_field, y_on_field, rotate, size):
        for cell in range(decks):
            cx = x_on_field + (cell if rotate == 'x' else 0)
            cy = y_on_field + (cell if rotate == 'y' else 0)
            
            if not (0 <= cx < size and 0 <= cy < size):
                return False

            for x, y in product([-1, 0, 1], repeat=2):
                dx, dy = cx + x, cy + y
                if 0 <= dx < size and 0 <= dy < size:
                    if self.field[dy][dx].type == 1:
                        return False
        return True

    def get_probability_map(self):
        size = len(self.field)
        weights = [[0 for _ in range(size)] for _ in range(size)]
        current_ships_len = self.ships_len
        for ship_len in current_ships_len:
            for y in range(size):
                for x in range(size):   
                    can_place_x = (x + ship_len <= size)
                    can_place_y = (y + ship_len <= size)
                    if can_place_x and self.check_around(ship_len, x, y, 'x', size):
                            for i in range(ship_len):
                                weights[y][x+i] += 1
                    if can_place_y and self.check_around(ship_len, x, y, 'y', size):
                        for i in range(ship_len):
                            weights[y+i][x] += 1
        return weights

    def get_x_y(self, decks):
        size = len(self.field)
        weights = self.get_probability_map()
        coords = []
        for rotate in ['x','y']:
            for y in range(size):
                for x in range(size):
                    if (rotate == 'x' and x + decks <= size) or (rotate == 'y' and y + decks <= size):
                        if self.check_around(decks, x, y, rotate, size):
                            current_weight = 0
                            for i in range(decks):
                                cx = x + (i if rotate == 'x' else 0)
                                cy = y + (i if rotate == 'y' else 0)
                                current_weight += weights[cy][cx]
                            coords.append((current_weight, x, y, rotate))
        if not coords:
            return None
        coords.sort(key=itemgetter(0)) 
        best_coords = coords[:6]
        weight, x, y ,rotate = random.choice(best_coords)
        return x, y ,rotate

    def put_ai_ships(self, ships):
        self.filedDrawer.clear_field()
        
        for i, decks in enumerate(self.ships_len):
            result = self.get_x_y(decks)
            if result is None:
                self.put_ai_ships()
                return
            x, y, rotate = self.get_x_y(decks)
            ai_ship = []
            for d in range(decks):
                cx = x + (d if rotate == 'x' else 0)
                cy = y + (d if rotate == 'y' else 0)

                cell = self.field[cy][cx]
                cell.set_type(1)
                cell.x_on_field = cx
                cell.y_on_field = cy
                cell.rotate = rotate
                ai_ship.append(cell)
            ships[i] = ai_ship
