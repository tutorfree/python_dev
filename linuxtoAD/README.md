# 🖥️ Linux AD Integrator
<img width="828" height="769" alt="linuxtoAD-02" src="https://github.com/user-attachments/assets/82560314-4312-4aeb-92e7-613ff29ac26c" />

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Debian%20%7C%20Ubuntu%20%7C%20Fedora%20%7C%20RHEL-orange)](https://github.com/tutorfree/python_dev)
[![AD](https://img.shields.io/badge/Active%20Directory-Integrated-blue)](https://github.com/tutorfree/python_dev)

> **Assistente gráfico para integração de estações Linux com Active Directory**

Uma ferramenta intuitiva estilo wizard que simplifica a integração de máquinas Linux com domínios Active Directory, oferecendo uma experiência similar ao PowerBroker Identity Services.

---

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Arquitetura](#-arquitetura)
- [Configuração](#-configuração)
- [Troubleshooting](#-troubleshooting)
- [Licença](#-licença)

---

## ✨ Funcionalidades

### 🎯 Principais Recursos

| Recurso | Descrição |
|---------|-----------|
| 🔐 **Join Automatizado** | Integração completa com domínio AD usando `realm` |
| 👤 **Login Curto** | Usuários podem logar apenas com nome de usuário (sem `DOMINIO\`) |
| 📁 **Pastas em Português** | Cria automaticamente estrutura de pastas localizadas |
| 🔧 **Sudo via AD** | Configura sudoers para integração com grupos AD |
| 🏢 **OU Específica** | Permite escolher a OU onde o computador será inserido |
| 🔄 **Rollback Automático** | Em caso de falha, reverte todas as alterações |
| 📝 **Logs Detalhados** | Registro completo de todas as operações |

### 🛡️ Segurança

- ✅ Validação de inputs com regex anti-injeção
- ✅ Sanitização de comandos shell com `shlex.quote()`
- ✅ Senha transmitida via stdin (não visível em processos)
- ✅ Backup automático de arquivos de configuração
- ✅ Verificação de pré-requisitos antes da execução

### 🖥️ Interface

- Interface gráfica intuitiva estilo wizard
- Teste de conectividade integrado (DNS, LDAP, Kerberos)
- Log técnico em tempo real durante a configuração
- Detecção automática de gerenciador de pacotes

---

### Tela de Boas-vindas
```
┌──────────────────────────────────────────────────────────────┐
│        Assistente de Ingresso no Active Directory            │
│                                                              │
│                         🖥️ 🔐                                │
│                                                              │
│  Este assistente configura o Linux para integração com o     │
│  Active Directory:                                           │
│                                                              │
│  • Login curto (recomendado)                                 │
│  • Pastas de usuário persistentes em português               │
│  • Sudo controlado pelo AD                                   │
│  • Escolha de OU específica (opcional)                       │
│                                                              │
│  ✔ Executando com privilégios de administrador              │
│                                                              │
│                                    [ Avançar → ]             │
└──────────────────────────────────────────────────────────────┘
```

### Tela de Credenciais
```
┌──────────────────────────────────────────────────────────────┐
│              Active Directory Membership                     │
│                                                              │
│  Domain:           [maua.sp.gov.br        ] ex: dominio.com  │
│                                                              │
│  User names are usually prefixed with the domain             │
│                                                              │
│  Usuário admin AD: [suporte.ti           ] ex: admin.user    │
│  Senha:            [••••••••••            ]                  │
│                                                              │
│  ┌─ User names prefix ─────────────────────────────────────┐ │
│  │ ☐ Enable default user name prefix (ex: MAUA\)           │ │
│  │   Login esperado: joao.silva → pasta: /home/joao.silva  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─ Organizational Unit ───────────────────────────────────┐ │
│  │ ⦿ Default (Computers ou OU previamente configurada)     │ │
│  │ ○ Specific OU path: [                              ]   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  [🔍 Testar Conectividade]    [← Voltar] [Configurar →]      │
└──────────────────────────────────────────────────────────────┘
```

### Tela de Progresso
```
┌──────────────────────────────────────────────────────────────┐
│         Configurando integração com Active Directory...      │
│                                                              │
│  ████████████████████████████████████████████                │
│                                                              │
│  3/8 Configurando SSSD (login curto + sudo AD)...            │
│                                                              │
│  ┌─ Log técnico ───────────────────────────────────────────┐ │
│  │ [INFO] Instalando pacotes: realmd, sssd, adcli...       │ │
│  │ [INFO] realm join --user=suporte.ti maua.sp.gov.br      │ │
│  │ [INFO] SSSD configurado com sucesso                     │ │
│  │ [DEBUG] Backup: /var/backups/ad-join/sssd.conf.bak-...  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  [ Cancelar ]                                                │
└──────────────────────────────────────────────────────────────┘
```
---

## ⚙️ Pré-requisitos

### Sistema Operacional

| Distribuição | Suporte | Gerenciador |
|--------------|---------|-------------|
| Debian 10+ | ✅ Total | APT |
| Ubuntu 18.04+ | ✅ Total | APT |
| Fedora 30+ | ✅ Total | DNF |
| RHEL/CentOS 7+ | ✅ Total | YUM/DNF |
| openSUSE Leap | ✅ Total | Zypper |

### Requisitos de Rede

- ✅ DNS configurado para resolver o domínio AD
- ✅ Porta 389 (LDAP) acessível
- ✅ Porta 88 (Kerberos) acessível
- ✅ Relógio sincronizado (NTP)

### Requisitos de Sistema

- Python 3.8 ou superior
- Privilégios de root (sudo)
- Ambiente gráfico (X11 ou Wayland)
- Conexão com a internet (para instalação de pacotes)

---

## 🚀 Uso

### Execução Básica

```bash
sudo python3 linuxtoAD.py
```

### Fluxo de Uso

1. **Tela de Boas-vindas**: Revise as funcionalidades e clique em "Avançar"

2. **Credenciais**:
   - Informe o domínio (ex: `empresa.com.br`)
   - Informe usuário com permissão de join no AD
   - Informe a senha
   - Configure opções de login e OU (opcional)
   - Clique em "Testar Conectividade" para validar

3. **Progresso**: Acompanhe a execução em tempo real

4. **Conclusão**: Teste o login e reinicie a máquina

### Exemplo de Teste Pós-Configuração

```bash
# Verifica se está no domínio
realm list

# Testa resolução de usuário AD
id joao.silva

# Testa login (em outro terminal)
```

### License

[License Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/)
