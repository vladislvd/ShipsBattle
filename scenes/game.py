import re
import pyglet
import pyglet.clock
from pyglet.gl.lib import errcheck
from pyglet.graphics import Batch
from pyglet.graphics.shader import _introspect_attributes
import application
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
        self.time_ai_sleep = 0.8
        self.ai_win = False
        self.pl_win = False
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
                                                 x_loc=window_width//2 + 135
                                                 )
        self.draw_double_AI_field = objects.FieldDrawer(window_width=self.window_width,
                                                        window_height=self.window_height,
                                                        batch=self.batch,
                                                        field_data=self.AI_field.field,
                                                        x_loc=window_width // 2 + 135
                                                        )
        self.init_components_for_game()
        self.move_arrow = objects.Arrow(x=self.draw_AI_field.field[9][5].x - config.ANCHOR - config.BORDER_SIZE//2,
                                       y=self.draw_AI_field.field[9][0].y + config.CELL_SIZE + 10,
                                       batch=self.batch)
        self.clear_pl_field_button = widgets.Border_Button(x=self.draw_player_field.field[9][8].x + config.ANCHOR + config.BORDER_SIZE,
                                                           y=self.draw_player_field.field[9][0].y + config.CELL_SIZE + 10,
                                                           width=config.CELL_SIZE*2,
                                                           height=35,
                                                           border=3,
                                                           border_color=(255, 255, 255),
                                                           color=(31, 51, 56),
                                                           text="Clear",
                                                           batch=self.batch
                                                           )
        self.end_text = pyglet.text.Label(
            text='PLAYER WIN',
            color=config.END_TEXT,
            x=window_width//2,
            y=window_height - window_height//15,
            font_size=60,
            font_name="Agency FB",
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )
        self.end_text.visible = False
        self.start_button = widgets.Button(
            x=window_width//2,
            y=window_height//4 - 50,
            width=200,
            height=50,
            text="Start",
            color=config.START_BUTTON,
            batch=self.batch,
        )
        self.back_button = widgets.Button(
            x=window_width//2 - 150,
            y=window_height//4 - 50,
            width=200,
            height=50,
            color=config.CLOSE_BUTTON,
            text="Back to menu",
            batch=self.batch,
        )
        self.back_button.visible = False
        self.back_button.label.visible = False
        self.reset_button = widgets.Button(
            x=window_width//2 + 150,
            y=window_height//4 - 50,
            width=200,
            height=50,
            color=config.START_BUTTON,
            text="Reset",
            batch=self.batch,
        )
        self.reset_button.visible = False
        self.reset_button.label.visible = False
    
    def init_player_ships(self):
        self.player_ships = objects.ShipsDrawer(
            batch=self.batch,
            start_x=self.draw_player_field.field[0][0].x,
            start_y=self.draw_player_field.field[0][0].y - (config.CELL_SIZE + config.BORDER_SIZE*4),
            max_long=4
        )
        self.player_ships.check_rotate()

    def init_components_for_game(self):
        self.init_player_ships()
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
        fl = False
        for ship in ships:
            for deck in ship:
                if not deck.on_field:
                    deck.set_type(4)
                    fl = True
        if fl:
            return False
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
        if self.start_button.visible == True and self.start_button.mouse_on(x, y):
            self.start_button.target_scale = 0.85
        if self.back_button.visible == True and self.back_button.mouse_on(x, y):
            self.back_button.target_scale = 0.85
        if self.reset_button.visible == True and self.reset_button.mouse_on(x, y):
            self.reset_button.target_scale = 0.85
        if self.clear_pl_field_button.visible == True and self.clear_pl_field_button.mouse_on(x, y):
            self.clear_pl_field_button.target_scale = 0.85
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
                if rotate == 'x':
                    right_side = x + len(self.dragged_object) * config.CELL_SIZE + config.BORDER_SIZE * (len(self.dragged_object) - 0.5)
                    but_check = right_side < self.start_button.x or x > self.start_button.x + self.start_button.width or \
                        y + config.CELL_SIZE < self.start_button.y or y > self.start_button.y + self.start_button.height
                    window_check = right_side < config.WINDOW_WIDTH and x > 0 and y + config.CELL_SIZE < config.WINDOW_HEIGHT and y > 0
                else:
                    up_side = y + len(self.dragged_object) * config.CELL_SIZE + config.BORDER_SIZE * (len(self.dragged_object) - 0.5)
                    but_check = x + config.CELL_SIZE < self.start_button.x or x > self.start_button.x + self.start_button.width or \
                        up_side < self.start_button.y or y > self.start_button.y + self.start_button.height
                    window_check = x + config.CELL_SIZE < config.WINDOW_WIDTH and x > 0 and up_side < config.WINDOW_HEIGHT and y > 0
                if but_check and window_check:
                    deck.x = (i if rotate == 'x' else x)
                    deck.y = (i if rotate == 'y' else y)
                    i += (config.CELL_SIZE + config.BORDER_SIZE)

    def on_mouse_release(self, x, y, button):
        if self.start_button.visible == True and self.start_button.mouse_on(x, y):
            self.start_button.target_scale = 1.0
            if not self.confirm_player_ships():
                return False
            self.start_button.label.visible = False
            self.start_button.visible = False
            self.is_game = True
            self.is_placing = False
        if self.back_button.visible == True and self.back_button.mouse_on(x, y):
            self.back_button.target_scale = 1.0
            self.application.switch_scene('menu')
        if self.reset_button.visible == True and self.reset_button.mouse_on(x, y):
            self.reset_button.target_scale = 1.0
            self.reset()
        if self.clear_pl_field_button.visible == True and self.clear_pl_field_button.mouse_on(x, y):
            self.clear_pl_field_button.target_scale = 1.0
            self.player_ships.delete_ships()
            self.init_player_ships()
            self.draw_player_field.clear_field()
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
                        deck.on_field = (False if cx >= 10 or cy >= 10 else True)
                        deck.error = True
                        deck.set_type(4)
                    self.dragged_object = None
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
            self.draw_double_AI_field.field[y_on_field][x_on_field].visible = False
            if cell.type == 2 or cell.type == 3:
                return False
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
                self.move_arrow.update_x(self.draw_player_field.field[9][5].x - config.ANCHOR - config.BORDER_SIZE//2)
            self.is_pl_win()
            pyglet.clock.schedule_once(self.process_logic, self.time_ai_sleep)

    def mouse_to_field(self, x, y, field_drawer):
        start_x = field_drawer.field[0][0].x - config.ANCHOR
        start_y = field_drawer.field[0][0].y - config.ANCHOR
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
            self.end_text.visible = True
            self.pl_win = True
            self.end()

    def is_ai_win(self):
        pl_killed_ships = 0
        for ship in range(len(self.player_ships.ships)):
            if self.AI_ships.is_kill(self.player_ships.ships[ship], "bool"):
                pl_killed_ships += 1
        if pl_killed_ships == len(self.player_ships.ships):
            self.end_text.text = "AI WIN"
            self.end_text.visible = True
            self.ai_win = True
            self.end()

    def reset(self):
        self.turn = 'Player'
        self.dragged_object = None
        self.is_game = False
        self.is_placing = True
        self.ai_win = False
        self.pl_win = False
        self.start_button.visible = True
        self.start_button.label.visible = True
        self.reset_button.visible = False
        self.reset_button.label.visible = False
        self.back_button.visible = False
        self.back_button.label.visible = False
        self.end_text.visible = False
        self.draw_player_field.clear_field()
        self.draw_AI_field.clear_field()
        self.move_arrow.update_x(self.draw_AI_field.field[9][5].x - config.ANCHOR - config.BORDER_SIZE//2)
        for row in self.draw_double_AI_field.field:
            for cell in row:
                cell.visible = True
        self.init_components_for_game()

    def end(self):
        self.is_game = False
        self.reset_button.visible = True
        self.reset_button.label.visible = True
        self.back_button.visible = True
        self.back_button.label.visible = True
        if self.ai_win:
            for row in self.draw_double_AI_field.field:
                for cell in row:
                    cell.visible = False

    def process_logic(self, dt):
        if self.is_game and self.turn == 'AI':
            if self.AI_game.take_move(field=self.draw_player_field.field,
                                      ships=self.player_ships.ships,
                                      ):
                self.turn = 'AI'
                pyglet.clock.schedule_once(self.process_logic, self.time_ai_sleep)
            else:
                self.turn = 'Player'
                self.move_arrow.update_x(self.draw_AI_field.field[9][5].x - config.ANCHOR - config.BORDER_SIZE//2)
            self.is_ai_win()

    def update(self, dt):
        for row in self.draw_double_AI_field.field:
            for cell in row:
                cell.update_animation(dt)
        for row in self.draw_AI_field.field:
            for cell in row:
                cell.update_animation(dt)
        for ship in self.player_ships.ships:
            for deck in ship:
                deck.update_animation(dt)
        if self.start_button.visible == True:
            self.start_button.update_animation(dt)
        if self.reset_button.visible == True:
            self.reset_button.update_animation(dt)
        if self.back_button.visible == True:
            self.back_button.update_animation(dt)
        if self.clear_pl_field_button.visible == True:
            self.clear_pl_field_button.update_animation(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        for row in self.draw_double_AI_field.field:
            for cell in row:
                if cell.mouse_on(x, y):
                    cell.target_scale = 1.15
                else:
                    cell.target_scale = 1.0
        for row in self.draw_AI_field.field:
            for cell in row:
                if cell.mouse_on(x, y):
                    cell.target_scale = 1.15
                else:
                    cell.target_scale = 1.0
        for ship in self.player_ships.ships:
            check = any(deck.mouse_on(x, y) for deck in ship)
            if check:
                for d in ship:
                    d.target_scale = 1.02
            else:
                for d in ship:
                    d.target_scale = 1.0
        if self.start_button.visible == True:
            if self.start_button.mouse_on(x, y):
                self.start_button.target_scale = 1.05
            else:
                self.start_button.target_scale = 1.0
        if self.reset_button.visible == True:
            if self.reset_button.mouse_on(x, y):
                self.reset_button.target_scale = 1.05
            else:
                self.reset_button.target_scale = 1.0
        if self.back_button.visible == True:
            if self.back_button.mouse_on(x, y):
                self.back_button.target_scale = 1.05
            else:
                self.back_button.target_scale = 1.0
        if self.clear_pl_field_button.visible == True:
            if self.clear_pl_field_button.mouse_on(x, y):
                self.clear_pl_field_button.target_scale = 1.05
            else:
                self.clear_pl_field_button.target_scale = 1.0
