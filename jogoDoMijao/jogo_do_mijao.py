import sqlite3
import tkinter as tk
import random

# Conectar ao banco de dados
conn = sqlite3.connect('F:\\dev\\tkinter\\jogoMilhao\\perguntas.sqlite')
cursor = conn.cursor()

# Criar a janela Tkinter
janela = tk.Tk()
janela.geometry("400x400+200+200")

# Lista para rastrear perguntas já exibidas
perguntas_exibidas = []

# Lista para armazenar todas as perguntas
todas_perguntas = []

# Variável para rastrear a pontuação
pontuacao = 0

# Função para selecionar todas as perguntas do banco de dados e embaralhá-las
def carregar_perguntas():
    cursor.execute("SELECT pergunta, resposta1, resposta2, resposta3, resposta4, resposta_certa, tipo FROM perguntas")
    todas_perguntas.extend(cursor.fetchall())
    random.shuffle(todas_perguntas)

# Função para exibir uma nova pergunta
def exibir_nova_pergunta():
    global pontuacao, perguntas_exibidas
    
    if not todas_perguntas:
        carregar_perguntas()
    
    pergunta, *respostas, resposta_certa, tipo = todas_perguntas.pop()

    # Exibir a nova pergunta
    pergunta_label["text"] = pergunta

    # Exibir as novas respostas como botões
    for resposta in respostas:
        botao_resposta = tk.Button(janela, text=resposta, command=lambda resp=resposta, correta=resposta_certa, tipo=tipo, respostas=respostas: verificar_resposta(resp, correta, tipo, respostas))
        botao_resposta.place(x=10, y=70 + respostas.index(resposta)*30, width=380, height=30)

    # Resetar a label de resultado
    label_resultado["text"] = ""

    # print("Respostas:", respostas)
    # print("Resposta correta:", resposta_certa)


# Função para verificar a resposta selecionada
def verificar_resposta(resposta_selecionada, resposta_certa, tipo, respostas):
    global pontuacao
    print("Resposta selecionada:", resposta_selecionada)
    print("Resposta correta:", resposta_certa)

    if resposta_selecionada == respostas[int(resposta_certa) - 1]:  # Comparar com a resposta correta
        pontuacao += 1000 if tipo == 'A' else 5000
        label_resultado["text"] = 'Parabéns! A resposta está correta.'
    else:
        label_resultado["text"] = 'Infelizmente, a resposta está incorreta.'

    # Atualizar label de pontuação
    label_pontuacao["text"] = f'Pontuação: {pontuacao}'

    # Exibir a próxima pergunta após 2 segundos
    janela.after(2000, exibir_nova_pergunta)


# Criar o rótulo da pergunta
pergunta_label = tk.Label(janela, text="", font=('Arial', 16))
pergunta_label.config(anchor='w')
pergunta_label.place(x=10, y=10, width=380, height=50)

# Criar o rótulo de resultado
label_resultado = tk.Label(janela, text="", foreground="blue", font="-weight bold")
label_resultado.place(x=10, y=250, width=380, height=30)

# Criar o rótulo de pontuação inicial
label_pontuacao = tk.Label(janela, text="Pontuação: 0", font=('Arial', 12))
label_pontuacao.place(x=10, y=300, width=380, height=30)

# Exibir a primeira pergunta
exibir_nova_pergunta()

# Exibir a janela
janela.mainloop()
