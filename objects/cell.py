import pyglet.shapes
import config
import objects


class Cell(pyglet.shapes.Rectangle):
    def __init__(self, x, y, batch, type: int, width=config.CELL_SIZE, height=config.CELL_SIZE):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            batch=batch
        )
        self.anchor_x = width // 2
        self.anchor_y = height // 2
        self.scale = 1.0
        self.target_scale = 1.0
        self.base_width = width
        self.base_height = height
        self.type = type
        self.rotate = ''
        self.x_on_field = None
        self.y_on_field = None
        self.error = True
        self.on_field = False
        self.dot = pyglet.shapes.Circle(
            x=self.x,
            y=self.y,
            radius=5,
            batch=self.batch,
            color=config.RED_DOT
        )
        self.cross = objects.Cross(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            anchor_x=self.anchor_x,
            anchor_y=self.anchor_y,
            batch=self.batch
        )
        self.check_types()
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.enable = True
        # 0 - вода
        # 1 - корабль
        # 2 - мимо
        # 3 - попадание
        # 4 - error

    def check_types(self):
        if self.type == 0:
            self.color = config.AIR
            self.dot.visible = False
            self.cross.line1.visible = False
            self.cross.line2.visible = False
        if self.type == 1:
            self.color = config.SHIP
            self.dot.visible = False
            self.cross.line1.visible = False
            self.cross.line2.visible = False
        if self.type == 2:
            self.color = config.AIR
            self.dot.visible = True
            self.cross.line1.visible = False
            self.cross.line2.visible = False
        if self.type == 3:
            self.color = config.SHIP
            self.dot.visible = False
            self.cross.line1.visible = True
            self.cross.line2.visible = True
        if self.type == 4:
            self.color = config.RED_ERROR

    def set_ship(self, x_on_field, y_on_field, field):
        field[y_on_field][x_on_field].type = 1
        field[y_on_field][x_on_field].check_types()

    def mouse_on(self, x, y):
        left_side = self.x - self.anchor_x
        bottom_side = self.y - self.anchor_y
        return left_side <= x <= left_side + self.width and bottom_side <= y <= bottom_side + self.height

    def on_mouse_click(self, x_on_field, y_on_field, field):
        if field[y_on_field][x_on_field].type == 0:
            field[y_on_field][x_on_field].set_type(2)
        if field[y_on_field][x_on_field].type == 1:
            field[y_on_field][x_on_field].set_type(3)

    def set_type(self, type_on_set):
        self.type = type_on_set
        self.check_types()

    def update_animation(self, dt):
        if abs(self.scale - self.target_scale) < 0.001:
            return
        speed = 0.5
        self.scale += (self.target_scale - self.scale) * speed
        self.width = self.base_width * self.scale
        self.height = self.base_height * self.scale
        self.anchor_x = self.width // 2
        self.anchor_y = self.height // 2
