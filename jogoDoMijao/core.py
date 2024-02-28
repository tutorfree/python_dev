import sqlite3
import random
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pygame

# Conectar ao banco de dados
conn = sqlite3.connect('perguntas.sqlite')
cursor = conn.cursor()

# Dicionário para armazenar listas de perguntas para cada tipo/nível
perguntas_por_nivel = {}

# Inicializar o mixer do pygame para reprodução de áudio
pygame.mixer.init()

# Variável para rastrear a pontuação
pontuacao = 0

# Variável para rastrear a quantidade de perguntas geradas
qtd_perguntas_geradas = 0

# Referência ao último botão clicado
ultimo_botao_clicado = None


def carregar_perguntas():
    global perguntas_por_nivel
    cursor.execute("SELECT pergunta, resposta1, resposta2, resposta3, resposta4, resposta_certa, tipo FROM perguntas")
    todas_perguntas = cursor.fetchall()
    
    for tipo in range(1, 6):
        perguntas_por_nivel[tipo] = [pergunta for pergunta in todas_perguntas if pergunta[-1] == str(tipo)]
        random.shuffle(perguntas_por_nivel[tipo])


def exibir_nova_pergunta(janela, pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas):
    global perguntas_por_nivel, qtd_perguntas_geradas
    if not perguntas_por_nivel:
        carregar_perguntas()

    nivel = min(5, qtd_perguntas_geradas // 3 + 1)

    perguntas_nivel = perguntas_por_nivel.get(nivel, [])

    if perguntas_nivel:
        pergunta, *respostas, resposta_certa, tipo = perguntas_nivel.pop()

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
            botao_resposta = ttk.Button(janela, text=resposta, command=lambda resp=resposta, correta=resposta_certa_texto, tipo=tipo, respostas=respostas: verificar_resposta(janela, resp, correta, tipo, respostas, pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas))
            botao_resposta.place(x=10, y=110 + (30 + espacamento_vertical) * i, width=380, height=30)


        # Atualizar a contagem de perguntas geradas
        qtd_perguntas_geradas += 1
        label_qtd_perguntas.config(text=f'Pergunta {qtd_perguntas_geradas}')

        # Resetar a label de resultado
        label_resultado.config(text="")
    else:
        # Se não houver mais perguntas disponíveis para nenhum nível, exibir uma mensagem ou tomar outra ação adequada
        print("Não há mais perguntas disponíveis.")


def verificar_resposta(janela, resposta_selecionada, resposta_certa, tipo, respostas, pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas):
    global pontuacao
    tipo = int(tipo)
    
    for botao in janela.winfo_children():
        if isinstance(botao, ttk.Button) and botao.cget('text') == resposta_selecionada:
            if resposta_selecionada == resposta_certa:
                botao.config(bootstyle=SUCCESS)
                pontuacao += 1000 * tipo
                label_resultado.config(text='Parabéns! A resposta está correta.')
                pygame.mixer.music.load('sound//acertou.mp3')
                pygame.mixer.music.play(0)
            else:
                botao.config(bootstyle=DANGER)
                label_resultado.config(text='Infelizmente, a resposta está incorreta.')
                pygame.mixer.music.load('sound//errou.mp3')
                pygame.mixer.music.play(0)

    label_pontuacao.config(text=f'Pontuação: {pontuacao}')
    janela.after(3000, lambda: exibir_nova_pergunta(janela, pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas))
