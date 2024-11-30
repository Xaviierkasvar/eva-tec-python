import pyodbc
from typing import Optional, Dict, Any
from datetime import datetime
from app.db import get_db_connection
from app.utils.date_utils import parse_datetime  # Nuevo módulo de utilidades para fechas

async def get_filtered_history(
    level: Optional[str] = None,
    description: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Obtiene el historial filtrado con paginación desde la base de datos SQL Server.
    
    Args:
        level (Optional[str]): Nivel de log para filtrar.
        description (Optional[str]): Descripción para filtrar por mensaje.
        start_date (Optional[datetime]): Fecha de inicio para filtrar.
        end_date (Optional[datetime]): Fecha de fin para filtrar.
        page (int): Número de página para paginación.
        page_size (int): Tamaño de página para paginación.
    
    Returns:
        Dict[str, Any]: Diccionario con información de paginación y registros.
    
    Raises:
        ValueError: Si los parámetros de entrada no son válidos.
    """
    # Validar parámetros de paginación
    _validate_pagination_params(page, page_size)

    # Obtener conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Construir consulta base y parámetros
        base_query, params = _build_base_query(level, description, start_date, end_date)

        # Obtener total de registros
        total_records = _get_total_records(cursor, base_query, params)

        # Calcular paginación
        total_pages = _calculate_total_pages(total_records, page_size)

        # Obtener registros paginados
        history = _fetch_paginated_records(cursor, base_query, params, page, page_size)

        return {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
            "records": history
        }

    except Exception as e:
        # Logging de errores (considera usar un logger profesional)
        print(f"Error en get_filtered_history: {e}")
        raise
    finally:
        # Asegurar cierre de cursor y conexión
        cursor.close()
        conn.close()

def _validate_pagination_params(page: int, page_size: int) -> None:
    """Validar parámetros de paginación."""
    if page < 1:
        raise ValueError("El número de página debe ser mayor o igual a 1.")
    if page_size < 1:
        raise ValueError("El tamaño de página debe ser mayor o igual a 1.")

def _build_base_query(
    level: Optional[str], 
    description: Optional[str], 
    start_date: Optional[datetime], 
    end_date: Optional[datetime]
) -> tuple:
    """Construir consulta base con filtros."""
    base_query = "SELECT id, level, message, log_type, timestamp FROM dbo.logs WHERE 1=1"
    params = []

    # Validar y añadir filtro de nivel
    if level:
        valid_levels = ["CARGA_DOCUMENTO", "IA", "INTERACCION_USUARIO"]
        if level not in valid_levels:
            raise ValueError(f"Nivel no válido. Los niveles permitidos son: {', '.join(valid_levels)}.")
        base_query += " AND level = ?"
        params.append(level)

    # Añadir filtro de descripción
    if description:
        base_query += " AND message LIKE ?"
        params.append(f"%{description}%")

    # Añadir filtros de fecha
    if start_date:
        start_date = parse_datetime(start_date)
        base_query += " AND timestamp >= ?"
        params.append(start_date)

    if end_date:
        end_date = parse_datetime(end_date)
        base_query += " AND timestamp <= ?"
        params.append(end_date)

    return base_query, params

def _get_total_records(cursor, base_query: str, params: list) -> int:
    """Obtener total de registros para la consulta."""
    count_query = f"SELECT COUNT(*) FROM ({base_query}) AS count_query"
    cursor.execute(count_query, params)
    return cursor.fetchone()[0]

def _calculate_total_pages(total_records: int, page_size: int) -> int:
    """Calcular total de páginas."""
    return (total_records // page_size) + (1 if total_records % page_size > 0 else 0)

def _fetch_paginated_records(
    cursor, 
    base_query: str, 
    params: list, 
    page: int, 
    page_size: int
) -> list:
    """Obtener registros paginados."""
    offset = (page - 1) * page_size
    query_with_pagination = f"{base_query} ORDER BY timestamp DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.extend([offset, page_size])

    cursor.execute(query_with_pagination, params)
    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "type": row[1],
            "description": row[2],
            "log_type": row[3],
            "datetime": row[4]
        } 
        for row in rows
    ]