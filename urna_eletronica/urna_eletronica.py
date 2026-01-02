import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import winsound
import os
import shutil

# =========================
# BASE
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def caminho(*p):
    return os.path.join(BASE_DIR, *p)

def tocar_som(arq):
    try:
        winsound.PlaySound(arq, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except:
        pass

SOM_TECLA = caminho("sons", "tecla.wav")
SOM_CONFIRMA = caminho("sons", "confirma.wav")
SOM_ERRO = caminho("sons", "erro.wav")

# =========================
# DADOS
# =========================
candidatos = {
    "11": {"nome": "Enzo", "foto": caminho("fotos", "11.png")},
    "12": {"nome": "José", "foto": caminho("fotos", "12.png")},
    "22": {"nome": "Chicão", "foto": caminho("fotos", "22.png")},
    "33": {"nome": "Zefinha", "foto": caminho("fotos", "33.png")},
    "34": {"nome": "Maria", "foto": caminho("fotos", "34.png")},
    "66": {"nome": "Onerildo", "foto": caminho("fotos", "66.png")},
}

votos = {k: 0 for k in candidatos}
voto = ""

# =========================
# FUNÇÕES URNA
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
                            f"Voto para {candidatos[voto]['nome']}")
    else:
        tocar_som(SOM_ERRO)
        messagebox.showwarning("VOTO NULO", "Número inválido")

    voto = ""
    atualizar()

