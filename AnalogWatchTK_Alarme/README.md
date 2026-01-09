🕰️ Relógio Analógico Temático com Alarmes
<img width="685" height="495" alt="2026-01-09 00_16_41-" src="https://github.com/user-attachments/assets/89ba92d8-56d2-4fcb-9983-412e78370577" />

https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Tkinter-GUI-orange
https://img.shields.io/badge/License-MIT-green
https://img.shields.io/badge/Platform-Windows%2520%257C%2520Linux%2520%257C%2520macOS-lightgrey

Um relógio analógico elegante e altamente personalizável para desktop com sistema completo de alarmes, temas visualmente atraentes e funcionalidades avançadas.
✨ Características Principais
🎨 Temas Visuais

    9 temas diferentes (Darkly, Flatly, Superhero, Cyborg, Vapor, Minty, Solar, Luxa, Morph)

    Interface moderna e minimalista

    Cores harmoniosas e contrastantes

⚙️ Personalização Total

    6 tamanhos disponíveis (150px a 400px)

    Controle de transparência (70% a 100%)

    Sempre no topo (opcional)

    Posicionamento livre na tela

⏰ Sistema de Alarmes Avançado

    Criação de múltiplos alarmes

    Descrições personalizadas

    Ativação/desativação individual

    Reposicionamento de janelas de alerta

    Adiar (snooze) por 5 minutos

    Persistência automática dos alarmes

🖱️ Interação Intuitiva

    Arraste para mover o relógio e janelas

    Menu de contexto com todas as opções

    Cursor indicativo em áreas arrastáveis

    Janelas modais arrastáveis

🚀 Instalação
Pré-requisitos

    Python 3.8 ou superior

    pip (gerenciador de pacotes Python)

Passo a Passo

    Clone o repositório:

bash

git clone https://github.com/seu-usuario/relogio-analogico.git
cd relogio-analogico

    Instale as dependências:

bash

pip install plyer

    Execute o aplicativo:

bash

python relogio_analogico.py

📖 Como Usar
🎮 Controles Básicos

    Clique esquerdo e arraste: Move o relógio

    Clique direito: Abre menu de contexto

    Botão direito em janelas de alarme: Menu de opções extras

⏰ Configurando Alarmes

    Clique direito no relógio

    Selecione "Alarmes" → "Adicionar Alarme"

    Defina hora, minuto e descrição (opcional)

    Clique em "Adicionar"

🎨 Personalizando o Relógio

    Mudar tema: Menu → Temas → Escolha um tema

    Alterar tamanho: Menu → Tamanho → Selecione o tamanho

    Ajustar transparência: Menu → Transparência → Escolha nível

    Fixar no topo: Menu → "Fixar no Topo"

🔔 Gerenciando Alarmes

    Ver alarmes existentes: Menu → Alarmes → "Ver Alarmes"

    Ativar/desativar: Clique na checkbox

    Remover alarme: Clique no botão ✗

    Limpar todos: Menu → Alarmes → "Limpar Todos Alarmes"

🗂️ Estrutura de Arquivos
text

relogio-analogico/
│
├── relogio_analogico.py      # Código principal
├── clock_settings.json       # Configurações do relógio (gerado automaticamente)
├── alarms.json              # Lista de alarmes (gerado automaticamente)
├── alarm_positions.json     # Posições dos alarmes (gerado automaticamente)
│
├── README.md                # Este arquivo
└── screenshots/             # Capturas de tela (opcional)

🛠️ Tecnologias Utilizadas

    Python 3.8+ - Linguagem principal

    Tkinter - Interface gráfica

    Plyer - Notificações do sistema (opcional)

    JSON - Armazenamento de configurações

    Threading - Verificação de alarmes em segundo plano

📱 Compatibilidade

    ✅ Windows 10/11

    ✅ Linux (distribuições com suporte a Tkinter)

    ✅ macOS (com suporte a X11)

🎯 Funcionalidades Técnicas
Sistema de Alarmes

    Verificação em tempo real (thread separada)

    Janelas de alerta personalizáveis

    Posições salvas individualmente por alarme

    Efeito visual de piscar para atenção

Persistência de Dados

    Configurações salvas automaticamente

    Alarmes mantidos entre sessões

    Posições das janelas preservadas

    Backup automático em arquivos JSON

Interface do Usuário

    Design responsivo e adaptável

    Feedback visual imediato

    Instruções contextuais

    Ícones e cores intuitivas

🐛 Solução de Problemas
Problemas Comuns

    "Plyer não encontrado"
    bash

pip install --upgrade plyer

    Janela não se move

        Certifique-se de clicar na área correta (barra de título ou área indicada)

    Alarmes não tocam

        Verifique se o alarme está ativado (checkbox marcado)
        Confira a hora do sistema

    Interface gráfica não aparece

        Instale Tkinter: sudo apt-get install python3-tk (Linux)

        Ou reinstale Python com Tkinter habilitado

Logs e Debug

O aplicativo gera logs no terminal para ajudar no diagnóstico:

    Carregamento de configurações;
    Alarmes carregados/salvos;
    Erros de execução;
🔧 Personalização Avançada.

Adicionando Novos Temas

Edite a função get_theme_colors() para adicionar novos esquemas de cores:

"novo_tema": {
    'bg': '#COR_FUNDO',
    'face': '#COR_MOSTRADOR',
    'border': '#COR_BORDA',
    'hour_hand': '#COR_PONTEIRO_HORA',
    'minute_hand': '#COR_PONTEIRO_MINUTO',
    'second_hand': '#COR_PONTEIRO_SEGUNDO',
    'hour_mark': '#COR_MARCAÇÃO',
    'center': '#COR_CENTRO',
    'text': '#COR_TEXTO'
}

Modificando Tamanhos Disponíveis

Altere a lista available_sizes na linha 23:

self.available_sizes = [150, 200, 250, 300, 350, 400, 450, 500]

🤝 Contribuindo

Contribuições são bem-vindas! Siga estes passos:

    Faça um Fork do projeto
    Crie uma Branch para sua feature (git checkout -b feature/AmazingFeature)
    Commit suas mudanças (git commit -m 'Add some AmazingFeature')
    Push para a Branch (git push origin feature/AmazingFeature)
    Abra um Pull Request

Áreas para Contribuição

    Novos temas visuais;
    Funcionalidades de alarmes (padrões de repetição, etc.);
    Integração com calendários;
    Suporte a múltiplos idiomas;
    Melhorias de performance;

📄 Licença

Distribuído sob licença MIT. Veja LICENSE para mais informações.
👏 Créditos

    Autor: Antoine Paul
    Inspiração: Relógios analógicos clássicos com toque moderno
    Agradecimentos: Comunidade Python e Tkinter

🌟 Estrelas no GitHub

Se você gostou deste projeto, por favor dê uma estrela no GitHub! ⭐
Feito com ❤️ e Python
Um relógio não é apenas para ver as horas, é para lembrar que cada momento é único. 🕰️✨
