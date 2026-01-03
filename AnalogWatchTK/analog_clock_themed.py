import tkinter as tk
from math import cos, sin, pi
from datetime import datetime
import json
import os

class ThemedAnalogClock(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.95)
        
        # Torna a janela transparente (área fora do relógio)
        self.attributes('-transparentcolor', 'grey15')
        
        # Variáveis de tamanho
        self.available_sizes = [150, 200, 250, 300, 350, 400]
        
        # Cores do tema atual
        self.current_theme = "darkly"
        
        # Carrega configurações salvas PRIMEIRO
        self.settings_file = "clock_settings.json"
        self.load_settings()
        
        # AGORA inicializa as variáveis do relógio com as configurações carregadas
        self.update_clock_geometry()
        
        # Configura canvas
        self.canvas = tk.Canvas(self, width=self.size, height=self.size,
                               bg='grey15', highlightthickness=0)
        self.canvas.pack()
        
        # Variáveis para movimento
        self._dragging = False
        
        # Bind para interação
        self.canvas.bind('<Button-1>', self.start_move)
        self.canvas.bind('<B1-Motion>', self.on_move)
        self.canvas.bind('<ButtonRelease-1>', self.end_move)
        self.canvas.bind('<Button-3>', self.show_context_menu)
        
        # Cursor de mover
        self.canvas.bind('<Enter>', lambda e: self.canvas.config(cursor='fleur'))
        self.canvas.bind('<Leave>', lambda e: self.canvas.config(cursor=''))
        
        # Desenha o relógio
        self.draw_clock_face()
        self.update_clock()
        
    def update_clock_geometry(self):
        """Atualiza todas as variáveis de geometria do relógio baseadas no tamanho atual"""
        self.center_x = self.size // 2
        self.center_y = self.size // 2
        self.radius = self.size // 2 - 15  # Margem consistente
        
    def get_theme_colors(self):
        """Retorna as cores para o tema atual"""
        themes = {
            "darkly": {
                'bg': '#222222',
                'face': '#2C3E50',
                'border': '#34495E',
                'hour_hand': '#ECF0F1',
                'minute_hand': '#BDC3C7',
                'second_hand': '#E74C3C',
                'hour_mark': '#ECF0F1',
                'center': '#E74C3C',
                'text': '#ECF0F1'
            },
            "flatly": {
                'bg': '#2C3E50',
                'face': '#34495E',
                'border': '#2C3E50',
                'hour_hand': '#ECF0F1',
                'minute_hand': '#BDC3C7',
                'second_hand': '#E74C3C',
                'hour_mark': '#ECF0F1',
                'center': '#E74C3C',
                'text': '#ECF0F1'
            },
            "superhero": {
                'bg': '#2B3E50',
                'face': '#4E5D6C',
                'border': '#DF691A',
                'hour_hand': '#EBEBEB',
                'minute_hand': '#5BC0DE',
                'second_hand': '#DF691A',
                'hour_mark': '#EBEBEB',
                'center': '#DF691A',
                'text': '#EBEBEB'
            },
            "cyborg": {
                'bg': '#060606',
                'face': '#2A2A2A',
                'border': '#00FF9D',
                'hour_hand': '#FFFFFF',
                'minute_hand': '#888888',
                'second_hand': '#00FF9D',
                'hour_mark': '#888888',
                'center': '#00FF9D',
                'text': '#FFFFFF'
            },
            "vapor": {
                'bg': '#1A1A2E',
                'face': '#16213E',
                'border': '#0F3460',
                'hour_hand': '#E94560',
                'minute_hand': '#533483',
                'second_hand': '#00FF9D',
                'hour_mark': '#E94560',
                'center': '#E94560',
                'text': '#FFFFFF'
            },
            "minty": {
                'bg': '#F7FFF7',
                'face': '#FFFFFF',
                'border': '#6AB187',
                'hour_hand': '#2F4858',
                'minute_hand': '#33658A',
                'second_hand': '#F6AE2D',
                'hour_mark': '#2F4858',
                'center': '#F6AE2D',
                'text': '#2F4858'
            },
            "solar": {
                'bg': '#002B36',
                'face': '#073642',
                'border': '#268BD2',
                'hour_hand': '#839496',
                'minute_hand': '#586E75',
                'second_hand': '#DC322F',
                'hour_mark': '#839496',
                'center': '#DC322F',
                'text': '#839496'
            },
            "luxa": {
                'bg': '#1E1E2E',
                'face': '#2D2D44',
                'border': '#7B68EE',
                'hour_hand': '#E6E6FA',
                'minute_hand': '#9370DB',
                'second_hand': '#FF69B4',
                'hour_mark': '#E6E6FA',
                'center': '#FF69B4',
                'text': '#E6E6FA'
            },
            "morph": {
                'bg': '#1A1A2E',
                'face': '#0F3460',
                'border': '#E94560',
                'hour_hand': '#FFFFFF',
                'minute_hand': '#16213E',
                'second_hand': '#0F3460',
                'hour_mark': '#FFFFFF',
                'center': '#E94560',
                'text': '#FFFFFF'
            }
        }
        
        return themes.get(self.current_theme, themes["darkly"])
    
    def load_settings(self):
        """Carrega configurações salvas"""
        # Valores padrão
        default_settings = {
            'size': 300,
            'theme': 'darkly',
            'position': [100, 100]
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                    # Usa os valores carregados ou os padrões
                    self.size = loaded_settings.get('size', default_settings['size'])
                    self.current_theme = loaded_settings.get('theme', default_settings['theme'])
                    position = loaded_settings.get('position', default_settings['position'])
                    
                    # Aplica a posição
                    self.geometry(f'+{position[0]}+{position[1]}')
            else:
                # Usa valores padrão
                self.size = default_settings['size']
                self.current_theme = default_settings['theme']
                self.geometry(f'+{default_settings["position"][0]}+{default_settings["position"][1]}')
                
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            # Usa valores padrão em caso de erro
            self.size = default_settings['size']
            self.current_theme = default_settings['theme']
            self.geometry(f'+{default_settings["position"][0]}+{default_settings["position"][1]}')
    
    def save_settings(self):
        """Salva configurações atuais"""
        try:
            settings = {
                'size': self.size,
                'theme': self.current_theme,
                'position': [self.winfo_x(), self.winfo_y()]
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
                
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def start_move(self, event):
        """Inicia movimento da janela"""
        self._dragging = True
        self._start_x = event.x
        self._start_y = event.y
    
    def on_move(self, event):
        """Move a janela"""
        if self._dragging:
            x = self.winfo_x() + event.x - self._start_x
            y = self.winfo_y() + event.y - self._start_y
            self.geometry(f'+{x}+{y}')
    
    def end_move(self, event):
        """Finaliza movimento"""
        self._dragging = False
        self.save_settings()
    
    def show_context_menu(self, event):
        """Mostra menu de contexto"""
        menu = tk.Menu(self, tearoff=0, bg='#2C3E50', fg='#ECF0F1', 
                      font=('Arial', 10))
        
        # Submenu de temas
        theme_menu = tk.Menu(menu, tearoff=0, bg='#2C3E50', fg='#ECF0F1')
        
        themes = [
            ("🌙 Darkly", "darkly"),
            ("☁️ Flatly", "flatly"),
            ("🦸 Superhero", "superhero"),
            ("🤖 Cyborg", "cyborg"),
            ("🌈 Vapor", "vapor"),
            ("🍃 Minty", "minty"),
            ("☀️ Solar", "solar"),
            ("💎 Luxa", "luxa"),
            ("🌊 Morph", "morph")
        ]
        
        for theme_name, theme_code in themes:
            theme_menu.add_command(
                label=theme_name,
                command=lambda t=theme_code: self.change_theme(t)
            )
        
        menu.add_cascade(label="🎨 Temas", menu=theme_menu)
        menu.add_separator()
        
        # Submenu de tamanhos
        size_menu = tk.Menu(menu, tearoff=0, bg='#2C3E50', fg='#ECF0F1')
        
        # Opções de tamanho com ícones
        sizes = [
            ("🔘 Pequeno (150px)", 150),
            ("🔘 Médio-Pequeno (200px)", 200),
            ("🔘 Médio (250px)", 250),
            ("🔘 Grande-Médio (300px)", 300),
            ("🔘 Grande (350px)", 350),
            ("🔘 Extra Grande (400px)", 400)
        ]
        
        for size_name, size_value in sizes:
            # Marca o tamanho atual com um ✓
            display_name = size_name
            if size_value == self.size:
                display_name = f"✓ {size_name[2:]}"  # Remove o ícone e adiciona ✓
            
            size_menu.add_command(
                label=display_name,
                command=lambda s=size_value: self.set_size(s)
            )
        
        menu.add_cascade(label="📏 Tamanho", menu=size_menu)
        menu.add_separator()
        
        # Submenu de transparência
        alpha_menu = tk.Menu(menu, tearoff=0, bg='#2C3E50', fg='#ECF0F1')
        alphas = [
            ("◐ Alta (70%)", 0.7),
            ("◑ Média-Alta (80%)", 0.8),
            ("◒ Média (90%)", 0.9),
            ("◓ Baixa (100%)", 1.0)
        ]
        
        for alpha_name, alpha_value in alphas:
            alpha_menu.add_command(
                label=alpha_name,
                command=lambda a=alpha_value: self.set_alpha(a)
            )
        
        menu.add_cascade(label="⚗️ Transparência", menu=alpha_menu)
        menu.add_separator()
        
        # Opção para alternar "sempre no topo"
        topmost_text = "📌 Desfixar do Topo" if self.attributes('-topmost') else "📌 Fixar no Topo"
        menu.add_command(
            label=topmost_text,
            command=self.toggle_always_on_top
        )
        
        menu.add_command(
            label="💾 Salvar Configurações",
            command=self.save_settings
        )
        
        menu.add_separator()
        
        # Opção de fechar
        menu.add_command(
            label="❌ Fechar",
            command=self.confirm_close,
            background='#ff4444',
            foreground='white'
        )
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def change_theme(self, theme_name):
        """Muda o tema do relógio"""
        self.current_theme = theme_name
        
        # Redesenha o relógio
        self.canvas.delete("all")
        self.draw_clock_face()
        
        # Salva configurações
        self.save_settings()
    
    def set_size(self, new_size):
        """Define um novo tamanho para o relógio"""
        if new_size in self.available_sizes:
            # Calcula nova posição para manter o centro
            old_center_x = self.winfo_x() + self.size // 2
            old_center_y = self.winfo_y() + self.size // 2
            
            # Atualiza o tamanho
            self.size = new_size
            
            # Atualiza TODAS as variáveis de geometria
            self.update_clock_geometry()
            
            # Nova posição (centro se mantém)
            new_x = old_center_x - new_size // 2
            new_y = old_center_y - new_size // 2
            
            # Atualiza geometria da janela
            self.geometry(f'{new_size}x{new_size}+{new_x}+{new_y}')
            
            # Atualiza canvas
            self.canvas.config(width=new_size, height=new_size)
            
            # Redesenha tudo
            self.canvas.delete("all")
            self.draw_clock_face()
            
            # Salva configurações
            self.save_settings()
    
    def set_alpha(self, value):
        """Define a transparência da janela"""
        self.attributes('-alpha', value)
        self.save_settings()
    
    def toggle_always_on_top(self):
        """Alterna o estado 'sempre no topo'"""
        current = self.attributes('-topmost')
        self.attributes('-topmost', not current)
        self.save_settings()
    
    def draw_clock_face(self):
        """Desenha a face do relógio"""
        colors = self.get_theme_colors()
        
        # Desenha fundo do relógio (círculo)
        margin = 15
        self.canvas.create_oval(
            margin, margin, self.size - margin, self.size - margin,
            fill=colors['face'], outline=colors['border'], width=3
        )
        
        # Desenha marcações das horas
        for i in range(12):
            angle = i * 30 - 90
            angle_rad = angle * (pi / 180)
            
            # Marcações mais longas para horas principais
            length = self.radius * 0.12 if i % 3 == 0 else self.radius * 0.08
            width = 3 if i % 3 == 0 else 2
            
            x1 = self.center_x + (self.radius - length) * cos(angle_rad)
            y1 = self.center_y + (self.radius - length) * sin(angle_rad)
            x2 = self.center_x + (self.radius - 8) * cos(angle_rad)
            y2 = self.center_y + (self.radius - 8) * sin(angle_rad)
            
            self.canvas.create_line(x1, y1, x2, y2, 
                                   width=width, fill=colors['hour_mark'])
        
        # Desenha marcações dos minutos (para relógios maiores)
        if self.size >= 250:
            for i in range(60):
                if i % 5 != 0:
                    angle = i * 6 - 90
                    angle_rad = angle * (pi / 180)
                    
                    length = self.radius * 0.04
                    x1 = self.center_x + (self.radius - length) * cos(angle_rad)
                    y1 = self.center_y + (self.radius - length) * sin(angle_rad)
                    x2 = self.center_x + (self.radius - 8) * cos(angle_rad)
                    y2 = self.center_y + (self.radius - 8) * sin(angle_rad)
                    
                    self.canvas.create_line(x1, y1, x2, y2, 
                                           width=1, fill=colors['hour_mark'], dash=(1, 1))
    
    def update_clock(self):
        """Atualiza os ponteiros do relógio"""
        self.canvas.delete("hands")
        
        now = datetime.now()
        colors = self.get_theme_colors()
        
        # Ângulos dos ponteiros
        hour_angle = (now.hour % 12 + now.minute / 60) * 30 - 90
        hour_angle_rad = hour_angle * (pi / 180)
        
        minute_angle = now.minute * 6 - 90
        minute_angle_rad = minute_angle * (pi / 180)
        
        second_angle = now.second * 6 - 90
        second_angle_rad = second_angle * (pi / 180)
        
        # Tamanhos dos ponteiros (proporcionais ao raio)
        hour_length = self.radius * 0.55    # 55% do raio
        minute_length = self.radius * 0.75  # 75% do raio
        second_length = self.radius * 0.90  # 90% do raio
        
        # Calcula pontos finais
        hour_x = self.center_x + hour_length * cos(hour_angle_rad)
        hour_y = self.center_y + hour_length * sin(hour_angle_rad)
        
        minute_x = self.center_x + minute_length * cos(minute_angle_rad)
        minute_y = self.center_y + minute_length * sin(minute_angle_rad)
        
        second_x = self.center_x + second_length * cos(second_angle_rad)
        second_y = self.center_y + second_length * sin(second_angle_rad)
        
        # Larguras proporcionais
        hour_width = max(6, int(self.size / 50))
        minute_width = max(4, int(self.size / 75))
        second_width = max(2, int(self.size / 150))
        
        # Desenha ponteiros
        self.canvas.create_line(
            self.center_x, self.center_y, hour_x, hour_y,
            width=hour_width, fill=colors['hour_hand'], 
            tags="hands", capstyle=tk.ROUND
        )
        
        self.canvas.create_line(
            self.center_x, self.center_y, minute_x, minute_y,
            width=minute_width, fill=colors['minute_hand'], 
            tags="hands", capstyle=tk.ROUND
        )
        
        self.canvas.create_line(
            self.center_x, self.center_y, second_x, second_y,
            width=second_width, fill=colors['second_hand'], 
            tags="hands", capstyle=tk.ROUND
        )
        
        # Centro do relógio
        center_size = max(8, int(self.size / 40))
        self.canvas.create_oval(
            self.center_x - center_size, self.center_y - center_size,
            self.center_x + center_size, self.center_y + center_size,
            fill=colors['center'], outline=colors['border'], 
            width=max(2, int(self.size / 150)), tags="hands"
        )
        
        # Ponto interno no centro
        inner_center = center_size // 2
        self.canvas.create_oval(
            self.center_x - inner_center, self.center_y - inner_center,
            self.center_x + inner_center, self.center_y + inner_center,
            fill=colors['face'], outline='', tags="hands"
        )
        
        # Agenda próxima atualização
        self.after(1000, self.update_clock)
    
    def confirm_close(self):
        """Mostra diálogo de confirmação para fechar"""
        dialog = tk.Toplevel(self)
        dialog.overrideredirect(True)
        dialog.attributes('-topmost', True)
        
        # Posiciona próximo ao relógio
        dialog_x = self.winfo_x() + (self.size // 2) - 100
        dialog_y = self.winfo_y() + (self.size // 2) - 50
        dialog.geometry(f'200x100+{dialog_x}+{dialog_y}')
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg='#2C3E50', 
                             relief='solid', borderwidth=2)
        main_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Label
        label = tk.Label(main_frame, text="Fechar relógio?", 
                        font=('Arial', 11, 'bold'),
                        bg='#2C3E50', fg='#ECF0F1')
        label.pack(pady=15)
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg='#2C3E50')
        btn_frame.pack(pady=10)
        
        btn_yes = tk.Button(btn_frame, text="✓ Sim", 
                           command=self.destroy,
                           bg='#4CAF50', fg='white',
                           width=8, font=('Arial', 10),
                           relief='flat')
        btn_yes.pack(side='left', padx=10)
        
        btn_no = tk.Button(btn_frame, text="✗ Não", 
                          command=dialog.destroy,
                          bg='#f44336', fg='white',
                          width=8, font=('Arial', 10),
                          relief='flat')
        btn_no.pack(side='left', padx=10)
    
    def destroy(self):
        """Fecha a janela salvando configurações"""
        self.save_settings()
        super().destroy()

if __name__ == "__main__":
    app = ThemedAnalogClock()
    app.mainloop()
