from game_logic.connect4 import Connect4
from tools.errors import InvalidMoveError, GameDraw, PlayerWin
import customtkinter as ctk
from AI.minimax import Minimax
from typing import Optional
from math import ceil


class Connect4_GUI(Connect4):
    def __init__(self, width: int = 700, height: int = 600):
        super().__init__()
        self.height: int = height
        self.width: int = width
        self.title: str = "Connect 4"
        self.font: ctk.CTkFont = ("Helvetica", 18)
        self.player_one_color = "#70D6FF"
        self.player_two_color = "#FF70A6"
        self.rows, self.columns = self.board.shape
        self.canvas_padding: int = 60
        self.game_cube_padding: int = 7

    def create_app(self):
        self._set_settings

        self.root = ctk.CTk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")

        self._main_menu()
        self.root.mainloop()

    def _main_menu(self):
        self._clear_canvas()

        self.PvP_button = self._create_button("PvP", self._initiate_pvp_game)
        self.PvP_button.place(relx=0.5, rely=0.45, anchor="center")

        self.PvE_button = self._create_button("PvE", self._initiate_pve_game)
        self.PvE_button.place(relx=0.5, rely=0.55, anchor="center")

    def _game_menu(self):
        self._clear_canvas()
        self._draw_game_grid()

        self._create_game_labels()

        self.canvas.bind("<Button-1>", self._on_game_grid_click)

    def _at_game_over(self):
        self._clear_canvas(self.canvas)
        self._main_menu()

    def _draw_game_grid(self):
        self.canvas = self._create_canvas()

        self._create_grid_rectangles(self.canvas)

        self.canvas.pack()

    def _initiate_pvp_game(self):
        self._game_menu()

    def _initiate_pve_game(self):
        pass

    def make_move(self, column: int) -> str | None:
        try:
            super().make_move(column)
            self.switch_player()

            self.Player_turn_label = self._update_label(
                self.Player_turn_label,
                f"Player {self.current_player.identifier}'s turn",
            )
        except GameDraw as e:
            self.Player_turn_label = self._update_label(self.Player_turn_label, f"{e}")
            print(e)

        except PlayerWin as e:
            self.Player_turn_label = self._update_label(self.Player_turn_label, f"{e}")
            print(e)

        except InvalidMoveError as e:
            self.Player_turn_label = self._update_label(self.Player_turn_label, f"{e}")
            print(e)

        finally:
            self._render_game_cubes()

    def _on_game_grid_click(self, event):
        horizontal_condition = (
            event.x > self.canvas_padding and event.x < self.width - self.canvas_padding
        )
        vertical_condition = (
            event.y > self.canvas_padding
            and event.y < self.height - self.canvas_padding
        )
        if horizontal_condition and vertical_condition:
            clicked_column = self._calculate_clicked_column(event)
            self.make_move(clicked_column)

    def _render_game_cubes(self):
        self.canvas.delete("cubes")
        self.rows, self.columns = self.board_layout().shape

        for col in range(self.columns):
            for row in range(self.rows):
                player_id = self.board_layout()[row, col]

                if player_id == 1:
                    color = self.player_one_color
                elif player_id == 2:
                    color = self.player_two_color
                else:
                    continue

                x1 = self.canvas_padding + col * (
                    (self.width - 2 * self.canvas_padding) / self.columns
                )
                y1 = self.canvas_padding + row * (
                    (self.height - 2 * self.canvas_padding) / self.rows
                )
                x2 = self.canvas_padding + (col + 1) * (
                    (self.width - 2 * self.canvas_padding) / self.columns
                )
                y2 = self.canvas_padding + (row + 1) * (
                    (self.height - 2 * self.canvas_padding) / self.rows
                )

                self.canvas.create_rectangle(
                    x1 + self.game_cube_padding,
                    y1 + self.game_cube_padding,
                    x2 - self.game_cube_padding,
                    y2 - self.game_cube_padding,
                    outline=color,
                    fill=color,
                    tags="cubes",
                )

    def _calculate_clicked_column(self, event) -> int:
        self.column_width = (self.width - 2 * self.canvas_padding) / self.columns
        self.clicked_column = (
            ceil((event.x - self.canvas_padding) / self.column_width) - 1
        )

        return self.clicked_column

    def _clear_canvas(self, canvas: Optional[ctk.CTkCanvas] = None):
        for widget in self.root.winfo_children():
            widget.destroy()

        if canvas:
            canvas.destroy("all")

    def _create_canvas(self) -> ctk.CTkCanvas:
        dark_gray_color = "#242424"

        return ctk.CTkCanvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=dark_gray_color,
            bd=0,
            highlightthickness=0,
        )

    def _create_grid_rectangles(self, canvas: ctk.CTkCanvas):
        for col in range(self.columns):
            for row in range(self.rows):
                x1 = self.canvas_padding + col * (
                    (self.width - 2 * self.canvas_padding) / self.columns
                )
                y1 = self.canvas_padding + row * (
                    (self.height - 2 * self.canvas_padding) / self.rows
                )
                x2 = self.canvas_padding + (col + 1) * (
                    (self.width - 2 * self.canvas_padding) / self.columns
                )
                y2 = self.canvas_padding + (row + 1) * (
                    (self.height - 2 * self.canvas_padding) / self.rows
                )

                canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def _create_game_labels(self):
        self.Player_turn_label = self._create_label(
            f"Player {self.current_player.identifier} starts the game!"
        )
        self.Player_turn_label.place(relx=0.5, rely=0.95, anchor="center")

        self.player_one_score_label = self._create_label(
            f"Player 1: {self.player_one.wins}"
        )
        self.player_one_score_label.place(relx=0.1, rely=0.05, anchor="center")

        self.player_two_score_label = self._create_label(
            f"Player 2: {self.player_two.wins}"
        )
        self.player_two_score_label.place(relx=0.9, rely=0.05, anchor="center")

    def _create_button(
        self,
        title: str,
        command: callable,
        x_ratio: float = 0.22,
        y_ratio: float = 0.085,
    ) -> ctk.CTkButton:
        button_width = self.width * x_ratio
        button_height = self.height * y_ratio

        return ctk.CTkButton(
            self.root,
            text=title,
            command=command,
            width=button_width,
            height=button_height,
            font=self.font,
        )

    def _update_label(self, label: ctk.CTkLabel, new_text: str) -> ctk.CTkLabel:
        label.destroy()
        return self._create_label(new_text)

    def _create_label(self, text: str, text_color="#1f6aa5") -> ctk.CTkLabel:
        return ctk.CTkLabel(self.root, text=text, font=self.font, text_color=text_color)

    def _set_settings(self, appearence: str = "dark", theme: str = "blue"):
        ctk.set_appearance_mode(appearence)
        ctk.set_default_color_theme(theme)
