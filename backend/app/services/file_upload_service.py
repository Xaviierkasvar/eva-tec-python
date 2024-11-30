from fastapi import HTTPException
from io import BytesIO, StringIO
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
import pandas as pd
from app.db import get_db_connection
from app.services.log_service import store_log

s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

def handle_file_upload(contents: bytes, filename: str, param1: str = None, param2: str = None):
    if not contents.strip():
        raise HTTPException(status_code=400, detail="El archivo está vacío.")
    
    if not filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo no es un CSV.")
    
    validation_results = validate_csv(contents)
    if validation_results:
        raise HTTPException(status_code=400, detail=f"Errores de validación: {validation_results}")
    
    store_csv_data(contents, param1, param2)
    
    s3_key = f"files/{filename}"
    upload_result = upload_file_to_s3(contents, s3_key)
    
    return {
        "upload_result": upload_result,
        "validation_results": validation_results
    }

def upload_file_to_s3(contents: bytes, s3_key: str):
    try:
        with BytesIO(contents) as file_data:
            s3_client.upload_fileobj(file_data, BUCKET_NAME, s3_key)
        message = f"Archivo subido con éxito a {BUCKET_NAME}/{s3_key}"
        store_log("CARGA_DOCUMENTO", message, "INFO")
        return {"message": message}
    except FileNotFoundError:
        message = "El archivo no fue encontrado."
        store_log("CARGA_DOCUMENTO", message, "ERROR")
        raise HTTPException(status_code=404, detail=message)
    except NoCredentialsError:
        message = "Credenciales no encontradas."
        store_log("CARGA_DOCUMENTO", message, "ERROR")
        raise HTTPException(status_code=403, detail=message)
    except PartialCredentialsError:
        message = "Credenciales incompletas."
        store_log("CARGA_DOCUMENTO", message, "ERROR")
        raise HTTPException(status_code=403, detail=message)
    except Exception as e:
        message = f"Ocurrió un error al subir el archivo: {e}"
        store_log("CARGA_DOCUMENTO", message, "ERROR")
        raise HTTPException(status_code=500, detail=message)

def validate_csv(contents: bytes):
    try:
        csv_file = StringIO(contents.decode("utf-8"))
        df = pd.read_csv(csv_file)

        validation_results = []
        if df.shape[1] != 2:
            validation_results.append("El archivo no tiene exactamente 2 columnas.")
        if df.isnull().values.any():
            validation_results.append("El archivo contiene valores vacíos.")
        if not all(df.dtypes == 'object'):
            validation_results.append("El archivo contiene tipos de datos incorrectos.")
        if df.duplicated().any():
            validation_results.append("El archivo contiene registros duplicados.")

        return validation_results
    except Exception as e:
        message = f"Ocurrió un error al validar el archivo: {e}"
        store_log("CARGA_DOCUMENTO", message, "ERROR")
        raise HTTPException(status_code=500, detail=message)

def store_csv_data(contents: bytes, param1: str = None, param2: str = None):
    try:
        csv_file = StringIO(contents.decode("utf-8"))
        df = pd.read_csv(csv_file)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            for index, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO uploaded_files (column1, column2) VALUES (?, ?)",
                    (row['column1'], row['column2'])
                )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

        message = "Archivo procesado y almacenado exitosamente."
        store_log("CARGA_DOCUMENTO", message, "INFO")
    except Exception as e:
        message = f"Ocurrió un error al almacenar el archivo: {e}"
        store_log("CARGA_DOCUMENTO", message, "ERROR")
        raise HTTPException(status_code=500, detail=message)