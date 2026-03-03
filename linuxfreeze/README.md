# LinuxFreeze (OverlayFS Edition)
<img width="720" height="603" alt="2026-03-02 22_03_54-Clone de Debian13b  Executando  - Oracle VirtualBox" src="https://github.com/user-attachments/assets/a63baba5-49e0-4012-aaa1-0b63f870469f" />

🧊 **Sistema de congelamento de estado para Linux usando OverlayFS**

O LinuxFreeze é um utilitário experimental escrito em Python que utiliza OverlayFS para criar um sistema de arquivos temporário sobre o sistema real, permitindo que alterações feitas durante o uso da máquina sejam descartadas automaticamente após reboot.

---

## 🎯 Para que serve?

Ele foi pensado para ambientes como:

- 🖥️ Laboratórios de informática
- 🎓 Ambientes educacionais
- 🌐 Cybercafés / lan houses
- 📚 Máquinas públicas ou compartilhadas
  
**A ideia central é simples:**  
O usuário pode usar a máquina livremente, mas nada persiste.

---

## ⚙️ Como funciona (em alto nível)

O sistema utiliza **OverlayFS**, combinando:

- `lowerdir` → sistema real (imutável)
- `upperdir` → camada temporária (RAM ou disco)
- `workdir` → diretório auxiliar do OverlayFS

### Durante a sessão:

- Alterações vão apenas para a camada `upper`
- O sistema real não é modificado

### Após reboot:

- A camada temporária é descartada
- O sistema volta ao estado original

**Nenhum `rsync`. Nenhuma cópia massiva de `/home`. Nenhuma lentidão desnecessária.**

---

## 🔐 Privilégios e Segurança

- O LinuxFreeze **precisa ser executado como root**
- Isso é **intencional** e não é um bug
- OverlayFS, montagem e integração com systemd exigem privilégios administrativos

### O aplicativo não tenta "enganar" o sistema:

- Se não for root, ele não inicia
- Não cria arquivos silenciosamente em locais protegidos

---

## 📁 Estrutura Geral

Exemplo conceitual:

```
/overlay
 ├── upper/
 ├── work/
 └── merged/
```
---

## Estado do Projeto

- ✅ **Funcional**
- ✅ **Experimental**
- ✅ **Educacional**

### Testado em:

- Sistemas Linux modernos
- Ambientes com systemd
- Cenários de uso compartilhado

---

## 📌 Avisos Importantes

⚠️ **Qualquer erro de configuração em OverlayFS pode impedir o boot**

- Teste sempre em máquina virtual antes
- Leia o código antes de usar em produção
- Use por sua conta e risco

---

## 🧭 Consideração Final

> *"Sistemas previsíveis libertam o usuário. Sistemas frágeis o aprisionam."*

Esse projeto é sobre **previsibilidade**, não controle.

---

## 📄 Licença

*Este programa é free para uso*
