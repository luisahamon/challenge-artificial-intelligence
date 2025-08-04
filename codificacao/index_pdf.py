import sqlite3
import PyPDF2
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
# Conecta ao banco de dados principal
conn = sqlite3.connect(os.path.join(ROOT, 'index.db'))
c = conn.cursor()
# Cria a tabela se não existir, com restrição de unicidade para evitar duplicidade
c.execute('CREATE TABLE IF NOT EXISTS pdfs (id INTEGER PRIMARY KEY, titulo TEXT UNIQUE, texto TEXT, num_paginas INTEGER)')
with open(r'C:\Users\LuisaHamon\challenge-artificial-intelligence\resources\Capítulo do Livro.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    texto = ''
    for page in reader.pages:
        texto += page.extract_text() or ''
    num_paginas = len(reader.pages)
# Insere apenas se não existir PDF com o mesmo título
c.execute('INSERT OR IGNORE INTO pdfs (titulo, texto, num_paginas) VALUES (?, ?, ?)', ('Capítulo do Livro', texto, num_paginas))
conn.commit()
conn.close()
