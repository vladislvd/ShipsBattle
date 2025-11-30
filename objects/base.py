import pyglet


class BaseObject(pyglet.shapes.Rectangle):
    def __init__(self, x, y, width, height, color, batch):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            color=color,
            batch=batch
        )
