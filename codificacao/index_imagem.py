import sqlite3
from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
# Conecta ao banco de dados principal
conn = sqlite3.connect(os.path.join(ROOT, 'index.db'))
c = conn.cursor()
# Cria a tabela se não existir, com restrição de unicidade para evitar duplicidade
c.execute('CREATE TABLE IF NOT EXISTS imagens (id INTEGER PRIMARY KEY, nome TEXT UNIQUE, formato TEXT, tamanho TEXT)')
img = Image.open(r'C:\Users\LuisaHamon\challenge-artificial-intelligence\resources\Infografico-1.jpg')
formato = img.format
tamanho = str(img.size)
# Insere apenas se não existir imagem com o mesmo nome
c.execute('INSERT OR IGNORE INTO imagens (nome, formato, tamanho) VALUES (?, ?, ?)', ('Infografico-1.jpg', formato, tamanho))
conn.commit()
conn.close()
