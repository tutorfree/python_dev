#!/usr/bin/env python
# -*- coding: utf-8 -*-

# É claro que você precisa ter um arquivo .txt com uma lista de URLs.
# Cada URL em uma linha.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import requests
import concurrent.futures
import threading
import queue
import time
from datetime import datetime

class VerificadorURLsTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificador de URLs")
        self.root.geometry("900x650")
        
        # Variáveis
        self.urls = []
        self.arquivo_atual = ""
        self.verificacao_em_andamento = False
        
        # Queue para comunicação entre threads
        self.fila_resultados = queue.Queue()
        
        # Configurar interface
        self.configurar_interface()
        
        # Iniciar thread para processar resultados
        self.iniciar_processador_resultados()
        
    def configurar_interface(self):
        """Configurar todos os elementos da interface gráfica"""
        
        # Frame principal com scrollbar
        frame_principal = ttk.Frame(self.root)
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos para expansão
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.rowconfigure(3, weight=1)
        
        # Título
        titulo_label = ttk.Label(
            frame_principal,
            text="Verificador de URLs",
            font=("Arial", 18, "bold")
        )
        titulo_label.grid(row=0, column=0, pady=(10, 5), sticky=tk.W)
        
        # Frame de controle
        frame_controle = ttk.LabelFrame(frame_principal, text="Controle", padding="10")
        frame_controle.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Botão para carregar arquivo
        botao_carregar = ttk.Button(
            frame_controle,
            text="Carregar Arquivo de URLs",
            command=self.carregar_arquivo,
            width=20
        )
        botao_carregar.grid(row=0, column=0, padx=(0, 10))
        
        # Label para mostrar arquivo atual
        self.label_arquivo = ttk.Label(
            frame_controle,
            text="Nenhum arquivo carregado",
            font=("Arial", 9),
            foreground="gray"
        )
        self.label_arquivo.grid(row=0, column=1, padx=(0, 10))
        
        # Botão para verificar URLs
        self.botao_verificar = ttk.Button(
            frame_controle,
            text="Iniciar Verificação",
            command=self.iniciar_verificacao,
            width=20,
            state="disabled"
        )
        self.botao_verificar.grid(row=0, column=2, padx=(0, 10))
        
        # Botão para parar verificação
        self.botao_parar = ttk.Button(
            frame_controle,
            text="Parar Verificação",
            command=self.parar_verificacao,
            width=20,
            state="disabled"
        )
        self.botao_parar.grid(row=0, column=3, padx=(0, 10))
        
        # Botão para limpar resultados
        botao_limpar = ttk.Button(
            frame_controle,
            text="Limpar Resultados",
            command=self.limpar_resultados,
            width=20
        )
        botao_limpar.grid(row=0, column=4)
        
        # Frame de estatísticas
        frame_stats = ttk.LabelFrame(frame_principal, text="Estatísticas", padding="10")
        frame_stats.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Labels para estatísticas
        self.label_total = ttk.Label(frame_stats, text="Total: 0")
        self.label_total.grid(row=0, column=0, padx=(0, 20))
        
        self.label_concluido = ttk.Label(frame_stats, text="Concluído: 0")
        self.label_concluido.grid(row=0, column=1, padx=(0, 20))
        
        self.label_sucesso = ttk.Label(frame_stats, text="Sucesso: 0", foreground="green")
        self.label_sucesso.grid(row=0, column=2, padx=(0, 20))
        
        self.label_erro = ttk.Label(frame_stats, text="Erro: 0", foreground="red")
        self.label_erro.grid(row=0, column=3, padx=(0, 20))
        
        self.label_redirecionamento = ttk.Label(frame_stats, text="Redirecionamento: 0", foreground="orange")
        self.label_redirecionamento.grid(row=0, column=4, padx=(0, 20))
        
        # Barra de progresso
        self.progresso = ttk.Progressbar(frame_stats, mode='determinate', length=200)
        self.progresso.grid(row=0, column=5, padx=(20, 0))
        
        # Frame de resultados
        frame_resultados = ttk.LabelFrame(frame_principal, text="Resultados", padding="10")
        frame_resultados.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5), padx=5)
        
        # Configurar expansão do frame de resultados
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
        
        # Área de texto com scroll para mostrar resultados
        self.texto_resultados = scrolledtext.ScrolledText(
            frame_resultados,
            wrap=tk.WORD,
            width=100,
            height=20,
            font=("Consolas", 9)
        )
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags para cores
        self.configurar_tags_cores()
        
        # Frame de rodapé
        frame_rodape = ttk.Frame(frame_principal)
        frame_rodape.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(5, 10))
        
        # Status
        self.status_var = tk.StringVar(value="Pronto. Carregue um arquivo para começar.")
        label_status = ttk.Label(frame_rodape, textvariable=self.status_var)
        label_status.grid(row=0, column=0, sticky=tk.W)
        
    def configurar_tags_cores(self):
        """Configurar tags para cores no widget de texto"""
        self.texto_resultados.tag_config("sucesso", foreground="green")
        self.texto_resultados.tag_config("erro", foreground="red")
        self.texto_resultados.tag_config("redirecionamento", foreground="orange")
        self.texto_resultados.tag_config("info", foreground="blue")
        self.texto_resultados.tag_config("timestamp", foreground="gray")
        
    def carregar_arquivo(self):
        """Carregar arquivo com URLs"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo de URLs",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'r', encoding='utf-8') as file:
                    self.urls = [linha.strip() for linha in file if linha.strip()]
                
                self.arquivo_atual = arquivo
                self.label_arquivo.config(text=f"Arquivo: {arquivo.split('/')[-1]} ({len(self.urls)} URLs)")
                self.botao_verificar.config(state="normal")
                self.atualizar_estatisticas(0, 0, 0, 0)
                self.status_var.set(f"Arquivo carregado: {len(self.urls)} URLs encontradas")
                
                # CORREÇÃO: Adicionar quebras de linha nas mensagens iniciais
                self.adicionar_log("info", f"Arquivo carregado: {arquivo}\n")
                self.adicionar_log("info", f"Total de URLs: {len(self.urls)}\n\n")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler arquivo:\n{str(e)}")
                self.status_var.set("Erro ao carregar arquivo")
    
    def iniciar_verificacao(self):
        """Iniciar a verificação das URLs"""
        if not self.urls:
            messagebox.showwarning("Aviso", "Nenhuma URL para verificar. Carregue um arquivo primeiro.")
            return
        
        self.verificacao_em_andamento = True
        self.botao_verificar.config(state="disabled")
        self.botao_parar.config(state="normal")
        self.progresso.config(maximum=len(self.urls), value=0)
        
        # Resetar estatísticas
        self.atualizar_estatisticas(len(self.urls), 0, 0, 0)
        
        # Iniciar thread para verificação
        thread_verificacao = threading.Thread(target=self.verificar_urls_thread)
        thread_verificacao.daemon = True
        thread_verificacao.start()
        
        self.status_var.set("Verificação em andamento...")
        # CORREÇÃO: Adicionar quebra de linha
        self.adicionar_log("info", "Iniciando verificação de URLs\n\n")
    
    def verificar_urls_thread(self):
        """Thread para verificar URLs em paralelo"""
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(self.verificar_url, url): url for url in self.urls}
                
                for future in concurrent.futures.as_completed(futures):
                    if not self.verificacao_em_andamento:
                        break
                    
                    try:
                        resultado = future.result()
                        self.fila_resultados.put(resultado)
                    except Exception as e:
                        self.fila_resultados.put({
                            'url': futures[future],
                            'status': 'erro',
                            'mensagem': f"Erro na thread: {str(e)}"
                        })
        
        except Exception as e:
            self.fila_resultados.put({
                'tipo': 'erro_sistema',
                'mensagem': f"Erro no executor: {str(e)}"
            })
        
        # Sinalizar que a verificação terminou
        self.fila_resultados.put({'tipo': 'finalizado'})
    
    def verificar_url(self, url):
        """Verificar uma URL individual"""
        resultado = {
            'url': url,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        
        try:
            # Realiza uma requisição HEAD com timeout
            response = requests.head(url, allow_redirects=True, timeout=10)
            status_code = response.status_code
            
            resultado['status_code'] = status_code
            
            if status_code == 200:
                resultado['status'] = 'sucesso'
                resultado['mensagem'] = f"Status Code 200 OK"
            else:
                resultado['status'] = 'erro'
                resultado['mensagem'] = f"Status Code {status_code}"
            
            # Verificar redirecionamento
            if response.history:
                resultado['redirecionamento'] = response.url
                resultado['status'] = 'redirecionamento'
                resultado['mensagem'] += f" → Redireciona para: {response.url}"
            
        except requests.exceptions.Timeout:
            resultado['status'] = 'erro'
            resultado['mensagem'] = "Timeout - Tempo de resposta excedido"
        except requests.exceptions.ConnectionError:
            resultado['status'] = 'erro'
            resultado['mensagem'] = "Erro de conexão - Não foi possível conectar"
        except requests.exceptions.RequestException as e:
            resultado['status'] = 'erro'
            resultado['mensagem'] = f"Erro: {str(e)}"
        except Exception as e:
            resultado['status'] = 'erro'
            resultado['mensagem'] = f"Erro inesperado: {str(e)}"
        
        return resultado
    
    def iniciar_processador_resultados(self):
        """Iniciar thread para processar resultados da fila"""
        def processar():
            while True:
                try:
                    resultado = self.fila_resultados.get(timeout=0.1)
                    
                    if resultado.get('tipo') == 'finalizado':
                        self.verificacao_concluida()
                        continue
                    elif resultado.get('tipo') == 'erro_sistema':
                        self.adicionar_log("erro", resultado['mensagem'] + "\n")
                        continue
                    
                    self.processar_resultado(resultado)
                    
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Erro no processador de resultados: {e}")
        
        thread_processador = threading.Thread(target=processar)
        thread_processador.daemon = True
        thread_processador.start()
    
    def processar_resultado(self, resultado):
        """Processar um resultado individual"""
        # Atualizar interface na thread principal
        self.root.after(0, self.atualizar_interface_com_resultado, resultado)
    
    def atualizar_interface_com_resultado(self, resultado):
        """Atualizar interface com um resultado (deve ser chamado na thread principal)"""
        # Atualizar estatísticas
        self.atualizar_estatisticas_com_resultado(resultado)
        
        # Adicionar log com formatação
        tag = resultado.get('status', 'info')
        timestamp = resultado.get('timestamp', '')
        url = resultado.get('url', '')
        mensagem = resultado.get('mensagem', '')
        
        # CORREÇÃO: Adicionar quebra de linha no final de cada resultado
        log_text = f"[{timestamp}] {url}: {mensagem}\n"
        self.adicionar_log(tag, log_text)
        
        # Atualizar barra de progresso
        if hasattr(self, 'concluido'):
            self.progresso['value'] = self.concluido
    
    def atualizar_estatisticas(self, total, concluido, sucesso, erro):
        """Atualizar estatísticas"""
        self.total = total
        self.concluido = concluido
        self.sucesso = sucesso
        self.erro = erro
        
        self.label_total.config(text=f"Total: {total}")
        self.label_concluido.config(text=f"Concluído: {concluido}")
        self.label_sucesso.config(text=f"Sucesso: {sucesso}")
        self.label_erro.config(text=f"Erro: {erro}")
        
        # Calcular redirecionamentos
        redirecionamentos = max(0, self.concluido - self.sucesso - self.erro)
        self.label_redirecionamento.config(text=f"Redirecionamento: {redirecionamentos}")
    
    def atualizar_estatisticas_com_resultado(self, resultado):
        """Atualizar estatísticas com base no resultado"""
        self.concluido += 1
        
        if resultado.get('status') == 'sucesso':
            self.sucesso += 1
        elif resultado.get('status') == 'erro':
            self.erro += 1
        # Nota: redirecionamentos são contados automaticamente pela diferença
        
        self.atualizar_estatisticas(self.total, self.concluido, self.sucesso, self.erro)
    
    def adicionar_log(self, tag, mensagem):
        """Adicionar mensagem à área de resultados"""
        self.texto_resultados.insert(tk.END, mensagem, tag)
        self.texto_resultados.see(tk.END)
        self.texto_resultados.update()
    
    def parar_verificacao(self):
        """Parar a verificação em andamento"""
        if self.verificacao_em_andamento:
            self.verificacao_em_andamento = False
            self.status_var.set("Verificação interrompida pelo usuário")
            # CORREÇÃO: Adicionar quebras de linha
            self.adicionar_log("info", "\n--- Verificação interrompida pelo usuário ---\n\n")
            self.verificacao_concluida()
    
    def verificacao_concluida(self):
        """Lidar com a conclusão da verificação"""
        self.verificacao_em_andamento = False
        self.botao_verificar.config(state="normal")
        self.botao_parar.config(state="disabled")
        
        # Atualizar status
        self.status_var.set(f"Verificação concluída. {self.concluido}/{self.total} URLs verificadas")
        
        # Adicionar resumo - CORREÇÃO: Já estava correto com quebras de linha
        resumo = f"\n{'='*60}\n"
        resumo += "RESUMO DA VERIFICAÇÃO:\n"
        resumo += f"Total de URLs: {self.total}\n"
        resumo += f"URLs verificadas: {self.concluido}\n"
        resumo += f"Com sucesso (200 OK): {self.sucesso}\n"
        resumo += f"Com redirecionamento: {self.concluido - self.sucesso - self.erro}\n"
        resumo += f"Com erro: {self.erro}\n"
        resumo += f"{'='*60}\n\n"  # CORREÇÃO: Adicionar quebra de linha extra no final
        
        self.adicionar_log("info", resumo)
    
    def limpar_resultados(self):
        """Limpar todos os resultados"""
        if self.verificacao_em_andamento:
            messagebox.showwarning("Aviso", "Não é possível limpar durante uma verificação.")
            return
        
        resposta = messagebox.askyesno(
            "Confirmar",
            "Tem certeza que deseja limpar todos os resultados?"
        )
        
        if resposta:
            self.texto_resultados.delete(1.0, tk.END)
            self.atualizar_estatisticas(0, 0, 0, 0)
            self.progresso['value'] = 0
            self.status_var.set("Resultados limpos")
            # CORREÇÃO: Adicionar mensagem após limpar
            self.adicionar_log("info", "Resultados limpos. Pronto para nova verificação.\n")
    
    def on_closing(self):
        """Lidar com o fechamento da janela"""
        if self.verificacao_em_andamento:
            resposta = messagebox.askyesno(
                "Verificação em andamento",
                "Uma verificação está em andamento. Deseja realmente sair?"
            )
            if not resposta:
                return
        
        self.root.destroy()

def main():
    """Função principal"""
    root = tk.Tk()
    app = VerificadorURLsTkinter(root)
    
    # Configurar fechamento da janela
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
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
