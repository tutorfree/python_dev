import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

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
        Messagebox.show_error("Não foi possível salvar o histórico!", "Erro")

def reset_entries():
    peso.delete(0, 'end')
    altura.delete(0, 'end')
    lb_resultado.config(text="Digite seus dados e clique em Calcular", bootstyle="")
    resetar_faixas()
    peso.focus_set()

def resetar_faixas():
    """Reseta a aparência de todas as faixas"""
    for i, card in enumerate(cards_faixas):
        # Resetar frame principal
        card.configure(bootstyle="")
        
        # Resetar todos os labels dentro do card
        for widget in card.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(bootstyle="")
            elif isinstance(widget, ttk.Frame):  # Frame do indicador
                widget.configure(bootstyle="default")

def calcular():
    try:
        # Substitui vírgula por ponto para conversão float
        peso_val = peso.get().replace(',', '.')
        altura_val = altura.get().replace(',', '.')

        if peso_val and altura_val:
            p = float(peso_val)
            a = float(altura_val)
            imc = p / (a**2)
            
            # Formata para 2 casas decimais
            imc_formatado = f"{imc:.2f}"
            lb_resultado.config(text=f"Seu IMC é: {imc_formatado}")
            
            # Determinar categoria e estilo
            categorias = [
                (17, "Muito abaixo do peso", "danger"),
                (18.49, "Abaixo do peso", "warning"),
                (24.99, "Peso normal", "success"),
                (29.99, "Acima do peso", "warning"),
                (34.99, "Obesidade Grau I", "danger"),
                (39.99, "Obesidade Grau II", "danger"),
                (float('inf'), "Obesidade Mórbida", "dark")
            ]
            
            # Resetar todas as faixas primeiro
            resetar_faixas()
            
            # Encontrar categoria
            categoria_nome = "Peso normal"
            bootstyle = "success"
            categoria_index = 2  # Default: peso normal
            
            for i, (limite, cat, style) in enumerate(categorias):
                if imc <= limite:
                    categoria_nome = cat
                    bootstyle = style
                    categoria_index = i
                    break
            
            # Destacar a faixa correspondente
            destacar_faixa(categoria_index, bootstyle)
            
            # Atualizar label de resultado com estilo
            lb_resultado.configure(bootstyle=f"{bootstyle}")
            
            # Salvar no histórico
            historico = carregar_historico()
            
            registro = {
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "peso": p,
                "altura": a,
                "imc": round(imc, 2),
                "categoria": categoria_nome
            }
            
            historico.append(registro)
            salvar_historico(historico)
            
            # Mostrar mensagem de sucesso
            Messagebox.show_info("Registro salvo no histórico com sucesso!", "Sucesso")
            
            # Atualizar estatísticas se a janela estiver aberta
            if hasattr(janela, 'janela_historico') and janela.janela_historico.winfo_exists():
                atualizar_estatisticas()

        else:
            Messagebox.show_warning("Preencha todos os campos!", "Atenção")
    except ValueError:
        Messagebox.show_error("Use apenas números válidos nos campos!", "Erro")

def destacar_faixa(index, estilo):
    """Destaca visualmente a faixa de IMC correspondente"""
    card = cards_faixas[index]
    
    # Destacar o frame principal
    card.configure(bootstyle=f"{estilo}")
    
    # Destacar o indicador
    for widget in card.winfo_children():
        if isinstance(widget, ttk.Frame) and widget.winfo_width() == 5:  # Indicador
            widget.configure(bootstyle=f"{estilo}")
    
    # Destacar os textos
    texto_frame = None
    for widget in card.winfo_children():
        if isinstance(widget, ttk.Frame) and widget.winfo_width() != 5:  # Frame de texto
            texto_frame = widget
            break
    
    if texto_frame:
        for widget in texto_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(bootstyle=f"{estilo}")

