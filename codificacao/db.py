"""
Módulo de gerenciamento de banco de dados SQLite otimizado.
Fornece conexões e utilitários para operações com o banco.
"""

import sqlite3
import os
import logging
from contextlib import contextmanager
from typing import Iterator, Optional
from pathlib import Path
from codificacao.config import Config

# Logger para operações de banco
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador otimizado de conexões com SQLite."""
    
    def __init__(self, db_path: str = Config.DB_PATH):
        self.db_path = Path(db_path)
        self._connection_cache: Optional[sqlite3.Connection] = None
    
    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """
        Context manager para conexões SQLite otimizadas.
        Usage:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                # operações...
        """
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path,
                timeout=30.0,  # Timeout para evitar locks
                check_same_thread=False
            )
            # Otimizações SQLite
            conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
            conn.execute("PRAGMA synchronous=NORMAL")  # Balance performance/safety
            conn.execute("PRAGMA cache_size=10000")  # Cache de 10MB
            conn.execute("PRAGMA temp_store=MEMORY")  # Temp tables in memory
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Erro na conexão SQLite: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_cursor(self) -> Iterator[sqlite3.Cursor]:
        """
        Context manager para cursors SQLite.
        Usage:
            with db_manager.get_cursor() as cursor:
                cursor.execute("SELECT ...")
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
            finally:
                cursor.close()
    
    def exists(self) -> bool:
        """Verifica se o banco de dados existe."""
        return self.db_path.exists()
    
    def create_if_not_exists(self) -> None:
        """Cria banco se não existir."""
        if not self.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with self.get_connection() as conn:
                logger.info(f"Banco criado: {self.db_path}")
    
    def get_size(self) -> int:
        """Retorna tamanho do banco em bytes."""
        return self.db_path.stat().st_size if self.exists() else 0
    
    def vacuum(self) -> None:
        """Otimiza e compacta o banco."""
        with self.get_connection() as conn:
            conn.execute("VACUUM")
            logger.info("Banco otimizado com VACUUM")

# Instância global otimizada
db_manager = DatabaseManager()

# Funções de compatibilidade (mantidas para não quebrar código existente)
def get_connection():
    """Função de compatibilidade - use db_manager.get_connection()."""
    import warnings
    warnings.warn("Use db_manager.get_connection() context manager", DeprecationWarning)
    conn = sqlite3.connect(db_manager.db_path)
    return conn, conn.cursor()

def check_db_or_exit() -> None:
    """Verifica se banco existe - versão otimizada sem Tkinter."""
    if not db_manager.exists():
        logger.error(f"Banco não encontrado: {db_manager.db_path}")
        print(f"❌ Erro: Banco não encontrado em {db_manager.db_path}")
        print("💡 Execute a indexação primeiro!")
        exit(1)

def close_connection(conn: Optional[sqlite3.Connection]) -> None:
    """Fecha conexão de forma segura."""
    if conn:
        try:
            conn.close()
        except sqlite3.Error as e:
            logger.warning(f"Erro ao fechar conexão: {e}")

# Utilitários adicionais
def execute_script(script_path: str) -> None:
    """Executa script SQL do arquivo."""
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script não encontrado: {script_path}")
    
    with open(script_path, 'r', encoding='utf-8') as f:
        script = f.read()
    with db_manager.get_connection() as conn:
        conn.executescript(script)
        logger.info(f"Script executado: {script_path}")

def backup_database(backup_path: str) -> None:
    """Cria backup do banco."""
    with db_manager.get_connection() as source:
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)
            logger.info(f"Backup criado: {backup_path}")
