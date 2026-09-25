import curses


class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.items = []
        self.current_row = 0

    def draw(self, title):
        self.stdscr.clear()

        height, width = self.stdscr.getmaxyx()

        self.stdscr.addstr(
            2,
            width // 2 - len(title) // 2,
            title,
            curses.A_BOLD
        )

        for index, item in enumerate(self.items):

            x = width // 2 - len(item) // 2
            y = height // 2 - len(self.items) // 2 + index

            if index == self.current_row:

                self.stdscr.attron(
                    curses.color_pair(2)
                )

                self.stdscr.addstr(
                    y,
                    x,
                    item
                )

                self.stdscr.attroff(
                    curses.color_pair(2)
                )

            else:

                self.stdscr.addstr(
                    y,
                    x,
                    item
                )

        self.stdscr.refresh()

    def navigation(self, key):

        if (
            key == curses.KEY_UP
            and self.current_row > 0
        ):
            self.current_row -= 1

        elif (
            key == curses.KEY_DOWN
            and self.current_row < len(self.items) - 1
        ):
            self.current_row += 1
