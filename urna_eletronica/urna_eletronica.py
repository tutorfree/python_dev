import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import winsound
import os

# =========================
# CAMINHO BASE
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def caminho(*pastas):
    return os.path.join(BASE_DIR, *pastas)

# =========================
# SONS (WAV)
# =========================
SOM_TECLA = caminho("sons", "tecla.wav")
SOM_CONFIRMA = caminho("sons", "confirma.wav")
SOM_ERRO = caminho("sons", "erro.wav")

def tocar_som(arquivo):
    try:
        winsound.PlaySound(
            arquivo,
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )
    except:
        pass

# =========================
# DADOS DOS CANDIDATOS
# =========================
candidatos = {
    "11": {
        "nome": "Enzo",
        "foto": caminho("fotos", "11.png")
    },
    "12": {
        "nome": "José",
        "foto": caminho("fotos", "12.png")
    },
    "22": {
        "nome": "Cafuso",
        "foto": caminho("fotos", "22.png")
    },
    "33": {
        "nome": "Zefinha",
        "foto": caminho("fotos", "33.png")
    },
    "34": {
        "nome": "Maria",
        "foto": caminho("fotos", "34.png")
    },
    "66": {
        "nome": "Ambrósio",
        "foto": caminho("fotos", "66.png")
    }
}

# =========================
# VOTOS
# =========================
votos = {
    "11": 0,
    "12": 0,
    "22": 0,
    "33": 0,
    "34": 0,
    "66": 0
}

voto = ""

# =========================
# FUNÇÕES PRINCIPAIS
# =========================
def digitar(numero):
    global voto
    if len(voto) < 2:
        tocar_som(SOM_TECLA)
        voto += str(numero)
        atualizar_tela()

def corrigir():
    global voto
    tocar_som(SOM_ERRO)
    voto = ""
    atualizar_tela()

def confirmar():
    global voto

    # voto incompleto
    if len(voto) < 2:
        tocar_som(SOM_ERRO)
        messagebox.showwarning(
            "VOTO INCOMPLETO",
            "Digite o número completo do candidato"
        )
        return

    if voto in candidatos:
        votos[voto] += 1
        tocar_som(SOM_CONFIRMA)
        messagebox.showinfo(
            "VOTO CONFIRMADO",
            f"Voto registrado para {candidatos[voto]['nome']}"
        )
    else:
        tocar_som(SOM_ERRO)
        messagebox.showwarning(
            "VOTO NULO",
            "Número inexistente. Voto anulado."
        )

    voto = ""
    atualizar_tela()

# =========================
# PLACAR (POPUP)
# =========================
def mostrar_placar():
    total = sum(votos.values())

    janela = tk.Toplevel(root)
    janela.title("Placar da Eleição")
    janela.geometry("420x580")
    janela.configure(bg="white")
    janela.resizable(False, False)

    tk.Label(
        janela,
        text="PLACAR ATUAL",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(pady=10)

    for codigo, dados in candidatos.items():
        qtd = votos[codigo]
        perc = (qtd / total * 100) if total > 0 else 0

        frame = tk.Frame(janela, bg="white")
        frame.pack(fill="x", padx=10, pady=5)

        try:
            img = Image.open(dados["foto"]).resize((60, 75))
            foto = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(frame, image=foto, bg="white")
            lbl_img.image = foto
            lbl_img.pack(side="left", padx=5)
        except:
            pass

        tk.Label(
            frame,
            text=(
                f"{dados['nome']}\n"
                f"Votos: {qtd}\n"
                f"{perc:.1f}%"
            ),
            font=("Arial", 12),
            bg="white",
            justify="left"
        ).pack(side="left", padx=10)

# =========================
# INTERFACE
# =========================
root = tk.Tk()
root.title("Urna Eletrônica")
root.geometry("800x450")
root.configure(bg="#d9d9d9")
root.resizable(False, False)

# Visor
visor = tk.Frame(root, bg="white", width=400, height=380)
visor.place(x=10, y=20)

lbl_numero = tk.Label(
    visor, text="Número: __",
    font=("Arial", 18), bg="white"
)
lbl_numero.place(x=20, y=20)

lbl_nome = tk.Label(
    visor, text="Nome:",
    font=("Arial", 16), bg="white"
)
lbl_nome.place(x=20, y=70)

lbl_foto = tk.Label(visor, bg="white")
lbl_foto.place(x=220, y=50)

# Teclado
teclado = tk.Frame(root, bg="#bfbfbf", width=260, height=380)
teclado.place(x=440, y=20)

numeros = [
    (1, 0, 0), (2, 0, 1), (3, 0, 2),
    (4, 1, 0), (5, 1, 1), (6, 1, 2),
    (7, 2, 0), (8, 2, 1), (9, 2, 2),
    (0, 3, 1)
]

for num, r, c in numeros:
    tk.Button(
        teclado, text=str(num),
        font=("Arial", 14),
        width=6, height=2,
        command=lambda n=num: digitar(n)
    ).grid(row=r, column=c, padx=5, pady=5)

# Botões especiais
tk.Button(
    teclado, text="BRANCO",
    font=("Arial", 10),
    width=10, height=2,
    command=corrigir
).grid(row=0, column=3, padx=5, pady=5)

tk.Button(
    teclado, text="CORRIGE",
    bg="orange",
    font=("Arial", 10),
    width=10, height=2,
    command=corrigir
).grid(row=1, column=3, padx=5, pady=5)

tk.Button(
    teclado, text="CONFIRMA",
    bg="green", fg="white",
    font=("Arial", 10),
    width=10, height=2,
    command=confirmar
).grid(row=2, column=3, padx=5, pady=5)

tk.Button(
    teclado, text="PLACAR",
    bg="blue", fg="white",
    font=("Arial", 10),
    width=10, height=2,
    command=mostrar_placar
).grid(row=3, column=3, padx=5, pady=5)

# =========================
# ATUALIZA VISOR
# =========================
def atualizar_tela():
    lbl_numero.config(text=f"Número: {voto if voto else '__'}")

    if voto in candidatos:
        dados = candidatos[voto]
        lbl_nome.config(text=f"Nome: {dados['nome']}")

        try:
            img = Image.open(dados["foto"]).resize((150, 180))
            foto = ImageTk.PhotoImage(img)
            lbl_foto.config(image=foto)
            lbl_foto.image = foto
        except:
            lbl_foto.config(image="")
    else:
        lbl_nome.config(text="Nome:")
        lbl_foto.config(image="")

atualizar_tela()
root.mainloop()
