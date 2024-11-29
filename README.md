# EVA-TEC-PYTHON

## Descripción

**EVA-TEC-PYTHON** es un proyecto de evaluación técnica en Python que utiliza **FastAPI** para desarrollar una aplicación web. El objetivo principal es crear APIs REST que integren herramientas de inteligencia artificial, manejen datos en **AWS** y almacenen información en bases de datos **SQLServer**.

---

## Requerimientos

- **Python** 3.8 o superior
- **FastAPI**
- **AWS S3** (para almacenamiento de archivos)
- **SQL Server** (para el almacenamiento de datos)
- **JWT** (JSON Web Token) para autenticación

---

## Estructura del Proyecto

```plaintext
eva-tec-python/
│   README.md
│   requirements.txt
│   .env
│   file_logs.log
│
├───app
│   │   __init__.py
│   │   main.py
│   │
│   ├───controllers
│   │   │   auth_controller.py
│   │   │   upload_file_controller.py
│   │
│   ├───services
│   │   │   auth_service.py
│   │   │   file_upload_service.py
│   │   │   log_service.py
│   │
└───venv/  # Entorno virtual
```

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Xaviierkasvar/eva-tec-python.git
cd eva-tec-python
```

### 2. Configurar Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Ejecución del Proyecto

### Iniciar Servidor

```bash
uvicorn app.main:app --reload
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
📧 javier_castillo_15@hotmail.com

