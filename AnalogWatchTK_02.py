import tkinter as tk
from math import cos, sin, pi
from datetime import datetime

class SimpleAnalogClock(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Remove a barra de título e bordas
        self.overrideredirect(True)
        
        # Torna a janela sempre no topo
        self.attributes('-topmost', True)
        
        # Configura transparência
        self.attributes('-alpha', 0.95)
        
        # Variáveis de tamanho
        self.size = 300  # Tamanho inicial
        self.min_size = 100
        self.max_size = 500
        
        # Calcula valores do relógio
        self.center_x = self.size // 2
        self.center_y = self.size // 2
        self.radius = self.size // 2 - 10
        
        # Configura canvas
        self.canvas = tk.Canvas(self, width=self.size, height=self.size, 
                               bg='white', highlightthickness=0)
        self.canvas.pack()
        
        # Variáveis para arrastar
        self._offset_x = 0
        self._offset_y = 0
        self._resizing = False
        self._resize_corner = None
        
        # Bind para interação
        self.canvas.bind('<Button-1>', self.start_interaction)
        self.canvas.bind('<B1-Motion>', self.on_motion)
        self.canvas.bind('<Button-3>', self.show_context_menu)
        self.canvas.bind('<Button-2>', self.toggle_always_on_top)  # Botão do meio
        
        # Bind para redimensionamento
        self.canvas.bind('<Enter>', self.on_enter)
        self.canvas.bind('<Leave>', self.on_leave)
        
        self.draw_clock()
        self.update_clock()
        
        # Atualiza cursor baseado na posição
        self.canvas.bind('<Motion>', self.update_cursor)
    
    def on_enter(self, event):
        self.canvas.config(cursor='fleur')
    
    def on_leave(self, event):
        self.canvas.config(cursor='')
    
    def update_cursor(self, event):
        """Muda o cursor quando estiver perto das bordas para redimensionamento"""
        x, y = event.x, event.y
        size = self.size
        
        # Verifica se está perto do canto inferior direito
        if x > size - 20 and y > size - 20:
            self.canvas.config(cursor='size_nw_se')
        else:
            self.canvas.config(cursor='fleur')
    
    def start_interaction(self, event):
        """Inicia movimento ou redimensionamento"""
        x, y = event.x, event.y
        size = self.size
        
        # Verifica se clicou no canto inferior direito para redimensionar
        if x > size - 20 and y > size - 20:
            self._resizing = True
            self._resize_start_x = event.x_root
            self._resize_start_y = event.y_root
            self._start_size = self.size
        else:
            self._resizing = False
            self._offset_x = event.x
            self._offset_y = event.y
    
    def on_motion(self, event):
        """Move ou redimensiona a janela"""
        if self._resizing:
            # Calcula novo tamanho baseado no movimento do mouse
            delta_x = event.x_root - self._resize_start_x
            delta_y = event.x_root - self._resize_start_y
            
            # Usa a maior mudança (x ou y) para redimensionamento proporcional
            delta = max(delta_x, delta_y)
            new_size = self._start_size + delta
            
            # Limita o tamanho
            new_size = max(self.min_size, min(self.max_size, new_size))
            
            if new_size != self.size:
                self.size = new_size
                self.canvas.config(width=new_size, height=new_size)
                self.center_x = new_size // 2
                self.center_y = new_size // 2
                self.radius = new_size // 2 - 10
                
                # Redesenha o relógio com novo tamanho
                self.canvas.delete("all")
                self.draw_clock()
        else:
            # Move a janela
            x = self.winfo_x() + event.x - self._offset_x
            y = self.winfo_y() + event.y - self._offset_y
            self.geometry(f'+{x}+{y}')
    
    def show_context_menu(self, event):
        """Mostra menu de contexto ao clicar com botão direito"""
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Fechar", command=self.confirm_close)
        menu.add_separator()
        menu.add_command(label="Tamanho Pequeno (150px)", 
                        command=lambda: self.resize_clock(150))
        menu.add_command(label="Tamanho Médio (250px)", 
                        command=lambda: self.resize_clock(250))
        menu.add_command(label="Tamanho Grande (350px)", 
                        command=lambda: self.resize_clock(350))
        menu.add_separator()
        menu.add_command(label="Transparência Alta", 
                        command=lambda: self.set_transparency(0.8))
        menu.add_command(label="Transparência Média", 
                        command=lambda: self.set_transparency(0.9))
        menu.add_command(label="Transparência Baixa", 
                        command=lambda: self.set_transparency(1.0))
        menu.add_separator()
        menu.add_command(label="Sempre no Topo", 
                        command=self.toggle_always_on_top)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def resize_clock(self, new_size):
        """Redimensiona o relógio para um tamanho específico"""
        new_size = max(self.min_size, min(self.max_size, new_size))
        self.size = new_size
        self.canvas.config(width=new_size, height=new_size)
        self.center_x = new_size // 2
        self.center_y = new_size // 2
        self.radius = new_size // 2 - 10
        
        self.canvas.delete("all")
        self.draw_clock()
    
    def set_transparency(self, value):
        """Define o nível de transparência"""
        self.attributes('-alpha', value)
    
    def toggle_always_on_top(self, event=None):
        """Alterna o estado 'sempre no topo'"""
        current = self.attributes('-topmost')
        self.attributes('-topmost', not current)
    
    def confirm_close(self):
        """Fecha a janela após confirmação"""
        dialog = tk.Toplevel(self)
        dialog.overrideredirect(True)
        dialog.attributes('-topmost', True)
        
        # Posiciona o diálogo próximo ao clique
        dialog.geometry('200x100+{}+{}'.format(
            self.winfo_x() + 50,
            self.winfo_y() + 50
        ))
        
        frame = tk.Frame(dialog, bg='white', relief='solid', borderwidth=2)
        frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        tk.Label(frame, text="Fechar relógio?", 
                bg='white', font=('Arial', 10)).pack(pady=15)
        
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Sim", command=self.destroy,
                 bg='#4CAF50', fg='white', width=8).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Não", command=dialog.destroy,
                 bg='#f44336', fg='white', width=8).pack(side='left', padx=5)
    
    def draw_clock(self):
        """Desenha o relógio com o tamanho atual"""
        margin = 5
        
        # Desenha círculo externo
        self.canvas.create_oval(
            margin, margin, self.size - margin, self.size - margin,
            outline='black', width=2
        )
        
        # Marcações das horas
        for i in range(12):
            angle = i * 30 - 90
            angle_rad = angle * (pi / 180)
            
            # Tamanho proporcional das marcações
            mark_length = self.radius * 0.15
            x1 = self.center_x + (self.radius - mark_length) * cos(angle_rad)
            y1 = self.center_y + (self.radius - mark_length) * sin(angle_rad)
            x2 = self.center_x + (self.radius - 5) * cos(angle_rad)
            y2 = self.center_y + (self.radius - 5) * sin(angle_rad)
            
            self.canvas.create_line(x1, y1, x2, y2, width=2)
        
        # Desenha um pequeno indicador de redimensionamento no canto
        self.canvas.create_rectangle(
            self.size - 15, self.size - 15,
            self.size - 5, self.size - 5,
            fill='gray', outline='black', width=1
        )
        self.canvas.create_line(
            self.size - 13, self.size - 7,
            self.size - 7, self.size - 13,
            width=2, fill='white'
        )
    
    def update_clock(self):
        """Atualiza os ponteiros do relógio"""
        self.canvas.delete("hands")
        
        now = datetime.now()
        
        # Calcula ângulos
        hour_angle = (now.hour % 12 + now.minute / 60) * 30 - 90
        hour_angle_rad = hour_angle * (pi / 180)
        
        minute_angle = now.minute * 6 - 90
        minute_angle_rad = minute_angle * (pi / 180)
        
        second_angle = now.second * 6 - 90
        second_angle_rad = second_angle * (pi / 180)
        
        # Tamanhos proporcionais dos ponteiros
        hour_length = self.radius * 0.5
        minute_length = self.radius * 0.7
        second_length = self.radius * 0.8
        
        # Calcula pontos finais
        hour_x = self.center_x + hour_length * cos(hour_angle_rad)
        hour_y = self.center_y + hour_length * sin(hour_angle_rad)
        
        minute_x = self.center_x + minute_length * cos(minute_angle_rad)
        minute_y = self.center_y + minute_length * sin(minute_angle_rad)
        
        second_x = self.center_x + second_length * cos(second_angle_rad)
        second_y = self.center_y + second_length * sin(second_angle_rad)
        
        # Desenha ponteiros
        self.canvas.create_line(
            self.center_x, self.center_y, hour_x, hour_y,
            width=4, fill='black', tags="hands"
        )
        self.canvas.create_line(
            self.center_x, self.center_y, minute_x, minute_y,
            width=3, fill='blue', tags="hands"
        )
        self.canvas.create_line(
            self.center_x, self.center_y, second_x, second_y,
            width=1, fill='red', tags="hands"
        )
        
        # Centro
        self.canvas.create_oval(
            self.center_x - 5, self.center_y - 5,
            self.center_x + 5, self.center_y + 5,
            fill='red', tags="hands"
        )
        
        self.after(1000, self.update_clock)

if __name__ == "__main__":
    app = SimpleAnalogClock()
    app.mainloop()
