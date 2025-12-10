from src.entidades.personas.persona import Persona
from typing import Optional, List, Dict, Any
import logging

# Configurar logger
logger = logging.getLogger('entidades.dueno')

class Dueno(Persona):
    """
    Clase Dueño
    Propósito: Representar al cliente que posee una o más mascotas.
    """

    def __init__(self, id_dueno: int, nombre: str, dni: str, telefono: str, email: str,
                 fecha_nacimiento: str, direccion: str):
        super().__init__(nombre, dni, telefono, email, fecha_nacimiento)
        self.id_dueno = id_dueno
        self.direccion = direccion

    # ------------------------------
    # Métodos estáticos de acceso a datos
    # ------------------------------

    @staticmethod
    def crear(db, nombre: str, dni: str, telefono: str, email: str,
              fecha_nacimiento: str, direccion: str) -> Optional[int]:
        """Crea un nuevo dueño en la base de datos y retorna su ID."""
        logger.info(f"Creando dueño '{nombre}' (DNI: {dni})")
        try:
            id_dueno = db.insertar_dueno(nombre, dni, telefono, email, fecha_nacimiento, direccion)
            if id_dueno:
                logger.info(f"Dueño creado exitosamente con ID: {id_dueno}")
            else:
                logger.error("Error al crear dueño: no se obtuvo ID")
            return id_dueno
        except Exception as e:
            logger.exception(f"Excepción al crear dueño: {str(e)}")
            raise

    @staticmethod
    def obtener_por_id(db, id_dueno: int) -> Optional[Dict[str, Any]]:
        """Obtiene un dueño por su ID."""
        return db.obtener_dueno(id_dueno)

    @staticmethod
    def obtener_todos(db) -> List[Dict[str, Any]]:
        """Obtiene todos los dueños."""
        return db.obtener_todos_duenos()

    @staticmethod
    def buscar(db, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Ejecuta una búsqueda personalizada de dueños."""
        return db.fetch_all(query, params)

    @staticmethod
    def actualizar(db, id_dueno: int, nombre: str = None, telefono: str = None,
                   email: str = None, direccion: str = None) -> bool:
        """Actualiza un dueño existente."""
        return db.actualizar_dueno(id_dueno, nombre, telefono, email, direccion)

    @staticmethod
    def eliminar(db, id_dueno: int) -> bool:
        """Elimina un dueño de la base de datos."""
        logger.info(f"Eliminando dueño {id_dueno}")
        try:
            resultado = db.eliminar_dueno(id_dueno)
            if resultado:
                logger.info(f"Dueño {id_dueno} eliminado exitosamente")
            else:
                logger.error(f"Error al eliminar dueño {id_dueno}")
            return resultado
        except Exception as e:
            logger.exception(f"Excepción al eliminar dueño {id_dueno}: {str(e)}")
            raise
