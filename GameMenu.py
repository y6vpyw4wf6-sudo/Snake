import curses
from Menu import Menu


class GameMenu(Menu):
    def __init__(
        self,
        stdscr,
        map_height,
        map_width,
        auto_save
    ):
        super().__init__(stdscr)

        self.map_height = map_height
        self.map_width = map_width
        self.auto_save = auto_save

        self.map_sizes = [
            (20, 40),
            (30, 60),
            (40, 80)
        ]

    def update_items(self, current_size):
        
        left_arrow = "<" if current_size > 0 else " "
        right_arrow = ">" if current_size < len(self.map_sizes) - 1 else " "

        self.items = [
            (
                f"{left_arrow} "
                f"Размер карты   "
                f"[ {self.map_sizes[current_size][0]}x"
                f"{self.map_sizes[current_size][1]} ]"
                f"{right_arrow}"
            ),
            (
                f"Автосохранение   "
                f"[ {'ВКЛ' if self.auto_save else 'ВЫКЛ'} ]"
            ),
            "Назад"
        ]

    def run(self):

        current_size = self.map_sizes.index(
            (self.map_height, self.map_width)
        )

        while True:

            self.update_items(current_size)

            self.draw("Игра")

            key = self.stdscr.getch()

            self.navigation(key)

            # Размер карты
            if (
                key == curses.KEY_LEFT
                and self.current_row == 0
            ):

                if current_size > 0:
                    current_size -= 1

            elif (
                key == curses.KEY_RIGHT
                and self.current_row == 0
            ):

                if current_size < len(self.map_sizes) - 1:
                    current_size += 1

            # Автосохранение
            elif (
                key == curses.KEY_LEFT
                and self.current_row == 1
            ):

                self.auto_save = False

            elif (
                key == curses.KEY_RIGHT
                and self.current_row == 1
            ):

                self.auto_save = True

            # Enter
            elif key in (
                curses.KEY_ENTER,
                10,
                13
            ):

                if self.current_row == 0:

                    self.map_height, self.map_width = (
                        self.map_sizes[current_size]
                    )

                elif self.current_row == 2:

                    return (
                        self.map_height,
                        self.map_width,
                        self.auto_save
                    )

            # ESC
            elif key == 27:

                return (
                    self.map_height,
                    self.map_width,
                    self.auto_save
                )
