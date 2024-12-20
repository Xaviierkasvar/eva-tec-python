# EVA-TEC-PYTHON

## Descripción

**EVA-TEC-PYTHON** es un proyecto de evaluación técnica en Python que utiliza **FastAPI** para desarrollar una aplicación web. El objetivo principal es crear APIs REST que integren herramientas de inteligencia artificial, manejen datos en AWS y almacenen información en bases de datos SQLServer. Además, incluye una parte de frontend desarrollada con **React**, donde se implementa un sistema de **login de autenticación** para acceder a la aplicación.

Una vez autenticado, el usuario puede acceder a una vista que muestra un **log de eventos registrados**, donde se puede visualizar y gestionar información relevante. Los eventos incluyen los siguientes campos:

- **ID del evento**
- **Tipo** (Carga de documento, IA, Interacción del usuario)
- **Descripción del evento**
- **Fecha y hora**

Las funcionalidades principales de esta vista incluyen:

- Filtros por **tipo**, **descripción** o **rango de fechas**.
- **Exportación** del contenido a **Excel**.

Este enfoque permite tener una interfaz completa tanto para la gestión de eventos como para el acceso controlado mediante autenticación.

---

## Requerimientos

### Backend
- **Python** 3.10.6 o superior

### Frontend
- **Node.js** 20.12.2 o superior

---

## Estructura del Proyecto

```plaintext
eva-tec-python/
|   docker-compose.yml
│   README.md
│
├───backend/
│   │   Dockerfile
│   │   requirements.txt
│   │   .env
|   |   pytest.ini
│   │
│   ├───app/
│   │   │   __init__.py
│   │   │   db.py
│   │   │   main.py
│   │   │
│   │   ├───controllers/
│   │   │   │   auth_controller.py
|   |   |   |   document_analysis_controller.py
│   │   │   │   upload_file_controller.py
│   │   │   │   history_controller.py
│   │   │
│   │   ├───services/
│   │   │   │   auth_service.py
|   |   |   |   document_analysis_service.py
│   │   │   │   file_upload_service.py
│   │   │   │   log_service.py
│   │   │   │   history_service.py
|   |   |   
│   │   └───utils/
│   │       │   date_utils.py
|   |       |   text_extraction_mapping.py
|   │       |
│   │       └───enums/
│   │           |  history_type.py
│   │
│   ├───tests/
│   │   ├───controllers/
│   │   │   │   test_auth_controller.py
|   |   |   |   test_document_analysis_controller.py
│   │   │   │   test_upload_file_controller.py
│   │   │   │   test_history_controller.py
│   │   │
│   │   └───services/
│   │       │   test_auth_service.py
|   |       |   test_document_analysis_service.py
│   │       │   test_file_upload_service.py
│   │       │   test_log_service.py
│   │       │   test_history_service.py
|   |        
|   ├────modifications/
|   |    |   file_manager.py
|   |    |
│   │    └──services/
│   │       └───document_analysis_service.py
│   │
│   └───venv/
│
└───frontend/
    |   Dockerfile
    │   package.json
    │
    ├───public/
    │   ├───favicon.ico
    │   ├───index.html
    │   ├───logo192.png
    │   ├───logo512.png
    │   ├───manifest.json
    │   └───robots.txt
    │
    ├───src/
    │   ├───components/
    │   │   ├───EventLog.jsx
    │   │   ├───Login.jsx
    │   │
    │   ├───App.css
    │   ├───App.js
    │   ├───App.test.js
    │   ├───index.css
    │   ├───index.js
    │   ├───logo.svg
    │   ├───reportWebVitals.js
    │   └───setupTests.js
    │
    └───node_modules/
```

---

# Instalación y Configuración

## Clonar el Repositorio

```bash
git clone https://github.com/Xaviierkasvar/eva-tec-python.git
cd eva-tec-python
```

## 1. Configuración del Backend

### Navegar al Directorio del Backend

```bash
cd backend
```

