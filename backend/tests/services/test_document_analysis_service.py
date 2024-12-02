import pytest
from unittest.mock import patch, MagicMock
from fastapi import UploadFile
from app.services.document_analysis_service import (
    analyze_document_with_textract,
    extract_data_from_textract_response,
    extract_key_value,
    extract_text_from_relationships,
    normalize_text,
    clean_key,
    find_matching_field,
    extract_fields_data,
    save_to_db,
    analyze_document
)

# === Fixtures ===

@pytest.fixture
def mock_textract_response():
    return {
        'Blocks': [
            {'Id': '1', 'BlockType': 'KEY_VALUE_SET', 'EntityTypes': ['KEY'], 'Relationships': [{'Type': 'CHILD', 'Ids': ['2']}]},
            {'Id': '2', 'BlockType': 'WORD', 'Text': 'Invoice Number'},
            {'Id': '3', 'BlockType': 'KEY_VALUE_SET', 'EntityTypes': ['VALUE'], 'Relationships': [{'Type': 'CHILD', 'Ids': ['4']}]},
            {'Id': '4', 'BlockType': 'WORD', 'Text': '12345'}
        ]
    }

@pytest.fixture
def mock_file():
    return UploadFile(filename="test.pdf", file=MagicMock())

# === Pruebas para analyze_document_with_textract ===

@patch('app.services.document_analysis_service.textract_client.analyze_document')
def test_analyze_document_with_textract(mock_analyze_document, mock_file, mock_textract_response):
    mock_analyze_document.return_value = mock_textract_response
    response = analyze_document_with_textract(mock_file)
    assert response == mock_textract_response

# === Pruebas para extract_text_from_relationships ===

def test_extract_text_from_relationships(mock_textract_response):
    blocks_by_id = {block['Id']: block for block in mock_textract_response['Blocks']}
    text = extract_text_from_relationships(mock_textract_response['Blocks'][0], blocks_by_id, 'CHILD')
    assert text == 'Invoice Number'

# === Pruebas para normalize_text ===

def test_normalize_text():
    assert normalize_text('ÁÉÍÓÚáéíóú') == 'aeiouaeiou'
    assert normalize_text('  Text  ') == 'text'
    assert normalize_text('') == ''

# === Pruebas para clean_key ===

def test_clean_key():
    assert clean_key('Key: Value') == ('Key', 'Value')
    assert clean_key('Key : Value') == ('Key', 'Value')
    assert clean_key('Key') == ('Key', '')

# === Pruebas para find_matching_field ===

def test_find_matching_field():
    keyword_mapping = {'field': ['keyword']}
    assert find_matching_field('keyword', keyword_mapping) == 'field'
    assert find_matching_field('nonexistent', keyword_mapping) is None

# === Pruebas para extract_fields_data ===

def test_extract_fields_data():
    data = {'Key: Value': 'Some value'}
    keyword_mapping = {'field': ['key']}
    extracted_data = extract_fields_data(data, keyword_mapping)
    assert extracted_data == {'field': 'Value'}

# === Pruebas para save_to_db ===

@patch('app.services.document_analysis_service.get_db_connection')
def test_save_to_db(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    data = {'client_name': 'Test Client', 'invoice_date': '2023-01-01'}
    record_id = save_to_db('invoices', data)
    assert record_id == 1

# === Pruebas para analyze_document ===

@patch('app.services.document_analysis_service.analyze_document_with_textract')
@patch('app.services.document_analysis_service.extract_data_from_textract_response')
@patch('app.services.document_analysis_service.extract_fields_data')
@patch('app.services.document_analysis_service.save_to_db')
@pytest.mark.asyncio
async def test_analyze_document(mock_save_to_db, mock_extract_fields_data, mock_extract_data_from_textract_response, mock_analyze_document_with_textract, mock_file, mock_textract_response):
    mock_analyze_document_with_textract.return_value = mock_textract_response
    mock_extract_data_from_textract_response.return_value = {'Invoice Number': '12345'}
    mock_extract_fields_data.return_value = {'invoice_number': '12345'}
    mock_save_to_db.return_value = 1

    result = await analyze_document(mock_file)
    assert result == {"message": "Factura almacenada en la base de datos.", "id": 1}