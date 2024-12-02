import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app  # Asegúrate de importar tu aplicación FastAPI
from app.controllers.document_analysis_controller import router  # Ajusta la ruta de importación

# Añadir el router a la aplicación para las pruebas
app.include_router(router)

client = TestClient(app)

# === Fixtures ===

@pytest.fixture
def mock_file():
    file = MagicMock()
    file.filename = "test.pdf"
    file.content_type = "application/pdf"
    file.file.read.return_value = b"fake file content"
    return file

# === Pruebas para el controlador ===

@patch('app.controllers.document_analysis_controller.verify_token')
@patch('app.controllers.document_analysis_controller.analyze_document')
@patch('app.controllers.document_analysis_controller.store_log')
def test_upload_document_success(mock_store_log, mock_analyze_document, mock_verify_token, mock_file):
    mock_verify_token.return_value = {"sub": "testuser"}
    mock_analyze_document.return_value = {"message": "Factura almacenada en la base de datos.", "id": 1}

    response = client.post(
        "/analyze-document",
        files={"file": ("test.pdf", mock_file.file.read(), "application/pdf")},
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "data": {"message": "Factura almacenada en la base de datos.", "id": 1}
    }

@patch('app.controllers.document_analysis_controller.verify_token')
@patch('app.controllers.document_analysis_controller.analyze_document')
@patch('app.controllers.document_analysis_controller.store_log')
def test_upload_document_analysis_error(mock_store_log, mock_analyze_document, mock_verify_token, mock_file):
    mock_verify_token.return_value = {"sub": "testuser"}
    mock_analyze_document.side_effect = Exception("Error de análisis")

    response = client.post(
        "/analyze-document",
        files={"file": ("test.pdf", mock_file.file.read(), "application/pdf")},
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Error al analizar el documento: Error de análisis"}
