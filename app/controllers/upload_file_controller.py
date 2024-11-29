from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.services.file_upload_service import handle_file_upload
from app.services.auth_service import verify_token
from app.services.log_service import store_log

# Definir el router
router = APIRouter()

# Configurar OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo para la respuesta de subida de archivo
class UploadResponse(BaseModel):
    upload_result: dict
    validation_results: list

    class Config:
        schema_extra = {
            "example": {
                "upload_result": {"message": "Archivo subido con éxito a bucket-name/files/filename.csv"},
                "validation_results": []
            }
        }

# Controlador para manejar la subida de archivos
@router.post("/upload", tags=["Archivos"], summary="Subida de archivo", description="Endpoint para subir archivos CSV.", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    param1: str = None,
    param2: str = None,
):
    """
    Endpoint para subir archivos CSV.
    """
    try:
        payload = verify_token(token)
        role = payload.get("role")
        
        if role != "admin":
            raise HTTPException(status_code=403, detail="No tiene permisos para realizar esta acción.")
        
        contents = await file.read()
        result = handle_file_upload(contents, file.filename, param1, param2)
        
        return result
    except HTTPException as e:
        store_log(e, "ERROR")
        raise e
    except Exception as e:
        store_log(e, "ERROR")
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {e}")