### Crear archivo .env

```bash
# Crear o reemplazar archivo .env
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

### Crear y Activar un Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

### Iniciar el Servidor FastAPI

```bash
uvicorn app.main:app --reload
```

## 2. Configuración del Frontend

### Navegar al Directorio del Frontend

```bash
cd frontend
```

### Instalar Dependencias de npm

```bash
npm install
```

### Iniciar el Servidor de Desarrollo

```bash
npm start
```

## 3. Configuración y Ejecución con Docker

### Instalación de Docker

#### En Windows
1. Descarga e instala **Docker Desktop** desde su sitio oficial: [Docker Desktop](https://www.docker.com/products/docker-desktop).
2. Asegúrate de habilitar la integración de WSL 2 durante la instalación si estás utilizando Windows 10 o superior.
3. Asegúrate contar con el archivo .env configurado con las credenciales correctas en la siguente ubicacion: backend/.env.

#### En Linux
1. Sigue las instrucciones para instalar Docker desde el sitio oficial: [Docker Engine](https://docs.docker.com/engine/install/).
2. Asegúrate de que Docker esté ejecutándose:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

3. Si también necesitas Docker Compose, instálalo con:

```bash
sudo apt-get update
sudo apt-get install docker-compose
```

4. Asegúrate contar con el archivo .env configurado con las credenciales correctas en la siguente ubicacion: backend/.env.

### Construir y Levantar los Contenedores

Desde la raíz del proyecto:

1. Construye las imágenes de los contenedores sin utilizar la caché:

```bash
docker-compose build --no-cache
```

2. Levanta los servicios:

```bash
docker-compose up
```

### Verificar la Aplicación
- El servidor backend estará disponible en `http://localhost:8000`
- El servidor frontend estará disponible en `http://localhost:3000`

### Detener los Contenedores

Cuando quieras detener los servicios:

```bash
docker-compose down
```

---

### Endpoints y Documentación

- **URL Base**: `http://127.0.0.1:8000`
- **Documentación Swagger**: `http://127.0.0.1:8000/docs`

---

### Ejecución pruebas unitarias

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
.\venv\Scripts\activate

# Ejecutar las pruebas unitarias
pytest -v --disable-warnings
```

---

# Implementación con OpenAI

## Configuración Previa

### 1. Configuración de API Key

Reemplaza en el archivo `.env` tu clave de OpenAI:
```
OPENAI_API_KEY="tu_clave_de_openai_aqui"
```

### 2. Ejecución del Script de Modificación

Desde la raíz del proyecto, ejecuta:
```bash
python backend/modifications/file_manager.py
```

## Uso del Script de Modificación

Al ejecutar el script, verás el menú interactivo:
```
Seleccione una opción:
1. Reemplazar archivo
2. Revertir cambios
3. Salir
```

### Opciones del Menú

- Ingresa `1` para reemplazar el archivo modificado.
- Ingresa `2` para restaurar el archivo original desde el respaldo.
- Ingresa `3` para salir.

## Notas Importantes

1. **Respaldo automático**: El script guarda el archivo original en la ruta `backend/app/services/backup/`.

2. **Eliminación del respaldo (opcional)**: Después de revertir, el respaldo se elimina automáticamente.

3. **Manejo de errores**: Si el archivo modificado o el respaldo no existen, el script te notificará.

## Características Principales

- Autenticación mediante **JWT**
- Integración con **AWS S3**
- Almacenamiento en **SQL Server**
- Documentación interactiva con **Swagger**

## Contribución

1. Hacer fork del repositorio
2. Crear rama de características
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realizar cambios y commits
4. Push a la rama
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abrir un Pull Request

---

## Notas Adicionales

- Entorno virtual `venv/` está en `.gitignore`
- Configurar archivo `.env` con credenciales de **AWS** y base de datos

## Autor

**Francisco Javier Castillo Barrios**  
📧 javier_castillo_15@hotmail.es

