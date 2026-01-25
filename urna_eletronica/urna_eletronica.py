import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil
import platform
import subprocess
import sys

# =========================
# FUNÇÕES MULTIPLATAFORMA
# =========================
def tocar_som(arquivo_som):
    """Toca som de forma multiplataforma"""
    sistema = platform.system().lower()
    
    if not os.path.exists(arquivo_som):
        return
    
    try:
        if sistema == "windows":
            import winsound
            winsound.PlaySound(arquivo_som, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif sistema == "darwin":
            subprocess.Popen(['afplay', arquivo_som],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)
        elif sistema == "linux":
            players = ['aplay', 'paplay', 'play', 'mpg123', 'mpg321']
            for player in players:
                try:
                    subprocess.run(['which', player], capture_output=True, check=True)
                    subprocess.Popen([player, arquivo_som],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL,
                                   start_new_session=True)
                    return
                except:
                    continue
    except Exception:
        pass

def atualizar_status():
    """Atualiza a barra de status com informações"""
    total_votos = sum(votos.values())
    status_text = f"🗳️ Urna Eletrônica | Sistema: {platform.system()} | Candidatos: {len(candidatos)} | Votos totais: {total_votos}"
    
    if hasattr(root, 'lbl_status'):
        root.lbl_status.config(text=status_text)
    
    return status_text

# =========================
# CONFIGURAÇÕES
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def caminho(*p):
    return os.path.join(BASE_DIR, *p)

# Criar diretórios
for pasta in ['sons', 'fotos']:
    os.makedirs(caminho(pasta), exist_ok=True)

SOM_TECLA = caminho("sons", "tecla.wav")
SOM_CONFIRMA = caminho("sons", "confirma.wav")
SOM_ERRO = caminho("sons", "erro.wav")

# =========================
# DADOS DOS CANDIDATOS
# =========================
candidatos_iniciais = {
    "11": {"nome": "Enzo", "foto": caminho("fotos", "11.png")},
    "12": {"nome": "José", "foto": caminho("fotos", "12.png")},
    "22": {"nome": "Chicão", "foto": caminho("fotos", "22.png")},
    "33": {"nome": "Zefinha", "foto": caminho("fotos", "33.png")},
    "34": {"nome": "Maria", "foto": caminho("fotos", "34.png")},
    "66": {"nome": "Onerildo", "foto": caminho("fotos", "66.png")},
}

def carregar_candidatos():
    candidatos = {}
    
    if os.path.exists(caminho("fotos")):
        for arquivo in os.listdir(caminho("fotos")):
            if arquivo.endswith(('.png', '.jpg', '.jpeg')):
                numero = arquivo.split('.')[0]
                if numero.isdigit() and len(numero) == 2:
                    nome = candidatos_iniciais.get(numero, {}).get('nome', f'Candidato {numero}')
                    candidatos[numero] = {
                        "nome": nome,
                        "foto": caminho("fotos", arquivo)
                    }
    
    if not candidatos:
        candidatos = candidatos_iniciais.copy()
        
    return candidatos

candidatos = carregar_candidatos()
votos = {k: 0 for k in candidatos}
voto = ""

# =========================
# FUNÇÕES DA URNA
# =========================
def digitar(n):
    global voto
    if len(voto) < 2:
        tocar_som(SOM_TECLA)
        voto += str(n)
        atualizar()

def corrigir():
    global voto
    tocar_som(SOM_ERRO)
    voto = ""
    atualizar()

def confirmar():
    global voto
    if voto in candidatos:
        votos[voto] += 1
        tocar_som(SOM_CONFIRMA)
        messagebox.showinfo("VOTO CONFIRMADO",
                          f"Voto para {candidatos[voto]['nome']} registrado!")
        atualizar_status()  # Atualiza status após voto
    else:
        tocar_som(SOM_ERRO)
        messagebox.showwarning("VOTO NULO", "Número inválido!")
    
    voto = ""
    atualizar()

def atualizar():
    """Atualiza a interface com o voto atual"""
    lbl_num.config(text=f"Número: {voto if voto else '__'}")
    
    if voto in candidatos:
        d = candidatos[voto]
        lbl_nome.config(text=f"Nome: {d['nome']}")
        
        try:
            # Carregar imagem
            img = Image.open(d["foto"])
            
            # Calcular tamanho para caber em 160x200 mantendo proporção
            largura_original, altura_original = img.size
            proporcao = min(160/largura_original, 200/altura_original)
            nova_largura = int(largura_original * proporcao)
            nova_altura = int(altura_original * proporcao)
            
            # Redimensionar
            img_redimensionada = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
            
            # Criar fundo branco
            img_fundo = Image.new('RGB', (160, 200), 'white')
            
            # Centralizar imagem no fundo
            offset_x = (160 - nova_largura) // 2
            offset_y = (200 - nova_altura) // 2
            img_fundo.paste(img_redimensionada, (offset_x, offset_y))
            
            # Converter para Tkinter
            foto_tk = ImageTk.PhotoImage(img_fundo)
            
            # Atualizar label
            lbl_foto.config(image=foto_tk)
            lbl_foto.image = foto_tk  # Manter referência
            lbl_foto.config(text="")  # Remover texto se houver
            
        except Exception as e:
            # Se erro, mostrar placeholder
            lbl_foto.config(image="")
            lbl_foto.config(text="Foto não\ncarregada", font=("Arial", 10))
            print(f"Erro ao carregar foto: {e}")
            
    else:
        lbl_nome.config(text="Nome:")
        lbl_foto.config(image="")
        lbl_foto.config(text="Digite número\npara ver foto", font=("Arial", 10))

# =========================
# PLACAR DE RESULTADOS
# =========================
def mostrar_placar():
    total = sum(votos.values())
    
    win = tk.Toplevel(root)
    win.title("📊 Placar da Eleição")
    win.geometry("480x600")
    win.configure(bg="white")
    win.resizable(False, False)
    
    tk.Label(
        win, text="📊 PLACAR ATUAL",
        font=("Arial", 18, "bold"),
        bg="white", fg="#2c3e50"
    ).pack(pady=15)
    
    tk.Label(
        win, text=f"Total de votos: {total}",
        font=("Arial", 12),
        bg="white", fg="#7f8c8d"
    ).pack()
    
    # Frame com scroll para muitos candidatos
    frame_container = tk.Frame(win, bg="white")
    frame_container.pack(fill="both", expand=True, padx=10, pady=10)
    
    canvas = tk.Canvas(frame_container, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Lista de candidatos
    for cod, dados in candidatos.items():
        qtd = votos.get(cod, 0)
        perc = (qtd / total * 100) if total else 0
        
        frame_cand = tk.Frame(scrollable_frame, bg="white", relief="solid", bd=1)
        frame_cand.pack(fill="x", padx=5, pady=8, ipady=5)
        
        # Foto
        try:
            img = Image.open(dados["foto"]).resize((50, 60))
            foto = ImageTk.PhotoImage(img)
            lbl_foto_cand = tk.Label(frame_cand, image=foto, bg="white")
            lbl_foto_cand.image = foto
            lbl_foto_cand.pack(side="left", padx=10, pady=5)
        except:
            tk.Label(frame_cand, text="📷", font=("Arial", 20), bg="white").pack(side="left", padx=10)
        
        # Informações
        info_frame = tk.Frame(frame_cand, bg="white")
        info_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(
            info_frame,
            text=f"{dados['nome']} ({cod})",
            font=("Arial", 12, "bold"),
            bg="white",
            anchor="w"
        ).pack(anchor="w")
        
        tk.Label(
            info_frame,
            text=f"Votos: {qtd} • {perc:.1f}%",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).pack(anchor="w")
        
        # Barra de progresso
        if perc > 0:
            barra_frame = tk.Frame(info_frame, bg="#ecf0f1", height=10, width=200)
            barra_frame.pack(anchor="w", pady=2)
            barra_frame.pack_propagate(False)
            
            barra = tk.Frame(barra_frame, bg="#3498db", height=10, width=perc*2)
            barra.pack(side="left")
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Botões
    btn_frame = tk.Frame(win, bg="white")
    btn_frame.pack(pady=10)
    
    tk.Button(
        btn_frame, text="🔄ATUALIZAR",
        bg="#3498db", fg="white",
        font=("Arial", 10),
        command=lambda: [win.destroy(), mostrar_placar()]
    ).pack(side="left", padx=5)
    
    tk.Button(
        btn_frame, text="💾 EXPORTAR",
        bg="#27ae60", fg="white",
        font=("Arial", 10),
        command=exportar_resultados
    ).pack(side="left", padx=5)
    
    tk.Button(
        btn_frame, text="❌ FECHAR",
        bg="#e74c3c", fg="white",
        font=("Arial", 10),
        command=win.destroy
    ).pack(side="left", padx=5)

def exportar_resultados():
    """Exporta resultados para arquivo de texto"""
    total = sum(votos.values())
    
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivo de texto", "*.txt"), ("Todos", "*.*")],
        initialfile="resultados_eleicao.txt"
    )
    
    if arquivo:
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("RESULTADOS DA ELEIÇÃO\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Data: {platform.system()} {platform.version()}\n")
            f.write(f"Total de votos: {total}\n\n")
            
            for cod, dados in sorted(candidatos.items()):
                qtd = votos.get(cod, 0)
                perc = (qtd / total * 100) if total else 0
                f.write(f"{cod} - {dados['nome']}: {qtd} votos ({perc:.1f}%)\n")
        
        messagebox.showinfo("✅ Exportado", f"Resultados salvos em:\n{arquivo}")

# =========================
# GERENCIAMENTO DE CANDIDATOS
# =========================
def adicionar_candidato():
    """Janela para adicionar novo candidato"""
    win = tk.Toplevel(root)
    win.title("➕ Adicionar Candidato")
    win.geometry("400x400")
    win.configure(bg="white")
    win.resizable(False, False)
    
    tk.Label(
        win, text="➕ NOVO CANDIDATO",
        font=("Arial", 14, "bold"), bg="white"
    ).pack(pady=10)
    
    # Número
    frame_num = tk.Frame(win, bg="white")
    frame_num.pack(pady=5, fill="x", padx=20)
    tk.Label(frame_num, text="Número (2 dígitos):", bg="white").pack(side="left")
    ent_num = tk.Entry(frame_num, width=10, font=("Arial", 12))
    ent_num.pack(side="left", padx=10)
    
    # Nome
    frame_nome = tk.Frame(win, bg="white")
    frame_nome.pack(pady=5, fill="x", padx=20)
    tk.Label(frame_nome, text="Nome completo:", bg="white").pack(side="left")
    ent_nome = tk.Entry(frame_nome, width=25, font=("Arial", 12))
    ent_nome.pack(side="left", padx=10)
    
    caminho_foto = {"path": ""}
    
    def escolher_foto():
        path = filedialog.askopenfilename(
            title="Selecionar foto do candidato",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp"), ("Todos", "*.*")]
        )
        if path:
            caminho_foto["path"] = path
            lbl_foto_info.config(
                text=f"✓ {os.path.basename(path)}",
                fg="green"
            )
    
    # Botão escolher foto
    tk.Button(
        win, text="📷 ESCOLHER FOTO",
        command=escolher_foto,
        bg="#3498db", fg="white",
        font=("Arial", 10)
    ).pack(pady=10)
    
    lbl_foto_info = tk.Label(
        win, text="Nenhuma foto selecionada",
        bg="white", fg="gray"
    )
    lbl_foto_info.pack()
    
    def salvar():
        num = ent_num.get().strip()
        nome = ent_nome.get().strip()
        
        # Validações
        if not num.isdigit() or len(num) != 2:
            messagebox.showerror("❌ Erro", "Número deve ter exatamente 2 dígitos!")
            return
        
        if num in candidatos:
            messagebox.showerror("❌ Erro", "Este número já está em uso!")
            return
        
        if not nome:
            messagebox.showerror("❌ Erro", "Digite o nome do candidato!")
            return
        
        if not caminho_foto["path"]:
            messagebox.showerror("❌ Erro", "Selecione uma foto para o candidato!")
            return
        
        # Copiar foto para pasta do projeto
        try:
            # Converter para PNG se necessário
            img = Image.open(caminho_foto["path"])
            destino_png = caminho("fotos", f"{num}.png")
            img.save(destino_png)
            
            # Adicionar ao dicionário de candidatos
            candidatos[num] = {"nome": nome, "foto": destino_png}
            votos[num] = 0
            
            messagebox.showinfo("✅ Sucesso", 
                              f"Candidato {nome} ({num}) adicionado com sucesso!")
            win.destroy()
            atualizar()
            atualizar_status()  # Atualiza status
            
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao processar imagem: {e}")
    
    # Botão salvar
    tk.Button(
        win, text="💾 SALVAR CANDIDATO",
        command=salvar,
        bg="#27ae60", fg="white",
        font=("Arial", 12, "bold"),
        width=25
    ).pack(pady=20)
    
    # Focar no campo do número
    ent_num.focus()

def remover_candidato():
    """Janela para remover candidato existente"""
    if not candidatos:
        messagebox.showinfo("ℹ️ Informação", "Nenhum candidato cadastrado!")
        return
    
    win = tk.Toplevel(root)
    win.title("➖ Remover Candidato")
    win.geometry("350x350")
    win.configure(bg="white")
    win.resizable(False, False)
    
    tk.Label(
        win, text="➖ REMOVER CANDIDATO",
        font=("Arial", 14, "bold"), bg="white"
    ).pack(pady=10)
    
    tk.Label(
        win, text="Selecione o candidato para remover:",
        bg="white"
    ).pack(pady=5)
    
    # Lista de candidatos
    lista_frame = tk.Frame(win, bg="white")
    lista_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    lista = tk.Listbox(
        lista_frame,
        font=("Arial", 11),
        selectmode="single",
        height=8
    )
    scrollbar = tk.Scrollbar(lista_frame, orient="vertical")
    lista.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista.yview)
    
    lista.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    for cod, d in candidatos.items():
        lista.insert("end", f"{cod} - {d['nome']}")
    
    def confirmar_remocao():
        sel = lista.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um candidato!")
            return
        
        item = lista.get(sel[0])
        num = item.split(" - ")[0]
        nome = candidatos[num]["nome"]
        
        if messagebox.askyesno(
            "⚠️ Confirmar Remoção",
            f"Tem certeza que deseja remover:\n\n{nome} ({num})?\n\nEsta ação não pode ser desfeita!",
            icon="warning"
        ):
            try:
                # Remove a foto
                if os.path.exists(candidatos[num]["foto"]):
                    os.remove(candidatos[num]["foto"])
                
                # Remove dos dicionários
                candidatos.pop(num)
                votos.pop(num, None)
                
                messagebox.showinfo("✅ Sucesso", "Candidato removido com sucesso!")
                win.destroy()
                atualizar()
                atualizar_status()  # Atualiza status
                
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao remover: {e}")
    
    # Botão remover
    tk.Button(
        win, text="🗑️ REMOVER SELECIONADO",
        command=confirmar_remocao,
        bg="#e74c3c", fg="white",
        font=("Arial", 11, "bold")
    ).pack(pady=15)

