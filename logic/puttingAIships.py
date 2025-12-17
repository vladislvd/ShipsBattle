import random
from itertools import product


class PuttingAIShips:
    def __init__(self, field, ships, filedDrawer):
        self.field = field
        self.ships = ships
        self.filedDrawer = filedDrawer
        self.max_attempts = 100
        self.put_ai_ships()

    def check_around(self, decks, x_on_field, y_on_field, rotate):
        for cell in range(decks):
            for x, y in product([-1, 0, 1], repeat=2):
                if rotate == 'x':
                    try:
                        if self.field[y_on_field + y][x_on_field + cell + x].type == 1:
                            return False
                    except:
                        continue
                if rotate == 'y':
                    try:
                        if self.field[y_on_field + cell + y][x_on_field + x].type == 1:
                            return False
                    except:
                        continue
        return True

    def get_x_y(self, ship):
        decks = len(self.ships[ship])
        row_len = len(self.field[0])
        col_len = len(self.field)
        rotate = random.choice(['x', 'y'])
        if rotate == 'x':
            max_x = row_len - decks
            x_on_field = random.randint(0, max_x)
            y_on_field = random.randint(0, col_len-1)
            attempt = 0
            while not self.check_around(decks, x_on_field, y_on_field, rotate):
                attempt += 1
                if attempt <= self.max_attempts:
                    x_on_field = random.randint(0, max_x)
                    y_on_field = random.randint(0, col_len - 1)
                    self.check_around(decks, x_on_field, y_on_field, rotate)
                else:
                    return 0
            return x_on_field, y_on_field, rotate
        if rotate == 'y':
            max_y = col_len - decks
            x_on_field = random.randint(0, row_len-1)
            y_on_field = random.randint(0, max_y)
            attempt = 0
            while not self.check_around(decks, x_on_field, y_on_field, rotate):
                attempt += 1
                if attempt <= self.max_attempts:
                    x_on_field = random.randint(0, row_len - 1)
                    y_on_field = random.randint(0, max_y)
                    self.check_around(decks, x_on_field, y_on_field, rotate)
                else:
                    return 0
            return x_on_field, y_on_field, rotate

    def put_ai_ships(self):
        for ship in range(len(self.ships)):
            result = self.get_x_y(ship)
            if result == 0:
                self.filedDrawer.clear_field()
                self.put_ai_ships()
            else:
                x_on_field, y_on_field, rotate = result
                decks = len(self.ships[ship])
                ai_ship = []
                for i in range(decks):
                    if rotate == 'x':
                        self.field[y_on_field][x_on_field+i].set_type(1)
                        ai_ship.append(self.field[y_on_field][x_on_field+i])
                    if rotate == 'y':
                        self.field[y_on_field+i][x_on_field].set_type(1)
                        ai_ship.append(self.field[y_on_field+i][x_on_field])
                self.ships[ship] = ai_ship
