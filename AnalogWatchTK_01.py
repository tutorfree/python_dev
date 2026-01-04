import tkinter as tk
from math import cos, sin, pi
from datetime import datetime

class SimpleAnalogClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Relógio Analógico Simples")
        
        self.canvas = tk.Canvas(self, width=300, height=300, bg='white')
        self.canvas.pack()
        
        self.center_x = 150
        self.center_y = 150
        self.radius = 140
        
        self.draw_clock()
        self.update_clock()
    
    def draw_clock(self):
        # Desenha círculo externo
        self.canvas.create_oval(
            10, 10, 290, 290,
            outline='black', width=2
        )
        
        # Marcações das horas
        for i in range(12):
            angle = i * 30 - 90
            angle_rad = angle * (pi / 180)
            
            x1 = self.center_x + (self.radius - 20) * cos(angle_rad)
            y1 = self.center_y + (self.radius - 20) * sin(angle_rad)
            x2 = self.center_x + (self.radius - 5) * cos(angle_rad)
            y2 = self.center_y + (self.radius - 5) * sin(angle_rad)
            
            self.canvas.create_line(x1, y1, x2, y2, width=3)
    
    def update_clock(self):
        # Limpa ponteiros anteriores
        self.canvas.delete("hands")
        
        now = datetime.now()
        
        # Ponteiro das horas
        hour_angle = (now.hour % 12 + now.minute / 60) * 30 - 90
        hour_angle_rad = hour_angle * (pi / 180)
        hour_x = self.center_x + 60 * cos(hour_angle_rad)
        hour_y = self.center_y + 60 * sin(hour_angle_rad)
        
        # Ponteiro dos minutos
        minute_angle = now.minute * 6 - 90
        minute_angle_rad = minute_angle * (pi / 180)
        minute_x = self.center_x + 90 * cos(minute_angle_rad)
        minute_y = self.center_y + 90 * sin(minute_angle_rad)
        
        # Ponteiro dos segundos
        second_angle = now.second * 6 - 90
        second_angle_rad = second_angle * (pi / 180)
        second_x = self.center_x + 100 * cos(second_angle_rad)
        second_y = self.center_y + 100 * sin(second_angle_rad)
        
        # Desenha ponteiros
        self.canvas.create_line(
            self.center_x, self.center_y, hour_x, hour_y,
            width=6, fill='black', tags="hands"
        )
        self.canvas.create_line(
            self.center_x, self.center_y, minute_x, minute_y,
            width=4, fill='blue', tags="hands"
        )
        self.canvas.create_line(
            self.center_x, self.center_y, second_x, second_y,
            width=2, fill='red', tags="hands"
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
