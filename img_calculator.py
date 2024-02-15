from tkinter import Tk, Entry, Label, Button


def reset_entries():
    peso.delete(0, 'end')
    altura.delete(0, 'end')
    lbDivisao["text"] = ""
    defaultbg = janela.cget('bg')

    # Lista de lbP
    lbP_list = [lbP1, lbP2, lbP3, lbP4, lbP5, lbP6, lbP7]

    # Configuração de fundo para todos os lbP
    for lbP in lbP_list:
        lbP.configure(bg=defaultbg)


def calcular():
    try:
        cor = ['Aquamarine', 'MediumAquamarine', 'LightGreen', 'yellow', 'salmon', 'Tomato', 'red']

        if Entry.get(peso).replace(',', '', 1).isdigit() and Entry.get(altura).replace(',', '', 1).isdigit():
            p = float(Entry.get(peso).replace(',', '.', 1))
            a = float(Entry.get(altura).replace(',', '.', 1))
            imc = float('%.2f' % (p / a**2))

            lbDivisao["text"] = str(imc).replace('.', ',', 1)

            for i in range(7):
                lbP = globals()[f"lbP{i+1}"]
                lbP.configure(bg=janela.cget('bg'))

            if imc <= 17:
                lbP1.configure(bg=cor[0])
            elif 17 < imc <= 18.49:
                lbP2.configure(bg=cor[1])
            elif 18.5 <= imc <= 24.99:
                lbP3.configure(bg=cor[2])
            elif 25 <= imc <= 29.99:
                lbP4.configure(bg=cor[3])
            elif 30 <= imc <= 34.99:
                lbP5.configure(bg=cor[4])
            elif 35 <= imc <= 39.99:
                lbP6.configure(bg=cor[5])
            else:
                lbP7.configure(bg=cor[6])

        else:
            lbDivisao["text"] = "Campo(s) Vazio(s) ou fora do padrão!"
    except ValueError:
        lbDivisao["text"] = "Campo(s) Vazio(s) ou fora do padrão!"


if __name__ == "__main__":
    janela = Tk()
    janela.title("IMC Calculator")

    lbPeso = Label(janela, text="Peso: ")
    lbPeso.place(x=50, y=40)

    lbAltura = Label(janela, text="Altura: ")
    lbAltura.place(x=50, y=70)

    peso = Entry(janela)
    peso.place(x=110, y=40, width=185)
    peso.focus_set()

    altura = Entry(janela)
    altura.place(x=110, y=70, width=185)

    btCalcular = Button(janela, text="Calcular", width=7, command=calcular)
    btCalcular.place(x=110, y=110)

    btLimpar = Button(janela, text="Limpar", width=7, command=reset_entries)
    btLimpar.place(x=213, y=110)

    lbDivisao = Label(janela, text="", foreground="blue", font="-weight bold")
    lbDivisao.place(x=50, y=150)

    lbP1 = Label(janela, text="Abaixo de 17 - Muito abaixo do peso ideal")
    lbP1.place(x=50, y=180)

    lbP2 = Label(janela, text="Entre 17 e 18,49 - Abaixo do peso ideal")
    lbP2.place(x=50, y=200)

    lbP3 = Label(janela, text="Entre 18,5 e 24,99 - Peso normal")
    lbP3.place(x=50, y=220)

    lbP4 = Label(janela, text="Entre 25 e 29,99 - Acima do peso")
    lbP4.place(x=50, y=240)

    lbP5 = Label(janela, text="Entre 30 e 34,99 - Obesidade (nível I)")
    lbP5.place(x=50, y=260)

    lbP6 = Label(janela, text="Entre 35 e 39,99 - Obesidade severa (nível II)")
    lbP6.place(x=50, y=280)

    lbP7 = Label(janela, text="Acima de 39,99 - Obesidade mórbida (nível III)")
    lbP7.place(x=50, y=300)

    janela.geometry("390x340+200+200")
    janela.mainloop()
