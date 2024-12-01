import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.controllers.auth_controller import router
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

# Configurar la aplicación para pruebas
app = FastAPI()
app.include_router(router)

client = TestClient(app)

@pytest.fixture
def mock_auth_service(monkeypatch):
    # Mock de la función de autenticación
    async def mock_authenticate_user(username, password):
        if username == "admin" and password == "admin123":
            return {
                "user_id": 1,
                "username": username,
                "role": "admin",
                "access_token": "fake-jwt-token"
            }
        return None  # En caso de fallo

    # Reemplaza la función real con la función simulada
    monkeypatch.setattr("app.services.auth_service.authenticate_user", mock_authenticate_user)


def test_login_success(mock_auth_service):
    response = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert response.json()["username"] == "admin"

def test_login_failure(mock_auth_service):
    response = client.post("/login", json={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401  # 401 para error de autenticación
    assert response.json()["detail"] == "Username or password is incorrect"  # Ajustar el mensaje de error

def test_refresh_token(mock_auth_service):
    invalid_token = "fake-invalid-jwt-token"  # Usamos un token inválido para simular el fallo
    response = client.post("/refresh-token", headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401  # El código de estado esperado cuando el token es inválido
    assert "detail" in response.json()  # Asegúrate de que la respuesta contenga un mensaje de error

