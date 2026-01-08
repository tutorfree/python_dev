import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Nome do arquivo para salvar o histórico
HISTORICO_FILE = "historico_imc.json"

def carregar_historico():
    """Carrega o histórico do arquivo JSON"""
    if os.path.exists(HISTORICO_FILE):
        try:
            with open(HISTORICO_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def salvar_historico(historico):
    """Salva o histórico no arquivo JSON"""
    try:
        with open(HISTORICO_FILE, 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
    except IOError:
        messagebox.showerror("Erro", "Não foi possível salvar o histórico!")

def reset_entries():
    peso.delete(0, 'end')
    altura.delete(0, 'end')
    lbDivisao.config(text="")
    for lbP in lbP_list:
        lbP.config(bg=default_bg)
    peso.focus_set()

def calcular():
    try:
        # Cores para cada faixa de IMC
        cor = ['Aquamarine', 'MediumAquamarine', 'LightGreen', 'yellow', 'salmon', 'Tomato', 'red']
        
        # Substitui vírgula por ponto para conversão float
        peso_val = peso.get().replace(',', '.')
        altura_val = altura.get().replace(',', '.')

        if peso_val and altura_val:
            p = float(peso_val)
            a = float(altura_val)
            imc = p / (a**2)
            
            # Formata para 2 casas decimais e exibe com vírgula
            imc_formatado = f"{imc:.2f}".replace('.', ',')
            lbDivisao.config(text=f"IMC: {imc_formatado}")

            # Reseta cores antes de destacar a nova
            for lbP in lbP_list:
                lbP.config(bg=default_bg)

            # Lógica de faixas
            limites_imc = [17, 18.49, 24.99, 29.99, 34.99, 39.99]
            categoria_index = 6  # Default: última categoria
            for i, limite in enumerate(limites_imc):
                if imc <= limite:
                    lbP_list[i].config(bg=cor[i])
                    categoria_index = i
                    break
            else:
                lbP_list[-1].config(bg=cor[-1])

            # Salvar no histórico
            historico = carregar_historico()
            
            # Obter categoria
            categorias = [
                "Muito abaixo do peso",
                "Abaixo do peso",
                "Peso normal",
                "Acima do peso",
                "Obesidade I",
                "Obesidade II",
                "Obesidade mórbida"
            ]
            
            registro = {
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "peso": p,
                "altura": a,
                "imc": round(imc, 2),
                "categoria": categorias[categoria_index]
            }
            
            historico.append(registro)
            salvar_historico(historico)
            
            messagebox.showinfo("Salvo", "Registro salvo no histórico com sucesso!")

        else:
            lbDivisao.config(text="Preencha os campos!")
    except ValueError:
        lbDivisao.config(text="Use apenas números e pontos/vírgulas!")

def ver_historico():
    """Exibe o histórico em uma nova janela"""
    historico = carregar_historico()
    
    if not historico:
        messagebox.showinfo("Histórico", "Nenhum registro encontrado!")
        return
    
    # Criar nova janela para o histórico
    janela_historico = tk.Toplevel(janela)
    janela_historico.title("Histórico de IMC")
    janela_historico.geometry("700x500")
    
    # Frame para os botões
    frame_botoes = tk.Frame(janela_historico)
    frame_botoes.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Button(frame_botoes, text="Ver Gráfico", command=lambda: mostrar_grafico(historico),
             cursor="hand2").pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Exportar JSON", command=exportar_json,
             cursor="hand2").pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Limpar Histórico", command=limpar_historico,
             cursor="hand2").pack(side=tk.LEFT, padx=5)
    
    # Frame para a tabela com scrollbar
    frame_tabela = tk.Frame(janela_historico)
    frame_tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Treeview (tabela)
    columns = ("Data", "Peso (kg)", "Altura (m)", "IMC", "Categoria")
    tree = ttk.Treeview(frame_tabela, columns=columns, show="headings", height=15)
    
    # Configurar colunas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    
    # Adicionar scrollbar
    scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Inserir dados
    for registro in reversed(historico):  # Mostrar do mais recente
        tree.insert("", "end", values=(
            registro["data"],
            registro["peso"],
            registro["altura"],
            registro["imc"],
            registro["categoria"]
        ))
    
    # Estatísticas
    frame_stats = tk.Frame(janela_historico)
    frame_stats.pack(fill=tk.X, padx=10, pady=5)
    
    if historico:
        ultimo = historico[-1]
        tk.Label(frame_stats, 
                text=f"Último IMC: {ultimo['imc']} | Categoria: {ultimo['categoria']}",
                font=("Arial", 10, "bold")).pack()