def criar_janela_historico():
    """Cria a janela de histórico"""
    if hasattr(janela, 'janela_historico') and janela.janela_historico.winfo_exists():
        janela.janela_historico.lift()
        return
    
    janela.janela_historico = ttk.Toplevel(title="Histórico de IMC")
    janela.janela_historico.geometry("900x600")
    janela.janela_historico.position_center()
    
    # Frame principal
    main_frame = ttk.Frame(janela.janela_historico)
    main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)
    
    # Frame de botões
    frame_botoes = ttk.Frame(main_frame)
    frame_botoes.pack(fill=X, pady=(0, 10))
    
    ttk.Button(frame_botoes, text="📊 Ver Gráfico", 
              command=mostrar_grafico,
              bootstyle="info").pack(side=LEFT, padx=5)
    
    ttk.Button(frame_botoes, text="📤 Exportar JSON", 
              command=exportar_json,
              bootstyle="success").pack(side=LEFT, padx=5)
    
    ttk.Button(frame_botoes, text="🗑️ Limpar Histórico", 
              command=limpar_historico,
              bootstyle="danger").pack(side=LEFT, padx=5)
    
    # Frame para tabela
    frame_tabela = ttk.Labelframe(main_frame, text="Registros", bootstyle="info")
    frame_tabela.pack(fill=BOTH, expand=YES)
    
    # Carregar histórico
    historico = carregar_historico()
    
    if historico:
        # Criar tabela
        coldata = [
            {"text": "Data/Hora", "stretch": False, "width": 150},
            {"text": "Peso (kg)", "stretch": False, "width": 100},
            {"text": "Altura (m)", "stretch": False, "width": 100},
            {"text": "IMC", "stretch": False, "width": 100},
            {"text": "Categoria", "stretch": True}
        ]
        
        tabela = Tableview(
            master=frame_tabela,
            coldata=coldata,
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle="primary",
            height=15,
            stripecolor=("#7ca37b", None)
        )
        
        # Adicionar dados (do mais recente para o mais antigo)
        for registro in reversed(historico):
            tabela.insert_row(
                "end",
                [
                    registro["data"],
                    f"{registro['peso']:.2f}",
                    f"{registro['altura']:.2f}",
                    f"{registro['imc']:.2f}",
                    registro["categoria"]
                ]
            )
        
        tabela.autofit_columns()
        tabela.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Frame de estatísticas
        frame_stats = ttk.Frame(main_frame)
        frame_stats.pack(fill=X, pady=(10, 0))
        
        atualizar_estatisticas()
        
    else:
        ttk.Label(frame_tabela, text="Nenhum registro encontrado.", 
                 font=("Helvetica", 12)).pack(pady=50)

