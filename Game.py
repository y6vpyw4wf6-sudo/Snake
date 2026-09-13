import curses 
import os
import json

from Food import Food
from Wall import Wall
from Snake import Snake


class Game:
    def __init__(self, stdscr, save_data=None, filename=None):
        self.stdscr = stdscr
        self.filename = filename

        self.height, self.width = stdscr.getmaxyx()

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
            15
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

        # If the food appears on the snake or the wall,
        # we recreate it.
        self.food.respawn(
            self.height,
            self.width,
            self.snake,
            self.walls
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
        
    def save_game(self, filename):
        save_data = {
            "snake": self.snake.body,
            "food": self.food.position,
            "walls": self.walls.positions,
            "score": self.score,
            "time_left": self.time_limit - self.ticks_since_food,
            "direction": self.snake.direction
        }
        
        os.makedirs("saves", exist_ok=True)

        with open(filename, "w") as file:
            json.dump(save_data, file, indent=4)
            
    @staticmethod
    def load_game(filename):
        if not os.path.exists(filename):
            return None
        
        with open(filename, "r") as file:
            save_data = json.load(file)
            
        return save_data            
            
    def get_new_save_filename(self):
        os.makedirs("saves", exist_ok=True)
        
        files = os.listdir("saves")
        next_number = len(files) + 1
        
        return f"saves/save_{next_number}.json"
        
    def check_game_over(self, score):
        if score > self.high_score:
            self.high_score = score

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

        if key in (
            curses.KEY_UP,
            curses.KEY_DOWN,
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
        ):
            self.snake.change_direction(key)

        return True

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
                
                if self.filename is None:
                    self.filename = self.get_new_save_filename()
            
                self.save_game(self.filename)
            
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
