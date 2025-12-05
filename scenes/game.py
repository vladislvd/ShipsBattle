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
        self.draw_player_field = objects.FieldDrawer(self.window_width,
                                                     self.window_height,
                                                     self.batch,
                                                     self.player_field.field,
                                                     x_loc=(window_width//2 - config.FIELD_SIZE) - 100
                                                     )
        self.draw_AI_field = objects.FieldDrawer(self.window_width,
                                                 self.window_height,
                                                 self.batch,
                                                 self.player_field.field,
                                                 x_loc=window_width//2 + 100
                                                 )

    def draw(self):
        glClearColor(0.12, 0.20, 0.22, 1.0)
        # glClearColor(0.53, 0.81, 0.92, 1.0)
        # glClearColor(0.05, 0.16, 0.29, 1.0)
        # glClearColor(0, 0.18, 0.33, 1.0)
        self.batch.draw()

    def on_key_press(self):
        if self.application.keys[pyglet.window.key._1]:
            self.application.switch_scene('menu')

    def update(self, dt):
        self.on_key_press()
