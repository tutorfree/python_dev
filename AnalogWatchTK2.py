import tkinter as tk
from math import cos, sin, pi
from datetime import datetime

class SimpleAnalogClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Relógio Analógico")
        
        # Canvas para o relógio
        self.canvas = tk.Canvas(self, width=400, height=400, bg='white')
        self.canvas.pack(pady=20)
        
        # Botão Sair
        exit_button = tk.Button(
            self, 
            text="SAIR", 
            command=self.destroy,  # Usando destroy corretamente
            bg='red',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=10
        )
        exit_button.pack(pady=10)
        
        self.center_x = 200
        self.center_y = 200
        self.radius = 180
        
        self.draw_clock()
        self.update_clock()
    
    def draw_clock(self):
        # Círculo externo
        self.canvas.create_oval(20, 20, 380, 380, outline='black', width=3)
        
        # Marcações
        for i in range(12):
            angle = i * 30 - 90
            angle_rad = angle * (pi / 180)
            x1 = self.center_x + (self.radius - 20) * cos(angle_rad)
            y1 = self.center_y + (self.radius - 20) * sin(angle_rad)
            x2 = self.center_x + (self.radius - 5) * cos(angle_rad)
            y2 = self.center_y + (self.radius - 5) * sin(angle_rad)
            self.canvas.create_line(x1, y1, x2, y2, width=3)
    
    def update_clock(self):
        self.canvas.delete("hands")
        
        now = datetime.now()
        
        # Ponteiros
        hour_angle = (now.hour % 12 + now.minute / 60) * 30 - 90
        hour_angle_rad = hour_angle * (pi / 180)
        hour_x = self.center_x + 70 * cos(hour_angle_rad)
        hour_y = self.center_y + 70 * sin(hour_angle_rad)
        
        minute_angle = now.minute * 6 - 90
        minute_angle_rad = minute_angle * (pi / 180)
        minute_x = self.center_x + 100 * cos(minute_angle_rad)
        minute_y = self.center_y + 100 * sin(minute_angle_rad)
        
        second_angle = now.second * 6 - 90
        second_angle_rad = second_angle * (pi / 180)
        second_x = self.center_x + 120 * cos(second_angle_rad)
        second_y = self.center_y + 120 * sin(second_angle_rad)
        
        # Desenhar
        self.canvas.create_line(self.center_x, self.center_y, hour_x, hour_y,
                               width=8, fill='black', tags="hands")
        self.canvas.create_line(self.center_x, self.center_y, minute_x, minute_y,
                               width=5, fill='blue', tags="hands")
        self.canvas.create_line(self.center_x, self.center_y, second_x, second_y,
                               width=2, fill='red', tags="hands")
        
        # Centro
        self.canvas.create_oval(self.center_x-8, self.center_y-8,
                               self.center_x+8, self.center_y+8,
                               fill='red', tags="hands")
        
        self.after(1000, self.update_clock)

if __name__ == "__main__":
    app = SimpleAnalogClock()
    app.mainloop()
