import sqlite3
import json
import os

ROOT = os.path.dirname(os.path.dirname(__file__))

# Conecta ao banco de dados principal
conn = sqlite3.connect(os.path.join(ROOT, 'index.db'))
c = conn.cursor()
# Cria a tabela se não existir, com restrição de unicidade para evitar duplicidade
c.execute('CREATE TABLE IF NOT EXISTS exercicios (id INTEGER PRIMARY KEY, tema TEXT, dificuldade TEXT, enunciado TEXT UNIQUE, resposta TEXT)')
with open(r'C:\Users\LuisaHamon\challenge-artificial-intelligence\resources\Exercícios.json', encoding='utf-8') as f:
    data = json.load(f)

# Extrai o tema geral
tema = data.get('name', '')

# Percorre as questões em data['content']
for questao in data.get('content', []):
    enunciado = questao.get('content', {}).get('html', '')
    # Busca a opção correta
    resposta = ''
    for opt in questao.get('content', {}).get('options', []):
        if opt.get('correct'):
            resposta = opt.get('content', {}).get('html', '')
            break
    # Insere apenas se não existir exercício com o mesmo enunciado
    c.execute('INSERT OR IGNORE INTO exercicios (tema, dificuldade, enunciado, resposta) VALUES (?, ?, ?, ?)',
              (tema, '', enunciado, resposta))
conn.commit()
conn.close()
