import curses 
import os
import json
from datetime import datetime
from Food import Food
from Wall import Wall
from Snake import Snake
from SaveManager import SaveManager


class Game:
    def __init__(self, stdscr, config, save_data=None, filename=None):
        self.stdscr = stdscr
        self.save_manager = SaveManager()
        self.filename = filename
        self.auto_save = config["auto_save"] if config else True

        if save_data:
            self.map_height = save_data["map"]["height"]
            self.map_width = save_data["map"]["width"]
        else:
            self.map_height = config["map"]["height"]
            self.map_width = config["map"]["width"]             

        self.height = self.map_height
        self.width = self.map_width
        
        self.score = 0

        # How many ticks are left until the time runs out.
        self.time_limit = 100

        self.ticks_since_food = 0

        self.snake = Snake(
            self.height // 2,
            self.width // 4
        )

        self.walls = Wall(
            self.height,
            self.width,
            15,
            self.snake.get_head()
        )

        self.food = Food(
            self.height // 2,
            self.width // 2
        )
        
        if save_data:
            self.score = save_data["score"]
            self.ticks_since_food = self.time_limit - save_data["time_left"]
            
            self.snake.body = save_data["snake"]
            self.snake.direction = save_data["direction"]
            
            self.food.position = save_data["food"]
            
            self.walls.positions = save_data["walls"]     
        else:
            self.food.respawn(
                self.height,
                self.width,
                self.snake,
                self.walls
            )   
            
        terminal_height, terminal_width = self.stdscr.getmaxyx()
        
        if self.height > terminal_height or self.width > terminal_width:
            raise ValueError(
                f"Карта {self.height}x{self.width}"
                f"не помещается в терминал "
                f"{terminal_height}x{terminal_width}"
            )

        self.window = curses.newwin(
            self.height,
            self.width,
            0,
            0
        )

        self.window.keypad(1)
        self.window.timeout(100)

        self.snake_color = curses.color_pair(1)
        
    def get_save_data(self): #Implemented variable storage
        save_data = {
            "snake": self.snake.body,
            "food": self.food.position,
            "walls": self.walls.positions,
            "score": self.score,
            "time_left": self.time_limit - self.ticks_since_food,
            "direction": self.snake.direction,
            "last_save_at": datetime.now().isoformat(), #Saving by date
            "map": {
                "height": self.map_height,
                "width": self.map_width
            }
        }
        return save_data
        
    def save_game(self, filename):
        save_data = self.get_save_data()
        
        self.save_manager.save(
            save_data,
            filename
        )         
    
    def create_save(self):
        filename = self.save_manager.get_new_save_filename()
        self.save_game(filename)
        
    def overwrite(self, filename):
        self.save_game(filename)

    def draw(self):
        """Draws the game board."""

        self.window.clear()

        # Game board frame.
        self.window.border(0)

        # Score.
        self.window.addstr(
            0,
            2,
            f" Счёт: {self.score} "
        )

        # Timer.
        seconds_left = max(
            0,
            (self.time_limit - self.ticks_since_food) // 10 + 1
        )

        timer_msg = f"Время: {seconds_left} "

        self.window.addnstr(
            0,
            self.width - len(timer_msg) - 2,
            timer_msg,
            len(timer_msg)
        )

        # Drawing walls.
        for y, x in self.walls.positions:
            self.window.addch(
                y,
                x,
                "#"
            )

        # Drawing food.
        food_y, food_x = self.food.position

        self.window.addch(
            food_y,
            food_x,
            curses.ACS_PI
        )

        # Drawing a snake.
        head_y, head_x = self.snake.get_head()

        self.window.addch(
            head_y,
            head_x,
            curses.ACS_CKBOARD,
            self.snake_color
        )

        # We draw the rest of the body parts.
        for y, x in self.snake.body[1:]:
            self.window.addch(
                y,
                x,
                curses.ACS_CKBOARD,
                self.snake_color
            )

        self.window.refresh()

    def handle_input(self):
        """Get the pressed key."""

        key = self.window.getch()

        if key == ord("q"):
            return False
        
        if key == ord(" "):
            self.pause_menu()

        if key in (
            curses.KEY_UP,
            curses.KEY_DOWN,
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
        ):
            self.snake.change_direction(key)

        return True
    
    def pause_menu(self): 
        while True: 
            self.window.clear()
        
            self.window.addstr(
                2,
                5,
                "ПАУЗА"
            )

            self.window.addstr(
                4,
                5,
                "S - Сохранить"
            )

            self.window.addstr(
                5,
                5,
                "Space - Продолжить"
            )

            self.window.addstr(
                6,
                5,
                "ESC - Выйти"
            )

            self.window.refresh()

            key = self.window.getch()

            if key in (ord("s"), ord("S")):
                self.save_menu()

            elif key == ord(" "):
                return

            elif key == 27:
                return
            
    def save_menu(self): 
        self.current_save_row = 0
        
        while True: 
            self.window.clear()
            
            files = [
                file for file in os.listdir("saves")
                if file.startswith("save_") and file.endswith(".json")
            ]

            saves = []
            
            for file in files:
                timestamp = file[5:-5]
                save_time = datetime.strptime(
                    timestamp,
                    "%Y%m%d_%H%M%S"
                )

                formatted_time = save_time.strftime(
                    "%d.%m.%Y %H:%M:%S"
                )

                saves.append(formatted_time)

            saves.append("Новое сохранение")
            saves.append("Назад")

            self.window.addstr(
                2,
                5,
                "СОХРАНИТЬ ИГРУ"
            )

            for index, save in enumerate(saves):
                prefix = "> " if index == self.current_save_row else "  "

                self.window.addstr(
                    4 + index,
                    5,
                    prefix + save
                )

            self.window.refresh()

            key = self.window.getch()

            if key == curses.KEY_UP:
                self.current_save_row = max(
                    0,
                    self.current_save_row - 1
                )

            elif key == curses.KEY_DOWN:
                self.current_save_row = min(
                    len(saves) - 1,
                    self.current_save_row + 1
                )

            elif key in (10, 13):
                selected = self.current_save_row
                
                if selected < len(files):
                    
                    filename = os.path.join(
                        "saves",
                        files[selected]
                    )

                    self.confirm_overwrite(filename)

                elif selected == len(files):
                    
                    self.create_save()

                else:
                    
                    return
                
    def confirm_overwrite(self, filename): 
        while True: 
            self.window.clear()
            self.window.addstr(
                4,
                5,
                "Перезаписать это сохранение?"
            )

            self.window.addstr(
                6,
                5,
                "Enter - Да"
            )

            self.window.addstr(
                7,
                5,
                "ESC - Нет"
            )

            self.window.refresh()

            key = self.window.getch()

            if key in (10, 13):
                self.overwrite(filename)
                return

            elif key == 27:
                return

    def check_collision(self, new_head):
        """Check the snake collisions."""
        # Colisions with walls.
        if self.walls.contains(new_head):
            return True

        # Colisions with herself.
        if self.snake.is_collision_with_self(new_head):
            return True

        return False

    def check_food(self, new_head):
        """Checks if the snake has eaten the food."""
        
        return new_head == self.food.position

    def game_over(self, message):
        """Display a game-over message."""

        message = f" {message} Счёт: {self.score} "

        self.window.addstr(
            self.height // 2,
            max(
                0,
                self.width // 2 - len(message) // 2
            ),
            message
        )

        self.window.refresh()

        self.window.timeout(-1)
        self.window.getch()
        
        if self.filename and os.path.exists(self.filename):
            os.remove(self.filename)

    def run(self):
        """Launches the game."""

        self.window.nodelay(0)

        while True:

            # Get the key.
            if not self.handle_input():
                break

            # Get the new head position.
            new_head = self.snake.get_new_head()
            
            new_head = self.wrap_position(new_head)

            # Checking for collisions.
            if self.check_collision(new_head):
                self.game_over("Game Over!")
                break

            # Increasing the timer.
            self.ticks_since_food += 1

            # Checking for time expiration.
            if self.ticks_since_food > self.time_limit:
                self.game_over("Time out!")
                break

            # Checking the food.
            ate_food = self.check_food(new_head)

            # Moving the snake.
            self.snake.move(
                new_head,
                grow=ate_food
            )

            # If the food has been eaten.
            if ate_food:

                self.score += 1

                # Adding 10 seconds.
                self.time_limit += 100

                # Resetting the timer.
                self.ticks_since_food = 0

                # Creating new food.
                self.food.respawn(
                    self.height,
                    self.width,
                    self.snake,
                    self.walls
                )
                if self.auto_save:
                    auto_save_filename = self.save_manager.get_auto_save_filename()
                    self.save_game(auto_save_filename)
            
            # Drawing a game.
            self.draw()
    def wrap_position(self, position):
        #allows movement between walls
        
        y, x = position
        
        if y == 0:
            y = self.height - 2
            
        elif y == self.height - 1:
            y = 1
            
        if x == 0:
            x = self.width - 2
            
        elif x == self.width - 1:
            x = 1
            
        return [y, x]
