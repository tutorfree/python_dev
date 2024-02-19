import tkinter as tk

def clear_entries():
    alcool.delete(0, 'end')
    gasolina.delete(0, 'end')
    lbDivisao.config(text="")
    lbResultado.config(text="")

def get_entry_value(entry):
    value = entry.get().replace(',', '.', 1)
    return float(value) if value else None

def calculate():
    alcool_val = get_entry_value(alcool)
    gasolina_val = get_entry_value(gasolina)
    
    if alcool_val is not None and gasolina_val is not None:
        resultado = alcool_val / gasolina_val * 100
        lbDivisao.config(text='%.2f %%' % resultado)
        
        if resultado < 70:
            lbResultado.config(text="Compensa mais abastecer com álcool.")
        else:
            lbResultado.config(text="Compensa mais abastecer com gasolina.")
    else:
        lbResultado.config(text="Um ou mais valores digitados estão fora do padrão!")

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Álcool ou Gasolina?")

    lbAlcool = tk.Label(janela, text="Álcool: ")
    lbAlcool.place(x=50, y=40)
    
    lbGasolina = tk.Label(janela, text="Gasolina: ")
    lbGasolina.place(x=50, y=70)
    
    alcool = tk.Entry(janela)
    alcool.place(x=120, y=40, width=185)
    alcool.focus_set()
    
    gasolina = tk.Entry(janela)
    gasolina.place(x=120, y=70, width=185)
    
    btCalcular = tk.Button(janela, text="Calcular", width=10, command=calculate)
    btCalcular.place(x=120, y=110)
    
    btLimpar = tk.Button(janela, text="Limpar", width=10, command=clear_entries)
    btLimpar.place(x=213, y=110)
    
    lbDivisao = tk.Label(janela, text="", foreground="blue")
    lbDivisao.place(x=50, y=150)
    
    lbResultado = tk.Label(janela, text="")
    lbResultado.place(x=50, y=170)
    
    janela.geometry("420x220+200+200")
    janela.mainloop()
