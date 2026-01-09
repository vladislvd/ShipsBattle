import re
import pyglet
import pyglet.clock
from pyglet.gl.lib import errcheck
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
        self.is_game = False
        self.is_placing = True
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
        self.player_ships.check_rotate()
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
        

    def draw(self):
        glClearColor(0.12, 0.20, 0.22, 1.0)
        self.batch.draw()

    def place_player_ships(self, ship, x_on_field, y_on_field, rotate, ship_index):
        size = len(self.draw_player_field.field)
        pl_ship = []
        for i, deck in enumerate(ship):
            cx = x_on_field + (i if rotate == 'x' else 0)
            cy = y_on_field + (i if rotate == 'y' else 0)
            field_cell = self.draw_player_field.field[cy][cx]
            field_cell.x_on_field = cx
            field_cell.y_on_field = cy
            field_cell.set_type(1)
            pl_ship.append(field_cell)
        self.player_ships.ships[ship_index] = pl_ship

    def confirm_player_ships(self):
        ships = self.player_ships.ships
        for ship_ind in range(len(ships)):
            fl = False
            ship = ships[ship_ind]
            pos = self.mouse_to_field(ship[0].x, ship[0].y, self.draw_player_field)
            if not pos:
                for ship in ships:
                    for deck in ship:
                        if deck.error == True:
                            deck.set_type(4)
                            fl = True
            else:
                for ship in ships:
                    rotate = ship[0].rotate
                    x_on_field, y_on_field = self.mouse_to_field(ship[0].x, ship[0].y, self.draw_player_field)
                    if not self.player_ships.check_around(len(ship), x_on_field, y_on_field, rotate, 10, self.draw_player_field.field, True):
                        for deck in ship:
                            deck.set_type(4)
                            deck.error = True
                            deck.on_field = True
                            fl = True
                    else:
                        for deck in ship:
                            deck.set_type(1)
                            deck.error = False
                            deck.on_field = True
        if fl:
            return False
        for ship_ind in range(len(ships)):
            ship = ships[ship_ind]
            x_on_field, y_on_field = self.mouse_to_field(ship[0].x, ship[0].y, self.draw_player_field)
            self.place_player_ships(ship, x_on_field, y_on_field, ship[0].rotate, ship_ind)
        return True

    def on_mouse_press(self, x, y, button):
        if self.start_button.on_click(x, y):
            if not self.confirm_player_ships():
                return False
            self.start_button.label.delete()
            self.start_button.delete()
            self.is_game = True
            self.is_placing = False
        if x > self.window_width//2 and self.is_game:
                self.mouse_press_ai(x, y)
        if button == pyglet.window.mouse.LEFT and self.is_placing and self.dragged_object == None:
            ships = self.player_ships.ships
            for ship in ships:
                dragged = False
                for deck in ship:
                    if deck.mouse_on(x, y):
                        if deck.on_field:
                            for deck in ship:
                                x_on_field, y_on_field = self.mouse_to_field(deck.x, deck.y, self.draw_player_field)
                                self.draw_player_field.field[y_on_field][x_on_field].set_type(0)
                        dragged = True
                if dragged:
                    self.dragged_object = ship

    def on_mouse_drag(self, x, y, buttons):
        if self.dragged_object is not None and self.is_placing:
            rotate = self.dragged_object[0].rotate
            i = (x if rotate == 'x' else y)
            for deck in self.dragged_object:
                deck.error = False
                deck.set_type(1)
                right_side = x + len(self.dragged_object) * config.CELL_SIZE + config.BORDER_SIZE*2
                if right_side < self.start_button.x or x > self.start_button.x + self.start_button.width or \
                    y + config.CELL_SIZE < self.start_button.y or y > self.start_button.y + self.start_button.height:
                    deck.x = (i if rotate == 'x' else x)
                    deck.y = (i if rotate == 'y' else y)
                    i += (config.CELL_SIZE + config.BORDER_SIZE)

    def on_mouse_release(self, x, y, button):
        if self.dragged_object is not None:
            pos = self.mouse_to_field(x, y, self.draw_player_field)
            if not pos:
                for deck in self.dragged_object:
                    deck.error = True
                    deck.on_field = False
                self.dragged_object = None
                return False
            x_on_field, y_on_field = pos
            field_start_x = self.draw_player_field.field[0][0].x
            field_start_y = self.draw_player_field.field[0][0].y
            for i, deck in enumerate(self.dragged_object):
                rotate = deck.rotate
                cx = x_on_field + (i if rotate == 'x' else 0)
                cy = y_on_field + (i if rotate == 'y' else 0)
                if cx >= 10 or cy >= 10 or self.draw_player_field.field[cy][cx].type == 1:
                    for deck in self.dragged_object:
                        deck.error = True
                        deck.set_type(4)
                    return False
            for i, deck in enumerate(self.dragged_object):
                rotate = deck.rotate
                step = i * (config.CELL_SIZE + config.BORDER_SIZE)
                if rotate == 'x':
                    deck.x = field_start_x + (x_on_field * (config.CELL_SIZE + config.BORDER_SIZE)) + step
                    deck.y = field_start_y + (y_on_field * (config.CELL_SIZE + config.BORDER_SIZE))
                else:
                    deck.x = field_start_x + (x_on_field * (config.CELL_SIZE + config.BORDER_SIZE))
                    deck.y = field_start_y + (y_on_field * (config.CELL_SIZE + config.BORDER_SIZE)) + step
                cx = x_on_field + (i if rotate == 'x' else 0)
                cy = y_on_field + (i if rotate == 'y' else 0)
                self.draw_player_field.field[cy][cx].set_type(1)
                deck.error = False
                deck.on_field = True
                
            if not self.player_ships.check_around(len(self.dragged_object), x_on_field, y_on_field, deck.rotate, 10, self.draw_player_field.field, True):
                for deck in self.dragged_object:
                    deck.error = True
                    deck.set_type(4)

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

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key._1:
            self.application.switch_scene('menu')
        if symbol == pyglet.window.key.R and self.dragged_object is not None:
            new_rotate = ('y' if self.dragged_object[0].rotate == 'x' else 'x')
            x, y = self.application._mouse_x, self.application._mouse_y
            self.player_ships.change_rotate(self.dragged_object, new_rotate, x, y)

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
        pass
