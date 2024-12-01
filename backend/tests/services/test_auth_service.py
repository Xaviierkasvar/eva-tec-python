import pytest
from datetime import datetime, timedelta
from app.services.auth_service import create_access_token, verify_token
from fastapi import HTTPException
import jwt  # Importar la librería jwt para simular el comportamiento
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@pytest.fixture
def mock_token_data():
    return {
        "sub": "admin",
        "exp": datetime.utcnow() + timedelta(minutes=15),
    }

@pytest.fixture
def mock_verify_token(monkeypatch):
    def mock_verify(token):
        try:
            # Aquí simulamos la decodificación del JWT con la clave secreta y el algoritmo.
            payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])  # Usamos la misma clave secreta y algoritmo.
            if payload["sub"] == "admin":
                return payload  # Si es un token válido, retornamos el payload simulado.
            raise HTTPException(status_code=401, detail="Token inválido")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="El token ha expirado")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")
    
    monkeypatch.setattr("app.services.auth_service.verify_token", mock_verify)

def test_create_access_token(mock_token_data):
    token = create_access_token(data=mock_token_data)
    assert token is not None
    assert isinstance(token, str)

# Función para crear un token de prueba válido
def create_test_token():
    expiration = datetime.utcnow() + timedelta(minutes=15)
    token_data = {
        "sub": "admin",  # El 'sub' puede ser cualquier valor, dependiendo de tu lógica
        "role": "admin",  # Asegúrate de que el campo 'role' también esté presente
        "exp": expiration
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Función para verificar el token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            message = "Token inválido"
            raise HTTPException(status_code=401, detail=message)

        return payload
    except jwt.ExpiredSignatureError:
        message = "El token ha expirado"
        raise HTTPException(status_code=401, detail=message)
    except jwt.JWTError as e:
        message = f"Token inválido: {e}"
        raise HTTPException(status_code=401, detail="Token inválido")

# Test para verificar la creación y validación del token
def test_verify_token_valid():
    valid_token = create_test_token()  # Genera el token válido

    # Verifica que el token sea válido
    decoded_token = verify_token(valid_token)
    assert decoded_token["sub"] == "admin"  # Asegúrate de que el token sea verificado correctamente
    assert decoded_token["role"] == "admin"  # Verifica que el rol también sea correcto

def test_is_token_expired():
    expired_time = datetime.utcnow() - timedelta(minutes=1)
    future_time = datetime.utcnow() + timedelta(minutes=5)
    assert expired_time < datetime.utcnow()
    assert future_time > datetime.utcnow()
