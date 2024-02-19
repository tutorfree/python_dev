import tkinter as tk
import re

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

        # Validando a entrada para strings não vazias e convertendo para float
        if peso_val and altura_val:
            p = float(peso_val)
            a = float(altura_val)
            imc = float('%.2f' % (p / a**2))
            lbDivisao.config(text=str(imc).replace('.', ',', 1))
            
            for lbP in lbP_list:
                lbP.config(bg=default_bg)

            if imc <= 17:
                lbP_list[0].config(bg=cor[0])
            elif 17 < imc <= 18.49:
                lbP_list[1].config(bg=cor[1])
            elif 18.5 <= imc <= 24.99:
                lbP_list[2].config(bg=cor[2])
            elif 25 <= imc <= 29.99:
                lbP_list[3].config(bg=cor[3])
            elif 30 <= imc <= 34.99:
                lbP_list[4].config(bg=cor[4])
            elif 35 <= imc <= 39.99:
                lbP_list[5].config(bg=cor[5])
            else:
                lbP_list[6].config(bg=cor[6])
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
        lbP.place(x=50, y=180 + 20*i)
        lbP_list.append(lbP)

    lbPeso = tk.Label(janela, text="Peso: ")
    lbPeso.place(x=50, y=40)

    peso = tk.Entry(janela)
    peso.place(x=110, y=40, width=185)
    peso.focus_set()

    lbAltura = tk.Label(janela, text="Altura: ")
    lbAltura.place(x=50, y=70)

    altura = tk.Entry(janela)
    altura.place(x=110, y=70, width=185)

    btCalcular = tk.Button(janela, text="Calcular", width=7, command=calcular)
    btCalcular.place(x=110, y=110)

    btLimpar = tk.Button(janela, text="Limpar", width=7, command=reset_entries)
    btLimpar.place(x=213, y=110)

    lbDivisao = tk.Label(janela, text="", foreground="blue", font="-weight bold")
    lbDivisao.place(x=50, y=150)

    janela.geometry("390x340+200+200")
    janela.mainloop()
