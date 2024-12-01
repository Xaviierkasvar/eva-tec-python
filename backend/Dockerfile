# Usa la imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala herramientas necesarias y dependencias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    unixodbc-dev \
    libpq-dev \
    gcc \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 && \
    rm -rf /var/lib/apt/lists/*

# Copia los archivos necesarios
COPY requirements.txt ./
COPY app ./app
COPY .env ./

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposición del puerto
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
