import sqlite3

# Conecta ao banco de dados principal
conn = sqlite3.connect('index.db')
c = conn.cursor()
# Cria a tabela se não existir, com restrição de unicidade para evitar duplicidade
c.execute('CREATE TABLE IF NOT EXISTS textos (id INTEGER PRIMARY KEY, titulo TEXT UNIQUE, conteudo TEXT)')
with open(r'C:\Users\LuisaHamon\challenge-artificial-intelligence\resources\Apresentação.txt', encoding='utf-8') as f:
    conteudo = f.read()
# Insere apenas se não existir texto com o mesmo título
c.execute('INSERT OR IGNORE INTO textos (titulo, conteudo) VALUES (?, ?)', ('Apresentação', conteudo))
conn.commit()
conn.close()
