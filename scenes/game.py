import pyglet


class GameScene:
    def __init__(self, window_width, window_height, application):
        self.application = application
        self.batch = pyglet.graphics.Batch()


    def draw(self):
        pass

    def on_key_press(self):
        if self.application.keys[pyglet.window.key._1]:
            self.application.switch_scene('menu')

    def update(self, dt):
        self.on_key_press()
