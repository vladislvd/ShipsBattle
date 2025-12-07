import pyglet
import config
import logic
import objects
from pyglet.gl import glClearColor


class GameScene:
    def __init__(self, window_width, window_height, application):
        self.application = application
        self.window_width = window_width
        self.window_height = window_height
        self.batch = pyglet.graphics.Batch()
        self.player_field = logic.PlayerField()
        self.AI_field = logic.AIField()
        self.draw_player_field = objects.FieldDrawer(window_width=self.window_width,
                                                     window_height=self.window_height,
                                                     batch=self.batch,
                                                     field_data=self.player_field.field,
                                                     x_loc=(window_width//2 - config.FIELD_SIZE) - 100,
                                                     )
        self.draw_AI_field = objects.FieldDrawer(window_width=self.window_width,
                                                 window_height=self.window_height,
                                                 batch=self.batch,
                                                 field_data=self.AI_field.field,
                                                 x_loc=window_width//2 + 100
                                                 )

    def draw(self):
        glClearColor(0.12, 0.20, 0.22, 1.0)
        self.batch.draw()

    def on_mouse_press(self, x, y):
        try:
            if x < self.window_width//2:
                self.mouse_press_pl(x, y)
            elif x > self.window_width//2:
                self.mouse_press_ai(x, y)
        except:
            pass

    def mouse_press_pl(self, x, y):
        x_on_field = int(x // (config.CELL_SIZE + config.BORDER_SIZE)) - 3
        y_on_field = int(y // (config.CELL_SIZE + config.BORDER_SIZE)) - 5
        if self.draw_player_field.field[y_on_field][x_on_field].on_click(x, y):
            self.draw_player_field.field[y_on_field][x_on_field].on_mouse_click(x_on_field,
                                                                                y_on_field,
                                                                                self.draw_player_field.field)

    def mouse_press_ai(self, x, y):
        x_on_field = int(x // (config.CELL_SIZE + config.BORDER_SIZE)) - 18
        y_on_field = int(y // (config.CELL_SIZE + config.BORDER_SIZE)) - 5
        if self.draw_AI_field.field[y_on_field][x_on_field].on_click(x, y):
            self.draw_AI_field.field[y_on_field][x_on_field].on_mouse_click(x_on_field,
                                                                            y_on_field,
                                                                            self.draw_AI_field.field)

    def on_key_press(self):
        if self.application.keys[pyglet.window.key._1]:
            self.application.switch_scene('menu')

    def update(self, dt):
        self.on_key_press()
