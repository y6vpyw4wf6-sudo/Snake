import curses 
import os

from Game import Game


class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.current_row = 0
        self.map_height = 30
        self.map_width = 60
        self.update_menu()
        
    def update_menu(self):
        self.menu = []
        
        if os.path.exists("saves") and os.listdir("saves"):
            self.menu.append("Продолжить")
            
        self.menu.append("Новая игра")
        self.menu.append("Загрузить")
        self.menu.append("Настройки")
        self.menu.append("Выход")

    def draw(self):
        """Draws the menu."""

        self.stdscr.clear()

        height, width = self.stdscr.getmaxyx()

        title = "ЗМЕЙКА"

        self.stdscr.addstr(
            2,
            width // 2 - len(title) // 2,
            title,
            curses.A_BOLD
        )

        for index, row in enumerate(self.menu):

            x = width // 2 - len(row) // 2

            y = (
                height // 2
                - len(self.menu) // 2
                + index
            )

            if index == self.current_row:

                self.stdscr.attron(
                    curses.color_pair(2)
                )

                self.stdscr.addstr(
                    y,
                    x,
                    row
                )

                self.stdscr.attroff(
                    curses.color_pair(2)
                )

            else:

                self.stdscr.addstr(
                    y,
                    x,
                    row
                    )

            self.stdscr.refresh()

    def run(self):
        """Launches the menu."""

        while True:
            
            self.update_menu()

            self.draw()

            key = self.stdscr.getch()

            if (
                key == curses.KEY_UP
                and self.current_row > 0
            ):
                self.current_row -= 1

            elif (
                key == curses.KEY_DOWN
                and self.current_row < len(self.menu) - 1
            ):
                self.current_row += 1

            elif key in (
                curses.KEY_ENTER,
                10,
                13
            ):

                choice = self.menu[self.current_row]

                if choice == "Продолжить":
                    
                    file = self.get_last_save()
                    
                    if file:
                        filename = os.path.join("saves", file)
                        save_data = Game.load_game(filename)
                        
                        if save_data:
                            game = Game(self.stdscr, save_data, filename)
                            game.run()
                        
                elif choice == "Загрузить":
                    
                    self.show_load_menu()
                        
                elif choice == "Новая игра":
                    
                    game = Game(self.stdscr, map_height=self.map_height, map_width=self.map_width)
                    game.run()

                elif choice == "Настройки":

                    self.show_settings()

                elif choice == "Выход":

                    break
                
    def show_load_menu(self):
        
        os.makedirs("saves", exist_ok=True)
        
        files = os.listdir("saves")
        
        print(files)
        
        self.stdscr.clear()

        height, width = self.stdscr.getmaxyx()
        
        title = "Загрузить"
        
        self.stdscr.addstr(
            2,
            width // 2 - len(title) // 2,
            title,
            curses.A_BOLD
        )        
        
        self.current_row = 0
        
        while True:
            
            files = os.listdir("saves")
            
            saves = []
            
            for index, file in enumerate(files, start=1):
                saves.append(f"Сохранение {index}")
                
            self.stdscr.clear()
                
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
            
            if key == 27: #ESC
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
                filename = os.path.join("saves", file)
                
                save_data = Game.load_game(filename)
                
                if save_data:
                    game = Game(self.stdscr, save_data, filename)
                    game.run()
                    
                return
            
            elif key in (ord("d"), ord("D")):
                if files:
                    file = files[self.current_row]
                    filename = os.path.join("saves", file)    
                    
                    os.remove(filename)
                    
                    if self.current_row >= len(files) - 1:
                        self.current_row = max(0, len(files) - 2)
                    
                    files = os.listdir("saves")
            
                    saves = []
            
                    for index, file in enumerate(files, start=1):
                        saves.append(f"Сохранение {index}")             

    def show_settings(self):
        """Shows settings."""
        
        self.current_row = 0

        settings_menu = [
            "Игра",
            "Назад"
        ]

        while True:

            self.stdscr.clear()

            height, width = self.stdscr.getmaxyx()

            title = "Настройки"

            self.stdscr.addstr(
                2,
                width // 2 - len(title) // 2,
                title,
                curses.A_BOLD
            )

            for index, row in enumerate(settings_menu):

                x = width // 2 - len(row) // 2
                y = height // 2 - len(settings_menu) // 2 + index

                if index == self.current_row:

                    self.stdscr.attron(
                        curses.color_pair(2)
                    )

                    self.stdscr.addstr(
                        y,
                        x,
                        row
                    )

                    self.stdscr.attroff(
                        curses.color_pair(2)
                    )

                else:

                    self.stdscr.addstr(
                        y,
                        x,
                        row
                    )

            self.stdscr.refresh()

            key = self.stdscr.getch()

            if (
                key == curses.KEY_UP
                and self.current_row > 0
            ):
                self.current_row -= 1

            elif (
                key == curses.KEY_DOWN
                and self.current_row < len(settings_menu) - 1
            ):
                self.current_row += 1

            elif key in (
                curses.KEY_ENTER,
                10,
                13
            ):

                choice = settings_menu[self.current_row]

                if choice == "Игра":
                    self.show_game_settings()

                elif choice == "Назад":
                    return

            elif key == 27:  # ESC
                return
            
    def show_game_settings(self):
        self.current_row = 0

        while True:
            
            height, width = self.stdscr.getmaxyx()
            
            max_map_height = height - 2
            max_map_width = width - 2
            
            game_settings = [
                "Маленькая - 20 x 40",
                "Средняя - 30 x 60",
                "Большая 40 x 80",
                "Назад"
            ]
            
            self.stdscr.clear()

            title = "Игра"

            self.stdscr.addstr(
                2,
                width // 2 - len(title) // 2,
                title,
                curses.A_BOLD
            )

            for index, row in enumerate(game_settings):

                x = width // 2 - len(row) // 2
                y = height // 2 - len(game_settings) // 2 + index

                if index == self.current_row:

                    self.stdscr.attron(
                        curses.color_pair(2)
                    )

                    self.stdscr.addstr(
                        y,
                        x,
                        row
                    )

                    self.stdscr.attroff(
                        curses.color_pair(2)
                    )

                else:

                    self.stdscr.addstr(
                        y,
                        x,
                        row
                    )

            self.stdscr.refresh()

            key = self.stdscr.getch()

            if (
                key == curses.KEY_UP
                and self.current_row > 0
            ):
                self.current_row -= 1

            elif (
                key == curses.KEY_DOWN
                and self.current_row < len(game_settings) - 1
            ):
                self.current_row += 1

            elif key in (
                curses.KEY_ENTER,
                10,
                13
            ):

                choice = game_settings[self.current_row]
                
                if choice == "Маленькая - 20 x 40":
                    if max_map_height >= 20 and max_map_width >= 40:
                        self.map_height = 20
                        self.map_width = 40
                    
                elif choice == "Средняя - 30 x 60":
                    if max_map_height >= 30 and max_map_width >= 60:
                        self.map_height = 30
                        self.map_width = 60
                    
                elif choice == "Большая - 40 x 80":
                    if max_map_height >= 40 and max_map_width >= 80:
                        self.map_height = 40
                        self.map_width = 80

                elif choice == "Назад":
                    return

            elif key == 27:  # ESC
                return

    def get_last_save(self):
        files = os.listdir("saves")
        
        if not files:
            return None
        
        files.sort()
        
        return files[-1]