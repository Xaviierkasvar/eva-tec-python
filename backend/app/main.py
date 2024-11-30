from fastapi import FastAPI
import uvicorn
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

# Importar los routers de los controladores
from app.controllers.auth_controller import router as auth_router
from app.controllers.upload_file_controller import router as upload_router
from app.controllers.document_analysis_controller import router as document_analysis_router  # Nuevo controlador
from app.controllers.history_controller import router as history_router  # Nuevo controlador

# Crear la instancia principal de la aplicación FastAPI
app = FastAPI(
    title="Prueba API Python",
    version="0.1.0",
    openapi_version="3.0.3"  # Cambiar a la versión que necesitas
)

# Agregar middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir el acceso desde tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Personalizar el esquema de OpenAPI
def custom_openapi():
    if app.openapi_schema:  # Evita recalcular si ya está definido
        return app.openapi_schema

    # Obtener el esquema por defecto
    openapi_schema = get_openapi(
        title="Swagger APIs Prueba Python OneCore",  # Cambiar el título
        version="1.0.0",  # Cambiar la versión
        description="Documentación de la APIs solicitas en prueba para desarrollo en Python.",
        routes=app.routes,
    )

    # Añadir el esquema de seguridad personalizado
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema

    return app.openapi_schema

# Sobrescribir la función de OpenAPI
app.openapi = custom_openapi

# Incluir los routers en la aplicación FastAPI
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(document_analysis_router)  # Nuevo router
app.include_router(history_router)  # Nuevo router

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)