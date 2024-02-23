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

# Variável para rastrear a quantidade de perguntas geradas
qtd_perguntas_geradas = 0

# Referência ao último botão clicado
ultimo_botao_clicado = None

# Função para selecionar todas as perguntas do banco de dados e embaralhá-las
def carregar_perguntas():
    global todas_perguntas
    cursor.execute("SELECT pergunta, resposta1, resposta2, resposta3, resposta4, resposta_certa, tipo FROM perguntas")
    todas_perguntas.extend(cursor.fetchall())
    random.shuffle(todas_perguntas)


def exibir_nova_pergunta():
    global todas_perguntas, qtd_perguntas_geradas
    if not todas_perguntas:
        carregar_perguntas()

    if todas_perguntas:
        pergunta, *respostas, resposta_certa, tipo = todas_perguntas.pop()

        # Verificar se a resposta está correta antes do embaralhamento
        resposta_index = int(resposta_certa) - 1
        resposta_certa_texto = respostas[resposta_index]

        # Embaralhar as respostas
        random.shuffle(respostas)

        # Exibir a nova pergunta
        pergunta_label.config(text=pergunta)

        # Exibir o nível da pergunta
        label_nivel_pergunta.config(text=f'Nível: {tipo}')

        # Exibir as novas respostas como botões
        espacamento_vertical = 5
        for i, resposta in enumerate(respostas):
            botao_resposta = ttk.Button(janela, text=resposta, command=lambda resp=resposta, correta=resposta_certa_texto, tipo=tipo, respostas=respostas: verificar_resposta(resp, correta, tipo, respostas))
            botao_resposta.place(x=10, y=110 + (30 + espacamento_vertical) * i, width=380, height=30)

        # Atualizar a contagem de perguntas geradas
        qtd_perguntas_geradas += 1
        label_qtd_perguntas.config(text=f'Pergunta {qtd_perguntas_geradas}')

        # Resetar a label de resultado
        label_resultado.config(text="")
    else:
        # Se não houver mais perguntas, exibir uma mensagem ou tomar outra ação adequada
        print("Não há mais perguntas disponíveis.")


def verificar_resposta(resposta_selecionada, resposta_certa, tipo, respostas):
    # Definindo pontuacao como variavel global
    global pontuacao
    # Convertendo tipo para um inteiro
    tipo = int(tipo) 
    # Marcar o botão clicado com o correto ou incorreto
    for botao in janela.winfo_children():
        if isinstance(botao, ttk.Button) and botao.cget('text') == resposta_selecionada:
            if resposta_selecionada == resposta_certa:
                botao.config(bootstyle=SUCCESS)
                if tipo == 1:
                    pontuacao += 1000
                elif tipo == 2:
                    pontuacao += 5000
                elif tipo == 3:
                    pontuacao += 10000
                elif tipo == 4:
                    pontuacao += 50000
                elif tipo == 5:
                    pontuacao += 1000000
                label_resultado.config(text='Parabéns! A resposta está correta.')
            else:
                botao.config(bootstyle=DANGER)
                label_resultado.config(text='Infelizmente, a resposta está incorreta.')

    # Atualizar label de pontuação
    label_pontuacao.config(text=f'Pontuação: {pontuacao}')

    # Exibir a próxima pergunta após 2 segundos
    janela.after(2000, exibir_nova_pergunta)


if __name__ == "__main__":
    # Criar a janela
    janela = ttk.Window(themename="darkly")
    janela.geometry("640x380+200+200")
    janela.title("Jogo do Milhão")

    # Gera o quadro da imagem decorativa
    image = tk.PhotoImage(file="tkinter\\jogoMilhao\\silvio2.png")
    image = image.subsample(1,1)
    labelimage = tk.Label(image=image)
    labelimage.place(x=430, y=50)

    # Criar o rótulo da pergunta
    pergunta_label = ttk.Label(janela, text="", font=('Arial', 16), justify=LEFT, anchor=W, wraplength=380)
    pergunta_label.place(x=10, y=10, width=380, height=75)

    # Criar o rótulo de resultado
    label_resultado = ttk.Label(janela, text="", font="-weight bold", bootstyle=WARNING)
    label_resultado.place(x=10, y=250, width=380, height=30)

    # Criar o rótulo de pontuação inicial
    label_pontuacao = ttk.Label(janela, text="Pontuação: 0", font=('Arial', 12))
    label_pontuacao.place(x=10, y=300, width=380, height=30)

    # Criar o rótulo do nível da pergunta
    label_nivel_pergunta = ttk.Label(janela, text="Nível: ", font=('Arial', 10))
    label_nivel_pergunta.place(x=10, y=330, width=380, height=30)

    # Criar o rótulo da quantidade de perguntas geradas
    label_qtd_perguntas = ttk.Label(janela, text="Pergunta 0", font=('Arial', 10))
    label_qtd_perguntas.place(x=90, y=330, width=100, height=30)

    # Exibir a primeira pergunta
    exibir_nova_pergunta()

    # Exibir a janela
    janela.mainloop()
