import os
import shutil
import sys

# Caminhos
db_path = '../index.db'
db_backup = '../index_backup.db'

# 1. Faz backup do banco original, sem sobrescrever backup existente
if os.path.exists(db_path):
    if os.path.exists(db_backup):
        print(f'Backup já existe em {db_backup}. Não será sobrescrito.')
    else:
        shutil.copy2(db_path, db_backup)
        print(f'Backup criado: {db_backup}')
else:
    print('index.db não encontrado, nada para fazer backup.')

# 2. Executa o script de indexação FTS5 automaticamente
import subprocess
print('Executando indexar_fts.py para criar/repopular as tabelas FTS5 no banco atual...')
result = subprocess.run([sys.executable, 'indexar_fts.py'], cwd=os.path.dirname(__file__))
if result.returncode == 0:
    print('Tabelas FTS5 criadas e populadas!')
else:
    print('Erro ao executar indexar_fts.py.')
