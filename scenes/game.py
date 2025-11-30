import pyglet


class GameScene:
    def __init__(self, window_width, window_height, application):
        self.application = application
        self.batch = pyglet.graphics.Batch()
        self.keys = pyglet.window.key.KeyStateHandler()
        self.application.push_handlers(self.keys)

    def draw(self):
        pass

    def on_key_press(self):
        if self.keys[pyglet.window.key.P]:
            self.application.switch_scene('menu')

    def update(self, dt):
        self.on_key_press()