# =========================
# PLACAR
# =========================
def mostrar_placar():
    total = sum(votos.values())

    win = tk.Toplevel(root)
    win.title("Placar da Eleição")
    win.geometry("420x580")
    win.configure(bg="white")
    win.resizable(False, False)

    tk.Label(
        win, text="PLACAR ATUAL",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(pady=10)

    for cod, dados in candidatos.items():
        qtd = votos.get(cod, 0)
        perc = (qtd / total * 100) if total else 0

        frame = tk.Frame(win, bg="white")
        frame.pack(fill="x", padx=10, pady=6)

        try:
            img = Image.open(dados["foto"]).resize((60, 75))
            foto = ImageTk.PhotoImage(img)
            lbl = tk.Label(frame, image=foto, bg="white")
            lbl.image = foto
            lbl.pack(side="left", padx=5)
        except:
            pass

        tk.Label(
            frame,
            text=f"{dados['nome']}\nVotos: {qtd}\n{perc:.1f}%",
            font=("Arial", 12),
            bg="white",
            justify="left"
        ).pack(side="left", padx=10)

# =========================
# ADICIONAR CANDIDATO
# =========================
def adicionar_candidato():
    win = tk.Toplevel(root)
    win.title("Adicionar Candidato")
    win.geometry("360x320")
    win.resizable(False, False)

    tk.Label(win, text="Número (2 dígitos):").pack(pady=5)
    ent_num = tk.Entry(win)
    ent_num.pack()

    tk.Label(win, text="Nome do candidato:").pack(pady=5)
    ent_nome = tk.Entry(win)
    ent_nome.pack()

    caminho_foto = {"path": ""}

    def escolher_foto():
        path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if path:
            caminho_foto["path"] = path
            lbl_foto.config(text=os.path.basename(path))

    lbl_foto = tk.Label(win, text="Nenhuma foto selecionada")
    lbl_foto.pack(pady=5)

    tk.Button(win, text="Escolher Foto", command=escolher_foto).pack()

    def salvar():
        num = ent_num.get().strip()
        nome = ent_nome.get().strip()

        if not num.isdigit() or len(num) != 2:
            messagebox.showerror("Erro", "Número inválido")
            return

        if num in candidatos:
            messagebox.showerror("Erro", "Número já existe")
            return

        if not nome or not caminho_foto["path"]:
            messagebox.showerror("Erro", "Campos incompletos")
            return

        destino = caminho("fotos", f"{num}.png")
        shutil.copy(caminho_foto["path"], destino)

        candidatos[num] = {"nome": nome, "foto": destino}
        votos[num] = 0

        messagebox.showinfo("OK", "Candidato adicionado")
        win.destroy()

    tk.Button(win, text="SALVAR", bg="green", fg="white", command=salvar)\
        .pack(pady=15)

# =========================
# REMOVER CANDIDATO
# =========================
def remover_candidato():
    if not candidatos:
        messagebox.showinfo("Info", "Nenhum candidato cadastrado")
        return

    win = tk.Toplevel(root)
    win.title("Remover Candidato")
    win.geometry("300x260")
    win.resizable(False, False)

    tk.Label(win, text="Selecione o candidato:").pack(pady=10)

    lista = tk.Listbox(win, font=("Arial", 11))
    lista.pack(fill="both", expand=True, padx=10)

    for cod, d in candidatos.items():
        lista.insert("end", f"{cod} - {d['nome']}")

    def confirmar_remocao():
        sel = lista.curselection()
        if not sel:
            return

        item = lista.get(sel[0])
        num = item.split(" - ")[0]

        if messagebox.askyesno(
            "Confirmar",
            f"Remover {candidatos[num]['nome']}?"
        ):
            try:
                os.remove(candidatos[num]["foto"])
            except:
                pass

            candidatos.pop(num)
            votos.pop(num, None)

            messagebox.showinfo("OK", "Candidato removido")
            win.destroy()
            atualizar()

    tk.Button(
        win, text="REMOVER",
        bg="red", fg="white",
        command=confirmar_remocao
    ).pack(pady=10)

# =========================
# INTERFACE
# =========================
root = tk.Tk()
root.title("Urna Eletrônica")
root.geometry("820x500")
root.configure(bg="#d9d9d9")
root.resizable(False, False)

# VISOR
col_esq = tk.Frame(root, bg="white", width=400, height=400)
col_esq.place(x=10, y=20)

lbl_num = tk.Label(col_esq, text="Número: __", font=("Arial", 18), bg="white")
lbl_num.place(x=20, y=20)

lbl_nome = tk.Label(col_esq, text="Nome:", font=("Arial", 16), bg="white")
lbl_nome.place(x=20, y=70)

lbl_foto = tk.Label(col_esq, bg="white")
lbl_foto.place(x=120, y=130)

# COLUNA DIREITA
col_dir = tk.Frame(root, bg="#d9d9d9", width=380, height=500)
col_dir.place(x=440, y=20)

# TECLADO
teclado = tk.Frame(col_dir, bg="#bfbfbf")
teclado.pack(pady=10)

nums = [
    (1,0,0),(2,0,1),(3,0,2),
    (4,1,0),(5,1,1),(6,1,2),
    (7,2,0),(8,2,1),(9,2,2),
    (0,3,1)
]

for n,r,c in nums:
    tk.Button(teclado, text=str(n), width=6, height=2,
              command=lambda x=n: digitar(x))\
        .grid(row=r, column=c, padx=6, pady=6)

tk.Button(teclado, text="BRANCO", width=10)\
    .grid(row=0, column=3)

tk.Button(teclado, text="CORRIGE", bg="orange", width=10, command=corrigir)\
    .grid(row=1, column=3)

tk.Button(teclado, text="CONFIRMA", bg="green", fg="white", width=10,
          command=confirmar)\
    .grid(row=2, column=3)

tk.Button(teclado, text="PLACAR", bg="blue", fg="white", width=10,
          command=mostrar_placar)\
    .grid(row=3, column=3)

# BOTÕES EXTRAS
tk.Frame(col_dir, height=60, bg="#d9d9d9").pack()

tk.Button(col_dir, text="Adicionar Candidato",
          bg="purple", fg="white", width=32,
          command=adicionar_candidato).pack(pady=5)

tk.Button(col_dir, text="Remover Candidato",
          bg="#8b0000", fg="white", width=32,
          command=remover_candidato).pack(pady=5)

# =========================
# ATUALIZA VISOR
# =========================
def atualizar():
    lbl_num.config(text=f"Número: {voto if voto else '__'}")

    if voto in candidatos:
        d = candidatos[voto]
        lbl_nome.config(text=f"Nome: {d['nome']}")
        img = Image.open(d["foto"]).resize((160, 200))
        foto = ImageTk.PhotoImage(img)
        lbl_foto.config(image=foto)
        lbl_foto.image = foto
    else:
        lbl_nome.config(text="Nome:")
        lbl_foto.config(image="")

atualizar()
root.mainloop()
