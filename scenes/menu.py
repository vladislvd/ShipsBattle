import pyglet
import objects
import widgets
from pyglet.gl import glClearColor


class MenuScene:
    def __init__(self, window_width, window_height, application):
        self.application = application
        self.batch = pyglet.graphics.Batch()
        self.start_button = widgets.Button(
            x=window_width//2 - 100,
            y=window_height//2 + 10,
            width=200,
            height=50,
            text="Start",
            color=(0, 255, 0),
            batch=self.batch,
        )
        self.close_button = widgets.Button(
            x=window_width // 2 - 100,
            y=window_height // 2 - 100,
            width=200,
            height=50,
            color=(255, 0, 0),
            text="Close",
            batch=self.batch,
        )
        self.keys = pyglet.window.key.KeyStateHandler()
        self.application.push_handlers(self.keys)

    def draw(self):
        glClearColor(0, 0, 0, 1.0)
        self.batch.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.start_button.on_click(x, y):
            self.application.switch_scene('game')
        if self.close_button.on_click(x, y):
            self.application.close()

    def on_key_press(self):
        if self.keys[pyglet.window.key._1]:
            self.application.switch_scene('game')

    def update(self, dt):
        self.on_key_press()
