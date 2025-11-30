import pyglet


class Button(pyglet.shapes.Rectangle):
    def __init__(self, x, y, width, height, color, text, batch):
        super().__init__(x=x, y=y, width=width, height=height, color=color, batch=batch)
        self.label = pyglet.text.Label(
            text=text,
            x=x + width // 2,
            y=y + height // 2,
            anchor_x="center",
            anchor_y="center",
            color=(0, 0, 0),
            batch=batch,
            font_size=20,
        )

    def on_click(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
