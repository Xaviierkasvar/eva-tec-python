import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app  # Asegúrate de importar tu aplicación FastAPI
from app.controllers.upload_file_controller import router

# Añadir el router a la aplicación para las pruebas
app.include_router(router)

client = TestClient(app)

# Datos de ejemplo para las pruebas
example_token = "example_token"
example_upload_response = {
    "upload_result": {"message": "Archivo subido con éxito a bucket-name/files/filename.csv"},
    "validation_results": []
}

# Fixture para simular la verificación del token
@pytest.fixture
def mock_verify_token():
    with patch("app.services.auth_service.verify_token") as mock:
        mock.return_value = {"sub": "user_id", "role": "admin"}
        yield mock

# Fixture para simular el servicio de subida de archivos
@pytest.fixture
def mock_handle_file_upload():
    with patch("app.services.file_upload_service.handle_file_upload") as mock:
        mock.return_value = example_upload_response
        yield mock

# Fixture para simular el servicio de logs
@pytest.fixture
def mock_store_log():
    with patch("app.services.log_service.store_log") as mock:
        yield mock

# Prueba para la ruta POST /upload con un archivo válido y token válido
def test_upload_file_valid(mock_verify_token, mock_handle_file_upload, mock_store_log):
    with open("testfile.csv", "wb") as f:
        f.write(b"test,data\n1,2,3")

    with open("testfile.csv", "rb") as f:
        response = client.post(
            "/upload",
            headers={"Authorization": f"Bearer {example_token}"},
            files={"file": ("testfile.csv", f, "text/csv")}
        )
    
    assert response.status_code == 200
    assert response.json() == example_upload_response

# Prueba para la ruta POST /upload sin token
def test_upload_file_no_token():
    with open("testfile.csv", "wb") as f:
        f.write(b"test,data\n1,2,3")

    with open("testfile.csv", "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("testfile.csv", f, "text/csv")}
        )
    
    assert response.status_code == 401  # Unauthorized

# Prueba para la ruta POST /upload con un token sin permisos
def test_upload_file_no_permission(mock_verify_token, mock_store_log):
    mock_verify_token.return_value = {"sub": "user_id", "role": "user"}

    with open("testfile.csv", "wb") as f:
        f.write(b"test,data\n1,2,3")

    with open("testfile.csv", "rb") as f:
        response = client.post(
            "/upload",
            headers={"Authorization": f"Bearer {example_token}"},
            files={"file": ("testfile.csv", f, "text/csv")}
        )
    
    assert response.status_code == 403  # Forbidden
    assert response.json() == {"detail": "No tiene permisos para realizar esta acción."}

# Prueba para el manejo de errores en el servicio de subida de archivos
def test_upload_file_service_error(mock_verify_token, mock_store_log):
    with patch("app.services.file_upload_service.handle_file_upload", side_effect=Exception("Service error")):
        with open("testfile.csv", "wb") as f:
            f.write(b"test,data\n1,2,3")

        with open("testfile.csv", "rb") as f:
            response = client.post(
                "/upload",
                headers={"Authorization": f"Bearer {example_token}"},
                files={"file": ("testfile.csv", f, "text/csv")}
            )
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Error al subir el archivo: Service error"}