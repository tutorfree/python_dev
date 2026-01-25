# 🗳️ Urna Eletrônica Multiplataforma
<img width="852" height="602" alt="Urna Eletrônica - Multiplataforma" src="https://github.com/user-attachments/assets/cd1218b5-17b2-4566-890a-4e5db94c6156" />

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![Pillow](https://img.shields.io/badge/Images-Pillow-lightblue)
![Multiplatform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Audio](https://img.shields.io/badge/Audio-Multiplatform-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Uma urna eletrônica completa desenvolvida em Python com suporte total para Windows, Linux e macOS.

## ✨ Funcionalidades Principais

### 🗳️ Sistema de Votação
- Teclado numérico completo (0-9)
- Confirmação de voto com feedback visual
- Correção de voto antes da confirmação
- Visualização do candidato em tempo real

### 👥 Gerenciamento de Candidatos
- **Adição dinâmica** de novos candidatos
- **Remoção** de candidatos existentes
- Upload de fotos dos candidatos
- Validação de dados (número de 2 dígitos)

### 📊 Resultados e Relatórios
- Placar em tempo real com porcentagens
- Barras de progresso visuais
- Exportação de resultados para arquivo TXT
- Interface de resultados com scroll

### 🔊 Sistema de Áudio Multiplataforma
- **Windows**: usa `winsound` nativo
- **macOS**: usa `afplay` nativo  
- **Linux**: suporta múltiplos players (`aplay`, `paplay`, `mpg123`, `vlc`)
- Fallback silencioso se áudio não disponível

## 🚀 Como Executar

### 1. Pré-requisitos

```bash
# Instale o Pillow para manipulação de imagens
pip install pillow
```

### 2. Estrutura de Pastas

```text
urna_eletronica/
├── urna.py              # Código principal
├── README.md            # Documentação
├── sons/                # Sons da urna (opcional)
│   ├── tecla.wav
│   ├── confirma.wav
│   └── erro.wav
└── fotos/               # Fotos dos candidatos
    ├── 11.png
    ├── 12.png
    └── ...
```

### 3. Executar a Aplicação
```bash
python urna.py
```

## 🎮 Como Usar

Para Votar:

    Digite o número do candidato (2 dígitos)
    Confirme as informações na tela
    Pressione CONFIRMA para registrar
    Use CORRIGE para apagar e recomeçar

Para Adicionar Candidato:

    Clique em "ADICIONAR CANDIDATO"
    Digite número (2 dígitos) e nome
    Selecione uma foto
    Clique em "SALVAR CANDIDATO"

Para Ver Resultados:

    Clique em "PLACAR"
    Veja votos e porcentagens
    Use "EXPORTAR RESULTADOS" para salvar
