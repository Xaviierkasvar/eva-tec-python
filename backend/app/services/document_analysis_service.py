import boto3
from fastapi import UploadFile
from datetime import datetime
import os
import re
from dotenv import load_dotenv
from app.db import get_db_connection
from app.utils.date_utils import transform_date_for_sqlserver
from app.utils.text_extraction_mapping import KEYWORD_MAPPING
import unicodedata

# Cargar las credenciales de AWS y la base de datos desde el archivo .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Configurar el cliente de Textract
textract_client = boto3.client(
    'textract',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

# === Funciones para procesar documentos ===

def analyze_document_with_textract(file: UploadFile):
    """
    Analiza un documento usando AWS Textract.
    """
    file_content = file.file.read()
    response = textract_client.analyze_document(
        Document={'Bytes': file_content},
        FeatureTypes=['TABLES', 'FORMS']
    )
    return response

def extract_data_from_textract_response(response):
    """
    Extrae datos clave-valor de la respuesta de Textract.
    """
    extracted_data = {}
    blocks_by_id = {block['Id']: block for block in response['Blocks']}

    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET' and 'KEY' in block.get('EntityTypes', []):
            key_text, value_text = extract_key_value(block, blocks_by_id)
            if key_text and value_text:
                extracted_data[key_text.strip()] = value_text.strip()

    return extracted_data

def extract_key_value(block, blocks_by_id):
    """
    Extrae el texto de clave y valor de un bloque de Textract.
    """
    key_text = extract_text_from_relationships(block, blocks_by_id, 'CHILD')
    value_text = ""
    if 'Relationships' in block:
        for rel in block['Relationships']:
            if rel['Type'] == 'VALUE':
                value_block = blocks_by_id[rel['Ids'][0]]
                value_text = extract_text_from_relationships(value_block, blocks_by_id, 'CHILD')
    return key_text, value_text

def extract_text_from_relationships(block, blocks_by_id, relationship_type):
    """
    Extrae texto basado en relaciones específicas dentro de los bloques.
    """
    text = ''
    if 'Relationships' in block:
        for rel in block['Relationships']:
            if rel['Type'] == relationship_type:
                text = ' '.join(
                    child['Text'] for child in (blocks_by_id[child_id] for child_id in rel['Ids'])
                    if child['BlockType'] == 'WORD'
                )
    return text

def normalize_text(text):
    """
    Normaliza un texto eliminando mayúsculas, tildes y espacios adicionales.
    """
    if not text:  # Manejar valores nulos o vacíos
        return ""
    text = text.lower().strip()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

def clean_key(key):
    """
    Limpia una clave para manejar posibles formatos como 'Clave:' o 'Clave : valor'.
    Extrae el valor si está incrustado en la clave.
    """
    if ':' in key:
        parts = key.split(':', 1)  # Dividir solo en la primera aparición
        field_name = parts[0].strip()
        value = parts[1].strip() if len(parts) > 1 else ""
        return field_name, value
    return key.strip(), ""

def find_matching_field(key, keyword_mapping):
    """
    Encuentra el campo correspondiente en el keyword_mapping para una clave dada.
    """
    normalized_key = normalize_text(key)
    for field, keywords in keyword_mapping.items():
        normalized_keywords = [normalize_text(k) for k in keywords]
        if any(normalized_key == keyword for keyword in normalized_keywords):
            return field
    return None

def extract_fields_data(data, keyword_mapping):
    """
    Extrae los campos clave del JSON utilizando el keyword_mapping.
    """
    extracted_data = {}

    for raw_key, raw_value in data.items():
        print(f"Procesando: {raw_key} = {raw_value}")  
        # Limpieza de clave y normalización
        cleaned_key, embedded_value = clean_key(raw_key)
        print("cleaned_key:", cleaned_key)
        print("keyword_mapping:", keyword_mapping)
        matching_field = find_matching_field(cleaned_key, keyword_mapping)

        # Priorizar el valor incrustado si existe
        value = embedded_value if embedded_value else raw_value

        # Si se encuentra un campo coincidente, asignar el valor
        if matching_field:
            extracted_data[matching_field] = value.strip() if value else ""

    return extracted_data

# === Base de datos ===

def save_to_db(table, data):
    """
    Guarda datos en la base de datos según la tabla especificada y retorna el ID del registro.
    
    Args:
        table (str): Nombre de la tabla donde se insertarán los datos
        data (dict): Diccionario con los datos a insertar
    
    Returns:
        int: ID del registro recién insertado
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now()

    try:
        if table == "invoices":
            cursor.execute(
                """
                INSERT INTO invoices (client_name, client_address, supplier_name, supplier_address, invoice_number, 
                invoice_date, total_invoice, products, timestamp) 
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get("client_name"), data.get("client_address"), data.get("supplier_name"), data.get("supplier_address"),
                    data.get("invoice_number"), transform_date_for_sqlserver(data.get("invoice_date")), data.get("total_invoice"), data.get("products"), timestamp
                ),
            )
            # Recuperar el ID insertado para la tabla de invoices
            inserted_id = cursor.fetchone()[0]
        
        elif table == "information":
            cursor.execute(
                """
                INSERT INTO information (description, summary, sentiment_analysis, timestamp) 
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?)
                """,
                (
                    data.get("description"), data.get("summary"), data.get("sentiment_analysis"), timestamp
                ),
            )
            # Recuperar el ID insertado para la tabla de information
            inserted_id = cursor.fetchone()[0]
        
        conn.commit()
        return inserted_id
    
    except Exception as e:
        # Manejar cualquier error de inserción
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

# === Función principal ===

async def analyze_document(file: UploadFile):
    """
    Función principal para analizar un archivo y guardar los resultados en la base de datos.
    """
    response = analyze_document_with_textract(file)
    extracted_data = extract_data_from_textract_response(response)

    # Palabras clave para clasificación
    invoice_keywords = {"invoice_date", "invoice_number", "client_name", "total_invoice"}
    information_keywords = {"description", "summary"}

    extract_fields = extract_fields_data(extracted_data, KEYWORD_MAPPING)
    data_keys = set(extract_fields.keys())

    print("Datos extraídos:", extract_fields)

    if data_keys & invoice_keywords:
        record_id = save_to_db("invoices", extract_fields)
        return {"message": "Factura almacenada en la base de datos.", "id": record_id}
    else:
        record_id = save_to_db("information", extract_fields)
        return {"message": "Información almacenada en la base de datos.", "id": record_id}
