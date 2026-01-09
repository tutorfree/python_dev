import sqlite3
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pygame
import warnings

# Suprimir avisos do pkg_resources do pygame
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

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

# Flag para controle de fim de jogo
jogo_ativo = True

# Variável para armazenar a resposta correta atual
resposta_correta_atual = None


def carregar_perguntas():
    """Carrega todas as perguntas do banco e organiza por nível"""
    global perguntas_por_nivel
    cursor.execute("SELECT pergunta, resposta1, resposta2, resposta3, resposta4, resposta_certa, tipo FROM perguntas")
    todas_perguntas = cursor.fetchall()
    
    for tipo in range(1, 6):
        perguntas_por_nivel[tipo] = [pergunta for pergunta in todas_perguntas if pergunta[-1] == str(tipo)]
        random.shuffle(perguntas_por_nivel[tipo])


def limpar_botoes_respostas(janela):
    """Remove todos os botões de resposta da tela"""
    for widget in janela.winfo_children():
        if isinstance(widget, ttk.Button) and widget.winfo_y() >= 110:
            widget.destroy()


def obter_pergunta_disponivel():
    """Obtém uma pergunta disponível considerando o nível atual"""
    global qtd_perguntas_geradas
    
    if not perguntas_por_nivel:
        carregar_perguntas()
    
    nivel = min(5, qtd_perguntas_geradas // 3 + 1)
    
    # Tenta encontrar perguntas no nível atual, se não, busca em níveis inferiores
    for n in range(nivel, 0, -1):
        if perguntas_por_nivel.get(n) and len(perguntas_por_nivel[n]) > 0:
            return perguntas_por_nivel[n].pop(), n
    
    return None, None


def exibir_nova_pergunta(janela, pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas):
    """Exibe uma nova pergunta na interface"""
    global qtd_perguntas_geradas, jogo_ativo, resposta_correta_atual
    
    if not jogo_ativo:
        return
    
    # Limpar botões de respostas anteriores
    limpar_botoes_respostas(janela)
    
    # Obter pergunta disponível
    pergunta_info, nivel = obter_pergunta_disponivel()
    
    if not pergunta_info:
        # Fim do jogo - sem mais perguntas
        pergunta_label.config(text="🎉 PARABÉNS! 🎉")
        label_resultado.config(text=f"Você respondeu todas as perguntas disponíveis!", bootstyle=INFO)
        label_nivel_pergunta.config(text=f"Pontuação Final: {pontuacao}")
        label_qtd_perguntas.config(text="Fim do Jogo!")
        jogo_ativo = False
        return
    
    # Desempacotar dados da pergunta
    pergunta, *respostas, resposta_certa, tipo = pergunta_info
    tipo = int(tipo)
    
    # Verificar se a resposta está correta antes do embaralhamento
    resposta_index = int(resposta_certa) - 1
    resposta_correta_atual = respostas[resposta_index]  # SALVAR A RESPOSTA CORRETA
    
    # Embaralhar as respostas
    respostas_embaralhadas = respostas.copy()
    random.shuffle(respostas_embaralhadas)
    
    # Exibir a nova pergunta
    pergunta_label.config(text=pergunta)
    
    # Exibir o nível da pergunta
    label_nivel_pergunta.config(text=f'Nível: {tipo}')
    
    # Atualizar contador de perguntas
    qtd_perguntas_geradas += 1
    label_qtd_perguntas.config(text=f'Pergunta {qtd_perguntas_geradas}')
    
    # Resetar label de resultado
    label_resultado.config(text="")
    
    # Criar botões para as respostas
    espacamento_vertical = 5
    for i, resposta in enumerate(respostas_embaralhadas):
        botao_resposta = ttk.Button(
            janela, 
            text=resposta,
            command=lambda resp=resposta: verificar_resposta(
                janela, resp, pergunta_label, label_resultado, 
                label_pontuacao, label_nivel_pergunta, label_qtd_perguntas
            )
        )
        botao_resposta.place(x=10, y=110 + (30 + espacamento_vertical) * i, width=380, height=30)


import sqlite3
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pygame
import warnings

# Suprimir avisos do pkg_resources do pygame
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

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

# Flag para controle de fim de jogo
jogo_ativo = True

# Variável para armazenar a resposta correta atual
resposta_correta_atual = None


def carregar_perguntas():
    """Carrega todas as perguntas do banco e organiza por nível"""
    global perguntas_por_nivel
    cursor.execute("SELECT pergunta, resposta1, resposta2, resposta3, resposta4, resposta_certa, tipo FROM perguntas")
    todas_perguntas = cursor.fetchall()
    
    for tipo in range(1, 6):
        perguntas_por_nivel[tipo] = [pergunta for pergunta in todas_perguntas if pergunta[-1] == str(tipo)]
        random.shuffle(perguntas_por_nivel[tipo])


def limpar_botoes_respostas(janela):
    """Remove todos os botões de resposta da tela"""
    for widget in janela.winfo_children():
        if isinstance(widget, ttk.Button) and widget.winfo_y() >= 110:
            widget.destroy()


def obter_pergunta_disponivel():
    """Obtém uma pergunta disponível considerando o nível atual"""
    global qtd_perguntas_geradas
    
    if not perguntas_por_nivel:
        carregar_perguntas()
    
    nivel = min(5, qtd_perguntas_geradas // 3 + 1)
    
    # Tenta encontrar perguntas no nível atual, se não, busca em níveis inferiores
    for n in range(nivel, 0, -1):
        if perguntas_por_nivel.get(n) and len(perguntas_por_nivel[n]) > 0:
            return perguntas_por_nivel[n].pop(), n
    
    return None, None


def exibir_nova_pergunta(janela, pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas):
    """Exibe uma nova pergunta na interface"""
    global qtd_perguntas_geradas, jogo_ativo, resposta_correta_atual
    
    if not jogo_ativo:
        return
    
    # Limpar botões de respostas anteriores
    limpar_botoes_respostas(janela)
    
    # Obter pergunta disponível
    pergunta_info, nivel = obter_pergunta_disponivel()
    
    if not pergunta_info:
        # Fim do jogo - sem mais perguntas
        pergunta_label.config(text="🎉 PARABÉNS! 🎉")
        label_resultado.config(text=f"Você respondeu todas as perguntas disponíveis!", bootstyle=INFO)
        label_nivel_pergunta.config(text=f"Pontuação Final: {pontuacao}")
        label_qtd_perguntas.config(text="Fim do Jogo!")
        jogo_ativo = False
        return
    
    # Desempacotar dados da pergunta
    pergunta, *respostas, resposta_certa, tipo = pergunta_info
    tipo = int(tipo)
    
    # Verificar se a resposta está correta antes do embaralhamento
    resposta_index = int(resposta_certa) - 1
    resposta_correta_atual = respostas[resposta_index]  # SALVAR A RESPOSTA CORRETA
    
    # Embaralhar as respostas
    respostas_embaralhadas = respostas.copy()
    random.shuffle(respostas_embaralhadas)
    
    # Exibir a nova pergunta
    pergunta_label.config(text=pergunta)
    
    # Exibir o nível da pergunta
    label_nivel_pergunta.config(text=f'Nível: {tipo}')
    
    # Atualizar contador de perguntas
    qtd_perguntas_geradas += 1
    label_qtd_perguntas.config(text=f'Pergunta {qtd_perguntas_geradas}')
    
    # Resetar label de resultado
    label_resultado.config(text="")
    
    # Criar botões para as respostas
    espacamento_vertical = 5
    for i, resposta in enumerate(respostas_embaralhadas):
        botao_resposta = ttk.Button(
            janela, 
            text=resposta,
            command=lambda resp=resposta: verificar_resposta(
                janela, resp, pergunta_label, label_resultado, 
                label_pontuacao, label_nivel_pergunta, label_qtd_perguntas
            )
        )
        botao_resposta.place(x=10, y=110 + (30 + espacamento_vertical) * i, width=380, height=30)


def verificar_resposta(janela, resposta_selecionada, pergunta_label, label_resultado, 
                       label_pontuacao, label_nivel_pergunta, label_qtd_perguntas):
    """Verifica se a resposta selecionada está correta - VERSÃO ALTERNATIVA"""
    global pontuacao, jogo_ativo, resposta_correta_atual, qtd_perguntas_geradas
    
    if not jogo_ativo:
        return
    
    tipo = min(5, (qtd_perguntas_geradas - 1) // 3 + 1)
    acertou = resposta_selecionada == resposta_correta_atual
    
    # Remover comandos de todos os botões (impedir novos cliques)
    for botao in janela.winfo_children():
        if isinstance(botao, ttk.Button) and botao.winfo_y() >= 110:
            botao.config(command=None)  # Remove a função de clique
            
            texto_botao = botao.cget('text')
            
            if acertou:
                # Se acertou: botão clicado fica verde
                if texto_botao == resposta_selecionada:
                    botao.config(bootstyle="success")
            else:
                # Se errou: resposta correta em verde, resposta errada em vermelho
                if texto_botao == resposta_correta_atual:
                    botao.config(bootstyle="success")
                elif texto_botao == resposta_selecionada:
                    botao.config(bootstyle="danger")
    
    # Resto do código permanece igual...
    if acertou:
        pontuacao += 1000 * tipo
        label_resultado.config(text='✓ Parabéns! Resposta correta!', bootstyle="success")
        try:
            pygame.mixer.music.load('sound/acertou.mp3')
            pygame.mixer.music.play(0)
        except:
            print("Áudio de acerto não encontrado")
    else:
        label_resultado.config(
            text=f'✗ Resposta incorreta! A correta era: "{resposta_correta_atual}"', 
            bootstyle="danger"
        )
        try:
            pygame.mixer.music.load('sound/errou.mp3')
            pygame.mixer.music.play(0)
        except:
            print("Áudio de erro não encontrado")
    
    label_pontuacao.config(text=f'Pontuação: {pontuacao}')
    
    janela.after(3000, lambda: exibir_nova_pergunta(
        janela, pergunta_label, label_resultado, label_pontuacao, 
        label_nivel_pergunta, label_qtd_perguntas
    ))


def reiniciar_jogo():
    """Reinicia o jogo para um novo jogador"""
    global pontuacao, qtd_perguntas_geradas, perguntas_por_nivel, jogo_ativo, resposta_correta_atual
    
    pontuacao = 0
    qtd_perguntas_geradas = 0
    jogo_ativo = True
    resposta_correta_atual = None
    
    # Recarregar perguntas (embaralhar novamente)
    for nivel in perguntas_por_nivel:
        random.shuffle(perguntas_por_nivel[nivel])
    
    return True