# =========================
# INTERFACE PRINCIPAL
# =========================
root = tk.Tk()
root.title("Urna Eletrônica - Multiplataforma")
root.geometry("850x550")  # Aumentado para acomodar rodapé
root.configure(bg="#f5f5f5")
root.resizable(False, False)

# =========================
# COLUNA ESQUERDA (VISOR)
# =========================
frame_esq = tk.Frame(root, bg="white", width=430, height=460)
frame_esq.place(x=15, y=20)

tk.Label(
    frame_esq, text="URNA ELETRÔNICA",
    font=("Arial", 20, "bold"),
    bg="white", fg="#2c3e50"
).place(x=20, y=15)

# Sistema detectado
sistema_atual = platform.system()
tk.Label(
    frame_esq, text=f"Sistema: {sistema_atual}",
    font=("Arial", 9), bg="white", fg="#7f8c8d"
).place(x=20, y=60)

# Visor do número
lbl_num = tk.Label(
    frame_esq, text="Número: __",
    font=("Arial", 18, "bold"),
    bg="white", fg="#2c3e50"
)
lbl_num.place(x=20, y=100)

# Nome do candidato
lbl_nome = tk.Label(
    frame_esq, text="Nome:",
    font=("Arial", 16),
    bg="white", fg="#34495e"
)
lbl_nome.place(x=20, y=150)

