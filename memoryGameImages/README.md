# 🎮 Jogo da Memória com Imagens

<img width="802" height="782" alt="memoryGameImages" src="https://github.com/user-attachments/assets/eb3618a3-002e-4c75-bd7e-917441c51626" />

Um divertido e envolvente Jogo da Memória desenvolvido em Python, com interface gráfica moderna e suporte a áudio. Teste sua memória encontrando os pares de imagens!

## ✨ Funcionalidades

- **Interface Gráfica Intuitiva:** Desenvolvido com `tkinter` para uma experiência de usuário agradável.
- **Jogabilidade Clássica:** Encontre pares de imagens escondidas para vencer.
- **Suporte a Áudio:** Efeitos sonoros para interações e trilha sonora de fundo, utilizando `pygame`.
- **Controle de Volume:** Opção para silenciar/ativar o áudio durante o jogo.
- **Sistema de Pontuação:** Acompanhe seus pares encontrados, tentativas e pontuação total.
- **Temporizador:** Monitore o tempo gasto para completar o jogo.
- **Configuração Flexível de Imagens:** Suporte para adicionar suas próprias imagens (6 pares).
- **Feedback Visual:** Indicações claras de acertos e erros.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter:** Para a construção da interface gráfica.
- **Pillow (PIL):** Para manipulação e carregamento de imagens.
- **Pygame:** Para gerenciamento e reprodução de áudio.
- **Módulo `random`:** Para embaralhar as cartas do jogo.

## 🚀 Instalação

Para rodar este jogo em sua máquina, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/tutorfree/python_dev
    cd memoryGameImages
    ```

2.  **Instale as dependências:**
    ```bash
    pip install Pillow pygame
    ```

3.  **Prepare as imagens:**
    Crie uma pasta chamada `images` na raiz do projeto. Dentro dela, coloque 6 imagens diferentes para as cartas (ex: `carta01.png`, `carta02.png`, ..., `carta06.png`). Opcionalmente, você pode adicionar uma imagem `back.png` para o verso das cartas.

4.  **Prepare os arquivos de áudio (opcional):**
    Crie uma pasta chamada `sound` na raiz do projeto e adicione um arquivo de música `trilha.mp3` ou `trilha.wav` para a trilha sonora de fundo. Você também pode adicionar outros arquivos de áudio para efeitos sonoros, se desejar.

5.  **Execute o jogo:**
    ```bash
    python memoryGameImages.py
    ```

## 🤝 Como Contribuir

Contribuições são bem-vindas! Se você tiver sugestões de melhoria, encontrar bugs ou quiser adicionar novas funcionalidades, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## 📄 Licença

Este projeto está licenciado sob a [Creative Commons Atribuição-NãoComercial 4.0 Internacional (CC BY-NC 4.0)](http://creativecommons.org/licenses/by-nc/4.0/).
