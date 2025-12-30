import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
import random
import time
import sys
import os
import pygame

class ColorMemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória de Cores")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f0f0')
        
        # Evitar redimensionamento
        self.root.resizable(False, False)

        # --- Variáveis para controle de áudio ---
        self.is_muted = False
        self.last_volume = 0.5

        # --- Adição de trilha sonora com pygame ---
        try:
            self.tocar_trilha_sonora()
        except:
            print("Áudio não disponível, continuando sem som...")
        
        # Configurações de cores para o jogo (6 pares = 12 cartas)
        self.base_colors = [
            '#FF0000',  # Vermelho
            '#00FF00',  # Verde
            '#0000FF',  # Azul
            '#FFFF00',  # Amarelo
            '#FF00FF',  # Magenta
            '#00FFFF',  # Ciano
        ]
        
        # Dicionário com nomes das cores
        self.color_names = {
            '#FF0000': 'Vermelho',
            '#00FF00': 'Verde',
            '#0000FF': 'Azul',
            '#FFFF00': 'Amarelo',
            '#FF00FF': 'Magenta',
            '#00FFFF': 'Ciano',
        }
        
        # Lista de cores embaralhadas
        self.color_pairs = []
        
        # Variáveis do jogo
        self.first_choice = None
        self.second_choice = None
        self.can_click = True
        self.matches_found = 0
        self.total_pairs = len(self.base_colors)
        self.score = 0
        self.attempts = 0
        self.game_started = False
        
        # Botões do jogo
        self.color_buttons = []
        
        # Interface
        self.setup_ui()
        
    def tocar_trilha_sonora(self):
    """Inicializa o pygame e toca a música."""
        try:
            # Caminho relativo mais simples
            caminho_musica = os.path.join(os.path.dirname(__file__), 'sound', 'trilha.mp3')
            
            # Ou se preferir o caminho absoluto da pasta atual:
            # caminho_musica = os.path.join(os.getcwd(), 'sound', 'trilha.mp3')
            
            print(f"Procurando música em: {caminho_musica}")
            
            # Verificar se arquivo existe
            if not os.path.exists(caminho_musica):
                # Tentar outro caminho comum
                caminho_musica = 'sound/trilha.mp3'
                print(f"Tentando caminho alternativo: {caminho_musica}")
                
            if not os.path.exists(caminho_musica):
                print("Arquivo de música não encontrado em nenhum dos caminhos.")
                return
                
            pygame.mixer.init()
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.last_volume)
            print(f"Trilha sonora carregada com sucesso: {caminho_musica}")
        except Exception as e:
            print(f"Erro ao carregar música: {e}")

    def setup_ui(self):
        # Cabeçalho mais compacto
        header_frame = Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        title_label = Label(header_frame, text="Jogo da Memória de Cores", 
                            font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True, pady=15)
        
        # Frame de instruções
        self.instructions_frame = Frame(self.root, bg='#f0f0f0')
        self.instructions_frame.pack(pady=3)
        
        self.instructions_label = Label(self.instructions_frame, 
                                        text="Clique em 'Novo Jogo' para começar!",
                                        font=('Arial', 12), bg='#f0f0f0', fg='#2c3e50')
        self.instructions_label.pack()
        
        # Frame do temporizador
        self.timer_frame = Frame(self.root, bg='#f0f0f0')
        self.timer_frame.pack(pady=3)
        
        self.timer_label = Label(self.timer_frame, text="Tempo: 0s", 
                                font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#e74c3c')
        self.timer_label.pack()
        
        # Frame do jogo
        self.game_container = Frame(self.root, bg='#f0f0f0')
        self.game_container.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Frame de pontuação
        self.score_frame = Frame(self.root, bg='#f0f0f0')
        self.score_frame.pack(pady=3)
        
        self.score_label = Label(self.score_frame, 
                                text=f"Pares: 0/{self.total_pairs} | Tentativas: 0 | Pontos: 0",
                                font=('Arial', 12), bg='#f0f0f0', fg='#2c3e50')
        self.score_label.pack()
        
        # --- Frame de botões ---
        self.button_frame = Frame(self.root, bg='#f0f0f0')
        self.button_frame.pack(pady=5)
        
        self.start_button = Button(self.button_frame, text="Novo Jogo", font=('Arial', 12, 'bold'),
                                     bg='#27ae60', fg='white', relief=tk.RAISED, bd=2,
                                     command=self.start_new_game, width=12, height=1)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = Button(self.button_frame, text="Reiniciar", font=('Arial', 12),
                                     bg='#3498db', fg='white', relief=tk.RAISED, bd=2,
                                     command=self.reset_game, width=12, height=1)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Controles de volume (menores)
        self.volume_frame = Frame(self.root, bg='#f0f0f0')
        self.volume_frame.pack(pady=3)

        Label(self.volume_frame, text="Volume:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)

        self.volume_scale = tk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                     command=self.set_volume, length=150, bg='#f0f0f0', fg='#2c3e50',
                                     troughcolor='#bdc3c7', highlightthickness=0, showvalue=0)
        self.volume_scale.set(self.last_volume * 100)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        self.mute_button = Button(self.volume_frame, text="Mute", font=('Arial', 10),
                                  bg='#e74c3c', fg='white', relief=tk.RAISED, bd=1,
                                  command=self.toggle_mute, width=6)
        self.mute_button.pack(side=tk.LEFT, padx=5)
        
        # Inicializar o grid de cores
        self.create_color_grid()
        
        # Inicializar temporizador
        self.start_time = 0
        self.timer_running = False
        
        # Garantir que a janela apareça
        self.root.update_idletasks()
        
    def set_volume(self, value):
        """Define o volume do mixer do pygame."""
        if pygame.mixer.get_init():
            new_volume = float(value) / 100
            pygame.mixer.music.set_volume(new_volume)
            self.last_volume = new_volume
            if self.is_muted and new_volume > 0:
                self.is_muted = False
                self.mute_button.config(text="Mute", bg='#e74c3c')
            elif new_volume == 0:
                self.is_muted = True
                self.mute_button.config(text="Unmute", bg='#2ecc71')

    def toggle_mute(self):
        """Alterna o estado de mute do áudio."""
        if pygame.mixer.get_init():
            if self.is_muted:
                # Desmuta
                pygame.mixer.music.set_volume(self.last_volume)
                self.volume_scale.set(self.last_volume * 100)
                self.mute_button.config(text="Mute", bg='#e74c3c')
                self.is_muted = False
            else:
                # Muta
                pygame.mixer.music.set_volume(0)
                self.volume_scale.set(0)
                self.mute_button.config(text="Unmute", bg='#2ecc71')
                self.is_muted = True

    def create_color_grid(self):
        """Cria o grid de botões para o jogo da memória."""
        # Criar um frame para o grid
        self.game_frame = Frame(self.game_container, bg='#f0f0f0')
        self.game_frame.pack(pady=5)
        
        # Limpar o frame do jogo se já existirem widgets
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Criar um grid 4x3 para 12 cartas (6 pares)
        self.color_buttons = []
        for i in range(4):  # 4 linhas
            for j in range(3):  # 3 colunas
                index = i * 3 + j
                btn = Button(self.game_frame, text="", font=('Arial', 10),
                               width=8, height=3, bg='#34495e', fg='white',
                               relief=tk.RAISED, bd=2,
                               command=lambda idx=index: self.card_clicked(idx))
                btn.grid(row=i, column=j, padx=4, pady=4)
                self.color_buttons.append(btn)
        
        # Garantir que os botões sejam visíveis
        self.game_frame.update_idletasks()
    
    def start_new_game(self):
        """Inicia um novo jogo."""
        self.reset_game()
        self.shuffle_cards()
        self.game_started = True
        self.show_all_cards_briefly()
    
    def reset_game(self):
        """Reinicia o jogo."""
        self.matches_found = 0
        self.score = 0
        self.attempts = 0
        self.first_choice = None
        self.second_choice = None
        self.can_click = True
        self.game_started = False
        self.timer_running = False
        
        # Resetar todos os botões
        for btn in self.color_buttons:
            btn.config(bg='#34495e', text="", state=tk.NORMAL)
        
        # Atualizar display
        self.update_score_display()
        self.timer_label.config(text="Tempo: 0s")
        self.instructions_label.config(text="Clique em 'Novo Jogo' para começar!")
    
    def shuffle_cards(self):
        """Embaralha as cartas (cores)."""
        # Criar pares de cores
        self.color_pairs = []
        for color in self.base_colors:
            self.color_pairs.append(color)
            self.color_pairs.append(color)
        
        # Embaralhar as cartas
        random.shuffle(self.color_pairs)
    
    def show_all_cards_briefly(self):
        """Mostra todas as cartas por 2 segundos para memorização."""
        self.instructions_label.config(text="Memorize as posições das cores!")
        
        # Mostrar todas as cartas
        for i, color in enumerate(self.color_pairs):
            if i < len(self.color_buttons):  # Garantir que não ultrapasse
                self.color_buttons[i].config(
                    bg=color, 
                    fg='white' if self.is_dark_color(color) else 'black',
                    state=tk.DISABLED
                )
        
        # Iniciar o timer
        self.start_timer()
        
        # Após 2 segundos, esconder as cartas
        self.root.after(2000, self.hide_all_cards)
    
    def hide_all_cards(self):
        """Esconde todas as cartas (volta para cor padrão)."""
        for btn in self.color_buttons:
            btn.config(bg='#34495e', fg='white', text="", state=tk.NORMAL)
        
        self.instructions_label.config(text="Encontre os pares de cores!")
        self.can_click = True
    
    def card_clicked(self, index):
        """Lida com o clique em uma carta."""
        if not self.can_click or not self.game_started:
            return
        
        # Verificar se índice é válido
        if index >= len(self.color_buttons) or index >= len(self.color_pairs):
            return
        
        btn = self.color_buttons[index]
        
        # Se a carta já foi encontrada ou já está virada, ignorar
        if btn['state'] == tk.DISABLED or btn['bg'] != '#34495e':
            return
        
        # Virar a carta
        color = self.color_pairs[index]
        btn.config(
            bg=color, 
            fg='white' if self.is_dark_color(color) else 'black',
            state=tk.DISABLED
        )
        
        if self.first_choice is None:
            # Primeira escolha
            self.first_choice = (index, color)
        else:
            # Segunda escolha
            self.second_choice = (index, color)
            self.can_click = False
            self.attempts += 1
            
            # Verificar se formou um par
            if self.first_choice[1] == self.second_choice[1]:
                self.root.after(500, self.handle_match)
            else:
                self.root.after(1000, self.handle_mismatch)
            
            self.update_score_display()
    
    def handle_match(self):
        """Lida com um par encontrado."""
        if self.first_choice and self.second_choice:
            self.matches_found += 1
            self.score += 10
            
            # Manter cartas viradas, mostrar nome da cor
            idx1, color1 = self.first_choice
            idx2, color2 = self.second_choice
            
            color_name = self.color_names.get(color1, "")
            self.color_buttons[idx1].config(text=color_name)
            self.color_buttons[idx2].config(text=color_name)
            
            # Resetar escolhas
            self.first_choice = None
            self.second_choice = None
            self.can_click = True
            
            # Verificar se o jogo acabou
            if self.matches_found == self.total_pairs:
                self.root.after(500, self.end_game)
    
    def handle_mismatch(self):
        """Lida com um par errado."""
        if self.first_choice:
            idx1, _ = self.first_choice
            self.color_buttons[idx1].config(bg='#34495e', fg='white', text="", state=tk.NORMAL)
        
        if self.second_choice:
            idx2, _ = self.second_choice
            self.color_buttons[idx2].config(bg='#34495e', fg='white', text="", state=tk.NORMAL)
        
        # Resetar escolhas
        self.first_choice = None
        self.second_choice = None
        self.can_click = True
    
    def start_timer(self):
        """Inicia o temporizador."""
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Atualiza o temporizador."""
        if self.timer_running and self.game_started:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Tempo: {elapsed}s")
            
            # Atualizar a cada segundo
            self.root.after(1000, self.update_timer)
    
    def update_score_display(self):
        """Atualiza o display de pontuação."""
        self.score_label.config(
            text=f"Pares: {self.matches_found}/{self.total_pairs} | Tentativas: {self.attempts} | Pontos: {self.score}"
        )
    
    def end_game(self):
        """Finaliza o jogo."""
        self.timer_running = False
        elapsed = int(time.time() - self.start_time)
        
        # Calcular pontuação final
        time_bonus = max(0, 120 - elapsed)  # 2 minutos máximo
        final_score = self.score + time_bonus
        
        messagebox.showinfo(
            "Parabéns!",
            f"Você encontrou todos os pares!\n\n"
            f"Tempo: {elapsed} segundos\n"
            f"Tentativas: {self.attempts}\n"
            f"Pontuação base: {self.score}\n"
            f"Bônus por tempo: {time_bonus}\n"
            f"Pontuação final: {final_score}"
        )
        
        self.instructions_label.config(text="Jogo concluído! Clique em 'Novo Jogo' para jogar novamente.")
        self.game_started = False
    
    def is_dark_color(self, hex_color):
        """Verifica se uma cor é escura para definir a cor do texto."""
        if not hex_color or hex_color[0] != '#':
            return False
        
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) != 6:
                return False
            
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return brightness < 128
        except:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    game = ColorMemoryGame(root)
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_closing():
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
    if pygame.mixer.get_init():
        pygame.quit()
