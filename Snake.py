import curses 


class Snake:
    def __init__(self, start_y, start_x):
    # Snake's body.
    # First element — head.
        self.body = [
            [start_y, start_x],
            [start_y, start_x - 1],
            [start_y, start_x - 2],
    ]

    # Initial direction to the right.
        self.direction = curses.KEY_RIGHT

    def change_direction(self, new_direction):
        """Changes the direction of the snake's movement."""

        opposites = {
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_RIGHT: curses.KEY_LEFT,
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_DOWN: curses.KEY_UP,
        }

        # we do not allow a 180 degree turn.
        if opposites.get(new_direction) != self.direction:
            self.direction = new_direction

    def get_new_head(self):
        """Returns the coordinates of the new head."""

        y, x = self.body[0]

        if self.direction == curses.KEY_DOWN:
            y += 1

        elif self.direction == curses.KEY_UP:
            y -= 1

        elif self.direction == curses.KEY_LEFT:
            x -= 1

        elif self.direction == curses.KEY_RIGHT:
            x += 1

        return [y, x]

    def move(self, new_head, grow=False):
        """Moves the snake."""

        # Adding a new head.
        self.body.insert(0, new_head)

        # If the snake shouldn't grow,
        # remove the tail.
        if not grow:
            self.body.pop()

    def get_head(self):
        """Returns the coordinates of the head."""

        return self.body[0]

    def is_collision_with_self(self, position):
        """Checks for collision with itself."""

        return position in self.body