def mostrar_grafico(historico):
    """Mostra um gráfico do histórico de IMC"""
    if len(historico) < 2:
        messagebox.showinfo("Gráfico", "É necessário pelo menos 2 registros para gerar um gráfico!")
        return
    
    # Extrair dados para o gráfico
    datas = [registro["data"].split()[0] for registro in historico]  # Apenas a data
    imcs = [registro["imc"] for registro in historico]
    indices = list(range(1, len(historico) + 1))
    
    # Criar janela para o gráfico
    janela_grafico = tk.Toplevel(janela)
    janela_grafico.title("Gráfico do Histórico de IMC")
    janela_grafico.geometry("600x400")
    
    # Criar figura do matplotlib
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    
    # Plotar linha do IMC
    ax.plot(indices, imcs, 'b-o', linewidth=2, markersize=6, label='IMC')
    
    # Adicionar linha de referência para peso normal (IMC 18.5-24.99)
    ax.axhspan(18.5, 24.99, alpha=0.2, color='green', label='Peso Normal')
    
    # Configurações do gráfico
    ax.set_xlabel('Registros')
    ax.set_ylabel('IMC')
    ax.set_title('Evolução do IMC')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Adicionar valores nos pontos
    for i, (idx, imc_val) in enumerate(zip(indices, imcs)):
        ax.annotate(f'{imc_val:.1f}', (idx, imc_val), 
                   textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.tight_layout()
    
    # Embeddar o gráfico na janela tkinter
    canvas = FigureCanvasTkAgg(fig, master=janela_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def exportar_json():
    """Exporta o histórico para um arquivo JSON"""
    historico = carregar_historico()
    if not historico:
        messagebox.showwarning("Exportar", "Nenhum dado para exportar!")
        return
    
    try:
        # Criar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"historico_imc_exportado_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Sucesso", f"Histórico exportado para:\n{filename}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")

def limpar_historico():
    """Limpa todo o histórico"""
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar todo o histórico?"):
        try:
            if os.path.exists(HISTORICO_FILE):
                os.remove(HISTORICO_FILE)
            messagebox.showinfo("Sucesso", "Histórico limpo com sucesso!")
            
            # Fechar janela de histórico se estiver aberta
            for window in janela.winfo_children():
                if isinstance(window, tk.Toplevel) and "Histórico" in window.title():
                    window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar histórico: {str(e)}")

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Calculadora IMC 2025 - Com Histórico")
    janela.geometry("390x400+200+200")
    janela.resizable(False, False)
    
    default_bg = janela.cget('bg')

    # Atalho: apertar Enter também calcula
    janela.bind('<Return>', lambda event: calcular())

    lbP_list = []
    lbP_labels = [
        "Abaixo de 17 - Muito abaixo do peso ideal",
        "Entre 17 e 18,49 - Abaixo do peso ideal",
        "Entre 18,5 e 24,99 - Peso normal",
        "Entre 25 e 29,99 - Acima do peso",
        "Entre 30 e 34,99 - Obesidade (nível I)",
        "Entre 35 e 39,99 - Obesidade severa (nível II)",
        "Acima de 39,99 - Obesidade mórbida (nível III)"
    ]

    for i, text in enumerate(lbP_labels, start=1):
        lbP = tk.Label(janela, text=text, anchor="w", justify="left")
        lbP.place(x=50, y=160 + 20*i, width=300)
        lbP_list.append(lbP)

    tk.Label(janela, text="Peso (Kg): ").place(x=50, y=40)
    peso = tk.Entry(janela)
    peso.place(x=115, y=40, width=185)
    peso.focus_set()

    tk.Label(janela, text="Altura (m): ").place(x=50, y=70)
    altura = tk.Entry(janela)
    altura.place(x=115, y=70, width=185)

    btCalcular = tk.Button(janela, text="Calcular", width=10, command=calcular, cursor="hand2")
    btCalcular.place(x=115, y=110)

    btLimpar = tk.Button(janela, text="Limpar", width=10, command=reset_entries, cursor="hand2")
    btLimpar.place(x=213, y=110)
    
    # Botão para ver histórico
    btHistorico = tk.Button(janela, text="Ver Histórico", width=15, command=ver_historico, cursor="hand2")
    btHistorico.place(x=140, y=320)

    lbDivisao = tk.Label(janela, text="", foreground="blue", font="Arial 10 bold")
    lbDivisao.place(x=50, y=150)

    janela.mainloop()
