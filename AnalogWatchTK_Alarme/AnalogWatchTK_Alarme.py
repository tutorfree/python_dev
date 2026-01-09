import tkinter as tk
from tkinter import ttk, messagebox
from math import cos, sin, pi
from datetime import datetime, time
import json
import os
import threading
import time as time_module
from plyer import notification  # Para notificações do sistema

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
        
        # Lista de alarmes
        self.alarms = []
        self.next_alarm_time = None
        self.alarm_alert_window = None
        self.alarm_dragging = False  # Para arrastar janela de alarme
        
        # Variáveis para arrastar janelas de diálogo
        self.active_dialog = None  # Janela de diálogo ativa
        self.dialog_dragging = False
        
        # Carrega configurações salvas PRIMEIRO
        self.settings_file = "clock_settings.json"
        self.alarms_file = "alarms.json"
        self.alarm_positions_file = "alarm_positions.json"
        self.load_settings()
        
        # Carrega posições salvas dos alarmes
        self.alarm_positions = self.load_alarm_positions()
        
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
        
        # Inicia thread para verificar alarmes
        self.alarm_thread = threading.Thread(target=self.check_alarms_thread, daemon=True)
        self.alarm_thread.start()
        
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
            
        # Carrega alarmes
        self.load_alarms()
    
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
            
    def load_alarm_positions(self):
        """Carrega posições salvas das janelas de alarme"""
        try:
            if os.path.exists(self.alarm_positions_file):
                with open(self.alarm_positions_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Erro ao carregar posições de alarme: {e}")
            return {}
    
    def save_alarm_positions(self):
        """Salva posições das janelas de alarme"""
        try:
            with open(self.alarm_positions_file, 'w') as f:
                json.dump(self.alarm_positions, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar posições de alarme: {e}")
    
    def load_alarms(self):
        """Carrega alarmes salvos"""
        try:
            if os.path.exists(self.alarms_file):
                with open(self.alarms_file, 'r') as f:
                    self.alarms = json.load(f)
                    print(f"Alarmes carregados: {self.alarms}")
            else:
                self.alarms = []
        except Exception as e:
            print(f"Erro ao carregar alarmes: {e}")
            self.alarms = []
    
    def save_alarms(self):
        """Salva alarmes atuais"""
        try:
            with open(self.alarms_file, 'w') as f:
                json.dump(self.alarms, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar alarmes: {e}")
    
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
        
        # Menu de alarmes
        alarm_menu = tk.Menu(menu, tearoff=0, bg='#2C3E50', fg='#ECF0F1')
        alarm_menu.add_command(
            label="⏰ Adicionar Alarme",
            command=self.add_alarm_dialog
        )
        alarm_menu.add_command(
            label="📋 Ver Alarmes",
            command=self.show_alarms_list
        )
        
        if self.alarms:
            alarm_menu.add_separator()
            alarm_menu.add_command(
                label="🗑️ Limpar Todos Alarmes",
                command=self.clear_all_alarms
            )
        
        menu.add_cascade(label="⏰ Alarmes", menu=alarm_menu)
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
    
    # ===== FUNCIONALIDADES DE ALARMES =====
    
    def add_alarm_dialog(self):
        """Abre diálogo para adicionar novo alarme"""
        dialog = tk.Toplevel(self)
        dialog.title("Adicionar Alarme")
        dialog.overrideredirect(True)
        dialog.attributes('-topmost', True)
        
        # Configura movimento para esta janela específica
        dialog.bind('<Button-1>', lambda e: self.start_move_dialog(e, dialog))
        dialog.bind('<B1-Motion>', lambda e: self.on_move_dialog(e, dialog))
        dialog.bind('<ButtonRelease-1>', self.end_move_dialog)
        
        colors = self.get_theme_colors()
        
        # Posiciona próximo ao relógio
        dialog_x = self.winfo_x() + (self.size // 2) - 150
        dialog_y = self.winfo_y() + (self.size // 2) - 120
        dialog.geometry(f'320x250+{dialog_x}+{dialog_y}')
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg=colors['face'], 
                             relief='solid', borderwidth=2)
        main_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Barra de título personalizada
        title_frame = tk.Frame(main_frame, bg=colors['border'], height=30)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        # Configura movimento na barra de título
        title_frame.bind('<Button-1>', lambda e: self.start_move_dialog(e, dialog))
        title_frame.bind('<B1-Motion>', lambda e: self.on_move_dialog(e, dialog))
        title_frame.bind('<ButtonRelease-1>', self.end_move_dialog)
        
        # Título
        title_label = tk.Label(title_frame, text="⏰ Novo Alarme", 
                              font=('Arial', 12, 'bold'),
                              bg=colors['border'], fg=colors['text'])
        title_label.pack(side='left', padx=10, pady=5)
        title_label.bind('<Button-1>', lambda e: self.start_move_dialog(e, dialog))
        title_label.bind('<B1-Motion>', lambda e: self.on_move_dialog(e, dialog))
        title_label.bind('<ButtonRelease-1>', self.end_move_dialog)
        
        # Botão de fechar
        close_btn = tk.Button(title_frame, text="×", 
                             command=dialog.destroy,
                             bg=colors['border'], fg=colors['text'],
                             font=('Arial', 14, 'bold'),
                             bd=0, highlightthickness=0,
                             activebackground='#ff4444',
                             activeforeground='white')
        close_btn.pack(side='right', padx=5)
        
        # Frame para hora
        time_frame = tk.Frame(main_frame, bg=colors['face'])
        time_frame.pack(pady=10)
        
        tk.Label(time_frame, text="Hora:", 
                bg=colors['face'], fg=colors['text']).grid(row=0, column=0, padx=5)
        
        hour_var = tk.StringVar(value="12")
        hour_spin = ttk.Spinbox(time_frame, from_=1, to=23, width=3, 
                               textvariable=hour_var, wrap=True)
        hour_spin.grid(row=0, column=1, padx=5)
        
        tk.Label(time_frame, text="Minuto:", 
                bg=colors['face'], fg=colors['text']).grid(row=0, column=2, padx=5)
        
        minute_var = tk.StringVar(value="00")
        minute_spin = ttk.Spinbox(time_frame, from_=0, to=59, width=3, 
                                 textvariable=minute_var, wrap=True, format="%02.0f")
        minute_spin.grid(row=0, column=3, padx=5)
        
        # Descrição
        tk.Label(main_frame, text="Descrição (opcional):", 
                bg=colors['face'], fg=colors['text']).pack()
        
        desc_var = tk.StringVar()
        desc_entry = tk.Entry(main_frame, textvariable=desc_var, 
                             bg='white', fg='black', width=30)
        desc_entry.pack(pady=5)
        
        # Instrução de movimento
        instruction_label = tk.Label(main_frame, text="(Arraste pela barra superior para mover)",
                                   font=('Arial', 8, 'italic'),
                                   bg=colors['face'], fg=colors['text'])
        instruction_label.pack(pady=5)
        
        # Frame para botões
        btn_frame = tk.Frame(main_frame, bg=colors['face'])
        btn_frame.pack(pady=15)
        
        def add_alarm():
            try:
                hour = int(hour_var.get())
                minute = int(minute_var.get())
                
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    messagebox.showerror("Erro", "Hora inválida!")
                    return
                
                desc = desc_var.get().strip()
                if not desc:
                    desc = f"Alarme {hour:02d}:{minute:02d}"
                
                # Adiciona alarme
                alarm_time = time(hour=hour, minute=minute)
                self.alarms.append({
                    'time': alarm_time.strftime("%H:%M"),
                    'description': desc,
                    'active': True
                })
                
                # Salva alarmes
                self.save_alarms()
                
                # Atualiza próximo alarme
                self.update_next_alarm_time()
                
                dialog.destroy()
                
                # Mostra confirmação
                self.show_notification("Alarme Adicionado", 
                                     f"Alarme configurado para {hour:02d}:{minute:02d}")
                
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos!")
        
        btn_add = tk.Button(btn_frame, text="✓ Adicionar", 
                           command=add_alarm,
                           bg='#4CAF50', fg='white',
                           width=12, font=('Arial', 10),
                           relief='flat')
        btn_add.pack(side='left', padx=10)
        
        btn_cancel = tk.Button(btn_frame, text="✗ Cancelar", 
                              command=dialog.destroy,
                              bg='#f44336', fg='white',
                              width=12, font=('Arial', 10),
                              relief='flat')
        btn_cancel.pack(side='left', padx=10)
        
        # Configura cursor de mover na barra de título
        title_frame.config(cursor='fleur')
    
    def show_alarms_list(self):
        """Mostra lista de alarmes configurados"""
        dialog = tk.Toplevel(self)
        dialog.title("Alarmes Configurados")
        dialog.overrideredirect(True)
        dialog.attributes('-topmost', True)
        
        # Configura movimento para esta janela específica
        dialog.bind('<Button-1>', lambda e: self.start_move_dialog(e, dialog))
        dialog.bind('<B1-Motion>', lambda e: self.on_move_dialog(e, dialog))
        dialog.bind('<ButtonRelease-1>', self.end_move_dialog)
        
        colors = self.get_theme_colors()
        
        # Calcula tamanho baseado no número de alarmes
        height = min(400, 200 + len(self.alarms) * 40)
        dialog_x = self.winfo_x() + (self.size // 2) - 200
        dialog_y = self.winfo_y() + (self.size // 2) - (height // 2)
        dialog.geometry(f'420x{height}+{dialog_x}+{dialog_y}')
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg=colors['face'], 
                             relief='solid', borderwidth=2)
        main_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Barra de título
        title_frame = tk.Frame(main_frame, bg=colors['border'], height=30)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        # Configura movimento na barra de título
        title_frame.bind('<Button-1>', lambda e: self.start_move_dialog(e, dialog))
        title_frame.bind('<B1-Motion>', lambda e: self.on_move_dialog(e, dialog))
        title_frame.bind('<ButtonRelease-1>', self.end_move_dialog)
        
        # Título
        title_label = tk.Label(title_frame, text="📋 Alarmes Configurados", 
                              font=('Arial', 12, 'bold'),
                              bg=colors['border'], fg=colors['text'])
        title_label.pack(side='left', padx=10, pady=5)
        title_label.bind('<Button-1>', lambda e: self.start_move_dialog(e, dialog))
        title_label.bind('<B1-Motion>', lambda e: self.on_move_dialog(e, dialog))
        title_label.bind('<ButtonRelease-1>', self.end_move_dialog)
        
        # Botão de fechar
        close_btn = tk.Button(title_frame, text="×", 
                             command=dialog.destroy,
                             bg=colors['border'], fg=colors['text'],
                             font=('Arial', 14, 'bold'),
                             bd=0, highlightthickness=0,
                             activebackground='#ff4444',
                             activeforeground='white')
        close_btn.pack(side='right', padx=5)
        
        if not self.alarms:
            no_alarms_label = tk.Label(main_frame, text="Nenhum alarme configurado.", 
                                      bg=colors['face'], fg=colors['text'])
            no_alarms_label.pack(pady=20)
        else:
            # Frame com scroll para lista de alarmes
            list_frame = tk.Frame(main_frame, bg=colors['face'])
            list_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            canvas = tk.Canvas(list_frame, bg=colors['face'], highlightthickness=0)
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=colors['face'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Mostra cada alarme
            for i, alarm in enumerate(self.alarms):
                alarm_frame = tk.Frame(scrollable_frame, bg=colors['face'])
                alarm_frame.pack(fill='x', pady=5)
                
                # Checkbox para ativar/desativar
                active_var = tk.BooleanVar(value=alarm['active'])
                
                def toggle_active(idx, var):
                    self.alarms[idx]['active'] = var.get()
                    self.save_alarms()
                    self.update_next_alarm_time()
                
                chk = tk.Checkbutton(alarm_frame, variable=active_var,
                                    command=lambda idx=i, var=active_var: 
                                    toggle_active(idx, var),
                                    bg=colors['face'], fg=colors['text'])
                chk.pack(side='left', padx=5)
                
                # Hora
                time_label = tk.Label(alarm_frame, text=alarm['time'],
                                     font=('Arial', 12, 'bold'),
                                     width=8, anchor='w',
                                     bg=colors['face'], fg=colors['text'])
                time_label.pack(side='left', padx=10)
                
                # Descrição
                desc_label = tk.Label(alarm_frame, text=alarm['description'],
                                     font=('Arial', 10),
                                     anchor='w',
                                     bg=colors['face'], fg=colors['text'])
                desc_label.pack(side='left', fill='x', expand=True, padx=10)
                
                # Botão remover
                def remove_alarm(idx):
                    del self.alarms[idx]
                    self.save_alarms()
                    self.update_next_alarm_time()
                    # Fecha e reabre a janela para atualizar
                    dialog.destroy()
                    self.show_alarms_list()
                
                btn_remove = tk.Button(alarm_frame, text="✗", 
                                      command=lambda idx=i: remove_alarm(idx),
                                      bg='#f44336', fg='white',
                                      width=3, font=('Arial', 8),
                                      relief='flat')
                btn_remove.pack(side='right', padx=5)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        # Configura cursor de mover na barra de título
        title_frame.config(cursor='fleur')
        
        # Botão fechar (alternativo)
        btn_frame = tk.Frame(main_frame, bg=colors['face'])
        btn_frame.pack(pady=10)
        
        btn_close = tk.Button(btn_frame, text="Fechar", 
                             command=dialog.destroy,
                             bg=colors['border'], fg='white',
                             width=15, font=('Arial', 10),
                             relief='flat')
        btn_close.pack()
    
    def start_move_dialog(self, event, dialog):
        """Inicia movimento de uma janela de diálogo específica"""
        self.dialog_dragging = True
        self._dialog_start_x = event.x_root
        self._dialog_start_y = event.y_root
        self._dialog_window_x = dialog.winfo_x()
        self._dialog_window_y = dialog.winfo_y()
        self.active_dialog = dialog  # Armazena a referência da janela ativa
    
    def on_move_dialog(self, event, dialog):
        """Move uma janela de diálogo específica"""
        if self.dialog_dragging:
            x = self._dialog_window_x + (event.x_root - self._dialog_start_x)
            y = self._dialog_window_y + (event.y_root - self._dialog_start_y)
            dialog.geometry(f'+{x}+{y}')
    
    def end_move_dialog(self, event):
        """Finaliza movimento de diálogo"""
        self.dialog_dragging = False
        self.active_dialog = None
    
    def clear_all_alarms(self):
        """Remove todos os alarmes"""
        if messagebox.askyesno("Confirmar", "Remover todos os alarmes?"):
            self.alarms = []
            self.save_alarms()
            self.update_next_alarm_time()
            self.show_notification("Alarmes Removidos", "Todos os alarmes foram removidos.")
    
    def update_next_alarm_time(self):
        """Atualiza o próximo horário de alarme"""
        now = datetime.now()
        next_alarm = None
        
        for alarm in self.alarms:
            if alarm['active']:
                alarm_time = datetime.strptime(alarm['time'], "%H:%M").time()
                alarm_datetime = datetime.combine(now.date(), alarm_time)
                
                # Se já passou hoje, considera amanhã
                if alarm_datetime < now:
                    alarm_datetime = alarm_datetime.replace(day=now.day + 1)
                
                if next_alarm is None or alarm_datetime < next_alarm:
                    next_alarm = alarm_datetime
        
        self.next_alarm_time = next_alarm
    
    def check_alarms_thread(self):
        """Thread para verificar alarmes"""
        while True:
            now = datetime.now()
            
            if self.next_alarm_time and now >= self.next_alarm_time:
                # Encontra alarmes que dispararam
                current_time_str = now.strftime("%H:%M")
                triggered_alarms = []
                
                for alarm in self.alarms:
                    if alarm['active'] and alarm['time'] == current_time_str:
                        triggered_alarms.append(alarm)
                
                # Dispara os alarmes na thread principal
                if triggered_alarms:
                    self.after(0, self.trigger_alarms, triggered_alarms)
                
                # Atualiza próximo alarme
                self.after(0, self.update_next_alarm_time)
            
            time_module.sleep(1)  # Verifica a cada segundo
    
    def trigger_alarms(self, alarms):
        """Dispara os alarmes"""
        for alarm in alarms:
            # Mostra notificação do sistema
            try:
                notification.notify(
                    title="⏰ Alarme!",
                    message=alarm['description'],
                    timeout=10
                )
            except:
                pass  # Ignora se não tiver plyer
            
            # Mostra janela de alerta
            self.show_alarm_alert(alarm)
    
    def show_alarm_alert(self, alarm):
        """Mostra janela de alerta de alarme"""
        if self.alarm_alert_window and self.alarm_alert_window.winfo_exists():
            # Fecha janela anterior se existir
            self.alarm_alert_window.destroy()
        
        self.alarm_alert_window = tk.Toplevel(self)
        self.alarm_alert_window.overrideredirect(True)
        self.alarm_alert_window.attributes('-topmost', True)
        
        # Configura a janela para ser arrastável
        self.alarm_alert_window.bind('<Button-1>', self.start_alarm_move)
        self.alarm_alert_window.bind('<B1-Motion>', self.on_alarm_move)
        self.alarm_alert_window.bind('<ButtonRelease-1>', self.end_alarm_move)
        
        # Cria identificador único para este alarme
        alarm_id = f"{alarm['time']}_{alarm['description']}"
        
        # Verifica se há posição salva para este alarme
        saved_position = self.alarm_positions.get(alarm_id)
        
        if saved_position:
            # Usa posição salva
            window_width = 400
            window_height = 220
            x = saved_position['x']
            y = saved_position['y']
        else:
            # Posiciona no centro da tela por padrão
            screen_width = self.alarm_alert_window.winfo_screenwidth()
            screen_height = self.alarm_alert_window.winfo_screenheight()
            window_width = 400
            window_height = 220
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
        
        self.alarm_alert_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Frame principal
        main_frame = tk.Frame(self.alarm_alert_window, bg='#FF6B6B', 
                             relief='solid', borderwidth=3)
        main_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Torna toda a janela arrastável
        main_frame.bind('<Button-1>', self.start_alarm_move)
        main_frame.bind('<B1-Motion>', self.on_alarm_move)
        main_frame.bind('<ButtonRelease-1>', self.end_alarm_move)
        
        # Barra de título personalizada
        title_frame = tk.Frame(main_frame, bg='#FF3333', height=35)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        # Título (arrastável)
        title_label = tk.Label(title_frame, text="⏰ ALARME!", 
                             font=('Arial', 14, 'bold'),
                             bg='#FF3333', fg='white')
        title_label.pack(side='left', padx=10, pady=7)
        title_label.bind('<Button-1>', self.start_alarm_move)
        title_label.bind('<B1-Motion>', self.on_alarm_move)
        title_label.bind('<ButtonRelease-1>', self.end_alarm_move)
        
        # Botão de fechar
        close_btn = tk.Button(title_frame, text="×", 
                             command=lambda: self.dismiss_alarm(alarm_id, alarm),
                             bg='#FF3333', fg='white',
                             font=('Arial', 16, 'bold'),
                             bd=0, highlightthickness=0,
                             activebackground='#ff4444',
                             activeforeground='white')
        close_btn.pack(side='right', padx=5)
        
        # Conteúdo principal
        content_frame = tk.Frame(main_frame, bg='#FF6B6B')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Hora
        time_label = tk.Label(content_frame, text=alarm['time'],
                             font=('Arial', 32, 'bold'),
                             bg='#FF6B6B', fg='white')
        time_label.pack(pady=(0, 10))
        
        # Descrição
        desc_label = tk.Label(content_frame, text=alarm['description'],
                             font=('Arial', 16),
                             bg='#FF6B6B', fg='white')
        desc_label.pack(pady=5)
        
        # Instrução de movimento
        instruction_label = tk.Label(content_frame, text="(Arraste para reposicionar)",
                                   font=('Arial', 9, 'italic'),
                                   bg='#FF6B6B', fg='white')
        instruction_label.pack(pady=10)
        
        # Frame para botões
        btn_frame = tk.Frame(content_frame, bg='#FF6B6B')
        btn_frame.pack(pady=15)
        
        # Botão para adiar alarme (snooze)
        def snooze_alarm():
            # Salva posição atual
            self.save_current_alarm_position(alarm_id)
            
            # Fecha janela atual
            self.alarm_alert_window.destroy()
            
            # Agenda para tocar novamente em 5 minutos
            self.after(300000, lambda: self.show_alarm_alert(alarm))
            
            # Mostra notificação
            self.show_notification("Alarme Adiado", 
                                 f"Alarme '{alarm['description']}' adiado por 5 minutos")
        
        btn_snooze = tk.Button(btn_frame, text="Adiar 5 min", 
                              command=snooze_alarm,
                              bg='#FFA726', fg='white',
                              width=12, font=('Arial', 10),
                              relief='flat')
        btn_snooze.pack(side='left', padx=10)
        
        # Botão para desativar alarme
        btn_dismiss = tk.Button(btn_frame, text="Desativar", 
                               command=lambda: self.dismiss_alarm(alarm_id, alarm),
                               bg='white', fg='#FF6B6B',
                               width=12, font=('Arial', 10, 'bold'),
                               relief='flat')
        btn_dismiss.pack(side='left', padx=10)
        
        # Configura cursor de mover em toda a janela
        main_frame.config(cursor='fleur')
        title_frame.config(cursor='fleur')
        content_frame.config(cursor='fleur')
        
        # Adiciona menu de contexto para a janela do alarme
        def show_alarm_menu(event):
            menu = tk.Menu(self.alarm_alert_window, tearoff=0, 
                          bg='#2C3E50', fg='#ECF0F1')
            
            menu.add_command(
                label="💾 Salvar Posição Atual",
                command=lambda: self.save_current_alarm_position(alarm_id)
            )
            
            menu.add_command(
                label="🗑️ Remover Esta Posição",
                command=lambda: self.remove_alarm_position(alarm_id)
            )
            
            menu.add_separator()
            
            menu.add_command(
                label="⏰ Adiar 5 minutos",
                command=snooze_alarm
            )
            
            menu.add_command(
                label="🔕 Desativar Alarme",
                command=lambda: self.dismiss_alarm(alarm_id, alarm)
            )
            
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
        
        self.alarm_alert_window.bind('<Button-3>', show_alarm_menu)
        main_frame.bind('<Button-3>', show_alarm_menu)
        
        # Fecha automaticamente após 30 segundos
        self.alarm_alert_window.after(30000, lambda: self.auto_close_alarm(alarm_id))
        
        # Faz a janela piscar para chamar atenção
        self.flash_window(self.alarm_alert_window)
    
    def start_alarm_move(self, event):
        """Inicia movimento da janela de alarme"""
        self.alarm_dragging = True
        self._alarm_start_x = event.x_root
        self._alarm_start_y = event.y_root
        self._alarm_window_x = self.alarm_alert_window.winfo_x()
        self._alarm_window_y = self.alarm_alert_window.winfo_y()
    
    def on_alarm_move(self, event):
        """Move a janela de alarme"""
        if self.alarm_dragging:
            x = self._alarm_window_x + (event.x_root - self._alarm_start_x)
            y = self._alarm_window_y + (event.y_root - self._alarm_start_y)
            self.alarm_alert_window.geometry(f'+{x}+{y}')
    
    def end_alarm_move(self, event):
        """Finaliza movimento da janela de alarme"""
        self.alarm_dragging = False
    
    def dismiss_alarm(self, alarm_id, alarm):
        """Desativa o alarme"""
        # Desativa este alarme específico
        for a in self.alarms:
            if a['time'] == alarm['time'] and a['description'] == alarm['description']:
                a['active'] = False
        
        self.save_alarms()
        self.update_next_alarm_time()
        
        # Salva a posição atual antes de fechar
        self.save_current_alarm_position(alarm_id)
        
        self.alarm_alert_window.destroy()
    
    def save_current_alarm_position(self, alarm_id):
        """Salva a posição atual da janela de alarme"""
        if self.alarm_alert_window and self.alarm_alert_window.winfo_exists():
            x = self.alarm_alert_window.winfo_x()
            y = self.alarm_alert_window.winfo_y()
            
            self.alarm_positions[alarm_id] = {'x': x, 'y': y}
            self.save_alarm_positions()
    
    def remove_alarm_position(self, alarm_id):
        """Remove a posição salva para um alarme"""
        if alarm_id in self.alarm_positions:
            del self.alarm_positions[alarm_id]
            self.save_alarm_positions()
            
            if self.alarm_alert_window and self.alarm_alert_window.winfo_exists():
                # Reposiciona no centro
                screen_width = self.alarm_alert_window.winfo_screenwidth()
                screen_height = self.alarm_alert_window.winfo_screenheight()
                window_width = 400
                window_height = 220
                x = (screen_width // 2) - (window_width // 2)
                y = (screen_height // 2) - (window_height // 2)
                self.alarm_alert_window.geometry(f'+{x}+{y}')
    
    def auto_close_alarm(self, alarm_id):
        """Fecha automaticamente a janela do alarme"""
        if self.alarm_alert_window and self.alarm_alert_window.winfo_exists():
            # Salva posição antes de fechar
            self.save_current_alarm_position(alarm_id)
            self.alarm_alert_window.destroy()
    
    def flash_window(self, window):
        """Faz a janela piscar"""
        def flash(count=0):
            if count < 10 and window.winfo_exists():  # Pisca 5 vezes (on/off)
                try:
                    # Alterna entre duas cores
                    if count % 2 == 0:
                        bg_color = '#FF3333'
                        title_bg = '#FF0000'
                    else:
                        bg_color = '#FF6B6B'
                        title_bg = '#FF3333'
                    
                    # Atualiza as cores
                    for widget in window.winfo_children():
                        if isinstance(widget, tk.Frame):
                            current_bg = widget.cget('bg')
                            if current_bg in ['#FF6B6B', '#FF3333', '#FF0000']:
                                widget.config(bg=bg_color)
                                # Atualiza widgets filhos
                                for child in widget.winfo_children():
                                    if isinstance(child, tk.Frame):
                                        child_bg = child.cget('bg')
                                        if child_bg in ['#FF6B6B', '#FF3333', '#FF0000']:
                                            child.config(bg=title_bg if child_bg == '#FF3333' else bg_color)
                    
                    window.after(500, flash, count + 1)
                except:
                    pass  # Janela pode ter sido fechada
        
        flash()
    
    def show_notification(self, title, message):
        """Mostra notificação no widget"""
        # Cria uma notificação temporária no próprio relógio
        colors = self.get_theme_colors()
        
        # Cria uma janela temporária
        notif_window = tk.Toplevel(self)
        notif_window.overrideredirect(True)
        notif_window.attributes('-topmost', True)
        notif_window.attributes('-alpha', 0.9)
        
        # Posiciona próximo ao relógio
        notif_x = self.winfo_x() + self.size + 10
        notif_y = self.winfo_y()
        notif_window.geometry(f'250x80+{notif_x}+{notif_y}')
        
        # Frame principal
        main_frame = tk.Frame(notif_window, bg=colors['border'], 
                             relief='solid', borderwidth=2)
        main_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Título
        title_label = tk.Label(main_frame, text=title,
                              font=('Arial', 11, 'bold'),
                              bg=colors['border'], fg='white')
        title_label.pack(pady=(5, 0))
        
        # Mensagem
        msg_label = tk.Label(main_frame, text=message,
                            font=('Arial', 9),
                            bg=colors['border'], fg='white')
        msg_label.pack(pady=5)
        
        # Fecha automaticamente após 3 segundos
        notif_window.after(3000, notif_window.destroy)
    
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
        self.save_alarms()
        self.save_alarm_positions()
        super().destroy()

if __name__ == "__main__":
    app = ThemedAnalogClock()
    app.mainloop()
