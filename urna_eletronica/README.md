# 🗳️ Urna Eletrônica em Python
<img width="822" height="532" alt="urna" src="https://github.com/user-attachments/assets/83313b0a-677e-403e-9768-77b1f045759e" />

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![Pillow](https://img.shields.io/badge/Images-Pillow-lightblue)
![Status](https://img.shields.io/badge/Status-Em_desenvolvimento-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

Uma urna eletrônica simulada desenvolvida em Python com interface gráfica usando Tkinter. Este projeto permite simular eleições com cadastro dinâmico de candidatos, sistema de votação e visualização de resultados em tempo real.
✨ Funcionalidades

    ✅ Sistema de votação completo com teclado numérico

    ✅ Cadastro dinâmico de candidatos (adicionar/remover)

    ✅ Placar em tempo real com porcentagens

    ✅ Efeitos sonoros para feedback ao usuário

    ✅ Interface intuitiva com fotos dos candidatos

    ✅ Persistência de imagens dos candidatos

    ✅ Validação de dados e tratamento de erros

## 🖼️ Capturas de Tela

Interface Principal

```text

[ Número: __ ]
[ Nome:      ]
[ Foto do candidato ]

[ 1 ][ 2 ][ 3 ][ BRANCO ]
[ 4 ][ 5 ][ 6 ][ CORRIGE ]
[ 7 ][ 8 ][ 9 ][ CONFIRMA ]
[   0   ][   PLACAR   ]
```

## Placar de Resultados

```text
PLACAR ATUAL

[Foto] Enzo      Votos: 15    25.0%
[Foto] José      Votos: 12    20.0%
...etc
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

## Passos para instalação

### Clone ou baixe o projeto

```bash
git clone https://github.com/tutorfree/python_dev/new/main/urna_eletronica.git
cd urna-eletronica
```

### Instale as dependências

```bash
pip install pillow
```

### Estruture as pastas necessárias

```bash
mkdir sons fotos
```

### Adicione os sons (opcional)

✅ Coloque os arquivos de som na pasta sons/:

    tecla.wav - som ao pressionar teclas numéricas
    confirma.wav - som ao confirmar voto
    erro.wav - som ao corrigir ou erro

✅ Adicione fotos dos candidatos (opcional):
    Coloque imagens PNG (160x200px recomendado) na pasta fotos/ com os nomes:

    11.png, 12.png, 22.png, etc.

## 🎮 Como Usar

### 1. Iniciar o Programa
```bash
python urna.py
```

### 2. Votar

    - Digite o número do candidato (2 dígitos);
    - Visualize as informações do candidato na tela;
    - Pressione "CONFIRMA" para registrar o voto;
    - Use "CORRIGE" para reiniciar a digitação.

### 3. Gerenciar Candidatos

    - Adicionar Candidato: Clique no botão roxo
    - Insira número (2 dígitos)
    -  Digite o nome
    - Selecione uma foto

### Remover Candidato: Clique no botão vermelho

    - Selecione da lista
    - Confirme a remoção

### 4. Ver Resultados

    Clique no botão "PLACAR" para ver:

    - Quantidade de votos por candidato
    - Percentual de cada um
    - Foto e nome dos candidatos

## 📁 Estrutura do Projeto

```text
urna-eletronica/
│
├── urna.py              # Código principal
├── README.md            # Este arquivo
│
├── sons/                # Sons do sistema
│   ├── tecla.wav
│   ├── confirma.wav
│   └── erro.wav
│
└── fotos/               # Fotos dos candidatos
    ├── 11.png
    ├── 12.png
    ├── 22.png
    └── ...
```

## ⚙️ Configuração

O sistema vem com 6 candidatos pré-cadastrados:

    11 - Enzo
    12 - José
    22 - Chicão
    33 - Zefinha
    34 - Maria
    66 - Onerildo

## Personalização

Existe uma função para adicionar candidatos no modo gráfico.
}

## 🛠️ Tecnologias Utilizadas

  - [x] Python 3.7+: Linguagem principal
  - [x] Tkinter: Framework para interface gráfica
  - [x] Pillow (PIL): Manipulação de imagens
  - [x] winsound (Windows) / playsound (multiplataforma): Reprodutor de áudio

## 📝 Notas Importantes

# Sistema Operacional

Windows: Suporte completo a sons

Linux/macOS: Sons podem não funcionar (modifique a função tocar_som)

```python
    # Alternativa multiplataforma
    def tocar_som(arq):
        if os.name == 'nt':  # Windows
            winsound.PlaySound(arq, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:  # Linux/macOS
            os.system(f"aplay {arq} 2>/dev/null || afplay {arq} 2>/dev/null")
```

## Formatos de Imagem

- Use PNG para transparência
- Tamanho recomendado: 160x200 pixels
- Nomeie as fotos como [número].png

## 🐛 Solução de Problemas

Problema:
"ModuleNotFoundError: No module named 'PIL'"

Execute: pip install pillow

Sons não funcionam no Linux/macOS:
Modifique a função tocar_som

Fotos não aparecem: Verifique se estão na pasta fotos/

Interface muito grande/pequena:	Ajuste a resolução em root.geometry()

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Agradecimentos

- À comunidade Python por Tkinter
- Aos desenvolvedores do Pillow (PIL Fork)
- A todos que testaram e deram feedback

Desenvolvido com ❤️ para fins educacionais

Nota: Este é um projeto de simulação. Para eleições oficiais, use sistemas certificados pelo TSE.
