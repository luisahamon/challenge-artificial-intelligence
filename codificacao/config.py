"""
Configurações centralizadas do sistema de aprendizagem adaptativa.
"""

from typing import List, Dict

class Config:
    """Configurações centralizadas do sistema."""
    
    # Banco de dados
    DB_PATH: str = 'index.db'
    BACKUP_PATH: str = 'index_backup.db'
    
    # Limites de conteúdo
    MAX_CONTENT_LENGTH: int = 1000
    MAX_SNIPPET_LENGTH: int = 500
    MAX_SEARCH_RESULTS: int = 5
    
    # Formatos suportados
    SUPPORTED_FORMATS: List[str] = ['Texto', 'PDF', 'Vídeo', 'Imagem', 'Exercício']
    
    # Níveis de conhecimento
    LEVELS: List[str] = ['iniciante', 'intermediário', 'avançado']
    
    # Templates e personalização
    MAX_TEMPLATES_PER_SECTION: int = 3
    MIN_TEMPLATE_LENGTH: int = 50
    
    # Machine Learning
    KMEANS_CLUSTERS: int = 3
    EMBEDDING_MODEL: str = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    
    # Cache
    CACHE_SIZE: int = 100
    CACHE_TTL: int = 3600  # 1 hora em segundos
    
    # Logging
    LOG_LEVEL: str = 'INFO'
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Validação
    MIN_TEMA_LENGTH: int = 2
    MAX_TEMA_LENGTH: int = 100
    
    @classmethod
    def validate_formato(cls, formato: str) -> bool:
        """Valida se o formato é suportado."""
        return formato in cls.SUPPORTED_FORMATS
    
    @classmethod
    def validate_nivel(cls, nivel: str) -> bool:
        """Valida se o nível é suportado."""
        return nivel.lower() in cls.LEVELS
    
    @classmethod
    def validate_tema(cls, tema: str) -> bool:
        """Valida se o tema atende aos critérios de tamanho."""
        return cls.MIN_TEMA_LENGTH <= len(tema.strip()) <= cls.MAX_TEMA_LENGTH

# Configurações de desenvolvimento (sobrescreve Config para testes)
class DevConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    
    DB_PATH: str = 'test_index.db'
    LOG_LEVEL: str = 'DEBUG'
    CACHE_SIZE: int = 10
    MAX_CONTENT_LENGTH: int = 200

# Configurações de produção
class ProdConfig(Config):
    """Configurações para ambiente de produção."""
    
    LOG_LEVEL: str = 'WARNING'
    CACHE_SIZE: int = 500
    MAX_CONTENT_LENGTH: int = 2000
