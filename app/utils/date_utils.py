from datetime import datetime
from typing import Union

def transform_date_for_sqlserver(date_str):
    """
    Transforma una fecha en varios formatos al formato YYYY-MM-DD compatible con SQL Server.
    
    Args:
    date_str (str): Fecha en cualquier formato común (e.g., DD/MM/YYYY, YYYY MM DD, YYYYMMDD, etc.)
    
    Returns:
    str: Fecha en formato YYYY-MM-DD para SQL Server, o None si el formato no es válido.
    """
    # Lista de posibles formatos de entrada
    formats = [
        "%d %m %Y",  # 29 11 2024
        "%Y %m %d",  # 2024 11 29
        "%d/%m/%Y",  # 29/11/2024
        "%Y%m%d",    # 20241129
        "%d%m%Y",    # 29112024
        "%Y-%m-%d",  # 2024-11-29 (ya en formato esperado)
    ]
    
    for fmt in formats:
        try:
            # Intentar analizar la fecha con el formato actual
            parsed_date = datetime.strptime(date_str, fmt)
            # Convertir a formato YYYY-MM-DD
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            # Intentar con el siguiente formato
            continue
    
    # Si no se pudo analizar, devolver None
    return None


def parse_datetime(date: Union[str, datetime]) -> datetime:
    """
    Parsea una fecha de diferentes formatos a un objeto datetime.
    
    Args:
        date (Union[str, datetime]): Fecha a parsear
    
    Returns:
        datetime: Objeto datetime parseado
    
    Raises:
        ValueError: Si el formato de fecha no es válido
    """
    if isinstance(date, datetime):
        return date
    
    date_formats = [
        "%Y-%m-%d %H:%M:%S",  # Formato estándar
        "%Y-%m-%dT%H:%M:%S",  # Formato ISO
        "%Y-%m-%d",           # Solo fecha
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Formato de fecha inválido: {date}. Formatos aceptados: YYYY-MM-DD HH:MM:SS, YYYY-MM-DDTHH:MM:SS")