
from src.logging.logging_config import get_logger


class Logger:
    """
    Servicio de logging centralizado para el proyecto.
    Cada módulo puede obtener su propio logger llamando a LoggerService(nombre_modulo)
    """

    def __init__(self, module_name: str):
        self.logger = get_logger(module_name)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)
