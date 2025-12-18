from itertools import product
import config


class AIgame:
    def __init__(self, turn):
        self.turn = turn

    def take_move(self, field, x_on_field, y_on_field):
        field[y_on_field][x_on_field].on_mouse_click(x_on_field=x_on_field,
                                                     y_on_field=y_on_field,
                                                     field=field)
