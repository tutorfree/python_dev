import tkinter as tk
import random
import string
import math

class AlphabetGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo do Alfabeto")
        self.root.geometry("800x600")
        
        # Frame superior - letras embaralhadas
        self.top_frame = tk.Frame(root, bg='lightblue', height=300)
        self.top_frame.pack(fill='both', expand=True)
        self.top_frame.pack_propagate(False)
        
        # Frame inferior - slots ordenados (agora em múltiplas linhas)
        self.bottom_frame = tk.Frame(root, bg='lightgreen', height=300)
        self.bottom_frame.pack(fill='both', expand=True)
        self.bottom_frame.pack_propagate(False)
        
        # Lista do alfabeto
        self.alphabet = list(string.ascii_uppercase)
        
        # Configuração do layout dos slots
        self.LETTERS_PER_ROW = 13  # Divide 26 letras em 2 linhas de 13
        
        # Letras embaralhadas
        self.shuffled_alphabet = self.alphabet.copy()
        random.shuffle(self.shuffled_alphabet)
        
        # Dicionário para armazenar widgets das letras
        self.letter_widgets = {}
        self.slot_widgets = {}
        
        # Dados para drag-and-drop
        self.drag_data = {"x": 0, "y": 0, "item": None}
        
        # Inicializar letras arrastáveis
        self.create_draggable_letters()
        
        # Inicializar slots (agora em múltiplas linhas)
        self.create_slots_multiline()
        
        # Botão de verificação
        self.check_button = tk.Button(root, text="Verificar", 
                                      command=self.check_order, 
                                      bg='yellow', font=('Arial', 14))
        self.check_button.pack(pady=10)
        
        # Label para feedback
        self.feedback_label = tk.Label(root, text="", font=('Arial', 14))
        self.feedback_label.pack()
    
    def create_draggable_letters(self):
        """Cria as letras arrastáveis no frame superior - agora mais espalhadas"""
        frame_width = 800
        frame_height = 300
        
        # Definir áreas de posicionamento mais amplas
        # Usar quase toda a largura do frame, deixando apenas uma pequena margem
        min_x = 20  # Margem esquerda reduzida
        max_x = frame_width - 70  # Margem direita considerando largura da letra (~50px)
        
        # Usar quase toda a altura do frame superior
        min_y = 20  # Margem superior reduzida
        max_y = frame_height - 70  # Margem inferior considerando altura da letra
        
        # Para evitar sobreposição excessiva, vamos usar uma abordagem mais inteligente
        positions_used = []
        
        for i, letter in enumerate(self.shuffled_alphabet):
            # Criar label como letra arrastável
            lbl = tk.Label(self.top_frame, text=letter, 
                          font=('Arial', 24, 'bold'),
                          bg='white', fg='blue',
                          relief='raised', bd=3,
                          width=3, height=1)
            
            # Tentar posicionar sem sobreposição excessiva
            max_attempts = 50
            placed = False
            
            for attempt in range(max_attempts):
                # Gerar posição aleatória
                x = random.randint(min_x, max_x)
                y = random.randint(min_y, max_y)
                
                # Verificar se está muito próximo de outras letras
                too_close = False
                for (px, py) in positions_used:
                    distance = math.sqrt((x - px)**2 + (y - py)**2)
                    if distance < 60:  # Distância mínima entre letras
                        too_close = True
                        break
                
                if not too_close or attempt == max_attempts - 1:
                    # Posicionar letra
                    lbl.place(x=x, y=y)
                    positions_used.append((x, y))
                    placed = True
                    break
            
            # Se não conseguiu posicionar sem sobreposição, posiciona de qualquer forma
            if not placed:
                x = random.randint(min_x, max_x)
                y = random.randint(min_y, max_y)
                lbl.place(x=x, y=y)
            
            # Vincular eventos de mouse
            lbl.bind("<ButtonPress-1>", self.on_press)
            lbl.bind("<B1-Motion>", self.on_drag)
            lbl.bind("<ButtonRelease-1>", self.on_release)
            
            # Armazenar referência
            self.letter_widgets[letter] = lbl
        
        # Adicionar título no frame superior
        title_label = tk.Label(self.top_frame, 
                              text="Arraste as letras para os slots corretos abaixo",
                              font=('Arial', 14, 'bold'),
                              bg='lightblue',
                              fg='darkblue')
        title_label.place(x=200, y=10)
    
    def create_slots_multiline(self):
        """Cria os slots ordenados em múltiplas linhas"""
        total_letters = len(self.alphabet)
        letters_per_row = self.LETTERS_PER_ROW
        
        # Calcular número de linhas necessárias
        num_rows = math.ceil(total_letters / letters_per_row)
        
        # Calcular posição inicial para centralizar
        frame_width = 800
        total_slots_width = letters_per_row * 60  # 50px slot + 10px margem
        start_x = (frame_width - total_slots_width) // 2
        
        # Ajustar start_x para deixar espaço para as labels
        start_x = max(80, start_x)  # Garante pelo menos 80px à esquerda para labels
        
        # Primeiro, criar todos os slots
        for i, letter in enumerate(self.alphabet):
            # Calcular em qual linha e coluna esta letra deve estar
            row = i // letters_per_row
            col = i % letters_per_row
            
            # Frame para slot
            slot_frame = tk.Frame(self.bottom_frame, 
                                 bg='white', 
                                 relief='sunken', 
                                 bd=2,
                                 width=50, height=50)
            
            # Posicionar
            x = start_x + (col * 60)
            y = 40 + (row * 70)  # 70px de altura por linha
            slot_frame.place(x=x, y=y)
            
            # Label com número/posição
            pos_label = tk.Label(slot_frame, text=str(i+1), 
                                font=('Arial', 10),
                                bg='lightgray')
            pos_label.pack(side='top', fill='x')
            
            # Label vazio para receber letra
            content_label = tk.Label(slot_frame, text="", 
                                    font=('Arial', 20, 'bold'),
                                    bg='white')
            content_label.pack(expand=True)
            
            # Armazenar referência
            self.slot_widgets[i] = {
                'frame': slot_frame,
                'pos_label': pos_label,
                'content_label': content_label,
                'occupied_by': None,
                'expected_letter': letter,
                'row': row,
                'col': col
            }
        
        # Agora criar labels das linhas à esquerda, sem sobrepor os slots
        for row in range(num_rows):
            start_idx = row * letters_per_row
            end_idx = min((row + 1) * letters_per_row, total_letters)
            
            # Label para a linha
            row_label = tk.Label(self.bottom_frame, 
                                text=f"Linha {row + 1}",
                                font=('Arial', 11, 'bold'),
                                bg='lightgreen',
                                fg='darkblue')
            
            # Posicionar à esquerda dos slots, alinhada verticalmente com a linha
            label_x = 10  # Bem à esquerda
            label_y = 55 + (row * 70)  # Centralizada verticalmente com os slots
            
            row_label.place(x=label_x, y=label_y)
            
            # Opcional: Label com o intervalo de letras (em uma linha separada ou menor)
            range_label = tk.Label(self.bottom_frame,
                                  text=f"({start_idx + 1}-{end_idx})",
                                  font=('Arial', 9),
                                  bg='lightgreen',
                                  fg='darkred')
            range_label.place(x=label_x, y=label_y + 20)
    
    def on_press(self, event):
        """Quando o mouse é pressionado sobre uma letra"""
        widget = event.widget
        self.drag_data["item"] = widget
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        # Elevar widget ao topo
        widget.lift()
        
        # Configurar cursor
        widget.config(cursor="hand2")
    
    def on_drag(self, event):
        """Durante o arrasto"""
        widget = self.drag_data["item"]
        if widget:
            # Calcular nova posição
            x = widget.winfo_x() + (event.x - self.drag_data["x"])
            y = widget.winfo_y() + (event.y - self.drag_data["y"])
            
            # Mover widget
            widget.place(x=x, y=y)
    
    def on_release(self, event):
        """Quando o mouse é solto"""
        widget = self.drag_data["item"]
        if not widget:
            return
        
        # Resetar cursor
        widget.config(cursor="")
        
        # Verificar se soltou sobre algum slot
        widget_x = widget.winfo_rootx()
        widget_y = widget.winfo_rooty()
        widget_width = widget.winfo_width()
        widget_height = widget.winfo_height()
        
        letter = widget.cget("text")
        slot_occupied = None
        
        # Verificar se está sobre algum slot
        for slot_id, slot_data in self.slot_widgets.items():
            slot_x = slot_data['frame'].winfo_rootx()
            slot_y = slot_data['frame'].winfo_rooty()
            slot_width = slot_data['frame'].winfo_width()
            slot_height = slot_data['frame'].winfo_height()
            
            # Verificar colisão
            if (widget_x < slot_x + slot_width and
                widget_x + widget_width > slot_x and
                widget_y < slot_y + slot_height and
                widget_y + widget_height > slot_y):
                
                slot_occupied = slot_id
                break
        
        if slot_occupied is not None:
            slot = self.slot_widgets[slot_occupied]
            
            # Se slot já está ocupado, retornar letra anterior ao topo
            if slot['occupied_by']:
                old_letter = slot['occupied_by']
                self.return_letter_to_top(old_letter)
            
            # Colocar letra no slot
            self.place_letter_in_slot(letter, slot_occupied)
            
            # Remover letra do frame superior
            widget.place_forget()
        else:
            # Se não soltou em slot, retornar ao topo
            self.return_letter_to_top(letter)
        
        self.drag_data["item"] = None
    
    def place_letter_in_slot(self, letter, slot_id):
        """Coloca uma letra em um slot específico"""
        slot = self.slot_widgets[slot_id]
        slot['content_label'].config(text=letter, fg='blue')
        slot['occupied_by'] = letter
    
    def return_letter_to_top(self, letter):
        """Retorna uma letra ao frame superior (se ainda existir)"""
        if letter in self.letter_widgets:
            widget = self.letter_widgets[letter]
            # Posicionar aleatoriamente no topo com área ampla
            frame_width = 800
            frame_height = 300
            x = random.randint(20, frame_width - 70)
            y = random.randint(20, frame_height - 70)
            widget.place(x=x, y=y)
        
        # Limpar slot se tinha alguma letra
        for slot_id, slot_data in self.slot_widgets.items():
            if slot_data['occupied_by'] == letter:
                slot_data['content_label'].config(text="")
                slot_data['occupied_by'] = None
    
    def check_order(self):
        """Verifica se as letras estão na ordem correta"""
        correct = 0
        total = len(self.alphabet)
        
        for slot_id, slot_data in self.slot_widgets.items():
            if slot_data['occupied_by'] == slot_data['expected_letter']:
                slot_data['content_label'].config(fg='green')
                slot_data['frame'].config(bg='lightgreen')
                correct += 1
            elif slot_data['occupied_by']:
                slot_data['content_label'].config(fg='red')
                slot_data['frame'].config(bg='lightcoral')
            else:
                slot_data['frame'].config(bg='white')
        
        if correct == total:
            self.feedback_label.config(text="Parabéns! Todas as letras estão corretas!", fg='green')
        else:
            self.feedback_label.config(text=f"Acertou {correct} de {total} letras. Continue tentando!", fg='orange')
        
        # Reiniciar jogo após 3 segundos se completo
        if correct == total:
            self.root.after(3000, self.reset_game)
    
    def reset_game(self):
        """Reinicia o jogo"""
        # Remover todas as letras
        for letter, widget in self.letter_widgets.items():
            widget.place_forget()
        
        # Limpar slots
        for slot_id, slot_data in self.slot_widgets.items():
            slot_data['content_label'].config(text="", fg='blue')
            slot_data['occupied_by'] = None
            slot_data['frame'].config(bg='white')
        
        # Embaralhar novamente
        random.shuffle(self.shuffled_alphabet)
        
        # Recriar letras (agora mais espalhadas)
        self.create_draggable_letters()
        
        # Limpar feedback
        self.feedback_label.config(text="")

def main():
    root = tk.Tk()
    game = AlphabetGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
