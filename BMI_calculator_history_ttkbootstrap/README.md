# Calculadora de IMC Avançada

<img width="1421" height="692" alt="BMI_calculator" src="https://github.com/user-attachments/assets/caf3b200-6c07-4f26-b43a-4ef419db0d77" />

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Tkinter](https://img.shields.io/badge/Tkinter-GUI-lightgrey.svg) ![ttkbootstrap](https://img.shields.io/badge/ttkbootstrap-Modern%20GUI-purple.svg) ![Matplotlib](https://img.shields.io/badge/Matplotlib-Plotting-orange.svg)

## 📝 Descrição

Este projeto apresenta uma **Calculadora de Índice de Massa Corporal (IMC) avançada**, desenvolvida em Python. A aplicação utiliza a biblioteca `tkinter` para a interface gráfica, aprimorada com `ttkbootstrap` para um visual moderno e responsivo. Além do cálculo básico do IMC, o aplicativo oferece funcionalidades robustas como o registro de histórico, análise estatística e visualização gráfica da evolução do IMC ao longo do tempo.

## ✨ Funcionalidades

*   **Cálculo Preciso de IMC:** Insira peso (kg) e altura (m) para obter seu IMC com duas casas decimais.
*   **Classificação Visual:** O IMC calculado é categorizado em faixas (ex: "Peso normal", "Obesidade Grau I"), com destaque visual por cores para fácil interpretação.
*   **Histórico Detalhado:** Todas as medições são salvas automaticamente em um arquivo `historico_imc.json`. O histórico pode ser consultado em uma janela dedicada, com tabela paginada e pesquisável.
*   **Estatísticas Abrangentes:** Visualize estatísticas como a última medição, média do IMC, variação de peso e o total de registros.
*   **Gráficos Interativos:** Acompanhe a evolução do seu IMC com gráficos de linha ou barra, gerados com `matplotlib`, que incluem áreas de referência para as faixas de peso normal.
*   **Exportação de Dados:** Exporte seu histórico completo para um arquivo JSON, facilitando o backup e a análise externa.
*   **Limpeza de Histórico:** Opção segura para limpar todos os registros do histórico.

## 🚀 Tecnologias Utilizadas

*   **Python 3.x**
*   **`tkinter`:** Biblioteca padrão para GUI.
*   **`ttkbootstrap`:** Temas e widgets modernos para `tkinter`.
*   **`json`:** Para persistência de dados do histórico.
*   **`os`:** Operações de sistema de arquivos.
*   **`datetime`:** Manipulação de datas e horas.
*   **`matplotlib`:** Geração de gráficos.

## ⚙️ Instalação

Para executar este aplicativo, você precisará ter o Python 3.x instalado em seu sistema. Siga os passos abaixo:

1.  **Clone o repositório (ou baixe o código-fonte):**
    ```bash
    git clone github.com/tutorfree/python_dev
    cd BMI_calculator_history_ttkbootstrap
    ```

2.  **Instale as dependências:**
    ```bash
    pip install ttkbootstrap matplotlib
    ```

## ▶️ Como Usar

1.  **Execute o aplicativo:**
    ```bash
    python BMI_calculator_history_ttkbootstrap.py
    ```

2.  **Calcule seu IMC:** Insira seu peso (em quilogramas) e altura (em metros) nos campos designados na janela principal e clique em "🧮 Calcular" ou pressione `Enter`.

3.  **Acesse o Histórico:** Clique no botão "📊 Histórico" para abrir a janela de histórico, onde você pode visualizar seus registros, estatísticas e gráficos.

4.  **Limpar Entradas:** Use o botão "🗑️ Limpar" na janela principal para resetar os campos de peso e altura.

5.  **Gerenciar Histórico:** Na janela de histórico, você pode "📊 Ver Gráfico", "📤 Exportar JSON" ou "🗑️ Limpar Histórico".


## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
