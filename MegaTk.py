import tkinter as tk
import random


def loteria():
    numero = int(apostas.get())
    lista.delete(0, 'end')  # Limpar a lista antes de adicionar novos itens
    for _ in range(numero):
        sorteio = sorted(random.sample(range(1, 61), 6))  # Usar sorted() diretamente ao invés de sorteio.sort()
        lista.insert('end', " ".join(map(str, sorteio)))  # Usar 'end' para inserir no final da lista


def limpar_apostas():
    lista.delete(0, 'end')


if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Megasena")

    lbApostas = tk.Label(janela, text="Digite o número de apostas: ")
    lbApostas.place(x=10, y=20)

    apostas = tk.Entry(janela)
    apostas.place(x=230, y=20, width=45)
    apostas.focus_set()

    btGerar = tk.Button(janela, text="Gerar", width=12, command=loteria)
    btGerar.place(x=280, y=16)

    lista = tk.Listbox(janela)
    lista.place(x=10, y=60, width=180)

    btLimpar = tk.Button(janela, text="Limpar apostas", width=12, command=limpar_apostas)
    btLimpar.place(x=280, y=50)

    btApagar = tk.Button(janela, text="Apagar jogo", width=10, command=lambda: lista.delete(tk.ANCHOR))
    btApagar.place(x=10, y=260)

    janela.geometry("430x300+200+200")
    janela.mainloop()
