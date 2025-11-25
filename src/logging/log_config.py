"""
Módulo de utilidades para configurar el sistema de logging de la aplicación.
"""
import logging
import logging.config
import os


def setup_logging(config_path: str = None):
    """
    Configura el sistema de logging usando el archivo de configuración.
    
    Args:
        config_path: Ruta al archivo de configuración. Si es None, usa la ruta por defecto.
    """
    if config_path is None:
        # Ruta por defecto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'logging.conf')
    
    # Crear directorio de logs si no existe
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(config_path))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Cargar configuración
    try:
        logging.config.fileConfig(config_path, disable_existing_loggers=False)
        logging.info("Sistema de logging configurado correctamente")
    except Exception as e:
        # Si falla, configurar logging básico
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.warning(f"No se pudo cargar logging.conf: {e}. Usando configuración básica.")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger con el nombre especificado.
    
    Args:
        name: Nombre del logger (ej: 'db_conn', 'entidades.factura')
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)
