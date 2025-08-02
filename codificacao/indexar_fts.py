import sqlite3

# Caminho do banco
DB_PATH = 'index.db'

# Conexão
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Criação das tabelas FTS5
fts_tables = [
    ('pdfs_fts', 'pdfs', 'titulo, texto'),
    ('videos_fts', 'videos', 'titulo, transcricao'),
    ('exercicios_fts', 'exercicios', 'tema, enunciado, resposta'),
]

for fts, origem, campos in fts_tables:
    try:
        c.execute(f"DROP TABLE IF EXISTS {fts}")
        c.execute(f"CREATE VIRTUAL TABLE {fts} USING fts5({campos})")
        print(f'Tabela {fts} criada.')
    except Exception as e:
        print(f'Erro ao criar {fts}: {e}')

# População das tabelas FTS5
def popular_fts(fts, origem, campos):
    try:
        campos_list = [c.strip() for c in campos.split(',')]
        campos_str = ', '.join(campos_list)
        c.execute(f'SELECT {campos_str} FROM {origem}')
        for row in c.fetchall():
            placeholders = ','.join(['?'] * len(campos_list))
            c.execute(f'INSERT INTO {fts} ({campos_str}) VALUES ({placeholders})', row)
        print(f'Tabela {fts} populada.')
    except Exception as e:
        print(f'Erro ao popular {fts}: {e}')

for fts, origem, campos in fts_tables:
    popular_fts(fts, origem, campos)

conn.commit()
conn.close()
print('Tabelas FTS5 criadas e populadas!')
