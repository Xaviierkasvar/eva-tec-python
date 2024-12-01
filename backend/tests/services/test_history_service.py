import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.history_service import get_filtered_history

# Datos de ejemplo para las pruebas
example_history_data = {
    "total_records": 50,
    "total_pages": 5,
    "current_page": 1,
    "page_size": 10,
    "records": [
        {
            "id": 1,
            "type": "Factura",
            "description": "Documento de prueba",
            "log_type": "CARGA_DOCUMENTO",
            "datetime": datetime(2024, 11, 29, 8, 42, 58)
        }
    ]
}

# Fixture para simular la conexión a la base de datos
@pytest.fixture
def mock_db_connection():
    with patch("app.services.history_service.get_db_connection") as mock:
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = [50]
        mock_cursor.fetchall.return_value = [
            (1, "Factura", "Documento de prueba", "CARGA_DOCUMENTO", datetime(2024, 11, 29, 8, 42, 58))
        ]
        mock.return_value = mock_conn
        yield mock

# Prueba para obtener el historial filtrado con parámetros válidos
@pytest.mark.asyncio
async def test_get_filtered_history_valid(mock_db_connection):
    result = await get_filtered_history(
        level="CARGA_DOCUMENTO",
        description="prueba",
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
        page=1,
        page_size=10
    )
    assert result == example_history_data

# Prueba para validar parámetros de paginación inválidos
@pytest.mark.asyncio
async def test_get_filtered_history_invalid_pagination(mock_db_connection):
    with pytest.raises(ValueError, match="El número de página debe ser mayor o igual a 1."):
        await get_filtered_history(page=-1, page_size=10)

    with pytest.raises(ValueError, match="El tamaño de página debe ser mayor o igual a 1."):
        await get_filtered_history(page=1, page_size=0)

# Prueba para el manejo de errores en la consulta
@pytest.mark.asyncio
async def test_get_filtered_history_query_error(mock_db_connection):
    mock_db_connection.side_effect = Exception("Database error")
    with pytest.raises(Exception, match="Database error"):
        await get_filtered_history(page=1, page_size=10)