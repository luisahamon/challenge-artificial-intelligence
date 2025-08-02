"""
Sistema de logging otimizado e estruturado.
"""

import logging
import os
import time
from functools import wraps, lru_cache
from typing import Optional
from .config import Config

# Cache global para formatters e loggers configurados
_configured_loggers = set()

@lru_cache(maxsize=4)
def _get_formatter() -> logging.Formatter:
    """Formatter com cache para reutilização."""
    return logging.Formatter(Config.LOG_FORMAT)

@lru_cache(maxsize=8)
def _get_log_level(level: Optional[str] = None) -> int:
    """Converte string de nível para int com cache."""
    log_level = level or Config.LOG_LEVEL
    return getattr(logging, log_level.upper())

def _ensure_log_dir() -> None:
    """Garante que diretório de logs existe."""
    if not os.path.exists('logs'):
        os.makedirs('logs')

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Configura logger otimizado com cache.
    Args:
        name (str): Nome do logger
        level (Optional[str]): Nível de log
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Cache - evita reconfiguração
    if name in _configured_loggers:
        return logger
    log_level_int = _get_log_level(level)
    logger.setLevel(log_level_int)
    
    # Formatter reutilizável
    formatter = _get_formatter()
    
    # Console handler otimizado
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level_int)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler otimizado
    _ensure_log_dir()
    file_handler = logging.FileHandler('logs/sistema.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    _configured_loggers.add(name)
    return logger

def log_function_call(func):
    """Decorator otimizado para log de chamadas."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        func_name = func.__name__
        logger.debug(f"→ {func_name}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"✓ {func_name}")
            return result
        except Exception as e:
            logger.error(f"✗ {func_name}: {e}")
            raise
    return wrapper

def log_performance(func):
    """Decorator otimizado para performance com cache de logger."""
    logger = logging.getLogger(func.__module__)  # Cache do logger
    func_name = func.__name__  # Cache do nome
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            logger.info(f"⚡ {func_name}: {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"💥 {func_name}: {elapsed:.3f}s - {e}")
            raise
    return wrapper

# Função de conveniência para logging rápido
def get_logger(name: str) -> logging.Logger:
    """Obtém logger configurado rapidamente."""
    return setup_logger(name)
