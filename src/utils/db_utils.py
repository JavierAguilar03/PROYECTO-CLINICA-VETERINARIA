"""
Utilidades para gestión de base de datos.
Centraliza la inicialización de conexiones a la BD.
"""
import os
import logging
from src.database_conn.db_conn import DatabaseConnection

# Configurar logger
logger = logging.getLogger('utils.db_utils')

def init_db():
    """
    Inicializa y retorna una conexión a la base de datos.
    Lee las credenciales desde variables de entorno con valores por defecto.
    """
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    
    logger.info(f"Inicializando conexión a BD: host={host}, database={database}")
    try:
        db = DatabaseConnection(host, user, password, database)
        logger.info("Conexión a BD inicializada exitosamente")
        return db
    except Exception as e:
        logger.exception(f"Error al inicializar conexión a BD: {str(e)}")
        raise
