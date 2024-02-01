from game_logic.connect4 import Connect4
from tools.errors import InvalidMoveError, GameDraw, PlayerWin
import customtkinter as ctk
from AI.minimax import Minimax
from typing import Optional
from math import ceil
import tkinter as tk


class Connect4_GUI(Connect4):
    """
    Represents the graphical user interface for the Connect4 game.

    Attributes:
        - width (int): The width of the GUI window.
        - height (int): The height of the GUI window.
        - _height (int): The actual height of the GUI window.
        - _width (int): The actual width of the GUI window.
        - _title (str): The title of the GUI window.
        - _font (ctk.CTkFont): The font used for the GUI elements.
        - rows (int): The number of rows in the game board.
        - columns (int): The number of columns in the game board.
        - _canvas_padding (int): The padding around the game board on the canvas.
        - _game_cube_padding (int): The padding around each game cube on the canvas.
        - _dark_gray_color (str): The color used for the background of the GUI.

    Methods:
        - __init__(self, width: int = 700, height: int = 600): Initializes a new instance of the Connect4_GUI class.
        - create_app(self): Creates and starts the GUI application.
        - _main_menu(self): Displays the main menu of the game.
        - _game_menu(self): Displays the game menu and starts a new game.
        - _game_over_menu(self, message: str): Displays the game over menu with the specified message.
        - _initiate_pvp_game(self): Initializes a player vs player game.
        - _initiate_pve_game(self): Initializes a player vs AI game.
        - _clear_scores(self): Clears the game board and resets the scores.
        - rematch(self): Restarts the game with the same players.
        - make_move(self, column: int) -> str | None: Makes a move in the specified column and handles game events.
        - _draw_game_grid(self): Draws the game grid on the canvas.
        - _on_game_grid_click(self, event): Handles the event when the game grid is clicked.
        - _render_game_cubes(self, canvas: ctk.CTkCanvas): Renders the game cubes on the canvas.
        - _calculate_clicked_column(self, event) -> int: Calculates the column index based on the x-coordinate of the mouse click event.
        - _clear_canvas(self, canvas: Optional[ctk.CTkCanvas] = None): Clears the canvas by destroying all widgets and clearing the canvas itself.
        - _create_canvas(self) -> ctk.CTkCanvas: Create and return a CTkCanvas object.
        - _create_grid_rectangles(self, canvas: ctk.CTkCanvas): Creates grid on the canvas.
        - _create_game_labels(self): Creates and places the game labels on the GUI.
        - _create_button(self): Create a button widget with the given title, command, and optional parameters.
        - _create_label(self, text: str, text_color="#1f6aa5", **kwargs) -> ctk.CTkLabel: Create and return a custom labeled widget.
        - _update_label(self, label: ctk.CTkLabel, text: str, **kwargs) -> ctk.CTkLabel: Updates the given label with the specified text and optional keyword arguments.
        - _set_settings(self, appearence: str = "dark", theme: str = "blue"): Set the appearance mode and default color theme for the GUI.
    """

    def __init__(self, width: int = 700, height: int = 600):
        """
        Initializes a new instance of the Connect4_GUI class.

        Args:
            - width (int): The width of the GUI window.
            - height (int): The height of the GUI window.
        """
        super().__init__()
        self._height: int = height
        self._width: int = width
        self._title: str = "Connect 4"
        self._font: ctk.CTkFont = ("Helvetica", 22)
        self.rows, self.columns = self._board.shape
        self._canvas_padding: int = 60
        self._game_cube_padding: int = 7

        self._dark_gray_color = "#242424"

    def create_app(self):
        """
        Creates and starts the GUI application.
        """
        self._set_settings

        self.root = ctk.CTk()
        self.root.title(self._title)
        self.root.geometry(f"{self._width}x{self._height}")

        self._main_menu()
        self.root.mainloop()

    def _main_menu(self):
        """
        Displays the main menu of the game.
        """
        self._clear_canvas()
        self._clear_scores()

        self.PvP_button = self._create_button("PvP", self._initiate_pvp_game)
        self.PvP_button.place(relx=0.5, rely=0.45, anchor="center")

        self.PvE_button = self._create_button("PvE", self._initiate_pve_game)
        self.PvE_button.place(relx=0.5, rely=0.55, anchor="center")

    def _game_menu(self):
        """
        Displays the game menu and starts a new game.
        """
        self.current_player = self.choose_starting_player(
            [self.Player_one, self.Player_two]
        )
        self._clear_canvas()
        self._draw_game_grid()

        self.menu_button = self._create_button(
            "Menu", self._main_menu, x_ratio=0.13, y_ratio=0.06
        )
        self.menu_button.place(
            relx=0.5,
            rely=0.05,
            anchor="center",
        )

        self.canvas.bind("<Button-1>", self._on_game_grid_click)

    def _game_over_menu(self, e: str):
        """
        Displays the game over menu with the specified message.

        Args:
            - message (str): The message to display.
        """
        self.bottom_label = self._update_label(
            self.bottom_label, f"{e}", text_color=self.current_player.color
        )
        self.bottom_label.place(relx=0.5, rely=0.95, anchor="center")

        self._draw_button = self._create_button(
            "Rematch",
            self.rematch,
            x_ratio=0.3,
            y_ratio=0.1,
        )
        self._draw_button.place(relx=0.5, rely=0.5, anchor="center")

    def _initiate_pvp_game(self):
        """
        Initializes a player vs player game.
        """
        self._game_menu()

    def _initiate_pve_game(self):
        """
        Initializes a player vs AI game.
        """
        pass

    def _clear_scores(self):
        """
        Clears the game board and resets the scores.
        """
        self.clear_board()
        self.game_state = 0
        self.Player_one.wins = 0
        self.Player_two.wins = 0

    def rematch(self):
        """
        Restarts the game with the same players.
        """
        super().rematch()
        self._game_menu()

    def make_move(self, column: int) -> str | None:
        """
        Makes a move in the specified column and handles game events.

        Args:
            - column (int): The column in which to make the move.

        Returns:
            - str | None: The game over message if the game is over, otherwise None.
        """
        try:
            super().make_move(column)
            self.bottom_label = self._update_label(
                self.bottom_label,
                f"Player {self.current_player.identifier}'s turn",
                text_color=self.current_player.color,
            )
            self.bottom_label.place(relx=0.5, rely=0.95, anchor="center")

        except GameDraw as e:
            self._game_over_menu(e)

        except PlayerWin as e:
            self._game_over_menu(e)

        except InvalidMoveError as e:
            self.bottom_label = self._update_label(
                self.bottom_label, f"{e}", text_color=self.current_player.color
            )
            self.bottom_label.place(relx=0.5, rely=0.95, anchor="center")

        finally:
            self._render_game_cubes(self.canvas)

    def _draw_game_grid(self):
        """
        Draws the game grid on the canvas.
        """

        self.canvas = self._create_canvas()
        self._create_game_labels()
        self._create_grid_rectangles(self.canvas)

        if self._num_of_moves != 0:
            self.bottom_label.destroy()

        self.canvas.pack()

    def _on_game_grid_click(self, event):
        """
        Handles the event when the game grid is clicked.

        Args:
            event (Event): The event object containing information about the click.

        Returns:
            None
        """
        horizontal_condition = (
            event.x > self._canvas_padding
            and event.x < self._width - self._canvas_padding
        )
        vertical_condition = (
            event.y > self._canvas_padding
            and event.y < self._height - self._canvas_padding
        )
        if horizontal_condition and vertical_condition:
            clicked_column = self._calculate_clicked_column(event)
            self.make_move(clicked_column)

    def _render_game_cubes(self, canvas: ctk.CTkCanvas):
        """
        Renders the game cubes on the canvas.

        Args:
            canvas (ctk.CTkCanvas): The canvas on which to render the game cubes.
        """
        self.canvas.delete("cubes")

        for col in range(self.columns):
            for row in range(self.rows):
                player_id = self.board_layout()[row, col]

                if player_id == 1:
                    color = self.Player_one.color
                elif player_id == 2:
                    color = self.Player_two.color
                else:
                    continue

                x1 = self._canvas_padding + col * (
                    (self._width - 2 * self._canvas_padding) / self.columns
                )
                y1 = self._canvas_padding + row * (
                    (self._height - 2 * self._canvas_padding) / self.rows
                )
                x2 = self._canvas_padding + (col + 1) * (
                    (self._width - 2 * self._canvas_padding) / self.columns
                )
                y2 = self._canvas_padding + (row + 1) * (
                    (self._height - 2 * self._canvas_padding) / self.rows
                )

                canvas.create_rectangle(
                    x1 + self._game_cube_padding,
                    y1 + self._game_cube_padding,
                    x2 - self._game_cube_padding,
                    y2 - self._game_cube_padding,
                    outline=color,
                    fill=color,
                    tags="cubes",
                )

    def _calculate_clicked_column(self, event) -> int:
        """
        Calculates the column index based on the x-coordinate of the mouse click event.

        Args:
            event: The mouse click event.

        Returns:
            The index of the clicked column.
        """
        self.column_width = (self._width - 2 * self._canvas_padding) / self.columns
        self.clicked_column = (
            ceil((event.x - self._canvas_padding) / self.column_width) - 1
        )

        return self.clicked_column

    def _clear_canvas(self, canvas: Optional[ctk.CTkCanvas] = None):
        """
        Clears the canvas by destroying all widgets and clearing the canvas itself.

        Args:
            canvas (Optional[ctk.CTkCanvas]): The canvas to be cleared. If not provided, all widgets will be destroyed but the canvas will not be cleared.

        Returns:
            None
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        if canvas:
            canvas.destroy("all")

    def _create_canvas(self) -> ctk.CTkCanvas:
        """
        Create and return a CTkCanvas object.

        Returns:
            ctk.CTkCanvas: The created CTkCanvas object.
        """
        return ctk.CTkCanvas(
            self.root,
            width=self._width,
            height=self._height,
            bg=self._dark_gray_color,
            bd=0,
            highlightthickness=0,
        )

    def _create_grid_rectangles(self, canvas: ctk.CTkCanvas):
        """
        Creates grid on the canvas.

        Args:
            canvas (ctk.CTkCanvas): The canvas on which to create the rectangles.
        """
        for col in range(self.columns):
            for row in range(self.rows):
                x1 = self._canvas_padding + col * (
                    (self._width - 2 * self._canvas_padding) / self.columns
                )
                y1 = self._canvas_padding + row * (
                    (self._height - 2 * self._canvas_padding) / self.rows
                )
                x2 = self._canvas_padding + (col + 1) * (
                    (self._width - 2 * self._canvas_padding) / self.columns
                )
                y2 = self._canvas_padding + (row + 1) * (
                    (self._height - 2 * self._canvas_padding) / self.rows
                )

                canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def _create_game_labels(self):
        """
        Creates and places the game labels on the GUI.
        """

        # Bottom label
        self.bottom_label = self._create_label(
            text=f"Player {self.current_player.identifier} starts",
            text_color=self.current_player.color,
        )

        self.bottom_label.place(relx=0.5, rely=0.95, anchor="center")

        # Player 1
        self.player_one_label = self._create_label(
            "Player 1", text_color=self.Player_one.color
        )
        self.player_one_label.place(relx=0.1, rely=0.05, anchor="center")
        # Score 1 Label
        self.player_one_score_label = self._create_label(
            f"{self.Player_one.wins}", text_color=self.Player_one.color
        )
        self.player_one_score_label.place(relx=0.4, rely=0.05, anchor="center")

        # Player 2
        self.player_two_score_label = self._create_label(
            f"Player 2", text_color=self.Player_two.color
        )
        self.player_two_score_label.place(relx=0.9, rely=0.05, anchor="center")
        # Score 2 label
        self.player_two_score_label = self._create_label(
            f"{self.Player_two.wins}", text_color=self.Player_two.color
        )
        self.player_two_score_label.place(relx=0.6, rely=0.05, anchor="center")

    def _create_button(
        self,
        title: str,
        command: callable,
        x_ratio: float = 0.22,
        y_ratio: float = 0.085,
        **kwargs,
    ) -> ctk.CTkButton:
        """
        Create a button widget with the given title, command, and optional parameters.

        Args:
            title (str): The text to be displayed on the button.
            command (callable): The function to be called when the button is clicked.
            x_ratio (float, optional): The width ratio of the button relative to the window width. Defaults to 0.22.
            y_ratio (float, optional): The height ratio of the button relative to the window height. Defaults to 0.085.
            **kwargs: Additional keyword arguments to be passed to the button widget.

        Returns:
            ctk.CTkButton: The created button widget.
        """
        button_width = self._width * x_ratio
        button_height = self._height * y_ratio

        return ctk.CTkButton(
            self.root,
            text=title,
            command=command,
            width=button_width,
            height=button_height,
            font=self._font,
            **kwargs,
        )

    def _update_label(self, label: ctk.CTkLabel, text: str, **kwargs) -> ctk.CTkLabel:
        """
        Updates the given label with the specified text and optional keyword arguments.

        Args:
            label (ctk.CTkLabel): The label to be updated.
            text (str): The new text for the label.
            **kwargs: Optional keyword arguments to be passed to the _create_label method.

        Returns:
            ctk.CTkLabel: The updated label.
        """
        if label:
            label.destroy()
        return self._create_label(text=text, **kwargs)

    def _create_label(self, text: str, text_color="#1f6aa5", **kwargs) -> ctk.CTkLabel:
        """
        Create and return a custom labeled widget.

        Args:
            text (tk.StringVar): The text to be displayed on the label.
            text_color (str, optional): The color of the text. Defaults to "#1f6aa5".
            **kwargs: Additional keyword arguments to be passed to the ctk.CTkLabel constructor.

        Returns:
            ctk.CTkLabel: The created label widget.
        """
        return ctk.CTkLabel(
            self.root,
            text=text,
            font=self._font,
            text_color=text_color,
            **kwargs,
        )

    def _set_settings(self, appearence: str = "dark", theme: str = "blue"):
        """
        Set the appearance mode and default color theme for the GUI.

        Args:
            appearence (str, optional): The appearance mode to set. Defaults to "dark".
            theme (str, optional): The default color theme to set. Defaults to "blue".
        """
        ctk.set_appearance_mode(appearence)
        ctk.set_default_color_theme(theme)
