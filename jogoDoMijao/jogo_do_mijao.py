import sqlite3
import random
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Conectar ao banco de dados
conn = sqlite3.connect('F:\\dev\\tkinter\\jogoMilhao\\perguntas.sqlite')
cursor = conn.cursor()

# Lista para armazenar todas as perguntas
todas_perguntas = []

# Variável para rastrear a pontuação
pontuacao = 0

# Função para selecionar todas as perguntas do banco de dados e embaralhá-las
def carregar_perguntas():
    global todas_perguntas
    cursor.execute("SELECT pergunta, resposta1, resposta2, resposta3, resposta4, resposta_certa, tipo FROM perguntas")
    todas_perguntas.extend(cursor.fetchall())
    random.shuffle(todas_perguntas)

# Função para exibir uma nova pergunta
def exibir_nova_pergunta():
    global todas_perguntas
    if not todas_perguntas:
        carregar_perguntas()
    
    pergunta, resposta1, resposta2, resposta3, resposta4, resposta_certa, tipo = todas_perguntas.pop()

    # Embaralhar as respostas
    respostas = [resposta1, resposta2, resposta3, resposta4]
    random.shuffle(respostas)

    # Exibir a nova pergunta
    pergunta_label.config(text=pergunta)

    # Exibir as novas respostas como botões
    for i, resposta in enumerate(respostas):
        botao_resposta = ttk.Button(janela, text=resposta, command=lambda resp=resposta, correta=resposta_certa: verificar_resposta(resp, correta))
        botao_resposta.place(x=10, y=70 + i*30, width=380, height=30)
        # Verificar se a resposta é a correta ao criar o botão
        if resposta == resposta_certa:
            botao_resposta.resposta_certa = True
        else:
            botao_resposta.resposta_certa = False

    # Resetar a label de resultado
    label_resultado["text"] = ""

# Função para verificar a resposta selecionada
def verificar_resposta(resposta_selecionada, resposta_certa):
    global pontuacao
    if resposta_certa:  # Comparar com a resposta correta
        pontuacao += 1000
        label_resultado["text"] = 'Parabéns! A resposta está correta.'
    else:
        label_resultado["text"] = 'Infelizmente, a resposta está incorreta.'

    # Atualizar label de pontuação
    label_pontuacao["text"] = f'Pontuação: {pontuacao}'

    # Exibir a próxima pergunta após 2 segundos
    janela.after(2000, exibir_nova_pergunta)

if __name__ == "__main__":
    # Criar a janela
    janela = ttk.Window(themename="flatly")
    janela.geometry("700x400+200+200")
    

    # Criar o rótulo da pergunta
    pergunta_label = ttk.Label(janela, text="", font=('Arial', 16))
    pergunta_label.place(x=10, y=10, width=380, height=50)

    # Criar o rótulo de resultado
    label_resultado = ttk.Label(janela, text="", foreground="blue", font="-weight bold")
    label_resultado.place(x=10, y=250, width=380, height=30)

    # Criar o rótulo de pontuação inicial
    label_pontuacao = ttk.Label(janela, text="Pontuação: 0", font=('Arial', 12))
    label_pontuacao.place(x=10, y=300, width=380, height=30)

    # Exibir a primeira pergunta
    exibir_nova_pergunta()

    # Exibir a janela
    janela.mainloop()
