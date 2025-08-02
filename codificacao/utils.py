from typing import List, Optional, Tuple, Any
import sqlite3
from .db import get_connection

def gerar_variacoes(termo: str) -> List[str]:
    """
    Gera variações de um termo para busca mais abrangente.
    
    Args:
        termo (str): Termo base para gerar variações
        
    Returns:
        List[str]: Lista de variações do termo incluindo sinônimos
    """
    termo = termo.strip().lower()
    variacoes = set()
    variacoes.add(termo)
    variacoes.add(termo.upper())
    variacoes.add(termo.capitalize())
    if termo.endswith('s'):
        variacoes.add(termo[:-1])
    else:
        variacoes.add(termo + 's')
    sinonimos = {
        'llm': ['llms', 'large language model', 'large language models'],
        'html': ['html5'],
        'html5': ['html'],
        'pdf': ['pdfs'],
        'vídeo': ['video', 'videos', 'vídeos'],
        'video': ['vídeo', 'vídeos', 'videos'],
        'exercício': ['exercicio', 'exercícios', 'exercicios'],
        'exercicio': ['exercício', 'exercícios', 'exercicios'],
    }
    for base, sins in sinonimos.items():
        if termo == base or termo in sins:
            variacoes.update(sins)
            variacoes.add(base)
    return list(variacoes)

def buscar_conteudo(tema: str, formato: str) -> Optional[str]:
    """
    Busca conteúdo relevante no banco de dados baseado no tema e formato.
    Utiliza FTS5 (Full-Text Search) como método principal e busca LIKE como fallback
    para garantir máxima compatibilidade e resultados relevantes.
    Args:
        tema (str): Tema ou tópico a ser buscado (ex: 'HTML', 'programação')
        formato (str): Formato do conteúdo desejado ('Texto', 'PDF', 'Vídeo', 'Imagem', 'Exercício')
    Returns:
        Optional[str]: Conteúdo encontrado formatado ou None se nenhum conteúdo for encontrado
    Raises:
        sqlite3.Error: Em caso de erro na consulta ao banco de dados
    """
    conn, c = get_connection()
    termos = gerar_variacoes(tema)
    fts_query = ' OR '.join([f'"{t}"' for t in termos])
    like_patterns = [f'%{t}%' for t in termos]
    if formato == 'Texto':
        try:
            c.execute(f"SELECT snippet(textos_fts, 1, '[', ']', '...', 10) FROM textos_fts WHERE textos_fts MATCH ? LIMIT 1", (fts_query,))
            row = c.fetchone()
            if row and row[0]:
                conn.close()
                return row[0]
        except Exception:
            pass
        for pattern in like_patterns:
            c.execute("SELECT conteudo FROM textos WHERE conteudo LIKE ? LIMIT 1", (pattern,))
            row = c.fetchone()
            if row:
                conn.close()
                return row[0][:500] + ('...' if len(row[0]) > 500 else '')
    elif formato == 'PDF':
        try:
            c.execute(f"SELECT titulo, snippet(pdfs_fts, 1, '[', ']', '...', 10), texto FROM pdfs_fts JOIN pdfs ON pdfs_fts.rowid = pdfs.rowid WHERE pdfs_fts MATCH ? LIMIT 1", (fts_query,))
            row = c.fetchone()
            if row:
                titulo, snippet_txt, texto_completo = row
                conn.close()
                if snippet_txt and len(snippet_txt.strip()) > 30:
                    return f"{titulo}: {snippet_txt}\n\nTrecho do PDF:\n{texto_completo[:1000]}{'...' if len(texto_completo) > 1000 else ''}"
                else:
                    return f"{titulo}:\n{texto_completo[:1000]}{'...' if len(texto_completo) > 1000 else ''}"
        except Exception:
            pass
        for pattern in like_patterns:
            c.execute("SELECT titulo, texto FROM pdfs WHERE texto LIKE ? LIMIT 1", (pattern,))
            row = c.fetchone()
            if row:
                conn.close()
                return f"{row[0]}:\n{row[1][:1000]}{'...' if len(row[1]) > 1000 else ''}"
    elif formato == 'Vídeo':
        try:
            c.execute(f"SELECT titulo, snippet(videos_fts, 1, '[', ']', '...', 10), transcricao FROM videos_fts JOIN videos ON videos_fts.rowid = videos.rowid WHERE videos_fts MATCH ? LIMIT 1", (fts_query,))
            row = c.fetchone()
            if row:
                titulo, snippet_txt, transcricao = row
                conn.close()
                if snippet_txt and len(snippet_txt.strip()) > 30:
                    return f"{titulo}: {snippet_txt}\n\nTrecho da transcrição:\n{transcricao[:1000]}{'...' if len(transcricao) > 1000 else ''}"
                else:
                    return f"{titulo}:\n{transcricao[:1000]}{'...' if len(transcricao) > 1000 else ''}"
        except Exception:
            pass
        for pattern in like_patterns:
            c.execute("SELECT titulo, transcricao FROM videos WHERE transcricao LIKE ? LIMIT 1", (pattern,))
            row = c.fetchone()
            if row:
                conn.close()
                return f"{row[0]}:\n{row[1][:1000]}{'...' if len(row[1]) > 1000 else ''}"
    elif formato == 'Imagem':
        for pattern in like_patterns:
            c.execute("SELECT nome, formato, tamanho FROM imagens WHERE nome LIKE ? LIMIT 1", (pattern,))
            row = c.fetchone()
            if row:
                conn.close()
                return f"Imagem: {row[0]} | Formato: {row[1]} | Tamanho: {row[2]}"
    elif formato == 'Exercício':
        try:
            c.execute(f"SELECT tema, snippet(exercicios_fts, 1, '[', ']', '...', 10) FROM exercicios_fts WHERE exercicios_fts MATCH ? LIMIT 1", (fts_query,))
            row = c.fetchone()
            if row and row[1]:
                conn.close()
                return f"{row[0]}: {row[1]}"
        except Exception:
            pass
        for pattern in like_patterns:
            c.execute("SELECT enunciado, resposta FROM exercicios WHERE enunciado LIKE ? LIMIT 1", (pattern,))
            row = c.fetchone()
            if row:
                conn.close()
                return f"Enunciado: {row[0][:200]}...\nResposta: {row[1][:200]}..."
    conn.close()
    return 'Nenhum conteúdo encontrado para esse tema e formato.'
