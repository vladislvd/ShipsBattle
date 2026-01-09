import pyglet.shapes
import config


class Cross:
    def __init__(self, x, y, width, height, anchor_x, anchor_y, batch):
        self.batch = batch
        self.line1 = pyglet.shapes.Line(
            x=x - anchor_x + 5,
            x2=x + anchor_x - 5,
            y=y - anchor_y + 5,
            y2=y + anchor_y - 5,
            thickness=3,
            color=config.RED_DOT,
            batch=batch
        )
        self.line2 = pyglet.shapes.Line(
            x=x + anchor_x - 5,
            x2=x - anchor_x + 5,
            y=y - anchor_y + 5,
            y2=y + anchor_y - 5,
            thickness=3,
            color=config.RED_DOT,
            batch=batch
        )
