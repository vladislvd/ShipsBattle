import pyglet


class Border_Button(pyglet.shapes.BorderedRectangle):
    def __init__(self, x, y, width, height, border, color, border_color, text, batch):
        super().__init__(x=x, y=y, width=width, height=height, border=border, color=color, border_color=border_color, batch=batch)
        self.anchor_x = width // 2
        self.anchor_y = height // 2
        self.scale = 1.0
        self.target_scale = 1.0
        self.base_width = width
        self.base_height = height
        self.label = pyglet.text.Label(
            text=text,
            x=x,
            y=y,
            anchor_x="center",
            anchor_y="center",
            font_name="Agency FB",
            color=(255, 255, 255),
            batch=batch,
            font_size=20,
        )

    def mouse_on(self, x, y):
        left_side = self.x - self.anchor_x
        bottom_side = self.y - self.anchor_y
        return left_side <= x <= left_side + self.width and bottom_side <= y <= bottom_side + self.height

    def update_animation(self, dt):
        speed = 0.8
        self.scale += (self.target_scale - self.scale) * speed
        self.width = self.base_width * self.scale
        self.height = self.base_height * self.scale
        self.anchor_x = self.width // 2
        self.anchor_y = self.height // 2

