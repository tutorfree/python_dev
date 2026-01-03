# ==============================
# SUPRESSÃO DE AVISOS NO INÍCIO
# ==============================
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
warnings.filterwarnings("ignore", message=".*deprecated.*")

import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
from PIL import Image, ImageTk  # Para manipular imagens
import random
import time
import os
import pygame
import sys

class ImageMemoryGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Jogo da Memória com Imagens")
        self.window.geometry("800x750")
        self.window.configure(bg='#f0f0f0')
        self.window.resizable(False, False)

        # Configurar ícone da janela (opcional)
        try:
            self.window.iconbitmap('icon.ico')
        except:
            pass
        
        # Variáveis para controle de áudio
        self.is_muted = False
        self.last_volume = 0.5

        # Inicializar pygame para áudio
        self.audio_initialized = False
        self.init_audio()
        
        # Configurações de imagens (6 pares = 12 cartas)
        self.image_files = [
            'carta01.png',
            'carta02.png',
            'carta03.png',
            'carta04.png',
            'carta05.png',
            'carta06.png'
        ]
        
        # Verificar se imagens existem
        if not self.check_images():
            return
        
        # Dicionário com nomes das imagens (opcional)
        self.image_names = {
            'carta01.png': 'Imagem 1',
            'carta02.png': 'Imagem 2',
            'carta03.png': 'Imagem 3',
            'carta04.png': 'Imagem 4',
            'carta05.png': 'Imagem 5',
            'carta06.png': 'Imagem 6'
        }
        
        # Lista de imagens embaralhadas
        self.image_pairs = []
        
        # Cache para imagens carregadas
        self.images_cache = {}
        self.back_image = None  # Imagem do verso das cartas
        
        # Variáveis do jogo
        self.first_choice = None
        self.second_choice = None
        self.can_click = True
        self.matches_found = 0
        self.total_pairs = len(self.image_files)
        self.score = 0
        self.attempts = 0
        self.game_started = False
        self.timer_running = False
        
        # Botões do jogo
        self.image_buttons = []
        
        # Carregar imagens
        if not self.load_images():
            return
        
        # Interface
        self.setup_ui()
        
    def init_audio(self):
        """Inicializa o sistema de áudio."""
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.audio_initialized = True
            self.tocar_trilha_sonora()
        except Exception as e:
            print(f"Áudio não disponível: {e}")
            self.audio_initialized = False
    
    def check_images(self):
        """Verifica se todas as imagens existem."""
        # Criar pasta images se não existir
        if not os.path.exists('images'):
            os.makedirs('images')
            messagebox.showinfo("Pasta Criada", 
                              "A pasta 'images' foi criada. Por favor, adicione suas imagens lá.")
            return False
        
        missing = []
        for img_file in self.image_files:
            img_path = os.path.join('images', img_file)
            if not os.path.exists(img_path):
                missing.append(img_file)
        
        if missing:
            messagebox.showwarning("Imagens faltando", 
                                  f"As seguintes imagens não foram encontradas:\n{', '.join(missing)}\n\n"
                                  f"Certifique-se de que todas estão na pasta 'images/'")
            return False
        return True
    
    def load_images(self):
        """Carrega todas as imagens em cache."""
        try:
            # Carregar imagem do verso (back)
            back_img_path = os.path.join('images', 'back.png')
            if os.path.exists(back_img_path):
                back_img = Image.open(back_img_path)
                print(f"Imagem do verso carregada: {back_img_path}")
            else:
                # Criar uma imagem de verso padrão
                print("Criando imagem do verso padrão...")
                back_img = Image.new('RGB', (100, 100), color='#34495e')
                # Adicionar um padrão simples
                from PIL import ImageDraw
                draw = ImageDraw.Draw(back_img)
                draw.rectangle([20, 20, 80, 80], outline='#2c3e50', width=3)
                draw.line([20, 20, 80, 80], fill='#2c3e50', width=2)
                draw.line([80, 20, 20, 80], fill='#2c3e50', width=2)
            
            # Redimensionar imagem do verso
            back_img = back_img.resize((100, 100), Image.Resampling.LANCZOS)
            self.back_image = ImageTk.PhotoImage(back_img)
            
            # Carregar imagens das cartas
            print("Carregando imagens das cartas...")
            for img_file in self.image_files:
                img_path = os.path.join('images', img_file)
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    # Redimensionar para tamanho consistente
                    img = img.resize((100, 100), Image.Resampling.LANCZOS)
                    self.images_cache[img_file] = ImageTk.PhotoImage(img)
                    print(f"  ✓ {img_file} carregada")
                else:
                    print(f"  ✗ {img_file} não encontrada")
                    return False
                    
            print("Todas as imagens foram carregadas com sucesso!")
            return True
                
        except Exception as e:
            print(f"Erro ao carregar imagens: {e}")
            messagebox.showerror("Erro", f"Não foi possível carregar as imagens:\n{e}")
            return False
    
    def tocar_trilha_sonora(self):
        """Inicializa o pygame e toca a música."""
        if not self.audio_initialized:
            return
            
        try:
            # Obter diretório atual
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Lista de possíveis caminhos para a música
            possible_paths = [
                os.path.join(current_dir, 'sound', 'trilha.mp3'),
                os.path.join(current_dir, 'sound', 'trilha.wav'),
                os.path.join(current_dir, 'trilha.mp3'),
                os.path.join(current_dir, 'trilha.wav'),
                'trilha.mp3',
                'trilha.wav',
                'sound/trilha.mp3',
                'sound/trilha.wav'
            ]
            
            music_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    music_path = path
                    print(f"🎵 Música encontrada: {path}")
                    break
            
            if not music_path:
                print("⚠️  Arquivo de música não encontrado. Continuando sem som.")
                return
            
            # Carregar e tocar música
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # -1 para loop infinito
            pygame.mixer.music.set_volume(self.last_volume)
            
        except pygame.error as e:
            print(f"Erro do pygame: {e}")
            self.audio_initialized = False
        except Exception as e:
            print(f"Erro ao carregar música: {e}")

    def setup_ui(self):
        # Cabeçalho
        header_frame = Frame(self.window, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        title_label = Label(header_frame, text="🎮 Jogo da Memória com Imagens 🎮", 
                            font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True, pady=15)
        
        # Frame de instruções
        self.instructions_frame = Frame(self.window, bg='#f0f0f0')
        self.instructions_frame.pack(pady=3)
        
        self.instructions_label = Label(self.instructions_frame, 
                                        text="Clique em 'Novo Jogo' para começar!",
                                        font=('Arial', 12), bg='#f0f0f0', fg='#2c3e50')
        self.instructions_label.pack()
        
        # Frame do temporizador
        self.timer_frame = Frame(self.window, bg='#f0f0f0')
        self.timer_frame.pack(pady=3)
        
        self.timer_label = Label(self.timer_frame, text="⏱️ Tempo: 0s", 
                                font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#e74c3c')
        self.timer_label.pack()
        
        # Frame do jogo
        self.game_container = Frame(self.window, bg='#f0f0f0')
        self.game_container.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Frame de pontuação
        self.score_frame = Frame(self.window, bg='#f0f0f0')
        self.score_frame.pack(pady=3)
        
        self.score_label = Label(self.score_frame, 
                                text=f"🔢 Pares: 0/{self.total_pairs} | 🔄 Tentativas: 0 | ⭐ Pontos: 0",
                                font=('Arial', 12), bg='#f0f0f0', fg='#2c3e50')
        self.score_label.pack()
        
        # Frame de botões
        self.button_frame = Frame(self.window, bg='#f0f0f0')
        self.button_frame.pack(pady=5)
        
        self.start_button = Button(self.button_frame, text="🆕 Novo Jogo", font=('Arial', 12, 'bold'),
                                     bg='#27ae60', fg='white', relief=tk.RAISED, bd=2,
                                     command=self.start_new_game, width=12, height=1)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = Button(self.button_frame, text="🔄 Reiniciar", font=('Arial', 12),
                                     bg='#3498db', fg='white', relief=tk.RAISED, bd=2,
                                     command=self.reset_game, width=12, height=1)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Controles de volume (só mostra se áudio estiver disponível)
        if self.audio_initialized:
            self.volume_frame = Frame(self.window, bg='#f0f0f0')
            self.volume_frame.pack(pady=3)

            Label(self.volume_frame, text="🔊 Volume:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)

            self.volume_scale = tk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                         command=self.set_volume, length=150, bg='#f0f0f0', fg='#2c3e50',
                                         troughcolor='#bdc3c7', highlightthickness=0, showvalue=False)
            self.volume_scale.set(self.last_volume * 100)
            self.volume_scale.pack(side=tk.LEFT, padx=5)

            self.mute_button = Button(self.volume_frame, text="🔇 Mute", font=('Arial', 10),
                                      bg='#e74c3c', fg='white', relief=tk.RAISED, bd=1,
                                      command=self.toggle_mute, width=8)
            self.mute_button.pack(side=tk.LEFT, padx=5)
        else:
            # Mostrar mensagem se áudio não estiver disponível
            no_audio_label = Label(self.window, text="🔇 Áudio não disponível", 
                                   font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
            no_audio_label.pack(pady=2)
        
        # Inicializar o grid de imagens
        self.create_image_grid()
        
        # Inicializar temporizador
        self.start_time = 0
        
        self.window.update_idletasks()
        
    def set_volume(self, value):
        if self.audio_initialized:
            new_volume = float(value) / 100
            pygame.mixer.music.set_volume(new_volume)
            self.last_volume = new_volume
            if self.is_muted and new_volume > 0:
                self.is_muted = False
                self.mute_button.config(text="🔇 Mute", bg='#e74c3c')
            elif new_volume == 0:
                self.is_muted = True
                self.mute_button.config(text="🔊 Unmute", bg='#2ecc71')

    def toggle_mute(self):
        if self.audio_initialized:
            if self.is_muted:
                pygame.mixer.music.set_volume(self.last_volume)
                self.volume_scale.set(self.last_volume * 100)
                self.mute_button.config(text="🔇 Mute", bg='#e74c3c')
                self.is_muted = False
            else:
                pygame.mixer.music.set_volume(0)
                self.volume_scale.set(0)
                self.mute_button.config(text="🔊 Unmute", bg='#2ecc71')
                self.is_muted = True

    def create_image_grid(self):
        """Cria o grid de cartas."""
        self.game_frame = Frame(self.game_container, bg='#f0f0f0')
        self.game_frame.pack(pady=5)
        
        # Limpar widgets existentes
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Criar um grid 4x3 para 12 cartas (6 pares)
        self.image_buttons = []
        for i in range(4):  # 4 linhas
            for j in range(3):  # 3 colunas
                index = i * 3 + j
                btn = Button(self.game_frame, image=self.back_image,
                               width=100, height=100, bg='#34495e',
                               relief=tk.RAISED, bd=2, cursor='hand2',
                               command=lambda idx=index: self.card_clicked(idx))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.image_buttons.append(btn)
        
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
        
        # Resetar todos os botões para mostrar o verso
        for btn in self.image_buttons:
            btn.config(image=self.back_image, state=tk.NORMAL, bd=2, relief=tk.RAISED)
        
        self.update_score_display()
        self.timer_label.config(text="⏱️ Tempo: 0s")
        self.instructions_label.config(text="Clique em 'Novo Jogo' para começar!")
    
    def shuffle_cards(self):
        """Embaralha as cartas."""
        self.image_pairs = []
        for img_file in self.image_files:
            # Adiciona cada imagem duas vezes (para formar pares)
            self.image_pairs.append(img_file)
            self.image_pairs.append(img_file)
        
        random.shuffle(self.image_pairs)
    
    def show_all_cards_briefly(self):
        """Mostra todas as cartas por 3 segundos para memorização."""
        self.instructions_label.config(text="👀 Memorize as posições das imagens!")
        
        # Mostrar todas as cartas
        for i, img_file in enumerate(self.image_pairs):
            if i < len(self.image_buttons):
                if img_file in self.images_cache:
                    self.image_buttons[i].config(image=self.images_cache[img_file])
                else:
                    self.image_buttons[i].config(text=f"Img {i+1}", bg='white')
                self.image_buttons[i].config(state=tk.DISABLED)
        
        # Iniciar temporizador
        self.start_timer()
        
        # Após 3 segundos, esconder as cartas
        self.window.after(3000, self.hide_all_cards)
    
    def hide_all_cards(self):
        """Esconde todas as cartas após o tempo de memorização."""
        for btn in self.image_buttons:
            btn.config(image=self.back_image, state=tk.NORMAL)
        
        self.instructions_label.config(text="🔍 Encontre os pares de imagens!")
        self.can_click = True
    
    def card_clicked(self, index):
        """Lida com o clique em uma carta."""
        if not self.can_click or not self.game_started:
            return
        
        if index >= len(self.image_buttons) or index >= len(self.image_pairs):
            return
        
        btn = self.image_buttons[index]
        
        if btn['state'] == tk.DISABLED:
            return
        
        # Virar a carta
        img_file = self.image_pairs[index]
        if img_file in self.images_cache:
            btn.config(image=self.images_cache[img_file])
        else:
            btn.config(text=self.image_names.get(img_file, f"Img {index+1}"), bg='white')
        btn.config(state=tk.DISABLED)
        
        if self.first_choice is None:
            self.first_choice = (index, img_file)
        else:
            self.second_choice = (index, img_file)
            self.can_click = False
            self.attempts += 1
            
            # Verificar se é um par
            if self.first_choice[1] == self.second_choice[1]:
                self.window.after(500, self.handle_match)
            else:
                self.window.after(1000, self.handle_mismatch)
            
            self.update_score_display()
    
    def handle_match(self):
        """Lida com um par encontrado."""
        if self.first_choice and self.second_choice:
            self.matches_found += 1
            self.score += 10
            
            idx1, img_file1 = self.first_choice
            idx2, _ = self.second_choice
            
            # Destacar as cartas encontradas
            self.image_buttons[idx1].config(bg='#2ecc71', relief=tk.SUNKEN)
            self.image_buttons[idx2].config(bg='#2ecc71', relief=tk.SUNKEN)
            
            self.first_choice = None
            self.second_choice = None
            self.can_click = True
            
            # Verificar se o jogo terminou
            if self.matches_found == self.total_pairs:
                self.window.after(500, self.end_game)
    
    def handle_mismatch(self):
        """Lida com um par errado."""
        if self.first_choice:
            idx1, _ = self.first_choice
            self.image_buttons[idx1].config(image=self.back_image, bg='#34495e', 
                                          state=tk.NORMAL, relief=tk.RAISED)
        
        if self.second_choice:
            idx2, _ = self.second_choice
            self.image_buttons[idx2].config(image=self.back_image, bg='#34495e',
                                          state=tk.NORMAL, relief=tk.RAISED)
        
        self.first_choice = None
        self.second_choice = None
        self.can_click = True
    
    def start_timer(self):
        """Inicia o temporizador."""
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Atualiza o temporizador a cada segundo."""
        if self.timer_running and self.game_started:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"⏱️ Tempo: {elapsed}s")
            self.window.after(1000, self.update_timer)
    
    def update_score_display(self):
        """Atualiza a exibição da pontuação."""
        self.score_label.config(
            text=f"🔢 Pares: {self.matches_found}/{self.total_pairs} | 🔄 Tentativas: {self.attempts} | ⭐ Pontos: {self.score}"
        )
    
    def end_game(self):
        """Finaliza o jogo quando todos os pares são encontrados."""
        self.timer_running = False
        elapsed = int(time.time() - self.start_time)
        
        # Calcular pontuação final
        time_bonus = max(0, 120 - elapsed)  # Bônus máximo de 120 segundos
        final_score = self.score + int(time_bonus)
        
        # Determinar mensagem baseada no desempenho
        if elapsed < 60:
            message = "🏆 EXCELENTE! Você é um mestre da memória! 🏆"
        elif elapsed < 90:
            message = "🎯 Muito bom! Tempo impressionante! 🎯"
        else:
            message = "👍 Bom trabalho! Você completou o jogo! 👍"
        
        messagebox.showinfo(
            "🎉 Parabéns! 🎉",
            f"{message}\n\n"
            f"⏱️  Tempo: {elapsed} segundos\n"
            f"🔄 Tentativas: {self.attempts}\n"
            f"⭐  Pontuação base: {self.score}\n"
            f"🏆 Bônus por tempo: +{int(time_bonus)} pontos\n"
            f"💯 Pontuação final: {final_score}"
        )
        
        self.instructions_label.config(text="✅ Jogo concluído! Clique em 'Novo Jogo' para jogar novamente.")
        self.game_started = False

def main():
    """Função principal para executar o jogo."""
    # Criar janela principal
    root = tk.Tk()
    
    # Criar instância do jogo
    game = ImageMemoryGame(root)
    
    # Centralizar a janela na tela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_closing():
        """Função chamada ao fechar a janela."""
        if game.audio_initialized:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        root.destroy()
    
    # Configurar ação ao fechar a janela
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    # Executar o jogo
    print("=" * 50)
    print("Iniciando Jogo da Memória com Imagens...")
    print("=" * 50)
    main()
