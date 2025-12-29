import os
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class AplicativoRenomeadorArquivos:
    def __init__(self, root):
        self.root = root
        self.root.title("Renomeador de Arquivos Aleatório")
        self.root.geometry("450x540")
        self.root.resizable(False, False)
        
        # Variável para armazenar o diretório selecionado
        self.diretorio_selecionado = tk.StringVar()
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Criar widgets
        self.criar_widgets()
        
    def configurar_estilos(self):
        """Configurar estilos para a aplicação"""
        style = ttk.Style()
        style.configure('Titulo.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))
        
    def criar_widgets(self):
        """Criar todos os widgets da interface"""
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        label_titulo = ttk.Label(frame_principal, 
                                text="Renomeador de Arquivos Aleatórios", 
                                style='Titulo.TLabel')
        label_titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seção de diretório
        frame_diretorio = ttk.LabelFrame(frame_principal, 
                                         text="Selecionar Diretório", 
                                         padding="10")
        frame_diretorio.grid(row=1, column=0, columnspan=3, 
                            sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Campo de entrada para mostrar o diretório
        entrada_diretorio = ttk.Entry(frame_diretorio, 
                                     textvariable=self.diretorio_selecionado, 
                                     width=50)
        entrada_diretorio.grid(row=0, column=0, padx=(0, 10))
        
        # Botão para buscar diretório
        botao_buscar = ttk.Button(frame_diretorio, text="Buscar...", 
                                 command=self.buscar_diretorio)
        botao_buscar.grid(row=0, column=1)
        
        # Seção de opções
        frame_opcoes = ttk.LabelFrame(frame_principal, text="Opções", padding="10")
        frame_opcoes.grid(row=2, column=0, columnspan=3, 
                         sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Comprimento do nome aleatório
        ttk.Label(frame_opcoes, text="Comprimento do nome:").grid(row=0, column=0, sticky=tk.W)
        self.var_comprimento = tk.IntVar(value=8)
        spinbox_comprimento = ttk.Spinbox(frame_opcoes, from_=4, to=20, 
                                         textvariable=self.var_comprimento, 
                                         width=10)
        spinbox_comprimento.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Checkbox para excluir este script
        self.var_excluir_script = tk.BooleanVar(value=True)
        checkbox_excluir = ttk.Checkbutton(frame_opcoes, 
                                          text="Excluir este script da renomeação", 
                                          variable=self.var_excluir_script)
        checkbox_excluir.grid(row=1, column=0, columnspan=2, 
                             pady=(10, 0), sticky=tk.W)
        
        # Área de informação
        frame_info = ttk.LabelFrame(frame_principal, text="Informações", padding="10")
        frame_info.grid(row=3, column=0, columnspan=3, 
                       sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Texto informativo
        texto_info = """Este programa renomeará todos os arquivos no diretório 
selecionado com nomes aleatórios.

Características:
• Gera nomes aleatórios com letras e números
• Pode excluir este script para evitar renomeá-lo
• Verifica se não há nomes duplicados
• Mostra um resumo das alterações"""
        
        label_info = ttk.Label(frame_info, text=texto_info, 
                              style='Info.TLabel', justify=tk.LEFT, 
                              wraplength=400)
        label_info.grid(row=0, column=0, sticky=tk.W)
        
        # Botões de ação
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.grid(row=4, column=0, columnspan=3)
        
        # Botão para renomear
        botao_renomear = ttk.Button(frame_botoes, text="Renomear Arquivos", 
                                   command=self.renomear_arquivos)
        botao_renomear.grid(row=0, column=0, padx=(0, 10))
        
        # Botão para sair
        botao_sair = ttk.Button(frame_botoes, text="Sair", 
                               command=self.root.quit)
        botao_sair.grid(row=0, column=1)
        
        # Barra de status
        self.var_status = tk.StringVar(value="Pronto. Selecione um diretório.")
        barra_status = ttk.Label(self.root, textvariable=self.var_status, 
                                relief=tk.SUNKEN, anchor=tk.W)
        barra_status.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar expansão das colunas
        frame_principal.columnconfigure(0, weight=1)
        
    def buscar_diretorio(self):
        """Abrir diálogo para selecionar diretório"""
        diretorio = filedialog.askdirectory(title="Selecionar Diretório")
        if diretorio:
            self.diretorio_selecionado.set(diretorio)
            self.var_status.set(f"Diretório selecionado: {diretorio}")
            
    def gerar_nome_aleatorio(self, comprimento=8):
        """Gerar um nome de arquivo aleatório"""
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(comprimento))
    
    def renomear_arquivos(self):
        """Função principal para renomear arquivos"""
        diretorio = self.diretorio_selecionado.get()
        
        # Validar se um diretório foi selecionado
        if not diretorio:
            messagebox.showerror("Erro", "Por favor, selecione um diretório primeiro.")
            return
            
        # Verificar se o diretório existe
        if not os.path.exists(diretorio):
            messagebox.showerror("Erro", f"O diretório não existe:\n{diretorio}")
            return
            
        # Confirmar com o usuário
        confirmar = messagebox.askyesno(
            "Confirmar",
            f"Tem certeza que deseja renomear todos os arquivos em:\n{diretorio}\n\n"
            "Esta ação não pode ser desfeita facilmente."
        )
        
        if not confirmar:
            return
            
        try:
            # Obter o nome do script atual se deve ser excluído
            script_atual = os.path.basename(__file__) if self.var_excluir_script.get() else None
            
            contador_renomeados = 0
            erros = []
            
            # Obter lista de arquivos
            arquivos = os.listdir(diretorio)
            
            # Processar cada arquivo
            for nome_arquivo in arquivos:
                try:
                    # Excluir o script atual se configurado
                    if script_atual and nome_arquivo == script_atual:
                        continue
                        
                    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
                    
                    # Verificar se é um arquivo (não um diretório)
                    if not os.path.isfile(caminho_arquivo):
                        continue
                    
                    # Separar nome e extensão
                    nome, extensao = os.path.splitext(nome_arquivo)
                    
                    # Gerar novo nome
                    novo_nome = self.gerar_nome_aleatorio(self.var_comprimento.get()) + extensao
                    
                    # Verificar se o novo nome já não existe
                    while os.path.exists(os.path.join(diretorio, novo_nome)):
                        novo_nome = self.gerar_nome_aleatorio(self.var_comprimento.get()) + extensao
                    
                    # Renomear o arquivo
                    novo_caminho = os.path.join(diretorio, novo_nome)
                    os.rename(caminho_arquivo, novo_caminho)
                    contador_renomeados += 1
                    
                except Exception as e:
                    erros.append(f"{nome_arquivo}: {str(e)}")
            
            # Mostrar resultados
            if erros:
                mensagem_resultado = (
                    f"Processo concluído com {len(erros)} erro(s).\n\n"
                    f"Arquivos renomeados: {contador_renomeados}\n\n"
                    f"Erros:\n" + "\n".join(erros[:10])  # Mostrar apenas os primeiros 10 erros
                )
                if len(erros) > 10:
                    mensagem_resultado += f"\n\n... e mais {len(erros) - 10} erro(s)."
                
                messagebox.showwarning("Resultado com erros", mensagem_resultado)
            else:
                messagebox.showinfo(
                    "Sucesso",
                    f"Processo concluído com sucesso!\n\n"
                    f"Total de arquivos renomeados: {contador_renomeados}"
                )
            
            self.var_status.set(f"Concluído: {contador_renomeados} arquivos renomeados em {diretorio}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado:\n{str(e)}")
            self.var_status.set("Erro durante o processo de renomeação")

def main():
    """Função principal para iniciar a aplicação"""
    root = tk.Tk()
    app = AplicativoRenomeadorArquivos(root)
    
    # Centralizar a janela na tela
    root.update_idletasks()
    largura = root.winfo_width()
    altura = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f'{largura}x{altura}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
