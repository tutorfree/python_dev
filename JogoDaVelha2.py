# jogo_da_velha_tk.py
# Python 3 + Tkinter (GUI)
# Execute: python jogo_da_velha_tk.py

import tkinter as tk
from tkinter import messagebox

THEME = {
    "bg": "#0b1020",
    "panel": "#121a33",
    "panel2": "#0f1630",
    "text": "#e9ecff",
    "muted": "#b8c0ff",
    "line": "#273056",
    "x": "#7c5cff",
    "o": "#22d3ee",
    "win": "#34d399",
    "button": "#1a2446",
    "button_hover": "#22305a",
    "danger": "#fb7185",
}

FONT_UI = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI Semibold", 14)
FONT_CELL = ("Segoe UI Black", 28)

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Velha — Tkinter")
        self.minsize(420, 520)
        self.configure(bg=THEME["bg"])

        # Estado
        self.board = [None] * 9
        self.turn = "X"
        self.locked = False
        self.score = {"X": 0, "O": 0, "D": 0}

        # Layout
        self._build_ui()
        self._bind_keys()
        self._update_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["bg"])
        header.pack(fill="x", padx=16, pady=(16, 10))

        title_row = tk.Frame(header, bg=THEME["bg"])
        title_row.pack(fill="x")

        self.title_lbl = tk.Label(
            title_row,
            text="Jogo da Velha",
            fg=THEME["text"],
            bg=THEME["bg"],
            font=FONT_TITLE
        )
        self.title_lbl.pack(side="left")

        self.turn_lbl = tk.Label(
            title_row,
            text="Vez: X",
            fg=THEME["muted"],
            bg=THEME["bg"],
            font=FONT_UI
        )
        self.turn_lbl.pack(side="right")

        # Score
        score = tk.Frame(self, bg=THEME["panel2"], highlightthickness=1, highlightbackground=THEME["line"])
        score.pack(fill="x", padx=16, pady=(0, 12))

        self.score_lbl = tk.Label(
            score,
            text="Placar — X: 0   O: 0   Empates: 0",
            fg=THEME["text"],
            bg=THEME["panel2"],
            font=FONT_UI,
            padx=10,
            pady=10
        )
        self.score_lbl.pack(fill="x")

        # Board
        board_frame = tk.Frame(self, bg=THEME["panel"], highlightthickness=1, highlightbackground=THEME["line"])
        board_frame.pack(fill="both", expand=True, padx=16, pady=0)

        grid = tk.Frame(board_frame, bg=THEME["panel"])
        grid.pack(expand=True, padx=14, pady=14)

        self.buttons = []
        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                btn = tk.Button(
                    grid,
                    text="",
                    width=4,
                    height=2,
                    font=FONT_CELL,
                    fg=THEME["text"],
                    bg=THEME["button"],
                    activebackground=THEME["button_hover"],
                    activeforeground=THEME["text"],
                    relief="flat",
                    bd=0,
                    highlightthickness=1,
                    highlightbackground=THEME["line"],
                    command=lambda i=idx: self.play(i)
                )
                btn.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
                self.buttons.append(btn)

        for i in range(3):
            grid.grid_rowconfigure(i, weight=1)
            grid.grid_columnconfigure(i, weight=1)

        # Footer controls
        footer = tk.Frame(self, bg=THEME["bg"])
        footer.pack(fill="x", padx=16, pady=16)

        self.new_btn = tk.Button(
            footer, text="Novo jogo (N)", font=FONT_UI,
            fg=THEME["text"], bg=THEME["x"],
            activebackground=THEME["x"], activeforeground=THEME["text"],
            relief="flat", bd=0, padx=12, pady=10,
            command=self.new_game
        )
        self.new_btn.pack(side="left", fill="x", expand=True)

        self.reset_btn = tk.Button(
            footer, text="Zerar placar (R)", font=FONT_UI,
            fg=THEME["text"], bg=THEME["button"],
            activebackground=THEME["button_hover"], activeforeground=THEME["text"],
            relief="flat", bd=0, padx=12, pady=10,
            command=self.reset_score
        )
        self.reset_btn.pack(side="left", fill="x", expand=True, padx=(10, 0))

    def _bind_keys(self):
        self.bind("<n>", lambda e: self.new_game())
        self.bind("<N>", lambda e: self.new_game())
        self.bind("<r>", lambda e: self.reset_score())
        self.bind("<R>", lambda e: self.reset_score())
        self.bind("<Escape>", lambda e: self.destroy())

    def _update_ui(self, win_line=None):
        self.turn_lbl.config(text=f"Vez: {self.turn}" + (" (fim)" if self.locked else ""))
        self.score_lbl.config(
            text=f"Placar — X: {self.score['X']}   O: {self.score['O']}   Empates: {self.score['D']}"
        )

        for i, btn in enumerate(self.buttons):
            val = self.board[i]
            btn.config(text=val if val else "")
            if val == "X":
                btn.config(fg=THEME["x"])
            elif val == "O":
                btn.config(fg=THEME["o"])
            else:
                btn.config(fg=THEME["text"])

            # Destaque vitória / reset estilo
            if win_line and i in win_line:
                btn.config(bg=THEME["win"], fg=THEME["panel2"])
            else:
                btn.config(bg=THEME["button"])

            # Travar botões preenchidos ou jogo finalizado
            state = "disabled" if (self.locked or val is not None) else "normal"
            btn.config(state=state)

    def winner(self):
        lines = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a,b,c in lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], (a,b,c)
        if all(v is not None for v in self.board):
            return "D", None
        return None, None

    def play(self, idx):
        if self.locked or self.board[idx] is not None:
            return

        self.board[idx] = self.turn
        result, line = self.winner()

        if result in ("X", "O"):
            self.locked = True
            self.score[result] += 1
            self._update_ui(win_line=line)
            messagebox.showinfo("Fim de jogo", f"{result} venceu!")
            return

        if result == "D":
            self.locked = True
            self.score["D"] += 1
            self._update_ui()
            messagebox.showinfo("Fim de jogo", "Empate!")
            return

        self.turn = "O" if self.turn == "X" else "X"
        self._update_ui()

    def new_game(self):
        self.board = [None] * 9
        self.turn = "X"
        self.locked = False
        self._update_ui()

    def reset_score(self):
        if messagebox.askyesno("Confirmar", "Zerar o placar?"):
            self.score = {"X": 0, "O": 0, "D": 0}
            self.new_game()

if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
