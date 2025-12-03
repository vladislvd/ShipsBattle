import pyglet
import config
import scenes


class Application(pyglet.window.Window):
    def __init__(self):
        super().__init__(
            width=config.WINDOW_WIDTH,
            height=config.WINDOW_HEIGHT,
            caption="ShipsBattle"
        )
        pyglet.clock.schedule_interval(self.update, 1/60)
        self.scenes = {
            'menu': scenes.MenuScene,
            'game': scenes.GameScene
        }

    def update(self, dt):
        pass
