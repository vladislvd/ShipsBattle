import pyglet.shapes
import config


class Cross:
    def __init__(self, x, y, width, height, batch):
        self.batch = batch
        self.line1 = pyglet.shapes.Line(
            x=x + 5,
            x2=x+width - 5,
            y=y + 5,
            y2=y+height - 5,
            thickness=3,
            color=config.RED_DOT,
            batch=batch
        )
        self.line2 = pyglet.shapes.Line(
            x=x+width - 5,
            x2=x + 5,
            y=y + 5,
            y2=y+height - 5,
            thickness=3,
            color=config.RED_DOT,
            batch=batch
        )
