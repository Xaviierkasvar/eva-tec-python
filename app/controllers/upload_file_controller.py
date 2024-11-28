from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from app.services.file_upload_service import handle_file_upload
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import verify_token
from app.services.log_service import store_log

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    param1: str = None,
    param2: str = None,
):
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
        raise