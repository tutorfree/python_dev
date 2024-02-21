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

# Variável para rastrear a pontuação
pontuacao = 0

# Função para selecionar uma nova pergunta não exibida
def selecionar_nova_pergunta():
    global perguntas_exibidas  # Adicionando a variável global
    # Selecionar todas as perguntas do banco de dados
    cursor.execute("SELECT pergunta, resposta1, resposta2, resposta3, resposta4, resposta_certa, tipo FROM perguntas")
    todas_perguntas = cursor.fetchall()

    # Embaralhar a ordem das perguntas
    random.shuffle(todas_perguntas)

    # Selecionar uma pergunta que não foi exibida
    for pergunta in todas_perguntas:
        if pergunta[0] not in perguntas_exibidas:
            return pergunta

    # Se todas as perguntas já foram exibidas, reiniciar a lista de perguntas exibidas
    perguntas_exibidas.clear()
    return todas_perguntas[0]

# Variável para rastrear se a próxima pergunta já foi exibida
proxima_pergunta_exibida = False

# Função para exibir uma nova pergunta
def exibir_nova_pergunta():
    global pontuacao, proxima_pergunta_exibida
    if not proxima_pergunta_exibida:
        pergunta, *respostas, resposta_certa, tipo = selecionar_nova_pergunta()

        # Exibir a nova pergunta
        pergunta_label["text"] = pergunta

        # Exibir as novas respostas como botões
        for resposta in respostas:
            botao_resposta = tk.Button(janela, text=resposta, command=lambda resp=resposta: verificar_resposta(resp, str(resposta_certa), tipo))
            botao_resposta.place(x=10, y=70 + respostas.index(resposta)*30, width=380, height=30)

        # Resetar a label de resultado
        label_resultado["text"] = ""

        # Marcar que a próxima pergunta foi exibida
        proxima_pergunta_exibida = True

# Função para verificar a resposta selecionada
def verificar_resposta(resposta_selecionada, resposta_certa, tipo):
    global pontuacao, proxima_pergunta_exibida
    if resposta_selecionada == resposta_certa:
        pontuacao += 1000 if tipo == 'A' else 5000
        label_resultado["text"] = 'Parabéns! A resposta está correta.'
    else:
        label_resultado["text"] = 'Infelizmente, a resposta está incorreta.'

    # Atualizar label de pontuação
    label_pontuacao["text"] = f'Pontuação: {pontuacao}'

    # Aguardar 3 segundos antes de marcar que a próxima pergunta pode ser exibida
    janela.after(3000, lambda: setattr(proxima_pergunta_exibida, False, exibir_nova_pergunta))
    janela.update()  # Forçar a atualização da janela

# Criar o rótulo da pergunta
pergunta_label = tk.Label(janela, text="", font=('Arial', 16))
pergunta_label.pack(pady=10)

# Criar o frame para os botões de resposta
frame_respostas = tk.Frame(janela)
frame_respostas.pack(pady=10)

# Criar o rótulo de resultado
label_resultado = tk.Label(janela, text="", foreground="blue", font="-weight bold")
label_resultado.pack()

# Criar o rótulo de pontuação inicial
label_pontuacao = tk.Label(janela, text="Pontuação: 0", font=('Arial', 12))
label_pontuacao.pack()

# Exibir a primeira pergunta
exibir_nova_pergunta()

janela.mainloop()
