import random

class Wall:
    def __init__(self, height, width, amount, snake_head):
        self.positions = []

        while len(self.positions) < amount:

            y = random.randint(1, height - 2)
            x = random.randint(1, width - 2)

            position = [y, x]
            
            if (
                y == snake_head[0]
                and snake_head[1] < x <= snake_head[1] + 5
            ):
                continue

            if position not in self.positions:
                self.positions.append(position)

    def contains(self, position):
        """Checks whether the position is located among walls."""

        return position in self.positions