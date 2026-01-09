import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from core import exibir_nova_pergunta, reiniciar_jogo
import warnings
import os

# Suprimir avisos do pkg_resources
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

# Configurações
CAMINHO_IMAGEM = "milhao.png"
CAMINHO_BANCO = "perguntas.sqlite"

def verificar_recursos():
    """Verifica se todos os recursos necessários existem"""
    recursos_faltando = []
    
    if not os.path.exists(CAMINHO_IMAGEM):
        recursos_faltando.append(CAMINHO_IMAGEM)
    
    if not os.path.exists(CAMINHO_BANCO):
        recursos_faltando.append(CAMINHO_BANCO)
    
    if recursos_faltando:
        print("AVISO: Os seguintes recursos não foram encontrados:")
        for recurso in recursos_faltando:
            print(f"  - {recurso}")
        return False
    
    return True


def criar_interface(janela):
    """Cria todos os elementos da interface gráfica"""
    # Título e imagem
    janela.title("Jogo do Milhão")
    janela.geometry("640x380+200+200")
    janela.resizable(0, 0)
    
    # Imagem do jogo
    if os.path.exists(CAMINHO_IMAGEM):
        try:
            image = tk.PhotoImage(file=CAMINHO_IMAGEM)
            image = image.subsample(1, 1)
            labelimage = tk.Label(janela, image=image)
            labelimage.image = image  # Manter referência
            labelimage.place(x=470, y=30)
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            criar_fallback_imagem(janela)
    else:
        criar_fallback_imagem(janela)
    
    # Label da pergunta (SEM BORDA/RELIEF)
    pergunta_label = ttk.Label(
        janela, 
        text="", 
        font=('Arial', 14), 
        justify=LEFT, 
        anchor=W, 
        wraplength=380,
    )
    pergunta_label.place(x=10, y=10, width=380, height=85)
    
    # Label de resultado
    label_resultado = ttk.Label(
        janela, 
        text="", 
        font=('Arial', 11, 'bold'), 
        bootstyle=WARNING,
        anchor="center"
    )
    label_resultado.place(x=10, y=250, width=380, height=30)
    
    # Label de pontuação
    label_pontuacao = ttk.Label(
        janela, 
        text="Pontuação: 0", 
        font=('Arial', 12, 'bold'),
        bootstyle="info"
    )
    label_pontuacao.place(x=10, y=285, width=380, height=25)
    
    # Label de nível
    label_nivel_pergunta = ttk.Label(
        janela, 
        text="Nível: 1", 
        font=('Arial', 10)
    )
    label_nivel_pergunta.place(x=10, y=315, width=100, height=25)
    
    # Label de contagem de perguntas
    label_qtd_perguntas = ttk.Label(
        janela, 
        text="Pergunta 0", 
        font=('Arial', 10)
    )
    label_qtd_perguntas.place(x=120, y=315, width=100, height=25)
    
    # Frame para botões de controle
    frame_controle = ttk.Frame(janela)
    frame_controle.place(x=420, y=200, width=200, height=150)
    
    # Botão de reiniciar
    btn_reiniciar = ttk.Button(
        frame_controle,
        text="🔄 Reiniciar Jogo",
        bootstyle="success-outline",
        width=20,
        command=lambda: reiniciar_interface(janela, pergunta_label, label_resultado, 
                                          label_pontuacao, label_nivel_pergunta, 
                                          label_qtd_perguntas)
    )
    btn_reiniciar.pack(pady=10, padx=20, fill=tk.X)
    
    # Botão de informações
    btn_info = ttk.Button(
        frame_controle,
        text="ℹ️ Informações",
        bootstyle="info-outline",
        width=20,
        command=mostrar_informacoes
    )
    btn_info.pack(pady=5, padx=20, fill=tk.X)
    
    # Botão de sair (CORRIGIDO: janela.destroy em vez de janela.quit)
    btn_sair = ttk.Button(
        frame_controle,
        text="🚪 Sair",
        bootstyle="danger-outline",
        width=20,
        command=janela.destroy  # CORREÇÃO AQUI
    )
    btn_sair.pack(pady=10, padx=20, fill=tk.X)
    
    return pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas


def criar_fallback_imagem(janela):
    """Cria uma imagem de fallback caso a original não exista"""
    fallback_frame = ttk.Frame(janela, bootstyle="dark")
    fallback_frame.place(x=420, y=50, width=200, height=200)
    
    titulo = ttk.Label(
        fallback_frame,
        text="JOGO DO\nMILHÃO",
        font=('Arial', 20, 'bold'),
        bootstyle="inverse-dark",
        justify="center"
    )
    titulo.pack(expand=True, fill='both', padx=10, pady=10)


def reiniciar_interface(janela, pergunta_label, label_resultado, label_pontuacao, 
                        label_nivel_pergunta, label_qtd_perguntas):
    """Reinicia toda a interface do jogo"""
    # Limpar botões de respostas
    for widget in janela.winfo_children():
        if isinstance(widget, ttk.Button) and widget.winfo_y() >= 110:
            widget.destroy()
    
    # Reiniciar jogo no core
    reiniciar_jogo()
    
    # Resetar labels
    pergunta_label.config(text="Preparando novo jogo...")
    label_resultado.config(text="")
    label_pontuacao.config(text="Pontuação: 0")
    label_nivel_pergunta.config(text="Nível: 1")
    label_qtd_perguntas.config(text="Pergunta 0")
    
    # Iniciar novo jogo após breve delay
    janela.after(1000, lambda: exibir_nova_pergunta(
        janela, pergunta_label, label_resultado, label_pontuacao, 
        label_nivel_pergunta, label_qtd_perguntas
    ))


def mostrar_informacoes():
    """Mostra informações sobre o jogo"""
    import tkinter.messagebox as messagebox
    
    info_texto = """
    JOGO DO MILHÃO
    
    Como jogar:
    1. Leia a pergunta cuidadosamente
    2. Clique na resposta que acha correta
    3. Ganhe 1000 pontos × nível por acerto
    
    Níveis:
    • Nível 1: Perguntas mais fáceis
    • Nível 5: Perguntas mais difíceis
    
    O nível aumenta a cada 3 perguntas!
    
    Desenvolvido com Python, Tkinter e SQLite
    """
    
    messagebox.showinfo("Sobre o Jogo", info_texto)


if __name__ == "__main__":
    # Verificar recursos
    if not verificar_recursos():
        print("Alguns recursos não foram encontrados, mas o jogo pode funcionar com limitações.")
    
    # Criar janela principal
    janela = ttk.Window(themename="darkly")
    
    # Criar interface
    elementos = criar_interface(janela)
    pergunta_label, label_resultado, label_pontuacao, label_nivel_pergunta, label_qtd_perguntas = elementos
    
    # Iniciar o jogo
    try:
        janela.after(500, lambda: exibir_nova_pergunta(
            janela, pergunta_label, label_resultado, label_pontuacao, 
            label_nivel_pergunta, label_qtd_perguntas
        ))
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        pergunta_label.config(text=f"Erro: {str(e)[:50]}...")
    
    # Iniciar loop principal
    janela.mainloop()
