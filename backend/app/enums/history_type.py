from enum import Enum

# Enum para los tipos de documento
class HistoryType(str, Enum):
    CARGA_DOCUMENTO = "CARGA_DOCUMENTO"
    IA = "IA"
    INTERACCION_USUARIO = "INTERACCION_USUARIO"