def atualizar_estatisticas():
    """Atualiza as estatísticas na janela de histórico"""
    if not hasattr(janela, 'janela_historico') or not janela.janela_historico.winfo_exists():
        return
    
    historico = carregar_historico()
    
    if historico and len(historico) > 0:
        # Encontrar ou criar frame de estatísticas
        for widget in janela.janela_historico.winfo_children():
            if isinstance(widget, ttk.Frame) and widget.winfo_children():
                if isinstance(widget.winfo_children()[0], ttk.Label) and "Estatísticas" in widget.winfo_children()[0].cget("text"):
                    widget.destroy()
                    break
        
        frame_stats = ttk.Labelframe(janela.janela_historico, text="Estatísticas", bootstyle="success")
        frame_stats.pack(fill=X, padx=20, pady=(10, 20))
        
        # Calcular estatísticas
        imcs = [r["imc"] for r in historico]
        pesos = [r["peso"] for r in historico]
        ultimo = historico[-1]
        
        cols = frame_stats.grid_size()[0]
        
        # Último registro
        ttk.Label(frame_stats, text="Última medição:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky=W, padx=10, pady=5)
        ttk.Label(frame_stats, text=f"{ultimo['imc']:.2f} - {ultimo['categoria']}", 
                 bootstyle="info", font=("Helvetica", 10, "bold")).grid(row=0, column=1, sticky=W, padx=10, pady=5)
        
        # Média
        ttk.Label(frame_stats, text="Média do IMC:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky=W, padx=10, pady=5)
        ttk.Label(frame_stats, text=f"{sum(imcs)/len(imcs):.2f}", 
                 bootstyle="secondary").grid(row=1, column=1, sticky=W, padx=10, pady=5)
        
        # Variação de peso
        if len(historico) > 1:
            primeiro_peso = historico[0]["peso"]
            variacao = ultimo["peso"] - primeiro_peso
            ttk.Label(frame_stats, text="Variação de peso:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky=W, padx=10, pady=5)
            estilo = "success" if variacao < 0 else "danger" if variacao > 0 else "secondary"
            sinal = "+" if variacao > 0 else ""
            ttk.Label(frame_stats, text=f"{sinal}{variacao:.2f} kg", 
                     bootstyle=estilo).grid(row=2, column=1, sticky=W, padx=10, pady=5)
        
        # Total de registros
        ttk.Label(frame_stats, text="Total de registros:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, sticky=W, padx=10, pady=5)
        ttk.Label(frame_stats, text=str(len(historico)), 
                 bootstyle="primary").grid(row=3, column=1, sticky=W, padx=10, pady=5)

def mostrar_grafico():
    """Mostra um gráfico do histórico de IMC"""
    historico = carregar_historico()
    
    if len(historico) < 2:
        Messagebox.show_info("É necessário pelo menos 2 registros para gerar um gráfico!", "Informação")
        return
    
    # Extrair dados para o gráfico
    datas = [datetime.strptime(r["data"], "%d/%m/%Y %H:%M:%S") for r in historico]
    imcs = [r["imc"] for r in historico]
    
    # Criar janela para o gráfico
    janela_grafico = ttk.Toplevel(title="Gráfico do Histórico de IMC")
    janela_grafico.geometry("800x500")
    janela_grafico.position_center()
    
    # Frame para controles
    frame_controles = ttk.Frame(janela_grafico)
    frame_controles.pack(fill=X, padx=20, pady=(20, 10))
    
    ttk.Label(frame_controles, text="Tipo de gráfico:", font=("Helvetica", 10)).pack(side=LEFT, padx=(0, 10))
    
    tipo_var = tk.StringVar(value="linha")
    
    ttk.Radiobutton(frame_controles, text="Linha", variable=tipo_var, value="linha",
                   command=lambda: atualizar_grafico(tipo_var.get())).pack(side=LEFT, padx=5)
    ttk.Radiobutton(frame_controles, text="Barras", variable=tipo_var, value="barras",
                   command=lambda: atualizar_grafico(tipo_var.get())).pack(side=LEFT, padx=5)
    
    # Frame para o gráfico
    frame_grafico = ttk.Frame(janela_grafico)
    frame_grafico.pack(fill=BOTH, expand=YES, padx=20, pady=10)
    
    def atualizar_grafico(tipo="linha"):
        """Atualiza o gráfico baseado no tipo selecionado"""
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        if tipo == "linha":
            ax.plot(datas, imcs, 'b-o', linewidth=2, markersize=6, label='IMC')
        else:
            ax.bar(range(len(imcs)), imcs, color='skyblue', alpha=0.7, label='IMC')
            ax.set_xticks(range(len(imcs)))
            ax.set_xticklabels([d.strftime("%d/%m") for d in datas], rotation=45)
        
        # Adicionar áreas de referência
        ax.axhspan(18.5, 24.99, alpha=0.2, color='green', label='Peso Normal')
        ax.axhline(y=18.5, color='green', linestyle='--', alpha=0.5)
        ax.axhline(y=24.99, color='green', linestyle='--', alpha=0.5)
        
        # Configurações do gráfico
        ax.set_xlabel('Data' if tipo == "linha" else 'Medições')
        ax.set_ylabel('IMC')
        ax.set_title('Evolução do IMC')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        if tipo == "linha":
            fig.autofmt_xdate()
        
        plt.tight_layout()
        
        # Embeddar o gráfico na janela tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
    
    # Criar gráfico inicial
    atualizar_grafico()

def exportar_json():
    """Exporta o histórico para um arquivo JSON"""
    historico = carregar_historico()
    if not historico:
        Messagebox.show_warning("Nenhum dado para exportar!", "Aviso")
        return
    
    try:
        # Criar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"historico_imc_exportado_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        
        Messagebox.show_info(f"Histórico exportado para:\n{filename}", "Sucesso")
    except Exception as e:
        Messagebox.show_error(f"Erro ao exportar: {str(e)}", "Erro")

def limpar_historico():
    """Limpa todo o histórico"""
    resposta = Messagebox.show_question(
        "Tem certeza que deseja limpar todo o histórico?\nEsta ação não pode ser desfeita.",
        "Confirmar",
        buttons=["Não:secondary", "Sim:primary"]
    )
    
    if resposta == "Sim":
        try:
            if os.path.exists(HISTORICO_FILE):
                os.remove(HISTORICO_FILE)
            Messagebox.show_info("Histórico limpo com sucesso!", "Sucesso")
            
            # Fechar janela de histórico se estiver aberta
            if hasattr(janela, 'janela_historico') and janela.janela_historico.winfo_exists():
                janela.janela_historico.destroy()
                del janela.janela_historico
        except Exception as e:
            Messagebox.show_error(f"Erro ao limpar histórico: {str(e)}", "Erro")

if __name__ == "__main__":
    # Criar janela principal com ttkbootstrap
    janela = ttk.Window(
        title="Calculadora de IMC Avançada",
        themename="superhero",  # Tema: darkly, solar, superhero, etc.
        size=(500, 650),
        resizable=(False, False),
        position=(100, 100)
    )
    
    # Configurar atalho Enter
    janela.bind('<Return>', lambda event: calcular())
    
    # Frame principal
    main_frame = ttk.Frame(janela)
    main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)
    
    # Título
    ttk.Label(
        main_frame,
        text="Calculadora de IMC",
        font=("Helvetica", 24, "bold"),
        bootstyle="primary"
    ).pack(pady=(0, 20))
    
    # Frame para entrada de dados
    frame_dados = ttk.Labelframe(main_frame, text="Dados Pessoais", bootstyle="info")
    frame_dados.pack(fill=X, pady=(0, 15))
    
    # Campo Peso
    ttk.Label(frame_dados, text="Peso (kg):", font=("Helvetica", 11)).grid(row=0, column=0, sticky=W, padx=10, pady=10)
    peso = ttk.Entry(frame_dados, font=("Helvetica", 11))
    peso.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
    peso.focus_set()
    
    # Campo Altura
    ttk.Label(frame_dados, text="Altura (m):", font=("Helvetica", 11)).grid(row=1, column=0, sticky=W, padx=10, pady=(0, 10))
    altura = ttk.Entry(frame_dados, font=("Helvetica", 11))
    altura.grid(row=1, column=1, padx=10, pady=(0, 10), sticky=EW)
    
    frame_dados.columnconfigure(1, weight=1)
    
    # Frame para botões
    frame_botoes = ttk.Frame(main_frame)
    frame_botoes.pack(fill=X, pady=(0, 20))
    
    ttk.Button(
        frame_botoes,
        text="🧮 Calcular",
        command=calcular,
        bootstyle="success",
        width=12
    ).pack(side=LEFT, padx=5)
    
    ttk.Button(
        frame_botoes,
        text="🗑️ Limpar",
        command=reset_entries,
        bootstyle="warning",
        width=12
    ).pack(side=LEFT, padx=5)
    
    ttk.Button(
        frame_botoes,
        text="📊 Histórico",
        command=criar_janela_historico,
        bootstyle="info",
        width=12
    ).pack(side=LEFT, padx=5)
    
    # Resultado
    lb_resultado = ttk.Label(
        main_frame,
        text="Digite seus dados e clique em Calcular",
        font=("Helvetica", 14, "bold"),
        anchor="center"
    )
    lb_resultado.pack(fill=X, pady=(0, 20))
    
    # Frame para faixas de IMC
    frame_faixas = ttk.Labelframe(main_frame, text="Faixas de IMC", bootstyle="primary")
    frame_faixas.pack(fill=BOTH, expand=YES)
    
    # Definir faixas de IMC
    faixas_imc = [
        ("Abaixo de 17", "Muito abaixo do peso", "danger"),
        ("17 - 18,49", "Abaixo do peso", "warning"),
        ("18,5 - 24,99", "Peso normal", "success"),
        ("25 - 29,99", "Acima do peso", "warning"),
        ("30 - 34,99", "Obesidade Grau I", "danger"),
        ("35 - 39,99", "Obesidade Grau II", "danger"),
        ("Acima de 40", "Obesidade Mórbida", "dark")
    ]
    
    cards_faixas = []
    
    for i, (imc_range, descricao, estilo) in enumerate(faixas_imc):
        card = ttk.Frame(frame_faixas)
        card.pack(fill=X, padx=10, pady=3)
        
        # Indicador colorido
        indicador = ttk.Frame(card, width=5, bootstyle=estilo)
        indicador.pack(side=LEFT, fill=Y)
        
        # Texto da faixa
        texto_frame = ttk.Frame(card)
        texto_frame.pack(side=LEFT, fill=X, expand=YES, padx=(10, 0))
        
        ttk.Label(
            texto_frame,
            text=imc_range,
            font=("Helvetica", 10, "bold"),
            bootstyle=estilo
        ).pack(anchor=W)
        
        ttk.Label(
            texto_frame,
            text=descricao,
            font=("Helvetica", 9)
        ).pack(anchor=W)
        
        cards_faixas.append(card)
    
    # Rodapé
    ttk.Separator(main_frame).pack(fill=X, pady=(20, 10))
    ttk.Label(
        main_frame,
        text="Desenvolvido com ttkbootstrap • Histórico salvo automaticamente",
        font=("Helvetica", 8),
        bootstyle="secondary"
    ).pack()
    
    janela.mainloop()
