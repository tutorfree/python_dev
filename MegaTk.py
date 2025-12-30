#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from tkinter import *
    from tkinter import ttk, messagebox
except:
    from Tkinter import *
    import ttk
    import tkMessageBox as messagebox

import random
import datetime

class MegaSenaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Apostas - Mega-Sena")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Configurar cores
        self.cor_fundo = "#f0f0f0"
        self.cor_botao = "#4CAF50"
        self.cor_botao_hover = "#45a049"
        self.cor_spinbox = "#ffffff"
        
        self.root.configure(bg=self.cor_fundo)
        
        # Variáveis
        self.numeros_gerados = []
        
        # Configurar interface
        self.configurar_interface()
        
    def configurar_interface(self):
        """Configurar todos os elementos da interface gráfica"""
        
        # Título
        titulo = Label(
            self.root,
            text="GERADOR DE APOSTAS - MEGA-SENA",
            font=("Arial", 16, "bold"),
            bg=self.cor_fundo,
            fg="#2196F3"
        )
        titulo.pack(pady=(20, 10))
        
        # Frame de entrada
        frame_entrada = Frame(self.root, bg=self.cor_fundo)
        frame_entrada.pack(pady=(0, 15))
        
        # Label para instrução
        lb_instrucao = Label(
            frame_entrada,
            text="Quantas apostas deseja gerar?",
            font=("Arial", 10),
            bg=self.cor_fundo
        )
        lb_instrucao.grid(row=0, column=0, padx=(0, 10))
        
        # Spinbox para número de apostas (usando ttk.Spinbox para melhor aparência)
        self.spinbox_apostas = ttk.Spinbox(
            frame_entrada,
            from_=1,           # Valor mínimo
            to=100,            # Valor máximo
            increment=1,       # Incremento por clique
            width=8,           # Largura
            font=("Arial", 10, "bold"),
            justify="center"
        )
        self.spinbox_apostas.grid(row=0, column=1, padx=(0, 10))
        self.spinbox_apostas.delete(0, END)
        self.spinbox_apostas.insert(0, "1")
        
        # Botão gerar
        self.bt_gerar = Button(
            frame_entrada,
            text="GERAR APOSTAS",
            font=("Arial", 10, "bold"),
            bg=self.cor_botao,
            fg="white",
            relief="raised",
            width=15,
            command=self.gerar_apostas
        )
        self.bt_gerar.grid(row=0, column=2, padx=(0, 10))
        
        # Bind Enter key no Spinbox
        self.spinbox_apostas.bind('<Return>', lambda event: self.gerar_apostas())
        
        # Frame para botões de quantidade rápida (acima da lista)
        frame_rapido_topo = Frame(self.root, bg=self.cor_fundo)
        frame_rapido_topo.pack(pady=(0, 10))
        
        # Label para botões rápidos
        Label(
            frame_rapido_topo,
            text="Gerar rapidamente:",
            font=("Arial", 9),
            bg=self.cor_fundo
        ).pack(side=LEFT, padx=(0, 10))
        
        # Frame para os botões de quantidade
        frame_botoes_quantidade = Frame(frame_rapido_topo, bg=self.cor_fundo)
        frame_botoes_quantidade.pack(side=LEFT)
        
        # Botões para diferentes quantidades
        quantidade_botoes = [
            ("1", "#4CAF50", lambda: self.definir_e_gerar(1)),
            ("3", "#2196F3", lambda: self.definir_e_gerar(3)),
            ("5", "#9C27B0", lambda: self.definir_e_gerar(5)),
            ("10", "#FF9800", lambda: self.definir_e_gerar(10)),
            ("20", "#F44336", lambda: self.definir_e_gerar(20))
        ]
        
        for texto, cor, comando in quantidade_botoes:
            btn = Button(
                frame_botoes_quantidade,
                text=texto,
                font=("Arial", 9, "bold"),
                bg=cor,
                fg="white",
                relief="flat",
                width=4,
                command=comando
            )
            btn.pack(side=LEFT, padx=2)
            
            # Efeito hover (escurecer ao passar o mouse)
            cor_escura = self.escurecer_cor(cor, 20)
            btn.bind("<Enter>", lambda e, b=btn, c=cor_escura: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=cor: b.config(bg=c))
        
        # Frame para lista de apostas
        frame_lista = Frame(self.root, bg=self.cor_fundo)
        frame_lista.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Label para a lista
        lb_lista = Label(
            frame_lista,
            text="APOSTAS GERADAS:",
            font=("Arial", 10, "bold"),
            bg=self.cor_fundo
        )
        lb_lista.pack(anchor=W, pady=(0, 5))
        
        # Frame para lista com scrollbar
        frame_listbox = Frame(frame_lista, bg=self.cor_fundo)
        frame_listbox.pack(fill=BOTH, expand=True)
        
        # Scrollbar vertical
        scrollbar_y = Scrollbar(frame_listbox)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        
        # Scrollbar horizontal
        scrollbar_x = Scrollbar(frame_listbox, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        
        # Listbox para mostrar as apostas
        self.lista_apostas = Listbox(
            frame_listbox,
            font=("Consolas", 10, "bold"),
            bg="white",
            fg="#333",
            selectbackground="#4CAF50",
            selectforeground="white",
            relief="solid",
            bd=2,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        self.lista_apostas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.lista_apostas.yview)
        scrollbar_x.config(command=self.lista_apostas.xview)
        
        # Frame para botões de controle
        frame_botoes = Frame(self.root, bg=self.cor_fundo)
        frame_botoes.pack(pady=(5, 15))
        
        # Botão limpar todas as apostas
        bt_limpar_todas = Button(
            frame_botoes,
            text="LIMPAR TODAS",
            font=("Arial", 9),
            bg="#FF9800",
            fg="white",
            relief="raised",
            width=18,
            command=self.limpar_todas
        )
        bt_limpar_todas.grid(row=0, column=1, padx=5)
        
        # Botão apagar selecionada
        bt_apagar_selecionada = Button(
            frame_botoes,
            text="APAGAR SELECIONADA",
            font=("Arial", 9),
            bg="#F44336",
            fg="white",
            relief="raised",
            width=20,
            command=self.apagar_selecionada
        )
        bt_apagar_selecionada.grid(row=0, column=2, padx=5)
        
        # Botão copiar apostas
        bt_copiar = Button(
            frame_botoes,
            text="COPIAR APOSTAS",
            font=("Arial", 9),
            bg="#2196F3",
            fg="white",
            relief="raised",
            width=18,
            command=self.copiar_apostas
        )
        bt_copiar.grid(row=0, column=3, padx=5)
        
        # Frame de informações
        frame_info = Frame(self.root, bg=self.cor_fundo)
        frame_info.pack(pady=(0, 15))
        
        # Informações
        info_texto = """• Cada aposta contém 6 números únicos entre 01 e 60
• Os números são automaticamente ordenados
• Use as setas (↑↓) ou digite para definir a quantidade
• Total de combinações possíveis: 50.063.860
• Apostas válidas apenas para fins de estudo"""
        
        lb_info = Label(
            frame_info,
            text=info_texto,
            font=("Arial", 8),
            bg=self.cor_fundo,
            fg="#666",
            justify=LEFT
        )
        lb_info.pack()
        
        # Configurar efeito hover nos botões principais
        self.configurar_efeitos_hover()
    
    def escurecer_cor(self, cor_hex, percentual):
        """Escurecer uma cor hex em um percentual"""
        # Converter hex para RGB
        cor_hex = cor_hex.lstrip('#')
        rgb = tuple(int(cor_hex[i:i+2], 16) for i in (0, 2, 4))
        
        # Escurecer cada componente
        rgb_escuro = tuple(max(0, int(c * (100 - percentual) / 100)) for c in rgb)
        
        # Converter de volta para hex
        return f'#{rgb_escuro[0]:02x}{rgb_escuro[1]:02x}{rgb_escuro[2]:02x}'
    
    def configurar_efeitos_hover(self):
        """Configurar efeitos hover nos botões"""
        botoes = [
            (self.bt_gerar, "#4CAF50", "#45a049"),
            (self.bt_gerar, "#45a049", "#4CAF50")
        ]
        
        for botao, cor_entrada, cor_saida in botoes:
            if botao:
                botao.bind("<Enter>", lambda e, b=botao, c=cor_entrada: b.config(bg=c))
                botao.bind("<Leave>", lambda e, b=botao, c=cor_saida: b.config(bg=c))
    
    def definir_e_gerar(self, quantidade):
        """Definir quantidade no spinbox e gerar apostas"""
        self.spinbox_apostas.delete(0, END)
        self.spinbox_apostas.insert(0, str(quantidade))
        self.gerar_apostas()
    
    def gerar_apostas(self):
        """Gerar apostas da Mega-Sena"""
        try:
            # Limpar lista anterior
            self.numeros_gerados = []
            
            # Obter número de apostas do Spinbox
            texto_apostas = self.spinbox_apostas.get().strip()
            
            # Validar entrada
            if not texto_apostas:
                messagebox.showwarning("Aviso", "Por favor, digite o número de apostas.")
                self.spinbox_apostas.focus_set()
                return
            
            numero_apostas = int(texto_apostas)
            
            # Validar número de apostas
            if numero_apostas <= 0:
                messagebox.showwarning("Aviso", "Digite um número maior que zero.")
                self.spinbox_apostas.select_range(0, END)
                self.spinbox_apostas.focus_set()
                return
            
            if numero_apostas > 100:
                resposta = messagebox.askyesno(
                    "Confirmação",
                    f"Deseja gerar {numero_apostas} apostas? Isso pode demorar um pouco.\n\n"
                    f"Recomenda-se gerar no máximo 100 apostas por vez."
                )
                if not resposta:
                    return
            
            if numero_apostas > 50:
                messagebox.showinfo(
                    "Aguarde",
                    f"Gerando {numero_apostas} apostas...\n"
                    f"Por favor, aguarde alguns instantes."
                )
            
            # Limpar lista atual
            self.lista_apostas.delete(0, END)
            
            # Gerar as apostas
            for i in range(numero_apostas):
                # Gerar 6 números únicos entre 1 e 60
                numeros = random.sample(range(1, 61), 6)
                numeros.sort()
                
                # Formatar os números com 2 dígitos
                numeros_formatados = [f"{num:02d}" for num in numeros]
                
                # Armazenar para possível cópia
                self.numeros_gerados.append(numeros_formatados)
                
                # Criar texto da aposta
                texto_aposta = f"Aposta {i+1:03d}: {' '.join(numeros_formatados)}"
                
                # Adicionar à lista
                self.lista_apostas.insert(END, texto_aposta)
            
            # Feedback visual
            if numero_apostas == 1:
                messagebox.showinfo("Sucesso", f"1 aposta gerada com sucesso!")
            else:
                messagebox.showinfo("Sucesso", f"{numero_apostas} apostas geradas com sucesso!")
            
            # Dar foco novamente ao Spinbox
            self.spinbox_apostas.select_range(0, END)
            self.spinbox_apostas.focus_set()
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite um número válido (1-100).")
            self.spinbox_apostas.delete(0, END)
            self.spinbox_apostas.insert(0, "1")
            self.spinbox_apostas.select_range(0, END)
            self.spinbox_apostas.focus_set()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado:\n{str(e)}")
    
    def limpar_todas(self):
        """Limpar todas as apostas da lista"""
        if self.lista_apostas.size() == 0:
            messagebox.showinfo("Informação", "Não há apostas para limpar.")
            return
        
        resposta = messagebox.askyesno(
            "Confirmar",
            "Tem certeza que deseja limpar todas as apostas?"
        )
        
        if resposta:
            self.lista_apostas.delete(0, END)
            self.numeros_gerados = []
            messagebox.showinfo("Sucesso", "Todas as apostas foram removidas.")
    
    def apagar_selecionada(self):
        """Apagar a aposta selecionada"""
        selecao = self.lista_apostas.curselection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma aposta para apagar.")
            return
        
        indice = selecao[0]
        
        resposta = messagebox.askyesno(
            "Confirmar",
            f"Apagar a aposta selecionada?\n\n{self.lista_apostas.get(indice)}"
        )
        
        if resposta:
            self.lista_apostas.delete(indice)
            if indice < len(self.numeros_gerados):
                self.numeros_gerados.pop(indice)
    
    def copiar_apostas(self):
        """Copiar apostas para a área de transferência"""
        if self.lista_apostas.size() == 0:
            messagebox.showwarning("Aviso", "Não há apostas para copiar.")
            return
        
        try:
            # Criar texto formatado
            texto_copia = "APOSTAS MEGA-SENA GERADAS:\n"
            texto_copia += "=" * 50 + "\n"
            
            for i, aposta in enumerate(self.numeros_gerados):
                texto_copia += f"Aposta {i+1:03d}: {' '.join(aposta)}\n"
            
            texto_copia += "=" * 50 + "\n"
            texto_copia += f"Total: {len(self.numeros_gerados)} apostas\n"
            
            data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            texto_copia += f"Gerado em: {data_hora}\n"
            
            # Copiar para área de transferência
            self.root.clipboard_clear()
            self.root.clipboard_append(texto_copia)
            self.root.update()  # Manter o conteúdo após fechar
            
            messagebox.showinfo("Sucesso", "Apostas copiadas para a área de transferência!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar:\n{str(e)}")

def main():
    """Função principal"""
    root = Tk()
    app = MegaSenaApp(root)
    
    # Centralizar janela
    root.update_idletasks()
    largura = root.winfo_width()
    altura = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f'{largura}x{altura}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
