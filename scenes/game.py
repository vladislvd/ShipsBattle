import pyglet
import pyglet.clock
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
        self.time_ai_sleep = 0.5
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
        self.draw_double_AI_field = objects.FieldDrawer(window_width=self.window_width,
                                                        window_height=self.window_height,
                                                        batch=self.batch,
                                                        field_data=self.AI_field.field,
                                                        x_loc=window_width // 2 + 100
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
        self.AI_game = logic.AIgame(ships=self.player_ships.ships,
                                    shipsDrawer=self.player_ships
                                    )

        """
        ДЛЯ ТЕСТОВ. УДАЛИТЬ!!
        """
        self.player_ships_on_field = logic.PuttingAIShips(
            field=self.draw_player_field.field,
            ships=self.player_ships.ships,
            filedDrawer=self.draw_player_field
        )
        self.end_text = pyglet.text.Label(
            text='',
            color=(255, 0, 0),
            x=window_width//2,
            y=window_height//4,
            font_size=100,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )
        """
        ДЛЯ ТЕСТОВ. УДАЛИТЬ!!
        """

    def draw(self):
        glClearColor(0.12, 0.20, 0.22, 1.0)
        self.batch.draw()

    def on_mouse_press(self, x, y, button):
        try:
            if x > self.window_width//2 and self.is_game:
                self.mouse_press_ai(x, y)
        except:
            pass
        if button == pyglet.window.mouse.LEFT:
            ship = self.player_ships.ships[0][0]
            if ship.mouse_on(x, y) and ship.enable:
                ship.is_dragging = True
                ship.offset_x = x - ship.x
                ship.offset_y = y - ship.y
                self.dragged_object = ship

    def on_mouse_drag(self, x, y, buttons):
        if buttons == pyglet.window.mouse.LEFT and self.dragged_object is not None:
            self.dragged_object.x = x - self.dragged_object.offset_x
            self.dragged_object.y = y - self.dragged_object.offset_y

    def on_mouse_release(self, x, y, button):
        if button == pyglet.window.mouse.LEFT and self.dragged_object is not None:
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

    def mouse_press_ai(self, x, y):
        if self.is_game and self.turn == 'Player':
            y_cells_to_field = int(self.draw_AI_field.field[0][0].y // config.CELL_SIZE)
            x_cells_to_field = int(self.draw_AI_field.field[0][0].x // config.CELL_SIZE) - 2
            x_on_field = int(x // (config.CELL_SIZE + config.BORDER_SIZE)) - x_cells_to_field
            y_on_field = int(y // (config.CELL_SIZE + config.BORDER_SIZE)) - y_cells_to_field
            if self.draw_AI_field.field[y_on_field][x_on_field].mouse_on(x, y) and \
                    self.draw_AI_field.field[y_on_field][x_on_field].type != 2:
                self.draw_double_AI_field.field[y_on_field][x_on_field].delete()
                if self.draw_AI_field.field[y_on_field][x_on_field].type == 1:
                    self.draw_AI_field.field[y_on_field][x_on_field].on_mouse_click(x_on_field,
                                                                                    y_on_field,
                                                                                    self.draw_AI_field.field)
                    ship_in_ai_ships = 0
                    for ship in range(len(self.AI_ships.ships)):
                        for deck in range(len(self.AI_ships.ships[ship])):
                            if self.AI_ships.ships[ship][deck] == self.draw_AI_field.field[y_on_field][x_on_field]:
                                ship_in_ai_ships = ship
                    if self.AI_ships.is_kill(self.AI_ships.ships[ship_in_ai_ships], "bool"):
                        self.AI_ships.tick_cells_around_ship(ship=self.AI_ships.ships[ship_in_ai_ships],
                                                             field=self.draw_AI_field.field,
                                                             double_field=self.draw_double_AI_field.field)
                else:
                    self.draw_AI_field.field[y_on_field][x_on_field].on_mouse_click(x_on_field,
                                                                                    y_on_field,
                                                                                    self.draw_AI_field.field)
                    self.turn = 'AI'
                self.is_pl_win()
                pyglet.clock.schedule_once(self.process_logic, self.time_ai_sleep)


    def on_key_press(self):
        if self.application.keys[pyglet.window.key._1]:
            self.application.switch_scene('menu')

    def is_pl_win(self):
        ai_killed_ships = 0
        for ship in range(len(self.AI_ships.ships)):
            if self.AI_ships.is_kill(self.AI_ships.ships[ship], "bool"):
                ai_killed_ships += 1
        if ai_killed_ships == len(self.AI_ships.ships):
            self.end_text.text = "PLAYER WIN"
            self.end()

    def is_ai_win(self):
        pl_killed_ships = 0
        for ship in range(len(self.player_ships.ships)):
            if self.AI_ships.is_kill(self.player_ships.ships[ship], "bool"):
                pl_killed_ships += 1
        if pl_killed_ships == len(self.player_ships.ships):
            self.end_text.text = "AI WIN"
            self.end()

    def end(self):
        self.is_game = False

    def process_logic(self, dt):
        if self.is_game and self.turn == 'AI':
            if self.AI_game.take_move(field=self.draw_player_field.field,
                                      ships=self.player_ships.ships,
                                      ):
                self.turn = 'AI'
                pyglet.clock.schedule_once(self.process_logic, self.time_ai_sleep)
            else:
                self.turn = 'Player'
            self.is_ai_win()

    def update(self, dt):
        self.on_key_press()
