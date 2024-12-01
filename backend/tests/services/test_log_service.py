import pytest
from unittest.mock import patch, MagicMock
from app.services.log_service import store_log

# Fixture para simular la conexión a la base de datos
@pytest.fixture
def mock_db_connection():
    with patch("app.services.log_service.get_db_connection") as mock:
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock.return_value = mock_conn
        yield mock

# Fixture para simular el logging
@pytest.fixture
def mock_logging():
    with patch("app.services.log_service.logging") as mock:
        yield mock

# Prueba para la función store_log con parámetros válidos
def test_store_log_valid(mock_db_connection, mock_logging):
    store_log("INFO", "Test message", "TEST_TYPE")
    mock_db_connection().cursor().execute.assert_called_once_with(
        "INSERT INTO logs (level, message, log_type) VALUES (?, ?, ?)",
        ("INFO", "Test message", "TEST_TYPE")
    )
    mock_db_connection().commit.assert_called_once()
    mock_db_connection().cursor().close.assert_called_once()
    mock_db_connection().close.assert_called_once()

# Prueba para la función store_log con error en la base de datos
def test_store_log_db_error(mock_db_connection, mock_logging):
    mock_db_connection().cursor().execute.side_effect = Exception("DB error")
    store_log("ERROR", "Test error message", "TEST_TYPE")
    mock_logging.error.assert_called_once_with("Error al almacenar el log: DB error")