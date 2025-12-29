import tkinter as tk

def reset_entries():
    peso.delete(0, 'end')
    altura.delete(0, 'end')
    lbDivisao.config(text="")
    for lbP in lbP_list:
        lbP.config(bg=default_bg)
    peso.focus_set()

def calcular():
    try:
        # Cores para cada faixa de IMC
        cor = ['Aquamarine', 'MediumAquamarine', 'LightGreen', 'yellow', 'salmon', 'Tomato', 'red']
        
        # Substitui vírgula por ponto para conversão float
        peso_val = peso.get().replace(',', '.')
        altura_val = altura.get().replace(',', '.')

        if peso_val and altura_val:
            p = float(peso_val)
            a = float(altura_val)
            imc = p / (a**2)
            
            # Formata para 2 casas decimais e exibe com vírgula
            imc_formatado = f"{imc:.2f}".replace('.', ',')
            lbDivisao.config(text=f"IMC: {imc_formatado}")

            # Reseta cores antes de destacar a nova
            for lbP in lbP_list:
                lbP.config(bg=default_bg)

            # Lógica de faixas
            limites_imc = [17, 18.49, 24.99, 29.99, 34.99, 39.99]
            for i, limite in enumerate(limites_imc):
                if imc <= limite:
                    lbP_list[i].config(bg=cor[i])
                    break
            else:
                lbP_list[-1].config(bg=cor[-1])

        else:
            lbDivisao.config(text="Preencha os campos!")
    except ValueError:
        lbDivisao.config(text="Use apenas números e pontos/vírgulas!")

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Calculadora IMC 2025")
    janela.geometry("390x350+200+200")
    janela.resizable(False, False) # Evita deformar o layout
    
    default_bg = janela.cget('bg')

    # Atalho: apertar Enter também calcula
    janela.bind('<Return>', lambda event: calcular())

    lbP_list = []
    lbP_labels = [
        "Abaixo de 17 - Muito abaixo do peso ideal",
        "Entre 17 e 18,49 - Abaixo do peso ideal",
        "Entre 18,5 e 24,99 - Peso normal",
        "Entre 25 e 29,99 - Acima do peso",
        "Entre 30 e 34,99 - Obesidade (nível I)",
        "Entre 35 e 39,99 - Obesidade severa (nível II)",
        "Acima de 39,99 - Obesidade mórbida (nível III)"
    ]

    for i, text in enumerate(lbP_labels, start=1):
        lbP = tk.Label(janela, text=text, anchor="w", justify="left")
        lbP.place(x=50, y=160 + 20*i, width=300)
        lbP_list.append(lbP)

    tk.Label(janela, text="Peso (Kg): ").place(x=50, y=40)
    peso = tk.Entry(janela)
    peso.place(x=115, y=40, width=185)
    peso.focus_set()

    tk.Label(janela, text="Altura (m): ").place(x=50, y=70)
    altura = tk.Entry(janela)
    altura.place(x=115, y=70, width=185)

    btCalcular = tk.Button(janela, text="Calcular", width=10, command=calcular, cursor="hand2")
    btCalcular.place(x=115, y=110)

    btLimpar = tk.Button(janela, text="Limpar", width=10, command=reset_entries, cursor="hand2")
    btLimpar.place(x=213, y=110)

    lbDivisao = tk.Label(janela, text="", foreground="blue", font="Arial 10 bold")
    lbDivisao.place(x=50, y=150)

    janela.mainloop()
