from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.services.auth_service import authenticate_user, verify_token, refresh_access_token

# Definir el router
router = APIRouter()

# Configurar OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo para recibir los datos del usuario
class UserLogin(BaseModel):
    username: str
    password: str

# Controlador para manejar el login
@router.post("/login")
async def login(user: UserLogin):
    """
    Endpoint para manejar el login del usuario.
    """
    result = await authenticate_user(user.username, user.password)
    if not result:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return result

# Controlador para refrescar el token
@router.post("/refresh-token")
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