# Foto do candidato
lbl_foto = tk.Label(
    frame_esq, 
    bg="white",
    relief="solid", 
    bd=2
)
lbl_foto.place(x=200, y=100, width=160, height=200)

# Informações
tk.Label(
    frame_esq,
    text="Instruções:\n1. Digite o número (2 dígitos)\n2. Verifique o candidato\n3. Pressione CONFIRMA",
    font=("Arial", 10),
    bg="white", fg="#7f8c8d",
    justify="left"
).place(x=20, y=350)

# =========================
# COLUNA DIREITA (TECLADO E CONTROLES)
# =========================
frame_dir = tk.Frame(root, bg="#f5f5f5", width=380, height=480)
frame_dir.place(x=460, y=20)

# Título do teclado
tk.Label(
    frame_dir, text="TECLADO NUMÉRICO",
    font=("Arial", 14, "bold"),
    bg="#f5f5f5", fg="#2c3e50"
).pack(pady=5)

# Frame do teclado
teclado_frame = tk.Frame(frame_dir, bg="#ecf0f1", relief="solid", bd=2)
teclado_frame.pack(pady=10)

# Botões numéricos
botoes_numericos = [
    ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
    ("0", 3, 1)
]

for texto, linha, coluna in botoes_numericos:
    btn = tk.Button(
        teclado_frame,
        text=texto,
        font=("Arial", 14, "bold"),
        width=5, height=2,
        bg="#3498db", fg="white",
        activebackground="#2980b9",
        command=lambda t=texto: digitar(int(t))
    )
    btn.grid(row=linha, column=coluna, padx=3, pady=3)

