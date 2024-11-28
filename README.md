# EVA-TEC-PYTHON

## Descripción

Este es un proyecto de evaluación técnica en Python que consiste en desarrollar una aplicación web con FastAPI. El objetivo es crear APIs REST, integrarlas con herramientas de IA y manejar datos en AWS y bases de datos SQL.

### Requerimientos

- Python 3.8 o superior
- FastAPI
- AWS (S3 para almacenamiento de archivos)
- SQL Server (para el almacenamiento de datos)
- JWT (JSON Web Token) para autenticación

---

## Estructura del Proyecto

```plaintext
C:.
│   db.py
│   main.py
│   __init__.py
│   
├───controllers
│   │   auth_controller.py
│   │   upload_file_controller.py
│   │   
│   └───__pycache__
│           auth_controller.cpython-310.pyc
│           upload_file_controller.cpython-310.pyc
│
├───services
│   │   auth_service.py
│   │   file_upload_service.py
│   │   log_service.py
│   │
│   └───__pycache__
│           auth_service.cpython-310.pyc
│           file_upload_service.cpython-310.pyc
│           log_service.cpython-310.pyc
│
└───__pycache__
        db.cpython-310.pyc
        main.cpython-310.pyc
        __init__.cpython-310.pyc

PS C:\laragon\www\Works\EVA-TEC-PYTHON\app> 

y fuera de app tengo 

venv
.env
file_logs.log
README.md
requirements.txt


Instalación

Clonar el repositorio
git clone https://github.com/Xaviierkasvar/eva-tec-python.git
cd eva-tec-python
Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
Activar el entorno virtual
En Windows:

.\venv\Scripts\activate
En macOS/Linux:

source venv/bin/activate
Instalar dependencias
pip install -r requirements.txt
Cómo ejecutar el proyecto
Para iniciar la aplicación:

Si usas FastAPI:
uvicorn app.main:app --reload

La API estará corriendo en http://127.0.0.1:8000 (FastAPI).

Accede a las rutas de la API para probar las funcionalidades.

Endpoints de la API
1. Inicio de Sesión
Ruta: /login
Método: POST
Descripción: Inicia sesión y devuelve un JWT para el usuario.
Parámetros:
username: Nombre de usuario
password: Contraseña
Respuesta:
token: JWT de autenticación

2. Carga y Validación de Archivos
Ruta: /upload
Método: POST
Descripción: Permite subir un archivo CSV a AWS S3 y almacenarlo en SQL Server.
Parámetros:
file: Archivo CSV
param1, param2: Parámetros adicionales
Respuesta:
Lista de validaciones aplicadas al archivo

3. Renovación de Token
Ruta: /refresh-token
Método: POST
Descripción: Renueva el JWT con un nuevo tiempo de expiración.
Parámetros:
old_token: Token actual
Respuesta:
new_token: Nuevo JWT
Contribución
Si deseas contribuir al proyecto, por favor sigue estos pasos:

Haz un fork del repositorio
Crea una nueva rama (git checkout -b feature-nueva-funcionalidad)
Realiza tus cambios
Haz un commit con tus cambios (git commit -am 'Añadir nueva funcionalidad')
Haz push a la rama (git push origin feature-nueva-funcionalidad)
Crea un pull request
