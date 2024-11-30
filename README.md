# EVA-TEC-PYTHON

## Descripción

**EVA-TEC-PYTHON** es un proyecto de evaluación técnica en Python que utiliza **FastAPI** para desarrollar una aplicación web. El objetivo principal es crear APIs REST que integren herramientas de inteligencia artificial, manejen datos en **AWS** y almacenen información en bases de datos **SQLServer**.

---

## Requerimientos

### Backend
- **Python** 3.8 o superior
- **FastAPI**
- **AWS S3** (para almacenamiento de archivos)
- **SQL Server** (para almacenamiento de datos)
- **JWT** (JSON Web Token) para autenticación

### Frontend
- **Node.js** 14.0 o superior
- **React** 17.0 o superior
- **npm** o **yarn**
- Bibliotecas adicionales:
  - **axios** para llamadas API
  - **react-router-dom** para navegación
  - **material-ui** o **shadcn/ui** para componentes
  - **react-excel-renderer** para exportación a Excel

---

## Estructura del Proyecto

```plaintext
eva-tec-python/
│   README.md
│
├───backend/
│   │   README.md
│   │   requirements.txt
│   │   .env
|   |   file_logs.log
│   │
│   ├───app/
│   │   │   __init__.py
│   │   │   db.py
│   │   │   main.py
│   │   │
│   │   ├───controllers/
│   │   │   │   auth_controller.py
│   │   │   │   upload_file_controller.py
│   │   │   │   history_controller.py
│   │   │
│   │   ├───services/
│   │   │   │   auth_service.py
│   │   │   │   file_upload_service.py
│   │   │   │   log_service.py
│   │   │   │   history_service.py
│   │   │
│   │   └───models/
│   │       │   history_model.py
│   │
│   └───venv/
│
└───frontend/
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

## Instalación y Configuración Backend

### Clonar el Repositorio

```bash
git clone https://github.com/Xaviierkasvar/eva-tec-python.git
cd eva-tec-python
```

### 1. Navegar al directorio backend

```bash
# Dirígete al directorio del backend:
cd backend
```

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### 3. Iniciar servidor FastAPI

```bash
uvicorn app.main:app --reload
```

### 1. Navegar al directorio frontend

```bash
# Dirígete al directorio del backend:
cd frontend
```

### 2. Instalar dependencias npm

```bash
npm install
```

### 3. Iniciar servidor de desarrollo

```bash
npm start
```



### Endpoints y Documentación

- **URL Base**: `http://127.0.0.1:8000`
- **Documentación Swagger**: `http://127.0.0.1:8000/docs`

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

## Notas Adicionales

- Entorno virtual `venv/` está en `.gitignore`
- Configurar archivo `.env` con credenciales de **AWS** y base de datos

## Autor

**Francisco Javier Castillo Barrios**  
📧 javier_castillo_15@hotmail.es

