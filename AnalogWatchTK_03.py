import tkinter as tk
from math import cos, sin, pi
from datetime import datetime

class FloatingClock:
    def __init__(self, master=None):
        if master is None:
            self.root = tk.Tk()
            self.root.withdraw()
        else:
            self.root = master
        
        self.window = tk.Toplevel(self.root)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.attributes('-alpha', 0.9)
        
        # Variáveis de tamanho
        self.size = 300
        self.min_size = 150
        self.max_size = 450
        
        # Calcula valores do relógio
        self.center_x = self.size // 2
        self.center_y = self.size // 2
        self.radius = self.size // 2 - 10
        
        # Posiciona no canto superior direito
        screen_width = self.window.winfo_screenwidth()
        self.window.geometry(f'{self.size}x{self.size}+{screen_width-320}+20')
        
        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size,
                               bg='white', highlightthickness=0)
        self.canvas.pack()
        
        # Controle de redimensionamento
        self._resizing = False
        self._dragging = False
        
        # Bind para interação
        self.canvas.bind('<Button-1>', self.start_interaction)
        self.canvas.bind('<B1-Motion>', self.on_motion)
        self.canvas.bind('<ButtonRelease-1>', self.end_interaction)
        self.canvas.bind('<Button-3>', self.show_context_menu)
        self.canvas.bind('<Control-MouseWheel>', self.zoom_with_wheel)
        
        # Cursor para redimensionamento
        self.canvas.bind('<Motion>', self.update_cursor)
        
        self.draw_clock()
        self.update_clock()
    
    def update_cursor(self, event):
        x, y = event.x, event.y
        size = self.size
        
        if x > size - 15 and y > size - 15:
            self.canvas.config(cursor='size_nw_se')
        elif x < 15 and y < 15:
            self.canvas.config(cursor='size_nw_se')
        else:
            self.canvas.config(cursor='fleur')
    
    def start_interaction(self, event):
        x, y = event.x, event.y
        size = self.size
        
        # Verifica canto inferior direito ou superior esquerdo para redimensionar
        if (x > size - 15 and y > size - 15) or (x < 15 and y < 15):
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
            # Redimensionamento proporcional
            delta_x = event.x_root - self._resize_start_x
            delta_y = event.x_root - self._resize_start_y
            
            # Se redimensionando do canto superior esquerdo, muda posição também
            if event.x < 15 and event.y < 15:
                delta = -max(abs(delta_x), abs(delta_y))
            else:
                delta = max(delta_x, delta_y)
            
            new_size = self._start_size + delta
            new_size = max(self.min_size, min(self.max_size, new_size))
            
            if new_size != self.size:
                self.size = new_size
                self.canvas.config(width=new_size, height=new_size)
                
                # Se redimensionando do canto superior esquerdo, move a janela
                if event.x < 15 and event.y < 15:
                    x = self.window.winfo_x() - (new_size - self._start_size)
                    y = self.window.winfo_y() - (new_size - self._start_size)
                    self.window.geometry(f'{new_size}x{new_size}+{x}+{y}')
                else:
                    self.window.geometry(f'{new_size}x{new_size}')
                
                self.center_x = new_size // 2
                self.center_y = new_size // 2
                self.radius = new_size // 2 - 10
                
                self.canvas.delete("all")
                self.draw_clock()
        
        elif self._dragging:
            x = self.window.winfo_x() + event.x - self._start_x
            y = self.window.winfo_y() + event.y - self._start_y
            self.window.geometry(f'+{x}+{y}')
    
    def end_interaction(self, event):
        self._resizing = False
        self._dragging = False
    
    def zoom_with_wheel(self, event):
        """Zoom com Ctrl + Scroll do mouse"""
        if event.delta > 0:
            new_size = min(self.max_size, self.size + 20)
        else:
            new_size = max(self.min_size, self.size - 20)
        
        if new_size != self.size:
            self.size = new_size
            self.canvas.config(width=new_size, height=new_size)
            self.window.geometry(f'{new_size}x{new_size}')
            
            self.center_x = new_size // 2
            self.center_y = new_size // 2
            self.radius = new_size // 2 - 10
            
            self.canvas.delete("all")
            self.draw_clock()
    
    def show_context_menu(self, event):
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Fechar", command=self.confirm_close)
        menu.add_separator()
        menu.add_command(label="Zoom +", command=lambda: self.zoom_clock(1.2))
        menu.add_command(label="Zoom -", command=lambda: self.zoom_clock(0.8))
        menu.add_separator()
        menu.add_command(label="Tamanho 200px", command=lambda: self.set_size(200))
        menu.add_command(label="Tamanho 300px", command=lambda: self.set_size(300))
        menu.add_command(label="Tamanho 400px", command=lambda: self.set_size(400))
        menu.add_separator()
        menu.add_command(label="Resetar Tamanho", command=lambda: self.set_size(300))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def zoom_clock(self, factor):
        new_size = int(self.size * factor)
        new_size = max(self.min_size, min(self.max_size, new_size))
        self.set_size(new_size)
    
    def set_size(self, new_size):
        self.size = new_size
        self.canvas.config(width=new_size, height=new_size)
        self.window.geometry(f'{new_size}x{new_size}')
        
        self.center_x = new_size // 2
        self.center_y = new_size // 2
        self.radius = new_size // 2 - 10
        
        self.canvas.delete("all")
        self.draw_clock()
    
    def confirm_close(self):
        self.window.destroy()
        if hasattr(self, 'root'):
            self.root.quit()
    
    def draw_clock(self):
        # Desenha indicadores de redimensionamento nos cantos
        self.canvas.create_rectangle(
            self.size - 15, self.size - 15,
            self.size - 5, self.size - 5,
            fill='#cccccc', outline='#888888', width=1,
            tags="resize_corner"
        )
        
        self.canvas.create_rectangle(
            5, 5, 15, 15,
            fill='#cccccc', outline='#888888', width=1,
            tags="resize_corner"
        )
        
        # Linhas diagonais nos indicadores
        self.canvas.create_line(
            self.size - 13, self.size - 7,
            self.size - 7, self.size - 13,
            width=2, fill='#666666', tags="resize_corner"
        )
        
        self.canvas.create_line(
            7, 7, 13, 13,
            width=2, fill='#666666', tags="resize_corner"
        )
        
        # Desenha círculo do relógio
        margin = 10
        self.canvas.create_oval(
            margin, margin, self.size - margin, self.size - margin,
            outline='black', width=2, fill='#f9f9f9'
        )
        
        # Marcações
        for i in range(12):
            angle = i * 30 - 90
            angle_rad = angle * (pi / 180)
            
            length = self.radius * 0.15 if i % 3 == 0 else self.radius * 0.1
            x1 = self.center_x + (self.radius - length) * cos(angle_rad)
            y1 = self.center_y + (self.radius - length) * sin(angle_rad)
            x2 = self.center_x + (self.radius - 5) * cos(angle_rad)
            y2 = self.center_y + (self.radius - 5) * sin(angle_rad)
            
            width = 3 if i % 3 == 0 else 2
            self.canvas.create_line(x1, y1, x2, y2, width=width, fill='black')
    
    def update_clock(self):
        self.canvas.delete("hands")
        
        now = datetime.now()
        
        hour_angle = (now.hour % 12 + now.minute / 60) * 30 - 90
        hour_angle_rad = hour_angle * (pi / 180)
        
        minute_angle = now.minute * 6 - 90
        minute_angle_rad = minute_angle * (pi / 180)
        
        second_angle = now.second * 6 - 90
        second_angle_rad = second_angle * (pi / 180)
        
        # Tamanhos proporcionais
        hour_length = self.radius * 0.5
        minute_length = self.radius * 0.7
        second_length = self.radius * 0.8
        
        hour_x = self.center_x + hour_length * cos(hour_angle_rad)
        hour_y = self.center_y + hour_length * sin(hour_angle_rad)
        
        minute_x = self.center_x + minute_length * cos(minute_angle_rad)
        minute_y = self.center_y + minute_length * sin(minute_angle_rad)
        
        second_x = self.center_x + second_length * cos(second_angle_rad)
        second_y = self.center_y + second_length * sin(second_angle_rad)
        
        # Ponteiros
        self.canvas.create_line(
            self.center_x, self.center_y, hour_x, hour_y,
            width=6, fill='#333333', tags="hands", capstyle=tk.ROUND
        )
        self.canvas.create_line(
            self.center_x, self.center_y, minute_x, minute_y,
            width=4, fill='#555555', tags="hands", capstyle=tk.ROUND
        )
        self.canvas.create_line(
            self.center_x, self.center_y, second_x, second_y,
            width=2, fill='red', tags="hands"
        )
        
        # Centro
        self.canvas.create_oval(
            self.center_x - 8, self.center_y - 8,
            self.center_x + 8, self.center_y + 8,
            fill='#222222', tags="hands"
        )
        self.canvas.create_oval(
            self.center_x - 4, self.center_y - 4,
            self.center_x + 4, self.center_y + 4,
            fill='red', tags="hands"
        )
        
        self.window.after(1000, self.update_clock)

if __name__ == "__main__":
    clock = FloatingClock()
    clock.window.mainloop()
