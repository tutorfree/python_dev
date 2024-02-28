import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from core import exibir_nova_pergunta
import pkgutil

if __name__ == "__main__":
    janela = ttk.Window(themename="darkly")
    janela.geometry("640x380+200+200")
    janela.title("Jogo do Milhão")
    
    image = tk.PhotoImage(file="E:\\dev\\tkinter\\jogoMilhao\\silvio2.png")
    image = image.subsample(1, 1)
    labelimage = tk.Label(image=image)
    labelimage.place(x=430, y=50)

    pergunta_label = ttk.Label(janela, text="", font=('Arial', 16), justify=LEFT, anchor=W, wraplength=380)
    pergunta_label.place(x=10, y=10, width=380, height=75)

    label_resultado = ttk.Label(janela, text="", font="-weight bold", bootstyle=WARNING)
    label_resultado.place(x=10, y=250, width=380, height=30)

    label_pontuacao = ttk.Label(janela, text="Pontuação: 0", font=('Arial', 12))
    label_pontuacao.place(x=10, y=300, width=380, height=30)

    label_nivel_pergunta = ttk.Label(janela, text="Nível: ", font=('Arial', 10))
    label_nivel_pergunta.place(x=10, y=330, width=380, height=30)

    label_qtd_perguntas = ttk.Label(janela, text="Pergunta 0", font=('Arial', 10))
    label_qtd_perguntas.place(x=90, y=330, width=100, height=30)

    exibir_nova_pergunta(janela, pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas)

    janela.mainloop()
