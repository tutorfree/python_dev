import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
from PIL import Image, ImageTk  # Para manipular imagens
import random
import time
import os
import pygame

class ImageMemoryGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Jogo da Memória com Imagens")
        self.window.geometry("800x750")
        self.window.configure(bg='#f0f0f0')
        self.window.resizable(False, False)

        # Variáveis para controle de áudio
        self.is_muted = False
        self.last_volume = 0.5

        # Trilha sonora
        try:
            self.tocar_trilha_sonora()
        except:
            print("Áudio não disponível, continuando sem som...")
        
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
        self.check_images()
        
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
        
        # Botões do jogo
        self.image_buttons = []
        
        # Carregar imagens
        self.load_images()
        
        # Interface
        self.setup_ui()
        
    def check_images(self):
        """Verifica se todas as imagens existem."""
        missing = []
        for img_file in self.image_files:
            if not os.path.exists(os.path.join('images', img_file)):
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
            back_img_path = os.path.join('images', 'back.jpg')
            if os.path.exists(back_img_path):
                back_img = Image.open(back_img_path)
            else:
                # Criar uma imagem de verso padrão
                back_img = Image.new('RGB', (100, 100), color='#34495e')
            
            # Redimensionar imagem do verso
            back_img = back_img.resize((100, 100), Image.Resampling.LANCZOS)
            self.back_image = ImageTk.PhotoImage(back_img)
            
            # Carregar imagens das cartas
            for img_file in self.image_files:
                img_path = os.path.join('images', img_file)
                img = Image.open(img_path)
                # Redimensionar para tamanho consistente
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                self.images_cache[img_file] = ImageTk.PhotoImage(img)
                
        except Exception as e:
            print(f"Erro ao carregar imagens: {e}")
            messagebox.showerror("Erro", f"Não foi possível carregar as imagens:\n{e}")
    
    def tocar_trilha_sonora(self):
        """Inicializa o pygame e toca a música."""
        try:
            caminho_musica = os.path.join(os.path.dirname(__file__), 'sound', 'trilha.mp3')
            
            print(f"Procurando música em: {caminho_musica}")
            
            if not os.path.exists(caminho_musica):
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
        # Cabeçalho
        header_frame = Frame(self.window, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        title_label = Label(header_frame, text="Jogo da Memória com Imagens", 
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
        
        self.timer_label = Label(self.timer_frame, text="Tempo: 0s", 
                                font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#e74c3c')
        self.timer_label.pack()
        
        # Frame do jogo
        self.game_container = Frame(self.window, bg='#f0f0f0')
        self.game_container.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Frame de pontuação
        self.score_frame = Frame(self.window, bg='#f0f0f0')
        self.score_frame.pack(pady=3)
        
        self.score_label = Label(self.score_frame, 
                                text=f"Pares: 0/{self.total_pairs} | Tentativas: 0 | Pontos: 0",
                                font=('Arial', 12), bg='#f0f0f0', fg='#2c3e50')
        self.score_label.pack()
        
        # Frame de botões
        self.button_frame = Frame(self.window, bg='#f0f0f0')
        self.button_frame.pack(pady=5)
        
        self.start_button = Button(self.button_frame, text="Novo Jogo", font=('Arial', 12, 'bold'),
                                     bg='#27ae60', fg='white', relief=tk.RAISED, bd=2,
                                     command=self.start_new_game, width=12, height=1)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = Button(self.button_frame, text="Reiniciar", font=('Arial', 12),
                                     bg='#3498db', fg='white', relief=tk.RAISED, bd=2,
                                     command=self.reset_game, width=12, height=1)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Controles de volume
        self.volume_frame = Frame(self.window, bg='#f0f0f0')
        self.volume_frame.pack(pady=3)

        Label(self.volume_frame, text="Volume:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)

        self.volume_scale = tk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                     command=self.set_volume, length=150, bg='#f0f0f0', fg='#2c3e50',
                                     troughcolor='#bdc3c7', highlightthickness=0, showvalue=False)
        self.volume_scale.set(self.last_volume * 100)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        self.mute_button = Button(self.volume_frame, text="Mute", font=('Arial', 10),
                                  bg='#e74c3c', fg='white', relief=tk.RAISED, bd=1,
                                  command=self.toggle_mute, width=6)
        self.mute_button.pack(side=tk.LEFT, padx=5)
        
        # Inicializar o grid de imagens
        self.create_image_grid()
        
        # Inicializar temporizador
        self.start_time = 0
        self.timer_running = False
        
        self.window.update_idletasks()
        
    def set_volume(self, value):
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
        if pygame.mixer.get_init():
            if self.is_muted:
                pygame.mixer.music.set_volume(self.last_volume)
                self.volume_scale.set(self.last_volume * 100)
                self.mute_button.config(text="Mute", bg='#e74c3c')
                self.is_muted = False
            else:
                pygame.mixer.music.set_volume(0)
                self.volume_scale.set(0)
                self.mute_button.config(text="Unmute", bg='#2ecc71')
                self.is_muted = True

    def create_image_grid(self):
        self.game_frame = Frame(self.game_container, bg='#f0f0f0')
        self.game_frame.pack(pady=5)
        
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Criar um grid 4x3 para 12 cartas (6 pares)
        self.image_buttons = []
        for i in range(4):  # 4 linhas
            for j in range(3):  # 3 colunas
                index = i * 3 + j
                btn = Button(self.game_frame, image=self.back_image if self.back_image else None,
                               width=100, height=100, bg='#34495e',
                               relief=tk.RAISED, bd=2,
                               command=lambda idx=index: self.card_clicked(idx))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.image_buttons.append(btn)
        
        self.game_frame.update_idletasks()
    
    def start_new_game(self):
        self.reset_game()
        self.shuffle_cards()
        self.game_started = True
        self.show_all_cards_briefly()
    
    def reset_game(self):
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
            if self.back_image:
                btn.config(image=self.back_image, state=tk.NORMAL)
            else:
                btn.config(text="?", bg='#34495e', state=tk.NORMAL)
        
        self.update_score_display()
        self.timer_label.config(text="Tempo: 0s")
        self.instructions_label.config(text="Clique em 'Novo Jogo' para começar!")
    
    def shuffle_cards(self):
        self.image_pairs = []
        for img_file in self.image_files:
            self.image_pairs.append(img_file)
            self.image_pairs.append(img_file)
        
        random.shuffle(self.image_pairs)
    
    def show_all_cards_briefly(self):
        self.instructions_label.config(text="Memorize as posições das imagens!")
        
        # Mostrar todas as cartas
        for i, img_file in enumerate(self.image_pairs):
            if i < len(self.image_buttons):
                if img_file in self.images_cache:
                    self.image_buttons[i].config(image=self.images_cache[img_file])
                else:
                    self.image_buttons[i].config(text=f"Img {i+1}", bg='white')
                self.image_buttons[i].config(state=tk.DISABLED)
        
        self.start_timer()
        
        # Após 3 segundos, esconder as cartas
        self.window.after(3000, self.hide_all_cards)
    
    def hide_all_cards(self):
        for btn in self.image_buttons:
            if self.back_image:
                btn.config(image=self.back_image)
            else:
                btn.config(text="?", bg='#34495e')
            btn.config(state=tk.NORMAL)
        
        self.instructions_label.config(text="Encontre os pares de imagens!")
        self.can_click = True
    
    def card_clicked(self, index):
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
            
            if self.first_choice[1] == self.second_choice[1]:
                self.window.after(500, self.handle_match)
            else:
                self.window.after(1000, self.handle_mismatch)
            
            self.update_score_display()
    
    def handle_match(self):
        if self.first_choice and self.second_choice:
            self.matches_found += 1
            self.score += 10
            
            # Cartas já estão viradas, mostrar nome se quiser
            idx1, img_file1 = self.first_choice
            idx2, _ = self.second_choice
            
            # Opcional: adicionar borda verde nas cartas encontradas
            self.image_buttons[idx1].config(bd=3, relief=tk.SUNKEN)
            self.image_buttons[idx2].config(bd=3, relief=tk.SUNKEN)
            
            self.first_choice = None
            self.second_choice = None
            self.can_click = True
            
            if self.matches_found == self.total_pairs:
                self.window.after(500, self.end_game)
    
    def handle_mismatch(self):
        if self.first_choice:
            idx1, _ = self.first_choice
            if self.back_image:
                self.image_buttons[idx1].config(image=self.back_image)
            else:
                self.image_buttons[idx1].config(text="?", bg='#34495e')
            self.image_buttons[idx1].config(state=tk.NORMAL)
        
        if self.second_choice:
            idx2, _ = self.second_choice
            if self.back_image:
                self.image_buttons[idx2].config(image=self.back_image)
            else:
                self.image_buttons[idx2].config(text="?", bg='#34495e')
            self.image_buttons[idx2].config(state=tk.NORMAL)
        
        self.first_choice = None
        self.second_choice = None
        self.can_click = True
    
    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running and self.game_started:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Tempo: {elapsed}s")
            self.window.after(1000, self.update_timer)
    
    def update_score_display(self):
        self.score_label.config(
            text=f"Pares: {self.matches_found}/{self.total_pairs} | Tentativas: {self.attempts} | Pontos: {self.score}"
        )
    
    def end_game(self):
        self.timer_running = False
        elapsed = int(time.time() - self.start_time)
        
        time_bonus = int(max(0, 120 - elapsed))
        final_score = self.score + time_bonus
        
        messagebox.showinfo(
            "Parabéns!",
            f"🎉 Você encontrou todos os pares! 🎉\n\n"
            f"⏱️  Tempo: {elapsed} segundos\n"
            f"🔄 Tentativas: {self.attempts}\n"
            f"⭐  Pontuação base: {self.score}\n"
            f"🏆 Bônus por tempo: {time_bonus}\n"
            f"💯 Pontuação final: {final_score}"
        )
        
        self.instructions_label.config(text="Jogo concluído! Clique em 'Novo Jogo' para jogar novamente.")
        self.game_started = False

if __name__ == "__main__":
    # Instalar Pillow se não tiver: pip install pillow
    root = tk.Tk()
    game = ImageMemoryGame(root)
    
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
