import curses
from MainMenu import MainMenu


def main(stdscr):
    # Hidding the cursor.
    curses.curs_set(0)

    # Turning on the keyboard.
    stdscr.keypad(1)

    # Turning on the colors.
    curses.start_color()

    # Snake color.
    curses.init_pair(
        1,
        curses.COLOR_BLUE,
        curses.COLOR_BLACK
    )

    # Highlighting a menu item.
    curses.init_pair(
        2,
        curses.COLOR_BLACK,
        curses.COLOR_WHITE
    )

    menu = MainMenu(stdscr)

    menu.run()
    
if __name__ == "__main__": 
    curses.wrapper(main)