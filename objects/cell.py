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
        self.type = type
        self.dot = pyglet.shapes.Circle(
            x=self.x + self.width//2,
            y=self.y + self.height//2,
            radius=5,
            batch=self.batch,
            color=config.RED_DOT
        )
        self.cross = objects.Cross(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
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

    def set_ship(self, x_on_field, y_on_field, field):
        field[y_on_field][x_on_field].type = 1
        field[y_on_field][x_on_field].check_types()

    def mouse_on(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def on_mouse_click(self, x_on_field, y_on_field, field):
        if field[y_on_field][x_on_field].type == 0:
            field[y_on_field][x_on_field].type = 2
            field[y_on_field][x_on_field].check_types()
        if field[y_on_field][x_on_field].type == 1:
            field[y_on_field][x_on_field].type = 3
            field[y_on_field][x_on_field].check_types()