# Botões de função
btn_branco = tk.Button(
    teclado_frame,
    text="BRANCO",
    font=("Arial", 10),
    width=12, height=2,
    bg="#95a5a6", fg="white",
    state="normal"
)
btn_branco.grid(row=0, column=3, padx=5, pady=3)

btn_corrige = tk.Button(
    teclado_frame,
    text="CORRIGE",
    font=("Arial", 10, "bold"),
    width=12, height=2,
    bg="#e67e22", fg="white",
    activebackground="#d35400",
    command=corrigir
)
btn_corrige.grid(row=1, column=3, padx=5, pady=3)

btn_confirma = tk.Button(
    teclado_frame,
    text="CONFIRMA",
    font=("Arial", 10, "bold"),
    width=12, height=2,
    bg="#27ae60", fg="white",
    activebackground="#229954",
    command=confirmar
)
btn_confirma.grid(row=2, column=3, padx=5, pady=3)

btn_placar = tk.Button(
    teclado_frame,
    text="PLACAR",
    font=("Arial", 10, "bold"),
    width=12, height=2,
    bg="#9b59b6", fg="white",
    activebackground="#8e44ad",
    command=mostrar_placar
)
btn_placar.grid(row=3, column=3, padx=5, pady=3)

# =========================
# CONTROLES ADICIONAIS
# =========================
controles_frame = tk.Frame(frame_dir, bg="#f5f5f5")
controles_frame.pack(pady=15)

