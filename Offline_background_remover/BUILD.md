🛠️ BUILD.md (compilação do EXE)
# BUILD – Compilação do Removedor de Fundo (EXE Offline)

Este documento explica como **compilar o Removedor de Fundo em um executável (.exe)**  
que funcione **sem Python instalado e sem internet**.

Sistema testado: **Windows 10 / 11**

---

## ⚠️ Versão do Python

❌ Não use Python 3.12  
✅ Use **Python 3.11.x**

Download recomendado:  
https://www.python.org/downloads/release/python-3110/

Durante a instalação:
- Marque **Add Python to PATH**

Verifique:

```powershell
python --version

1️⃣ Criar ambiente virtual

Na pasta do projeto:

python -m venv venv
venv\Scripts\activate


O prompt deve mostrar:

(venv)

2️⃣ Instalar dependências (ordem obrigatória)
pip install numpy==1.26.4
pip install opencv-python-headless
pip install rembg

3️⃣ Testar o rembg

Crie o arquivo teste_rembg.py:

from rembg import remove
print("rembg carregou com sucesso")


Execute:

python teste_rembg.py


Resultado esperado:

rembg carregou com sucesso

4️⃣ Ajuste obrigatório para aplicações GUI (Tkinter)

No topo do arquivo removedor_fundo.py, antes de qualquer outro import:

import sys
import os

if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")


⚠️ Sem isso, o executável fecha sozinho ao rodar.

5️⃣ Testar o aplicativo no Python
python removedor_fundo.py


✔ Interface abre
✔ Remove fundo corretamente

Somente continue se funcionar perfeitamente.

6️⃣ Instalar PyInstaller
pip install pyinstaller

7️⃣ Gerar o executável
pyinstaller --onefile --windowed removedor_fundo.py


O EXE final será criado em:

dist/removedor_fundo.exe

8️⃣ Testar como usuário final

Feche o terminal

Vá até a pasta dist

Dê duplo clique no EXE

Se funcionar sem Python instalado, a compilação foi bem-sucedida 🎉

❗ Problemas comuns
NumPy 2.x / _ARRAY_API not found

Use apenas:

pip install numpy==1.26.4

EXE abre e fecha sozinho

Verifique se o redirecionamento de stdout e stderr foi aplicado.

Erro cv2 não encontrado

Instale:

pip install opencv-python-headless

📦 Observações finais

O EXE pode ter entre 80 e 150 MB

Antivírus podem acusar falso positivo

Ideal para distribuição via ZIP ou pendrive
