import pyglet
import pyglet.clock
import config
import logic
import objects
import widgets
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
        self.time_ai_sleep = 0
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
                                                        batch=None,
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
            filedDrawer=self.draw_AI_field,
            shipsDrawer=self.AI_ships
        )
        self.AI_game = logic.AIgame(ships=self.player_ships.ships,
                                    shipsDrawer=self.player_ships
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
        self.start_button = widgets.Button(
            x=window_width//2 - 100,
            y=window_height//4 - 25,
            width=200,
            height=50,
            text="Start",
            color=(0, 255, 0),
            batch=self.batch,
        )
        # self.player_ships_on_field = logic.PuttingAIShips(
        #     field=self.draw_player_field.field,
        #     ships=self.player_ships.ships,
        #     filedDrawer=self.draw_player_field
        # )
        
        

    def draw(self):
        glClearColor(0.12, 0.20, 0.22, 1.0)
        self.batch.draw()

    # def place_player_ships(self, ship, x_on_field, y_on_field, rotate):
    #     size = len(self.draw_player_field.field)
    #     if not self.player_ships.check_around(len(ship), x_on_field, y_on_field, rotate, size, self.draw_player_field.field):
    #         return False
    #     for i, cell in enumerate(ship):
    #         cx = x_on_field + (i if rotate == 'x' else 0)
    #         cy = y_on_field + (i if rotate == 'y' else 0)
    #         field_cell = self.draw_player_field.field[cy][cx]
    #         cell.x = field_cell.x
    #         cell.y = field_cell.y
    #         cell.x_on_field = cx
    #         cell.y_on_field = cy
    #         cell.type = 1
    #         self.draw_player_field.field[cy][cx] = cell

    # def confirm_player_ships(self):
    #     for ship in self.player_ships.ships:
    #         self.place_player_ships(ship, ship[0].x_on_field, ship[0].y_on_field, ship[0].rotate)

    def on_mouse_press(self, x, y, button):
        if self.start_button.on_click(x, y):
            self.confirm_player_ships()
            self.start_button.label.delete()
            self.start_button.delete()
        try:
            if x > self.window_width//2 and self.is_game:
                self.mouse_press_ai(x, y)
        except:
            pass
        if button == pyglet.window.mouse.LEFT:
            for ship in self.player_ships.ships:
                dragged = False
                for deck in ship:
                    if deck.mouse_on(x, y):
                        dragged = True
                        deck.offset_x = x - deck.x
                        deck.offset_y = y - deck.y
                if dragged:
                    self.dragged_object = ship

    def on_mouse_drag(self, x, y, buttons):
        if self.dragged_object is not None:
            i = x
            for deck in self.dragged_object:
                deck.x = i
                deck.y = y
                i += (config.CELL_SIZE + config.BORDER_SIZE)

    def on_mouse_release(self, x, y, button):
        if self.dragged_object is not None:
            pos = self.mouse_to_field(x, y, self.draw_player_field)
            if not pos:
                return False
            x_on_field, y_on_field = pos
            field_start_x = self.draw_player_field.field[0][0].x
            field_start_y = self.draw_player_field.field[0][0].y
            i = 0
            for deck in self.dragged_object:
                deck.x = field_start_x + x_on_field * (config.CELL_SIZE + config.BORDER_SIZE) + i * (config.CELL_SIZE + config.BORDER_SIZE)
                deck.y = field_start_y + y_on_field * (config.CELL_SIZE + config.BORDER_SIZE)
                i += 1
            self.dragged_object = None

    def mouse_press_ai(self, x, y):
        if self.is_game and self.turn == 'Player':
            pos = self.mouse_to_field(x, y, self.draw_AI_field)
            if not pos:
                return False
            x_on_field, y_on_field = pos
            cell = self.draw_AI_field.field[y_on_field][x_on_field]
            if cell.type == 2 or cell.type == 3:
                return False
            self.draw_double_AI_field.field[y_on_field][x_on_field].delete()
            cell.on_mouse_click(x_on_field, y_on_field, self.draw_AI_field.field)
            if cell.type == 3:
                ship_in_ai_ships = None
                for i, ship in enumerate(self.AI_ships.ships):
                    if cell in ship:
                        ship_in_ai_ships = i
                        break
                if ship_in_ai_ships is not None and self.AI_ships.is_kill(self.AI_ships.ships[ship_in_ai_ships], "bool"):
                        self.AI_ships.tick_cells_around_ship(
                            ship=self.AI_ships.ships[ship_in_ai_ships],
                            field=self.draw_AI_field.field,
                            double_field=self.draw_double_AI_field.field
                        )
            else:
                self.turn = 'AI'
            self.is_pl_win()
            pyglet.clock.schedule_once(self.process_logic, self.time_ai_sleep)

    def mouse_to_field(self, x, y, field_drawer):
        start_x = field_drawer.field[0][0].x
        start_y = field_drawer.field[0][0].y
        step = config.CELL_SIZE + config.BORDER_SIZE
        cx = int((x - start_x) // step)
        cy = int((y - start_y) // step)
        if (0 <= cx < len(field_drawer.field[0])) and (0 <= cy < len(field_drawer.field)):
            return cx, cy
        return None

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
            self.AI_game.get_probability_map(self.draw_player_field.field)
            if self.AI_game.take_move(field=self.draw_player_field.field,
                                      ships=self.player_ships.ships,
                                      ):
                self.turn = 'AI'
                pyglet.clock.schedule_once(self.process_logic, self.time_ai_sleep)
            else:
                pyglet.clock.schedule_once(self.process_logic, self.time_ai_sleep)
                self.turn = 'Player'
            self.is_ai_win()

    def update(self, dt):
        self.on_key_press()
