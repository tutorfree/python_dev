import tkinter as tk
from tkinter import messagebox

class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")
        self.root.resizable(False, False)

        # Estado
        self.tabuleiro = [""] * 9
        self.jogador = "X"
        self.em_jogo = True

        # UI
        self.top = tk.Frame(root, padx=12, pady=12)
        self.top.pack(fill="x")

        self.status = tk.Label(self.top, text=f"Vez de: {self.jogador}", font=("Segoe UI", 12, "bold"))
        self.status.pack(side="left")

        tk.Button(self.top, text="Reiniciar", command=self.reiniciar, font=("Segoe UI", 10)).pack(side="right")

        self.grid = tk.Frame(root, padx=12, pady=12)
        self.grid.pack()

        self.botoes = []
        for i in range(9):
            btn = tk.Button(
                self.grid,
                text="",
                width=6,
                height=3,
                font=("Segoe UI", 18, "bold"),
                command=lambda i=i: self.jogar(i)
            )
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=6)
            self.botoes.append(btn)

    def linhas_vitoria(self):
        return [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]

    def checar_vencedor(self):
        for a, b, c in self.linhas_vitoria():
            if self.tabuleiro[a] and self.tabuleiro[a] == self.tabuleiro[b] == self.tabuleiro[c]:
                return self.tabuleiro[a], (a, b, c)
        if all(self.tabuleiro):
            return "EMPATE", None
        return None, None

    def jogar(self, i):
        if not self.em_jogo or self.tabuleiro[i]:
            return

        self.tabuleiro[i] = self.jogador
        self.botoes[i].config(text=self.jogador)

        vencedor, linha = self.checar_vencedor()
        if vencedor:
            self.em_jogo = False
            if vencedor == "EMPATE":
                messagebox.showinfo("Fim de jogo", "Deu empate!")
            else:
                # Destaque simples da linha vencedora
                if linha:
                    for idx in linha:
                        self.botoes[idx].config(bg="#c7d2fe")  # indigo-200
                messagebox.showinfo("Fim de jogo", f"{vencedor} venceu!")
            self.status.config(text="Fim de jogo")
            return

        self.jogador = "O" if self.jogador == "X" else "X"
        self.status.config(text=f"Vez de: {self.jogador}")

    def reiniciar(self):
        self.tabuleiro = [""] * 9
        self.jogador = "X"
        self.em_jogo = True
        self.status.config(text=f"Vez de: {self.jogador}")
        for b in self.botoes:
            b.config(text="", bg=self.root.cget("bg"))

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoDaVelha(root)
    root.mainloop()
