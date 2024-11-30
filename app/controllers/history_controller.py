from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.enums.history_type import HistoryType
from app.services.history_service import get_filtered_history
from app.services.auth_service import verify_token

# Configurar OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Definir el router
router = APIRouter()

# Modelo para la respuesta de historial con paginación
class HistoryResponse(BaseModel):
    status: str
    total_records: int
    total_pages: int
    current_page: int
    page_size: int
    data: list

    class Config:
        json_schema_extra = {
            "example": {
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
        }

# Controlador para obtener el historial de análisis con filtros y paginación
@router.get("/history", tags=["Historial de Documentos"], summary="Obtener historial de análisis con filtros y paginación", response_model=HistoryResponse)
async def get_filtered_history_data(
    type: Optional[HistoryType] = None,
    description: Optional[str] = None,
    start_date: Optional[datetime] = Query(None, description="Fecha de inicio en formato YYYY-MM-DDTHH:MM:SS"),
    end_date: Optional[datetime] = Query(None, description="Fecha de fin en formato YYYY-MM-DDTHH:MM:SS"),
    page: int = 1,
    page_size: int = 10,
    token: str = Depends(oauth2_scheme)
):
    """
    Endpoint para obtener el historial de análisis de documentos con filtros opcionales y paginación.
    Los filtros incluyen tipo, descripción y rango de fechas.
    Si no se pasa ningún filtro, se obtienen todos los datos.
    """
    try:
        # Verificar el token
        payload = verify_token(token)
        print(f"Start Date: {start_date}, End Date: {end_date}")
        # Obtener el historial filtrado y paginado
        history = await get_filtered_history(
            type, 
            description, 
            start_date, 
            end_date, 
            page, 
            page_size
        )
        
        # Retornar la respuesta con la paginación
        return {
            "status": "success",
            "total_records": history['total_records'],
            "total_pages": history['total_pages'],
            "current_page": page,
            "page_size": page_size,
            "data": history['records']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el historial filtrado: {e}")