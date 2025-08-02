import os
import sys
import subprocess

# Caminho do banco
db_path = 'index.db'

# Remove o banco se já existir
if os.path.exists(db_path):
    os.remove(db_path)
    print('Banco antigo removido.')
else:
    print('Nenhum banco antigo encontrado.')

# Lista dos scripts de indexação
scripts = [
    'index_video.py',
    'index_pdf.py',
    'index_exercicios.py',
    'index_imagem.py',
    'index_texto.py',
]

# Executa cada script
for script in scripts:
    print(f'Executando {script}...')
    result = subprocess.run([sys.executable, script], cwd=os.path.dirname(__file__))
    if result.returncode != 0:
        print(f'Erro ao executar {script}.')
        break
else:
    print('Todos os scripts de indexação executados com sucesso!')
