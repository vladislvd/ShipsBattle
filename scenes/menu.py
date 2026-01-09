import pyglet
import config
import widgets
from pyglet.gl import glClearColor


class MenuScene:
    def __init__(self, window_width, window_height, application):
        self.application = application
        self.batch = pyglet.graphics.Batch()
        self.start_button = widgets.Button(
            x=window_width//2,
            y=window_height//2 + 50,
            width=200,
            height=50,
            text="Start",
            color=config.START_BUTTON,
            batch=self.batch,
        )
        self.close_button = widgets.Button(
            x=window_width // 2,
            y=self.start_button.y - 100,
            width=200,
            height=50,
            color=config.CLOSE_BUTTON,
            text="Close",
            batch=self.batch,
        )
        self.keys = pyglet.window.key.KeyStateHandler()
        self.application.push_handlers(self.keys)

    def draw(self):
        glClearColor(0.12, 0.20, 0.22, 1.0)
        self.batch.draw()

    def on_mouse_press(self, x, y, button):
        if self.start_button.mouse_on(x, y):
            self.start_button.target_scale = 0.85
        if self.close_button.mouse_on(x, y):
            self.close_button.target_scale = 0.85

    def on_mouse_drag(self, x, y, buttons):
        pass

    def on_mouse_release(self, x, y, button):
        if self.start_button.mouse_on(x, y):
            self.start_button.target_scale = 1.0
            self.application.switch_scene('game')
        if self.close_button.mouse_on(x, y):
            self.close_button.target_scale = 1.0
            self.application.close()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key._2:
            self.application.switch_scene('game')

    def on_mouse_motion(self, x, y, dx, dy):
        if self.start_button.mouse_on(x, y):
            self.start_button.target_scale = 1.05
        else:
            self.start_button.target_scale = 1.0
        if self.close_button.mouse_on(x, y):
            self.close_button.target_scale = 1.05
        else:
            self.close_button.target_scale = 1.0


    def update(self, dt):
        self.start_button.update_animation(dt)
        self.close_button.update_animation(dt)