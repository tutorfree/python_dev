import tkinter as tk

def reset_entries():
    peso.delete(0, 'end')
    altura.delete(0, 'end')
    lbDivisao.config(text="")
    for lbP in lbP_list:
        lbP.config(bg=default_bg)


def calcular():
    try:
        cor = ['Aquamarine', 'MediumAquamarine', 'LightGreen', 'yellow', 'salmon', 'Tomato', 'red']
        peso_val = peso.get().replace(',', '.', 1)
        altura_val = altura.get().replace(',', '.', 1)

        if peso_val and altura_val:
            p = float(peso_val)
            a = float(altura_val)
            imc = float('%.2f' % (p / a**2))
            lbDivisao.config(text=str(imc).replace('.', ',', 1))

            for lbP in lbP_list:
                lbP.config(bg=default_bg)

            limites_imc = [17, 18.49, 24.99, 29.99, 34.99, 39.99]
            for i, limite in enumerate(limites_imc):
                if imc <= limite:
                    lbP_list[i].config(bg=cor[i])
                    break
            else:
                lbP_list[-1].config(bg=cor[-1])  # Caso o IMC seja maior que o último limite

        else:
            lbDivisao.config(text="Campo(s) Vazio(s) ou fora do padrão!")
    except ValueError:
        lbDivisao.config(text="Campo(s) Vazio(s) ou fora do padrão!")


if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("IMC Calculator")
    default_bg = janela.cget('bg')

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
        lbP = tk.Label(janela, text=text)
        lbP.place(x=50, y=160 + 20*i)
        lbP_list.append(lbP)

    lbPeso = tk.Label(janela, text="Peso (Kg): ")
    lbPeso.place(x=50, y=40)

    peso = tk.Entry(janela)
    peso.place(x=115, y=40, width=185)
    peso.focus_set()

    lbAltura = tk.Label(janela, text="Altura (m): ")
    lbAltura.place(x=50, y=70)

    altura = tk.Entry(janela)
    altura.place(x=115, y=70, width=185)

    btCalcular = tk.Button(janela, text="Calcular", width=10, command=calcular)
    btCalcular.place(x=115, y=110)

    btLimpar = tk.Button(janela, text="Limpar", width=10, command=reset_entries)
    btLimpar.place(x=213, y=110)

    lbDivisao = tk.Label(janela, text="", foreground="blue", font="-weight bold")
    lbDivisao.place(x=50, y=150)

    janela.geometry("390x350+200+200")
    janela.mainloop()
