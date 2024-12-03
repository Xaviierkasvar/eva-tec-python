from datetime import datetime
import openai
import os
from fastapi import HTTPException, UploadFile
from app.services.file_upload_service import upload_file_to_s3
from app.db import get_db_connection
from io import BytesIO
import unicodedata
import boto3

# Configuración de OpenAI y AWS
openai.api_key = os.getenv("OPENAI_API_KEY")
textract_client = boto3.client(
    "textract",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-2"
)

# === Funciones de Textract ===

def analyze_document_with_textract(file: UploadFile):
    """Analiza un documento usando AWS Textract."""
    try:
        file_content = file.file.read()
        response = textract_client.analyze_document(
            Document={'Bytes': file_content},
            FeatureTypes=['TABLES', 'FORMS']
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar documento con Textract: {e}")

def extract_data_from_textract_response(response):
    """Extrae datos clave-valor de la respuesta de Textract."""
    extracted_data = {}
    blocks_by_id = {block['Id']: block for block in response['Blocks']}

    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET' and 'KEY' in block.get('EntityTypes', []):
            key_text, value_text = extract_key_value(block, blocks_by_id)
            if key_text and value_text:
                extracted_data[key_text.strip()] = value_text.strip()

    return extracted_data

def extract_key_value(block, blocks_by_id):
    """Extrae el texto de clave y valor de un bloque de Textract."""
    key_text = extract_text_from_relationships(block, blocks_by_id, 'CHILD')
    value_text = ""
    if 'Relationships' in block:
        for rel in block['Relationships']:
            if rel['Type'] == 'VALUE':
                value_block = blocks_by_id[rel['Ids'][0]]
                value_text = extract_text_from_relationships(value_block, blocks_by_id, 'CHILD')
    return key_text, value_text

def extract_text_from_relationships(block, blocks_by_id, relationship_type):
    """Extrae texto basado en relaciones específicas dentro de los bloques."""
    text = ''
    if 'Relationships' in block:
        for rel in block['Relationships']:
            if rel['Type'] == relationship_type:
                text = ' '.join(
                    child['Text'] for child in (blocks_by_id[child_id] for child_id in rel['Ids'])
                    if child['BlockType'] == 'WORD'
                )
    return text

# === Funciones de OpenAI ===

def classify_document(content: str):
    print('key;', os.getenv("OPENAI_API_KEY"));
    """Clasifica el documento usando OpenAI."""
    prompt = f"Clasifica el siguiente texto como Factura o Información:\n\n{content}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=10,
        temperature=0.5,
    )
    classification = response.choices[0].text.strip()
    if classification not in ["Factura", "Información"]:
        raise HTTPException(status_code=422, detail="No se pudo clasificar el documento.")
    return classification

def extract_data(content: str, classification: str):
    """Extrae datos según la clasificación."""
    prompt_map = {
        "Factura": (
            "Extrae los siguientes datos: Cliente (nombre, dirección), Proveedor (nombre, dirección), "
            "Número de factura, fecha, productos (cantidad, nombre, precio unitario, total) y Total de la factura.\n\n"
        ),
        "Información": (
            "Extrae los siguientes datos: descripción del texto, un resumen del contenido y "
            "el análisis de sentimiento (positivo, negativo o neutral).\n\n"
        ),
    }
    prompt = f"{prompt_map[classification]}{content}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=500,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# === Función Principal ===

def analyze_document(file: UploadFile):
    """Procesa un documento cargado."""
    try:
        # Análisis con Textract
        textract_response = analyze_document_with_textract(file)
        textract_data = extract_data_from_textract_response(textract_response)

        # Generación de contenido plano para OpenAI
        plain_content = "\n".join(f"{key}: {value}" for key, value in textract_data.items())

        # Clasificación con OpenAI
        classification = classify_document(plain_content)

        # Extracción de datos con OpenAI
        extracted_data = extract_data(plain_content, classification)

        # Almacenamiento en la base de datos
        inserted_id = store_data_in_db(extracted_data, classification)

        # Subida a S3
        s3_key = f"files/document_analysis/{file.filename}"
        upload_result = upload_file_to_s3(file.file.read(), s3_key)

        return {
            "message": "Procesamiento exitoso",
            "classification": classification,
            "inserted_id": inserted_id,
            "s3_upload_result": upload_result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el documento: {e}")

