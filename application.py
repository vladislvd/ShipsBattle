import pyglet
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from scenes.menu import MenuScene
from scenes.game import GameScene


class Application(pyglet.window.Window):
    def __init__(self):
        super().__init__(
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            caption="ShipsBattle"
        )
        pyglet.clock.schedule_interval(self.update, 1/60)
        self.scenes = {
            'menu': MenuScene,
            'game': GameScene
        }

    def update(self, dt):
        pass
