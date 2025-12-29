import tkinter as tk
from tkinter import ttk, messagebox
import math

class VerificadorPrimoTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificador de Números Primos")
        self.root.geometry("470x520")
        self.root.resizable(False, False)
        
        # Configurar cores
        self.cor_primo = "#2ecc71"  # Verde
        self.cor_nao_primo = "#e74c3c"  # Vermelho
        self.cor_neutro = "#ecf0f1"  # Cinza claro
        
        # Variáveis
        self.numero_var = tk.StringVar()
        self.resultado_var = tk.StringVar(value="Digite um número para verificar")
        
        # Configurar interface
        self.configurar_interface()
        
    def configurar_interface(self):
        """Configurar todos os elementos da interface gráfica"""
        
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo_label = ttk.Label(
            frame_principal,
            text="Verificador de Números Primos",
            font=("Arial", 16, "bold")
        )
        titulo_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de entrada
        frame_entrada = ttk.LabelFrame(frame_principal, text="Entrada", padding="15")
        frame_entrada.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Label para instrução
        instrucao_label = ttk.Label(
            frame_entrada,
            text="Digite um número inteiro positivo:",
            font=("Arial", 10)
        )
        instrucao_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Campo de entrada
        entrada_numero = ttk.Entry(
            frame_entrada,
            textvariable=self.numero_var,
            font=("Arial", 12),
            width=20,
            justify="center"
        )
        entrada_numero.grid(row=1, column=0, pady=(0, 10))
        entrada_numero.focus_set()
        
        # Botão de verificação
        botao_verificar = ttk.Button(
            frame_entrada,
            text="Verificar se é Primo",
            command=self.verificar_primo,
            width=20
        )
        botao_verificar.grid(row=2, column=0, pady=(5, 0))
        
        # Frame de resultado
        frame_resultado = ttk.LabelFrame(frame_principal, text="Resultado", padding="15")
        frame_resultado.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Label de resultado
        self.label_resultado = ttk.Label(
            frame_resultado,
            textvariable=self.resultado_var,
            font=("Arial", 12, "bold"),
            anchor="center",
            relief="solid",
            padding=10
        )
        self.label_resultado.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.label_resultado.configure(background=self.cor_neutro)
        
        # Frame de informações
        frame_info = ttk.LabelFrame(frame_principal, text="Informações sobre Primos", padding="15")
        frame_info.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Texto informativo
        texto_info = """• Número primo é aquele que é divisível apenas por 1 e por ele mesmo
• Exemplos: 2, 3, 5, 7, 11, 13, 17, 19, 23...
• O número 1 NÃO é considerado primo
• O número 2 é o único número primo par"""
        
        info_label = ttk.Label(
            frame_info,
            text=texto_info,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Frame de botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        # Botão de limpar
        botao_limpar = ttk.Button(
            frame_botoes,
            text="Limpar",
            command=self.limpar_campos,
            width=15
        )
        botao_limpar.grid(row=0, column=0, padx=(0, 10))
        
        # Botão de sair
        botao_sair = ttk.Button(
            frame_botoes,
            text="Sair",
            command=self.root.quit,
            width=15
        )
        botao_sair.grid(row=0, column=1)
        
        # Configurar expansão
        frame_principal.columnconfigure(0, weight=1)
        frame_resultado.columnconfigure(0, weight=1)
        
        # Vincular tecla Enter
        entrada_numero.bind('<Return>', lambda event: self.verificar_primo())
        
    def eh_primo(self, n):
        """Função para verificar se um número é primo"""
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        limite = int(math.sqrt(n)) + 1
        for i in range(3, limite, 2):
            if n % i == 0:
                return False
        return True
    
    def verificar_primo(self):
        """Função principal para verificar se o número é primo"""
        try:
            # Obter o número digitado
            texto_numero = self.numero_var.get().strip()
            
            # Validar se há entrada
            if not texto_numero:
                messagebox.showwarning("Aviso", "Por favor, digite um número.")
                return
            
            # Converter para inteiro
            numero = int(texto_numero)
            
            # Verificar se é positivo
            if numero < 0:
                messagebox.showwarning("Aviso", "Por favor, digite um número positivo.")
                return
            
            # Verificar se é primo
            if self.eh_primo(numero):
                resultado = f"{numero} É um número primo! ✓"
                cor_fundo = self.cor_primo
            else:
                resultado = f"{numero} NÃO é um número primo ✗"
                cor_fundo = self.cor_nao_primo
            
            # Atualizar resultado
            self.resultado_var.set(resultado)
            self.label_resultado.configure(background=cor_fundo)
            
            # Mostrar informações adicionais para números não primos
            if numero > 1 and not self.eh_primo(numero):
                self.mostrar_divisores(numero)
                
        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite um número inteiro válido.")
            self.numero_var.set("")
            self.resultado_var.set("Digite um número para verificar")
            self.label_resultado.configure(background=self.cor_neutro)
    
    def mostrar_divisores(self, numero):
        """Mostrar divisores de um número não primo"""
        if numero <= 1:
            return
        
        divisores = []
        for i in range(2, numero):
            if numero % i == 0:
                divisores.append(str(i))
        
        if divisores:
            if len(divisores) > 5:
                mensagem = f"Divisores: {', '.join(divisores[:5])}... (total: {len(divisores)} divisores)"
            else:
                mensagem = f"Divisores: {', '.join(divisores)}"
            
            # Criar janela popup com os divisores
            self.criar_popup_divisores(numero, divisores)
    
    def criar_popup_divisores(self, numero, divisores):
        """Criar popup com lista de divisores"""
        popup = tk.Toplevel(self.root)
        popup.title(f"Divisores de {numero}")
        popup.geometry("300x400")
        popup.resizable(False, False)
        popup.transient(self.root)  # Torna a janela filha
        popup.grab_set()  # Torna modal
        
        # Centralizar popup
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Frame principal
        frame = ttk.Frame(popup, padding="15")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(
            frame,
            text=f"Divisores de {numero}",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, pady=(0, 10))
        
        # Texto informativo
        ttk.Label(
            frame,
            text=f"Total de divisores: {len(divisores)}",
            font=("Arial", 10)
        ).grid(row=1, column=0, pady=(0, 10))
        
        # Frame para lista de divisores com scrollbar
        container = ttk.Frame(frame)
        container.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas e scrollbar
        canvas = tk.Canvas(container, height=100)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Adicionar divisores à lista
        for idx, divisor in enumerate(divisores):
            ttk.Label(
                scrollable_frame,
                text=f"• {divisor}",
                font=("Arial", 9)
            ).grid(row=idx, column=0, sticky=tk.W, pady=2)
        
        # Botão fechar
        ttk.Button(
            frame,
            text="Fechar",
            command=popup.destroy
        ).grid(row=3, column=0, pady=(15, 0))
        
        # Configurar expansão
        frame.columnconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        
        # Mostrar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def limpar_campos(self):
        """Limpar todos os campos e resetar interface"""
        self.numero_var.set("")
        self.resultado_var.set("Digite um número para verificar")
        self.label_resultado.configure(background=self.cor_neutro)
        
        # Dar foco ao campo de entrada
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame):
                        for entry in child.winfo_children():
                            if isinstance(entry, ttk.Entry):
                                entry.focus_set()
                                break

def main():
    """Função principal para iniciar a aplicação"""
    root = tk.Tk()
    app = VerificadorPrimoTkinter(root)
    
    # Centralizar a janela
    root.update_idletasks()
    largura = root.winfo_width()
    altura = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f'{largura}x{altura}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
