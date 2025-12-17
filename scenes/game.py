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
        self.turn = 'Player'
        self.dragged_object = None
        self.is_game = True
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
        self.player_ships = objects.ShipsDrawer(
            batch=self.batch,
            start_x=self.draw_player_field.field[0][0].x,
            start_y=self.draw_player_field.field[0][0].y - (config.CELL_SIZE + config.BORDER_SIZE*4),
            max_long=4
        )
        self.AI_ships = objects.ShipsDrawer(
            batch=self.batch,
            start_x=self.draw_AI_field.field[0][0].x,
            start_y=self.draw_AI_field.field[0][0].y - (config.CELL_SIZE + config.BORDER_SIZE * 4),
            max_long=4
        )
        self.AI_ships_on_field = logic.PuttingAIShips(
            field=self.draw_AI_field.field,
            ships=self.AI_ships.ships,
            filedDrawer=self.draw_AI_field
        )

    def draw(self):
        glClearColor(0.12, 0.20, 0.22, 1.0)
        self.batch.draw()

    def on_mouse_press(self, x, y, button):
        try:
            if x < self.window_width//2 and self.is_game:
                self.mouse_press_pl(x, y)
            elif x > self.window_width//2 and self.is_game:
                self.mouse_press_ai(x, y)
        except:
            pass
        if button == pyglet.window.mouse.LEFT and not self.is_game:
            ship = self.player_ships.ships[0][0]
            if ship.mouse_on(x, y) and ship.enable:
                ship.is_dragging = True
                ship.offset_x = x - ship.x
                ship.offset_y = y - ship.y
                self.dragged_object = ship

    def on_mouse_drag(self, x, y, buttons):
        if buttons == pyglet.window.mouse.LEFT and self.dragged_object is not None and not self.is_game:
            self.dragged_object.x = x - self.dragged_object.offset_x
            self.dragged_object.y = y - self.dragged_object.offset_y

    def on_mouse_release(self, x, y, button):
        if button == pyglet.window.mouse.LEFT and self.dragged_object is not None and not self.is_game:
            self.dragged_object.is_dragged = False
            y_cells_to_field = int(self.draw_player_field.field[0][0].y // config.CELL_SIZE)
            x_cells_to_field = int(self.draw_player_field.field[0][0].x // config.CELL_SIZE)
            x_on_field = int(x // (config.CELL_SIZE + config.BORDER_SIZE)) - x_cells_to_field
            y_on_field = int(y // (config.CELL_SIZE + config.BORDER_SIZE)) - y_cells_to_field
            if self.draw_player_field.field[y_on_field][x_on_field].mouse_on(x, y):
                self.draw_player_field.field[y_on_field][x_on_field].set_ship(x_on_field,
                                                                              y_on_field,
                                                                              self.draw_player_field.field)
                self.dragged_object.enable = False
                self.dragged_object.visible = False
            self.dragged_object = None


    def mouse_press_pl(self, x, y):
        y_cells_to_field = int(self.draw_player_field.field[0][0].y//config.CELL_SIZE)
        x_cells_to_field = int(self.draw_player_field.field[0][0].x // config.CELL_SIZE)
        x_on_field = int(x // (config.CELL_SIZE + config.BORDER_SIZE)) - x_cells_to_field
        y_on_field = int(y // (config.CELL_SIZE + config.BORDER_SIZE)) - y_cells_to_field
        if self.draw_player_field.field[y_on_field][x_on_field].mouse_on(x, y):
            self.draw_player_field.field[y_on_field][x_on_field].on_mouse_click(x_on_field,
                                                                                y_on_field,
                                                                                self.draw_player_field.field)

    def mouse_press_ai(self, x, y):
        y_cells_to_field = int(self.draw_AI_field.field[0][0].y // config.CELL_SIZE)
        x_cells_to_field = int(self.draw_AI_field.field[0][0].x // config.CELL_SIZE) - 2
        x_on_field = int(x // (config.CELL_SIZE + config.BORDER_SIZE)) - x_cells_to_field
        y_on_field = int(y // (config.CELL_SIZE + config.BORDER_SIZE)) - y_cells_to_field
        if self.draw_AI_field.field[y_on_field][x_on_field].mouse_on(x, y):
            self.draw_AI_field.field[y_on_field][x_on_field].on_mouse_click(x_on_field,
                                                                            y_on_field,
                                                                            self.draw_AI_field.field)

    def on_key_press(self):
        if self.application.keys[pyglet.window.key._1]:
            self.application.switch_scene('menu')

    def process_logic(self):
        pass

    def update(self, dt):
        self.on_key_press()
