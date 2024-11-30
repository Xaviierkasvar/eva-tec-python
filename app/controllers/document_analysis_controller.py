from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.services.document_analysis_service import analyze_document
from app.services.log_service import store_log  # Importando la función para almacenar logs
from app.services.auth_service import verify_token  # Importando la función para verificar el token

# Configurar OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Definir el router
router = APIRouter()

# Modelo para la respuesta de análisis de documentos
class DocumentAnalysisResponse(BaseModel):
    status: str
    data: dict

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "type": "Factura",
                    "cliente": "Nombre del Cliente",
                    "proveedor": "Nombre del Proveedor",
                    "numero_factura": "12345",
                    "fecha": "2024-11-29",
                    "productos": [
                        {"cantidad": 1, "nombre": "Producto A", "precio_unitario": 100.0, "total": 100.0}
                    ],
                    "total_factura": 100.0
                }
            }
        }

# Controlador para manejar la carga y análisis de documentos
@router.post("/analyze-document", tags=["Análisis de Documentos"], summary="Cargar y analizar documento", description="Endpoint para cargar y analizar documentos PDF, JPG o PNG.", response_model=DocumentAnalysisResponse)
async def upload_document(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    """
    Endpoint para manejar la carga y análisis de documentos.
    """
    try:
        # Verificar el token
        payload = verify_token(token)
        
        # Validar tipo de archivo
        allowed_types = ["application/pdf", "image/jpeg", "image/png"]
        if file.content_type not in allowed_types:
            store_log("IA", f"Tipo de archivo no válido: {file.content_type}", "ERROR")
            raise HTTPException(status_code=400, detail="Tipo de archivo no permitido. Solo se permiten archivos PDF, JPG o PNG.")

        # Procesar el documento
        result = await analyze_document(file)
        store_log("IA", f"{result['message']} ID: {result['id']}", "INFO")
        return {"status": "success", "data": result}

    except Exception as e:
        store_log("IA", f"Error al analizar el documento: {str(e)}", "ERROR")
        raise HTTPException(status_code=500, detail=f"Error al analizar el documento: {e}")