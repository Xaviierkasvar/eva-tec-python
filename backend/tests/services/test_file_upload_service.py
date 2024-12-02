import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.services.file_upload_service import handle_file_upload, upload_file_to_s3, validate_csv, store_csv_data

# Datos de ejemplo para las pruebas
example_contents = b"column1,column2\nvalue1,value2\nvalue3,value4"
example_filename = "testfile.csv"
example_s3_key = f"files/{example_filename}"
example_upload_result = {"message": f"Archivo subido con éxito a bucket-name/{example_s3_key}"}

# Fixture para simular la conexión a la base de datos
@pytest.fixture
def mock_db_connection():
    with patch("app.services.file_upload_service.get_db_connection") as mock:
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock.return_value = mock_conn
        yield mock

# Fixture para simular el cliente S3
@pytest.fixture
def mock_s3_client():
    with patch("app.services.file_upload_service.s3_client") as mock:
        yield mock

# Fixture para simular el servicio de logs
@pytest.fixture
def mock_store_log():
    with patch("app.services.log_service.store_log") as mock:
        yield mock

# Prueba para la función handle_file_upload con un archivo vacío
def test_handle_file_upload_empty_file():
    with pytest.raises(HTTPException) as excinfo:
        handle_file_upload(b"", example_filename)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "El archivo está vacío."

# Prueba para la función handle_file_upload con un archivo no CSV
def test_handle_file_upload_invalid_file_type():
    with pytest.raises(HTTPException) as excinfo:
        handle_file_upload(example_contents, "testfile.txt")
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "El archivo no es un CSV."

# Prueba para la función validate_csv con un archivo válido
def test_validate_csv_valid():
    validation_results = validate_csv(example_contents)
    assert validation_results == []

# Prueba para la función store_csv_data con datos válidos
def test_store_csv_data_valid(mock_db_connection, mock_store_log):
    store_csv_data(example_contents)
    mock_db_connection().cursor().execute.assert_called()

# Prueba para la función store_csv_data con error en la base de datos
def test_store_csv_data_db_error(mock_db_connection, mock_store_log):
    mock_db_connection().cursor().execute.side_effect = Exception("DB error")
    with pytest.raises(HTTPException) as excinfo:
        store_csv_data(example_contents)
    assert excinfo.value.status_code == 500
    assert "Ocurrió un error al almacenar el archivo: DB error" in excinfo.value.detail