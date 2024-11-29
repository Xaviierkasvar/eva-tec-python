from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.services.auth_service import authenticate_user, refresh_access_token

# Definir el router
router = APIRouter()

# Configurar OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo para recibir los datos del usuario
class UserLogin(BaseModel):
    username: str = "admin"
    password: str = "admin123"

# Modelo para la respuesta de autenticación
class AuthResponse(BaseModel):
    user_id: int
    username: str
    role: str
    access_token: str

# Controlador para manejar el login
@router.post("/login", tags=["Autenticación"], summary="Login de usuario", description="Endpoint para manejar el login del usuario.", response_model=AuthResponse)
async def login(user: UserLogin):
    """
    Endpoint para manejar el login del usuario.
    """
    result = await authenticate_user(user.username, user.password)
    if not result:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return result

# Modelo para la respuesta de refrescar token
class TokenResponse(BaseModel):
    access_token: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "new-fake-jwt-token"
            }
        }

# Controlador para refrescar el token
@router.post("/refresh-token", tags=["Autenticación"], summary="Refrescar token", description="Endpoint para refrescar el token JWT.", response_model=TokenResponse)
async def refresh_token(token: str = Depends(oauth2_scheme)):
    """
    Endpoint para refrescar el token JWT.
    """
    try:
        new_token = refresh_access_token(token)
        return {"access_token": new_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al refrescar el token: {e}")