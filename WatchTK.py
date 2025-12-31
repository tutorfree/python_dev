import tkinter as tk
from datetime import datetime

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Relógio TK")
        self.label = tk.Label(self, font=('Helvetica', 48), fg='red')
        self.label.pack(padx=20, pady=20)
        
        self.update_clock()

    def update_clock(self):
        # datetime.now().strftime é levemente mais eficiente para strings formatadas
        now = datetime.now().strftime("%H:%M:%S")
        self.label.config(text=now)
        
        # O método after agenda a execução sem travar a interface
        self.after(1000, self.update_clock)

if __name__ == "__main__":
    app = Clock()
    app.mainloop()
