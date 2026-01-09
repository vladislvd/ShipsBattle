from pyglet.shapes import Line
import config


class Arrow:
    def __init__(self, x, y, batch):
        self.line1 = Line(x=x - config.CELL_SIZE//2,
                          y=y + config.CELL_SIZE,
                          x2=x+1,
                          y2=y,
                          color=config.END_TEXT,
                          thickness=5,
                          batch=batch
                          )
        self.line2 = Line(x=x + config.CELL_SIZE//2,
                          y=y + config.CELL_SIZE,
                          x2=x-1,
                          y2=y,
                          color=config.END_TEXT,
                          thickness=5,
                          batch=batch
                          )

    def update_x(self, x):
        self.line1.x = x - config.CELL_SIZE//2
        self.line1.x2 = x+1
        self.line2.x = x + config.CELL_SIZE//2
        self.line2.x2 = x - 1