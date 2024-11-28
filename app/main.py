from fastapi import FastAPI
import uvicorn

# Importar los routers de los controladores
from app.controllers.auth_controller import router as auth_router
from app.controllers.upload_file_controller import router as upload_router

# Crear la instancia principal de la aplicación FastAPI
app = FastAPI()

# Incluir los routers en la aplicación FastAPI
app.include_router(auth_router)
app.include_router(upload_router)  # Asegúrate de que este router esté incluido

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
