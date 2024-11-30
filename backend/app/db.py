import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_HOST')},{os.getenv('DB_PORT')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"UID={os.getenv('DB_USERNAME')};"
        f"PWD={os.getenv('DB_PASSWORD')}"
    )
    return connection