tk.Button(
    controles_frame,
    text="➕ ADICIONAR CANDIDATO",
    font=("Arial", 10),
    bg="#3498db", fg="white",
    width=25, height=2,
    command=adicionar_candidato
).pack(pady=3)

tk.Button(
    controles_frame,
    text="➖ REMOVER CANDIDATO",
    font=("Arial", 10),
    bg="#e74c3c", fg="white",
    width=25, height=2,
    command=remover_candidato
).pack(pady=3)

tk.Button(
    controles_frame,
    text="📊 EXPORTAR RESULTADOS",
    font=("Arial", 10),
    bg="#f39c12", fg="white",
    width=25, height=2,
    command=exportar_resultados
).pack(pady=3)

# =========================
# RODAPÉ (STATUS BAR) - RESTAURADO
# =========================
rodape_frame = tk.Frame(root, bg="#2c3e50", height=35)
rodape_frame.pack(side="bottom", fill="x")

# Label de status
root.lbl_status = tk.Label(
    rodape_frame,
    text=atualizar_status(),  # Texto inicial
    font=("Arial", 9),
    bg="#2c3e50", 
    fg="white",
    anchor="w",
    padx=10
)
root.lbl_status.pack(side="left", fill="x", expand=True)

# Botões no rodapé
rodape_btn_frame = tk.Frame(rodape_frame, bg="#2c3e50")
rodape_btn_frame.pack(side="right", padx=10)

def sobre():
    """Janela de informações sobre o programa"""
    sobre_win = tk.Toplevel(root)
    sobre_win.title("ℹ️ Sobre a Urna Eletrônica")
    sobre_win.geometry("400x300")
    sobre_win.resizable(False, False)
    sobre_win.configure(bg="white")
    
    tk.Label(
        sobre_win,
        text="URNA ELETRÔNICA",
        font=("Arial", 18, "bold"),
        bg="white", fg="#2c3e50"
    ).pack(pady=15)
    
    info_text = f"""
    Versão: 2.0 Multiplataforma
    Sistema: {platform.system()} {platform.version()}
    Python: {platform.python_version()}
    
    Desenvolvido com:
    • Tkinter (Interface gráfica)
    • Pillow (Processamento de imagens)
    • Suporte multiplataforma
    
    Funcionalidades:
    • Sistema de votação completo
    • Gerenciamento de candidatos
    • Resultados em tempo real
    • Exportação de dados
    
    Para fins educacionais
    """
    
    tk.Label(
        sobre_win,
        text=info_text,
        font=("Arial", 10),
        bg="white",
        justify="left"
    ).pack(pady=10)
    
    tk.Button(
        sobre_win,
        text="FECHAR",
        bg="#95a5a6", fg="white",
        command=sobre_win.destroy
    ).pack(pady=10)

