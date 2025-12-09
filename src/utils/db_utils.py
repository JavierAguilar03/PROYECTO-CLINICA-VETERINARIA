"""
Utilidades para gestión de base de datos.
Centraliza la inicialización de conexiones a la BD.
"""
import os
from src.database_conn.db_conn import DatabaseConnection


def init_db():
    """
    Inicializa y retorna una conexión a la base de datos.
    Lee las credenciales desde variables de entorno con valores por defecto.
    """
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    
    return DatabaseConnection(host, user, password, database)
