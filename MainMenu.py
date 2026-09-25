import curses 
import os
from Game import Game 
from SaveManager import SaveManager 
from Menu import Menu 
from GameMenu import GameMenu


class MainMenu(Menu):
    def __init__(self, stdscr):
        super().__init__(stdscr)

        self.save_manager = SaveManager()

        self.map_height = 30
        self.map_width = 60
        self.auto_save = True

        self.update_menu()

    def update_menu(self):

        self.items = []

        if os.path.exists("saves") and os.listdir("saves"):
            self.items.append("Продолжить")

        self.items.append("Новая игра")
        self.items.append("Загрузить")
        self.items.append("Настройки")
        self.items.append("Выход")

    def run(self):

        while True:

            self.update_menu()

            self.draw("ЗМЕЙКА")

            key = self.stdscr.getch()

            self.navigation(key)

            if key in (
                curses.KEY_ENTER,
                10,
                13
            ):

                choice = self.items[self.current_row]

                if choice == "Продолжить":

                    self.continue_game()

                elif choice == "Новая игра":

                    self.new_game()

                elif choice == "Загрузить":

                    self.show_load_menu()

                elif choice == "Настройки":

                    self.show_settings()

                elif choice == "Выход":

                    return

    def new_game(self):

        config = {
            "map": {
                "height": self.map_height,
                "width": self.map_width
            },
            "auto_save": self.auto_save,
            "save_data": None,
            "filename": None
        }

        game = Game(
            self.stdscr,
            config
        )

        game.run()

    def continue_game(self):

        file = self.get_last_save()

        if file:

            filename = os.path.join(
                "saves",
                file
            )

            save_data = self.save_manager.load(filename)

            if save_data:

                config = {
                    "map": {
                        "height": self.map_height,
                        "width": self.map_width
                    },
                    "auto_save": self.auto_save,
                    "save_data": None,
                    "filename": None
                }

                game = Game(
                    self.stdscr,
                    config
                )

                game.run()

    def get_last_save(self):

        files = [
            file
            for file in os.listdir("saves")
            if file.startswith("save_")
            and file.endswith(".json")
        ]

        if not files:
            return None

        files.sort()

        return files[-1]

    def show_load_menu(self):

        os.makedirs("saves", exist_ok=True)

        self.current_row = 0

        while True:

            files = [
                file
                for file in os.listdir("saves")
                if file.startswith("save_")
                and file.endswith(".json")
            ]

            saves = []

            for index, file in enumerate(files, start=1):
                saves.append(f"Сохранение {index}")

            self.stdscr.clear()

            height, width = self.stdscr.getmaxyx()

            title = "Загрузить"

            self.stdscr.addstr(
                2,
                width // 2 - len(title) // 2,
                title,
                curses.A_BOLD
            )

            if not saves:

                message = "Сохранений нет!"

                self.stdscr.addstr(
                    height // 2,
                    max(
                        0,
                        width // 2 - len(message) // 2
                    ),
                    message
                )

            for index, save in enumerate(saves):

                x = width // 2 - len(save) // 2
                y = height // 2 + index

                if index == self.current_row:

                    self.stdscr.attron(
                        curses.color_pair(2)
                    )

                    self.stdscr.addstr(
                        y,
                        x,
                        save
                    )

                    self.stdscr.attroff(
                        curses.color_pair(2)
                    )

                else:

                    self.stdscr.addstr(
                        y,
                        x,
                        save
                    )

            hint = "D - Удалить | ESC - назад"

            self.stdscr.addstr(
                height - 2,
                width // 2 - len(hint) // 2,
                hint
            )

            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == 27:
                self.current_row = 0
                return

            if (
key == curses.KEY_UP
            and self.current_row > 0
        ):
                self.current_row -= 1

            elif (
                key == curses.KEY_DOWN
                and self.current_row < len(saves) - 1
            ):
                self.current_row += 1

            elif key in (
                curses.KEY_ENTER,
                10,
                13
            ):

                if not saves:
                    continue

                file = files[self.current_row]

                filename = os.path.join(
                    "saves",
                    file
                )

                save_data = self.save_manager.load(filename)

                if save_data:

                    game = Game(
                        self.stdscr,
                        None,
                        save_data,
                        filename
                    )

                    game.run()

                self.current_row = 0
                return

            elif key in (
                ord("d"),
                ord("D")
            ):

                if files:

                    file = files[self.current_row]

                    filename = os.path.join(
                        "saves",
                        file
                    )

                    os.remove(filename)

                    if self.current_row >= len(files) - 1:
                        self.current_row = max(
                            0,
                            len(files) - 2
                        )

    def show_settings(self):

        game_menu = GameMenu(
            self.stdscr,
            self.map_height,
            self.map_width,
            self.auto_save
        )

        (
            self.map_height,
            self.map_width,
            self.auto_save
        ) = game_menu.run()
