import logging
from app.db import get_db_connection

# Configurar logging
logging.basicConfig(filename='file_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Función para almacenar logs en la base de datos
def store_log(level: str, message: str, log_type: str, ):
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Convertir los parámetros a cadenas de texto
        level_str = str(level).upper()  # Asegurarse de que el nivel esté en mayúsculas
        message_str = str(message)
        log_type_str = str(log_type)
        
        # Insertar el log en la tabla
        cursor.execute("INSERT INTO logs (level, message, log_type) VALUES (?, ?, ?)", (level_str, message_str, log_type_str))
        
        # Confirmar la transacción
        conn.commit()
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
    except Exception as e:
        logging.error(f"Error al almacenar el log: {e}")