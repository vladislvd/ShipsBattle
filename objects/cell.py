import pyglet.shapes
import config


class Cell(pyglet.shapes.Rectangle):
    def __init__(self, x, y, batch, type: int, width=config.CELL_SIZE, height=config.CELL_SIZE):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            batch=batch
        )
        self.type = type
        self.check_types()

    def check_types(self):
        if self.type == 0:
            self.color = config.AIR