def reiniciar_votacao():
    """Reinicia todos os votos"""
    if messagebox.askyesno("🔄 Reiniciar Votação", 
                         "Tem certeza que deseja reiniciar TODOS os votos?\n\nEsta ação não pode ser desfeita!"):
        for cod in votos:
            votos[cod] = 0
        atualizar_status()
        messagebox.showinfo("✅ Reiniciado", "Contagem de votos reiniciada com sucesso!")

def fechar_programa():
    """Fecha o programa com confirmação"""
    if messagebox.askyesno("❌ Sair", "Tem certeza que deseja sair da Urna Eletrônica?"):
        root.destroy()

# Botões no rodapé
tk.Button(
    rodape_btn_frame,
    text="ℹ️ SOBRE",
    font=("Arial", 8),
    bg="#3498db", fg="white",
    width=8,
    command=sobre
).pack(side="left", padx=2)

tk.Button(
    rodape_btn_frame,
    text="🔄 REINICIAR",
    font=("Arial", 8),
    bg="#f39c12", fg="white",
    width=10,
    command=reiniciar_votacao
).pack(side="left", padx=2)

tk.Button(
    rodape_btn_frame,
    text="❌ SAIR",
    font=("Arial", 8),
    bg="#e74c3c", fg="white",
    width=6,
    command=fechar_programa
).pack(side="left", padx=2)

# =========================
# MENU PRINCIPAL
# =========================
menu_bar = tk.Menu(root)

# Menu Arquivo
menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_arquivo.add_command(label="Exportar Resultados", command=exportar_resultados)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Reiniciar Votação", command=reiniciar_votacao)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=fechar_programa)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)

# Menu Candidatos
menu_candidatos = tk.Menu(menu_bar, tearoff=0)
menu_candidatos.add_command(label="Adicionar Candidato", command=adicionar_candidato)
menu_candidatos.add_command(label="Remover Candidato", command=remover_candidato)
menu_bar.add_cascade(label="Candidatos", menu=menu_candidatos)

# Menu Resultados
menu_resultados = tk.Menu(menu_bar, tearoff=0)
menu_resultados.add_command(label="Ver Placar", command=mostrar_placar)
menu_resultados.add_command(label="Exportar Resultados", command=exportar_resultados)
menu_bar.add_cascade(label="Resultados", menu=menu_resultados)

# Menu Ajuda
menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_ajuda.add_command(label="Sobre", command=sobre)
menu_ajuda.add_command(label="Instruções", 
                      command=lambda: messagebox.showinfo("Instruções", 
                                                       "1. Digite o número do candidato (2 dígitos)\n"
                                                       "2. Verifique o nome e foto na tela\n"
                                                       "3. Pressione CONFIRMA para votar\n"
                                                       "4. Use CORRIGE para apagar"))
menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)

root.config(menu=menu_bar)

# =========================
# INICIALIZAR
# =========================
def inicializar():
    """Inicializa a aplicação"""
    print("=" * 60)
    print("URNA ELETRÔNICA - INICIANDO")
    print("=" * 60)
    
    # Verificar dependências
    try:
        from PIL import Image, ImageTk
        print("✅ Pillow (PIL) carregado com sucesso")
    except ImportError:
        print("❌ ERRO: Pillow não instalado!")
        messagebox.showerror(
            "Erro de Dependência",
            "A biblioteca Pillow não está instalada.\n\n"
            "Execute no terminal:\npip install pillow"
        )
    
    print(f"👥 Candidatos carregados: {len(candidatos)}")
    print(f"🗳️  Sistema: {platform.system()}")
    print("=" * 60)
    
    # Atualizar interface
    atualizar()
    atualizar_status()
    
    # Mostrar dica inicial
    if len(candidatos) > 0:
        primeiro = list(candidatos.keys())[0]
        lbl_foto.config(text=f"Digite {primeiro} para testar")

# Iniciar aplicação
inicializar()
root.mainloop()
