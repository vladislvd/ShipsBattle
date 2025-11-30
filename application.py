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
            'menu': scenes.MenuScene(self.width, self.height, self),
            'game': scenes.GameScene(self.width, self.height, self)
        }
        self.current_scene = 'menu'

    def on_draw(self):
        self.clear()
        self.scenes[self.current_scene].draw()

    def switch_scene(self, next_scene):
        self.current_scene = next_scene

    def on_mouse_press(self, x, y,  button, modifiers):
        self.scenes[self.current_scene].on_mouse_press(x, y, button, modifiers)

    def update(self, dt):
        self.scenes[self.current_scene].update(dt)
