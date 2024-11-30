import os
from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from app.db import get_db_connection
from app.services.log_service import store_log  # Importar el servicio de logs

# Cargar variables de entorno desde el archivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Token expira en 15 minutos por defecto
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(username: str, password: str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Consulta del usuario por username
            query = "SELECT user_id, username, password, role FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            db_user = cursor.fetchone()

            # Si el usuario no existe o la contraseña es incorrecta
            if db_user is None or db_user[2] != password:
                # Detalle específico para el log
                if db_user is None:
                    message = "Username does not exist"
                else:
                    message = f"Incorrect password for username: {username}"

                # Guardar el error en el log con detalle específico
                store_log("INTERACCION_USUARIO", message, "ERROR")
                
                # Mensaje genérico para el cliente
                raise HTTPException(status_code=401, detail="Username or password is incorrect")

            # Generar el token de acceso
            access_token_expires = timedelta(minutes=15)  # Token expira en 15 minutos
            access_token = create_access_token(
                data={"sub": db_user[1], "role": db_user[3]},
                expires_delta=access_token_expires
            )

            # Log de autenticación exitosa
            message = f"user_id:{db_user[0]}, successfully authenticated."
            store_log("INTERACCION_USUARIO", message, "INFO")

            # Respuesta exitosa
            return {
                "user_id": db_user[0],
                "username": db_user[1],
                "role": db_user[3],
                "access_token": access_token,
            }
    except HTTPException as e:
        raise e
    except Exception as e:
        message = f"Error al autenticar usuario: {e}"
        store_log("INTERACCION_USUARIO", message, "ERROR")
        raise HTTPException(status_code=500, detail=message)
    finally:
        connection.close()

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            message = "Token inválido"
            store_log("INTERACCION_USUARIO", message, "ERROR")
            raise HTTPException(status_code=401, detail=message)

        return payload
    except ExpiredSignatureError:
        message = "El token ha expirado"
        raise HTTPException(status_code=401, detail=message)
    except JWTError as e:
        message = f"Token inválido: {e}"
        raise HTTPException(status_code=401, detail="Token inválido")

def is_token_expired(payload: dict) -> bool:
    exp = payload.get("exp")
    if exp:
        return datetime.utcnow() > datetime.utcfromtimestamp(exp)
    return False

def refresh_access_token(token: str):
    try:
        payload = verify_token(token)

        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            raise HTTPException(status_code=401, detail="Información del token inválida")

        new_token = create_access_token(data={"sub": username, "role": role}, expires_delta=timedelta(minutes=15))

        message = f"successfully refresh access token."
        store_log("INTERACCION_USUARIO", message, "INFO")

        return new_token
    except HTTPException as e:
        store_log("INTERACCION_USUARIO", e, "ERROR")
        raise e
    except Exception as e:
        message = f"Error al refrescar el token: {e}"
        store_log("INTERACCION_USUARIO", message, "ERROR")
        raise HTTPException(status_code=500, detail=message)