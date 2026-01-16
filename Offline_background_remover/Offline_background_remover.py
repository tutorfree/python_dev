import sys
import os

if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import faulthandler
faulthandler.enable()


try:
    from rembg import remove
    REMBG_AVAILABLE = True
    REMBG_ERROR = ""
except Exception as e:
    REMBG_AVAILABLE = False
    REMBG_ERROR = (
        "Não foi possível carregar a IA de remoção de fundo.\n\n"
        "Detalhes técnicos:\n"
        f"{e}\n\n"
        "Possíveis causas:\n"
        "- NumPy incompatível\n"
        "- OpenCV ausente ou incompatível\n"
        "- onnxruntime não suportado\n"
        "- Versão errada do Python"
    )


THEME = {
    "bg": "#0b1020",
    "panel": "#121a33",
    "text": "#e9ecff",
    "muted": "#b8c0ff",
    "accent": "#7c5cff",
    "success": "#34d399",
    "button": "#1a2446",
    "button_hover": "#22305a",
}

class BackgroundRemoverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Removedor de Fundo Offline")
        self.geometry("600x500")
        self.configure(bg=THEME["bg"])
        
        self.input_path = None
        self.processing = False

        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["bg"], pady=20)
        header.pack(fill="x")
        
        tk.Label(
            header, text="Removedor de Fundo AI", 
            font=("Segoe UI Semibold", 18), fg=THEME["text"], bg=THEME["bg"]
        ).pack()
        
        tk.Label(
            header, text="Processamento 100% Local e Offline", 
            font=("Segoe UI", 10), fg=THEME["muted"], bg=THEME["bg"]
        ).pack()

        # Main Panel
        self.main_panel = tk.Frame(self, bg=THEME["panel"], padx=20, pady=20, highlightthickness=1, highlightbackground="#273056")
        self.main_panel.pack(padx=40, pady=10, fill="both", expand=True)

        # Drop Area / Selection
        self.info_lbl = tk.Label(
            self.main_panel, text="Nenhuma imagem selecionada",
            font=("Segoe UI", 11), fg=THEME["muted"], bg=THEME["panel"],
            wraplength=400
        )
        self.info_lbl.pack(expand=True)

        self.select_btn = tk.Button(
            self.main_panel, text="Selecionar Imagem",
            font=("Segoe UI Semibold", 11), bg=THEME["accent"], fg="white",
            activebackground=THEME["accent"], activeforeground="white",
            relief="flat", padx=20, pady=10, command=self.select_image
        )
        self.select_btn.pack(pady=10)

        # Progress Bar (Hidden by default)
        self.progress = ttk.Progressbar(self.main_panel, mode='indeterminate', length=300)
        
        # Footer
        self.footer = tk.Frame(self, bg=THEME["bg"], pady=20)
        self.footer.pack(fill="x")

        self.process_btn = tk.Button(
            self.footer, text="Remover Fundo e Salvar",
            font=("Segoe UI Semibold", 11), bg=THEME["button"], fg=THEME["muted"],
            activebackground=THEME["button_hover"], activeforeground=THEME["text"],
            relief="flat", padx=30, pady=12, state="disabled", command=self.start_processing
        )
        self.process_btn.pack()

    def select_image(self):
        file_types = [('Imagens', '*.png *.jpg *.jpeg *.webp')]
        path = filedialog.askopenfilename(title="Escolha uma imagem", filetypes=file_types)
        
        if path:
            self.input_path = path
            filename = os.path.basename(path)
            self.info_lbl.config(text=f"Selecionado:\n{filename}", fg=THEME["text"])
            self.process_btn.config(state="normal", bg=THEME["success"], fg=THEME["bg"])

    def start_processing(self):
        if self.processing or not self.input_path:
            return

        if not REMBG_AVAILABLE:
            messagebox.showerror("Erro", REMBG_ERROR)
            return

        # ABRE O DIALOGO NA THREAD PRINCIPAL
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG file", "*.png")],
            initialfile=os.path.splitext(
                os.path.basename(self.input_path)
            )[0] + "_no_bg.png"
        )

        if not output_path:
            return

        self.processing = True
        self.process_btn.config(state="disabled", text="Processando...")
        self.select_btn.config(state="disabled")
        self.progress.pack(pady=10)
        self.progress.start()

        threading.Thread(
            target=self.process_image,
            args=(output_path,),
            daemon=True
        ).start()


    def process_image(self, output_path):
        try:
            with open(self.input_path, 'rb') as i:
                input_data = i.read()

            output_data = remove(input_data)

            with open(output_path, 'wb') as o:
                o.write(output_data)

            self.after(0, lambda: messagebox.showinfo(
                "Sucesso",
                f"Fundo removido com sucesso!\nSalvo em:\n{output_path}"
            ))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Erro",
                str(e)
            ))

        finally:
            self.after(0, self.reset_ui)


    def reset_ui(self):
        self.processing = False
        self.progress.stop()
        self.progress.pack_forget()
        self.process_btn.config(state="normal", text="Remover Fundo e Salvar")
        self.select_btn.config(state="normal")

if __name__ == "__main__":
    app = BackgroundRemoverApp()
    app.mainloop()
