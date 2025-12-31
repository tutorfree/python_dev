import tkinter as tk
from tkinter import ttk, messagebox

class AlcoolGasolinaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Álcool ou Gasolina? - Calculadora")
        self.root.geometry("500x380")
        self.root.resizable(False, False)
        
        # Configurar estilo
        self.setup_styles()
        
        # Variáveis
        self.alcool_val = tk.StringVar()
        self.gasolina_val = tk.StringVar()
        self.resultado_divisao = tk.StringVar(value="")
        self.resultado_texto = tk.StringVar(value="Digite os preços para calcular")
        
        # Cores
        self.cor_alcool = "#FF9800"  # Laranja
        self.cor_gasolina = "#F44336"  # Vermelho
        self.cor_compensa = "#4CAF50"  # Verde
        self.cor_nao_compensa = "#9E9E9E"  # Cinza
        
        # Configurar interface
        self.setup_interface()
        
        # Configurar validação de entrada
        self.setup_validation()
        
        # Configurar fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        
    def setup_styles(self):
        """Configurar estilos para a aplicação"""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 10))
        style.configure('Result.TLabel', font=('Arial', 11, 'bold'))
        style.configure('BigResult.TLabel', font=('Arial', 14, 'bold'))
        
    def setup_interface(self):
        """Configurar todos os elementos da interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="ÁLCOOL OU GASOLINA?",
            style='Title.TLabel',
            foreground="#333"
        )
        title_label.pack(pady=(0, 5))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            main_frame,
            text="Calcule qual combustível compensa mais abastecer",
            style='Subtitle.TLabel',
            foreground="#666"
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Preços dos Combustíveis", padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Container para as entradas usando grid com colunas fixas
        entries_container = ttk.Frame(input_frame)
        entries_container.pack()
        
        # Configurar colunas no container principal
        entries_container.columnconfigure(0, minsize=30)   # Coluna para ícones
        entries_container.columnconfigure(1, minsize=180)  # Coluna para labels
        entries_container.columnconfigure(2, minsize=120)  # Coluna para entries
        
        # Linha 0: Álcool
        # Ícone para álcool
        alcool_icon = tk.Label(
            entries_container,
            text="⛽",
            font=("Arial", 14),
            foreground=self.cor_alcool
        )
        alcool_icon.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        # Label para álcool
        alcool_label = ttk.Label(
            entries_container,
            text="Preço do Álcool (R$/litro):",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        alcool_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        # Campo de entrada para álcool
        self.alcool_entry = ttk.Entry(
            entries_container,
            textvariable=self.alcool_val,
            font=("Arial", 12),
            width=15,
            justify="right"
        )
        self.alcool_entry.grid(row=0, column=2, sticky=tk.W)
        self.alcool_entry.focus_set()
        
        # Linha 1: Gasolina
        # Ícone para gasolina
        gasolina_icon = tk.Label(
            entries_container,
            text="⛽",
            font=("Arial", 14),
            foreground=self.cor_gasolina
        )
        gasolina_icon.grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        
        # Label para gasolina
        gasolina_label = ttk.Label(
            entries_container,
            text="Preço da Gasolina (R$/litro):",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        gasolina_label.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # Campo de entrada para gasolina
        self.gasolina_entry = ttk.Entry(
            entries_container,
            textvariable=self.gasolina_val,
            font=("Arial", 12),
            width=15,
            justify="right"
        )
        self.gasolina_entry.grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        
        # Frame de botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(0, 15))
        
        # Botão Calcular
        self.calc_button = ttk.Button(
            button_frame,
            text="CALCULAR",
            command=self.calculate,
            width=12
        )
        self.calc_button.pack(side=tk.LEFT, padx=5)
        
        # Botão Limpar
        clear_button = ttk.Button(
            button_frame,
            text="LIMPAR",
            command=self.clear_entries,
            width=12
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Botão Sair - CORRIGIDO
        exit_button = ttk.Button(
            button_frame,
            text="SAIR",
            command=self.fechar_aplicacao,  # Alterado para a função correta
            width=12
        )
        exit_button.pack(side=tk.LEFT, padx=5)
        
        # Frame de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultado", padding="10")
        result_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        # Porcentagem
        self.percentage_label = ttk.Label(
            result_frame,
            textvariable=self.resultado_divisao,
            style='BigResult.TLabel',
            foreground="#2196F3"
        )
        self.percentage_label.pack(pady=(0, 5))
        
        # Recomendação
        self.recommendation_label = tk.Label(
            result_frame,
            textvariable=self.resultado_texto,
            font=("Arial", 11, "bold"),
            wraplength=380,
            anchor="center",
            justify="center"
        )
        self.recommendation_label.pack()
        
        # Frame de detalhes do cálculo
        details_frame = ttk.LabelFrame(main_frame, text="Detalhes do Cálculo", padding="8")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Variáveis para detalhes
        self.detalhes_texto = tk.StringVar(value="Aguardando cálculo...")
        
        # Label para detalhes
        self.details_label = tk.Label(
            details_frame,
            textvariable=self.detalhes_texto,
            font=("Consolas", 9),
            bg="#f5f5f5",
            relief="flat",
            padx=8,
            pady=4,
            justify=tk.LEFT,
            wraplength=380,
            anchor="w"
        )
        self.details_label.pack(fill=tk.BOTH, expand=True)
        
        # Vincular tecla Enter
        self.alcool_entry.bind('<Return>', lambda event: self.gasolina_entry.focus_set())
        self.gasolina_entry.bind('<Return>', lambda event: self.calculate())
        
    def setup_validation(self):
        """Configurar validação para entradas numéricas"""
        # Função para validar entrada numérica
        def validate_numeric(P):
            if P == "" or P == "." or P == ",":
                return True
            try:
                # Substituir vírgula por ponto para validação
                test_value = P.replace(',', '.', 1)
                float(test_value)
                return True
            except ValueError:
                return False
        
        # Registrar função de validação
        vcmd = (self.root.register(validate_numeric), '%P')
        
        # Aplicar validação às entradas
        self.alcool_entry.config(validate="key", validatecommand=vcmd)
        self.gasolina_entry.config(validate="key", validatecommand=vcmd)
        
    def get_entry_value(self, value):
        """Obter valor numérico da entrada"""
        if not value:
            return None
        # Substituir vírgula por ponto e converter para float
        try:
            return float(value.replace(',', '.', 1))
        except ValueError:
            return None
        
    def calculate(self):
        """Calcular qual combustível compensa mais"""
        alcool_val = self.get_entry_value(self.alcool_val.get())
        gasolina_val = self.get_entry_value(self.gasolina_val.get())
        
        # Validar entradas
        if alcool_val is None or gasolina_val is None:
            messagebox.showwarning(
                "Valores inválidos",
                "Por favor, digite valores numéricos válidos para ambos os combustíveis."
            )
            return
            
        if alcool_val <= 0 or gasolina_val <= 0:
            messagebox.showwarning(
                "Valores inválidos",
                "Os preços devem ser maiores que zero."
            )
            return
            
        if gasolina_val == 0:
            messagebox.showerror(
                "Erro de cálculo",
                "O preço da gasolina não pode ser zero."
            )
            return
        
        # Calcular porcentagem
        resultado = (alcool_val / gasolina_val) * 100
        self.resultado_divisao.set(f"{resultado:.2f}%")
        
        # Determinar recomendação
        if resultado < 70:
            recomendacao = "✅ COMPENSA MAIS ABASTECER COM ÁLCOOL"
            cor = self.cor_compensa
        else:
            recomendacao = "⛽ COMPENSA MAIS ABASTECER COM GASOLINA"
            cor = self.cor_nao_compensa
        
        # Atualizar labels
        self.resultado_texto.set(recomendacao)
        self.percentage_label.config(foreground=cor)
        self.recommendation_label.config(foreground=cor)
        
        # Atualizar detalhes do cálculo
        detalhes = f"Álcool: R$ {alcool_val:.3f}/litro\n"
        detalhes += f"Gasolina: R$ {gasolina_val:.3f}/litro\n"
        detalhes += f"Fórmula: ({alcool_val:.3f} ÷ {gasolina_val:.3f}) × 100 = {resultado:.2f}%\n"
        
        if resultado < 70:
            detalhes += f"Conclusão: {resultado:.2f}% < 70% → Compensa Álcool"
        else:
            detalhes += f"Conclusão: {resultado:.2f}% ≥ 70% → Compensa Gasolina"
            
        self.detalhes_texto.set(detalhes)
        
        # Garantir que a janela não redimensione
        self.root.update_idletasks()
        
    def clear_entries(self):
        """Limpar todas as entradas e resultados"""
        self.alcool_val.set("")
        self.gasolina_val.set("")
        self.resultado_divisao.set("")
        self.resultado_texto.set("Digite os preços para calcular")
        self.detalhes_texto.set("Aguardando cálculo...")
        self.percentage_label.config(foreground="#2196F3")
        self.recommendation_label.config(foreground="black")
        self.alcool_entry.focus_set()
    
    def fechar_aplicacao(self):
        """Função para fechar a aplicação"""
        resposta = messagebox.askyesno(
            "Confirmar saída",
            "Tem certeza que deseja sair?"
        )
        
        if resposta:
            self.root.destroy()  # Fecha completamente a aplicação

def main():
    """Função principal"""
    root = tk.Tk()
    app = AlcoolGasolinaApp(root)
    
    # Centralizar janela
    root.update_idletasks()
    largura = root.winfo_width()
    altura = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f'{largura}x{altura}+{x}+{y}')
    
    # Garantir tamanho fixo
    root.minsize(500, 380)
    root.maxsize(500, 380)
    
    root.mainloop()

if __name__ == "__main__":
    main()
