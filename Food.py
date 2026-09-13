import random


class Food:
    def __init__(self, y, x):
        self.position = [y, x]

    def respawn(self, height, width, snake, walls):
        """Создаёт еду в случайном свободном месте."""

        while True:
            y = random.randint(1, height - 2)
            x = random.randint(1, width - 2)

            new_position = [y, x]

            if (
                new_position not in snake.body
                and new_position not in walls.positions
            ):
                self.position = new_position
                break