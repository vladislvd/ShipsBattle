from objects import Cell
import config.settings as config


class FieldDrawer:
    def __init__(self, window_width, window_height, batch,  field_data, x_loc):
        self.field = []
        self.window_width = window_width
        self.window_height = window_height
        self.x_loc = x_loc
        self.batch = batch
        for row in range(len(field_data)):
            field_row = []
            for col in range(len(field_data[row])):
                cell = Cell(
                    x=col * (config.CELL_SIZE+config.BORDER_SIZE) + x_loc,
                    y=row * (config.CELL_SIZE+config.BORDER_SIZE) + self.window_height//2 - config.FIELD_SIZE//2,
                    type=int(field_data[row][col]),
                    batch=self.batch
                )
                field_row.append(cell)
            self.field.append(field_row)

    def clear_field(self):
        for row in range(len(self.field)):
            for col in range(len(self.field[row])):
                self.field[row][col].set_type(0)
