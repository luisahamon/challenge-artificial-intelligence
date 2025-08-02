"""
Sistema de validação robusto para parâmetros de entrada.
"""

from typing import Any, List, Optional
from .config import Config

class ValidationError(Exception):
    """Exceção customizada para erros de validação."""
    pass

class Validator:
    """Classe para validações de entrada do sistema."""
    
    @staticmethod
    def validate_tema(tema: str) -> str:
        """
        Valida e normaliza o tema de entrada.
        Args:
            tema (str): Tema a ser validado
        Returns:
            str: Tema normalizado
        Raises:
            ValidationError: Se o tema for inválido
        """
        if not isinstance(tema, str):
            raise ValidationError(f"Tema deve ser string, recebido {type(tema)}")
        tema_clean = tema.strip()
        if not tema_clean:
            raise ValidationError("Tema não pode estar vazio")
        if not Config.validate_tema(tema_clean):
            raise ValidationError(
                f"Tema deve ter entre {Config.MIN_TEMA_LENGTH} e {Config.MAX_TEMA_LENGTH} caracteres")
        return tema_clean
    
    @staticmethod
    def validate_nivel(nivel: str) -> str:
        """
        Valida e normaliza o nível de conhecimento.
        Args:
            nivel (str): Nível a ser validado
        Returns:
            str: Nível normalizado
        Raises:
            ValidationError: Se o nível for inválido
        """
        if not isinstance(nivel, str):
            raise ValidationError(f"Nível deve ser string, recebido {type(nivel)}")
        nivel_clean = nivel.strip().lower()
        if not Config.validate_nivel(nivel_clean):
            raise ValidationError(f"Nível deve ser um de: {', '.join(Config.LEVELS)}")
        return nivel_clean
    
    @staticmethod
    def validate_formato(formato: str) -> str:
        """
        Valida e normaliza o formato de saída.
        Args:
            formato (str): Formato a ser validado
        Returns:
            str: Formato normalizado
        Raises:
            ValidationError: Se o formato for inválido
        """
        if not isinstance(formato, str):
            raise ValidationError(f"Formato deve ser string, recebido {type(formato)}")
        formato_clean = formato.strip()
        if not Config.validate_formato(formato_clean):
            raise ValidationError(f"Formato deve ser um de: {', '.join(Config.SUPPORTED_FORMATS)}")
        return formato_clean
    
    @staticmethod
    def validate_historico_dificuldades(historico: Optional[List[str]]) -> Optional[List[str]]:
        """
        Valida o histórico de dificuldades.
        Args:
            historico (Optional[List[str]]): Histórico a ser validado
        Returns:
            Optional[List[str]]: Histórico validado
        Raises:
            ValidationError: Se o histórico for inválido
        """
        if historico is None:
            return None
        if not isinstance(historico, list):
            raise ValidationError(f"Histórico deve ser lista, recebido {type(historico)}")
        
        # Valida cada item do histórico
        historico_clean = []
        for item in historico:
            if not isinstance(item, str):
                raise ValidationError(f"Itens do histórico devem ser strings, recebido {type(item)}")
            item_clean = item.strip()
            if item_clean:  # Ignora strings vazias
                historico_clean.append(item_clean)
        return historico_clean if historico_clean else None

def validate_input_parameters(tema: str, nivel: str, formato: str, 
                            historico_dificuldades: Optional[List[str]] = None) -> tuple:
    """
    Valida todos os parâmetros de entrada de uma vez.
    Args:
        tema (str): Tema a ser validado
        nivel (str): Nível a ser validado
        formato (str): Formato a ser validado
        historico_dificuldades (Optional[List[str]]): Histórico a ser validado
    Returns:
        tuple: Tupla com parâmetros validados (tema, nivel, formato, historico)
        
    Raises:
        ValidationError: Se algum parâmetro for inválido
    """
    validator = Validator()
    try:
        tema_valid = validator.validate_tema(tema)
        nivel_valid = validator.validate_nivel(nivel)
        formato_valid = validator.validate_formato(formato)
        historico_valid = validator.validate_historico_dificuldades(historico_dificuldades)
        return tema_valid, nivel_valid, formato_valid, historico_valid
        
    except ValidationError as e:
        # Re-lança com contexto adicional
        raise ValidationError(f"Erro de validação nos parâmetros de entrada: {e}")
    except Exception as e:
        # Captura erros inesperados
        raise ValidationError(f"Erro inesperado na validação: {e}")
