import subprocess
import sys

# Executa a indexação
print('Iniciando indexação dos dados...')
ret = subprocess.run([sys.executable, "-m", "codificacao.indexar_tudo"])
if ret.returncode != 0:
    print('Erro na indexação. Abortando.')
    sys.exit(1)

# Executa a interface adaptativa
print('Iniciando interface adaptativa...')
subprocess.run([sys.executable, "-m", "codificacao.prompt_adaptativo_gui"])
