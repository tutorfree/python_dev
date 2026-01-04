import tkinter as tk
from math import cos, sin, pi
from datetime import datetime

class MinimalClock(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-transparentcolor', 'white')
        self.attributes('-alpha', 0.9)
        
        self.config(bg='white')
        
        # Variáveis de tamanho
        self.size = 200
        self.min_size = 100
        self.max_size = 400
        
        self.canvas = tk.Canvas(self, width=self.size, height=self.size, 
                               bg='white', highlightthickness=0)
        self.canvas.pack()
        
        self.center_x = self.size // 2
        self.center_y = self.size // 2
        
        # Posiciona no canto inferior direito
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{self.size}x{self.size}+{screen_width-220}+{screen_height-220}')
        
        # Controle de interação
        self._dragging = False
        self._resizing = False
        
        # Bind para interação
        self.canvas.bind('<Button-1>', self.start_interaction)
        self.canvas.bind('<B1-Motion>', self.on_motion)
        self.canvas.bind('<ButtonRelease-1>', self.end_interaction)
        self.canvas.bind('<Button-3>', self.show_context_menu)
        
        # Detecta cantos para redimensionamento
        self.canvas.bind('<Motion>', self.update_cursor)
        
        self.update_clock()
    
    def update_cursor(self, event):
        x, y = event.x, event.y
        size = self.size
        
        # Canto inferior direito para redimensionamento
        if x > size - 10 and y > size - 10:
            self.canvas.config(cursor='size_nw_se')
        else:
            self.canvas.config(cursor='fleur')
    
    def start_interaction(self, event):
        x, y = event.x, event.y
        size = self.size
        
        if x > size - 15 and y > size - 15:
            self._resizing = True
            self._resize_start_x = event.x_root
            self._resize_start_y = event.y_root
            self._start_size = self.size
        else:
            self._dragging = True
            self._start_x = event.x
            self._start_y = event.y
    
    def on_motion(self, event):
        if self._resizing:
            # Redimensionamento simples
            delta_x = event.x_root - self._resize_start_x
            delta_y = event.x_root - self._resize_start_y
            delta = max(delta_x, delta_y)
            
            new_size = self._start_size + delta
            new_size = max(self.min_size, min(self.max_size, new_size))
            
            if new_size != self.size:
                self.size = new_size
                self.canvas.config(width=new_size, height=new_size)
                self.geometry(f'{new_size}x{new_size}')
                
                self.center_x = new_size // 2
                self.center_y = new_size // 2
        
        elif self._dragging:
            x = self.winfo_x() + event.x - self._start_x
            y = self.winfo_y() + event.y - self._start_y
            self.geometry(f'+{x}+{y}')
    
    def end_interaction(self, event):
        self._resizing = False
        self._dragging = False
    
    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Fechar", command=self.confirm_close)
        menu.add_separator()
        menu.add_command(label="Pequeno (150px)", 
                        command=lambda: self.set_size(150))
        menu.add_command(label="Médio (200px)", 
                        command=lambda: self.set_size(200))
        menu.add_command(label="Grande (250px)", 
                        command=lambda: self.set_size(250))
        menu.add_separator()
        menu.add_command(label="Resetar", 
                        command=lambda: self.set_size(200))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def set_size(self, new_size):
        new_size = max(self.min_size, min(self.max_size, new_size))
        self.size = new_size
        self.canvas.config(width=new_size, height=new_size)
        self.geometry(f'{new_size}x{new_size}')
        
        self.center_x = new_size // 2
        self.center_y = new_size // 2
    
    def confirm_close(self):
        self.destroy()
    
    def update_clock(self):
        self.canvas.delete("all")
        
        now = datetime.now()
        
        # Desenha um pequeno indicador de redimensionamento
        self.canvas.create_rectangle(
            self.size - 8, self.size - 8,
            self.size - 2, self.size - 2,
            fill='gray', outline='', tags="resize_indicator"
        )
        
        # Desenha apenas os ponteiros
        hour_angle = (now.hour % 12 + now.minute / 60) * 30 - 90
        hour_angle_rad = hour_angle * (pi / 180)
        
        minute_angle = now.minute * 6 - 90
        minute_angle_rad = minute_angle * (pi / 180)
        
        second_angle = now.second * 6 - 90
        second_angle_rad = second_angle * (pi / 180)
        
        # Tamanhos proporcionais (baseado no tamanho da janela)
        base_size = min(self.size, 300)  # Limita o tamanho base
        hour_length = base_size * 0.15
        minute_length = base_size * 0.22
        second_length = base_size * 0.25
        
        # Ponteiro das horas
        hour_x = self.center_x + hour_length * cos(hour_angle_rad)
        hour_y = self.center_y + hour_length * sin(hour_angle_rad)
        
        # Ponteiro dos minutos
        minute_x = self.center_x + minute_length * cos(minute_angle_rad)
        minute_y = self.center_y + minute_length * sin(minute_angle_rad)
        
        # Ponteiro dos segundos
        second_x = self.center_x + second_length * cos(second_angle_rad)
        second_y = self.center_y + second_length * sin(second_angle_rad)
        
        # Desenha ponteiros
        self.canvas.create_line(
            self.center_x, self.center_y, hour_x, hour_y,
            width=3, fill='black', tags="hands"
        )
        self.canvas.create_line(
            self.center_x, self.center_y, minute_x, minute_y,
            width=2, fill='blue', tags="hands"
        )
        self.canvas.create_line(
            self.center_x, self.center_y, second_x, second_y,
            width=1, fill='red', tags="hands"
        )
        
        # Ponto central
        self.canvas.create_oval(
            self.center_x - 2, self.center_y - 2,
            self.center_x + 2, self.center_y + 2,
            fill='red', tags="hands"
        )
        
        self.after(1000, self.update_clock)

if __name__ == "__main__":
    app = MinimalClock()
    app.mainloop()
