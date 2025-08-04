import subprocess
import sys
import os

# Executa a indexação
print('Iniciando indexação dos dados...')
ret = subprocess.run([sys.executable, os.path.join('codificacao', 'indexar_tudo.py')])
if ret.returncode != 0:
    print('Erro na indexação. Abortando.')
    sys.exit(1)

# Executa a interface adaptativa
print('Iniciando interface adaptativa...')
subprocess.run([sys.executable, os.path.join('codificacao', 'prompt_adaptativo_gui.py')])
