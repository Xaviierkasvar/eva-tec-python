import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app  # Asegúrate de importar tu aplicación FastAPI
from app.controllers.history_controller import router

# Añadir el router a la aplicación para las pruebas
app.include_router(router)

client = TestClient(app)

# Datos de ejemplo para las pruebas
example_token = "example_token"
example_history_response = {
    "status": "success",
    "total_records": 50,
    "total_pages": 5,
    "current_page": 1,
    "page_size": 10,
    "data": [
        {
            "id": 1,
            "type": "Factura",
            "cliente": "Juan Pérez",
            "proveedor": "Proveedor XYZ",
            "numero_factura": "12345",
            "fecha": "2024-11-29T08:42:58",
            "total_factura": 200.0
        }
    ]
}

# Fixture para simular la verificación del token
@pytest.fixture
def mock_verify_token():
    with patch("app.services.auth_service.verify_token") as mock:
        mock.return_value = {"sub": "user_id"}
        yield mock

# Fixture para simular el servicio de historial
@pytest.fixture
def mock_get_filtered_history():
    with patch("app.services.history_service.get_filtered_history") as mock:
        mock.return_value = example_history_response
        yield mock

# Prueba para la ruta GET /history sin token
def test_get_filtered_history_no_token():
    response = client.get("/history")
    assert response.status_code == 401  # Unauthorized
