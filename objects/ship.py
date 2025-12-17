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
                x_for_ships_in_row = self.ships[-1][-1].x + config.CELL_SIZE + config.BORDER_SIZE*4
            self.start_y -= config.CELL_SIZE + config.BORDER_SIZE*4

    def is_kill(self, ship):
        killed_decks = 0
        for deck in range(len(ship)):
            if ship[deck].type == 3:
                killed_decks += 1
        if killed_decks != len(ship):
            return False
        else:
            return True