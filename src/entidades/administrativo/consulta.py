from typing import Optional, List, Dict, Any
import logging

# Configurar logger
logger = logging.getLogger('entidades.consulta')

class Consulta:
    """
    Clase Consulta
    Propósito: Registrar la información médica derivada de una cita.
    """

    def __init__(
        self,
        id_consulta: int,
        id_cita: int,
        diagnostico: Optional[str] = None,
        tratamiento: Optional[str] = None,
        observaciones: Optional[str] = None,
    ):
        self.id_consulta = id_consulta
        self.id_cita = id_cita
        self.diagnostico = diagnostico or "No registrado"
        self.tratamiento = tratamiento or "No asignado"
        self.observaciones = observaciones or ""
        self.id_factura: Optional[int] = None

    # ------------------------------
    # Métodos estáticos de acceso a datos
    # ------------------------------

    @staticmethod
    def crear(db, id_cita: int, diagnostico: str = None,
              tratamiento: str = None, observaciones: str = None) -> Optional[int]:
        """Crea una nueva consulta en la base de datos y retorna su ID."""
        logger.info(f"Creando consulta para cita {id_cita}")
        try:
            id_consulta = db.insertar_consulta(id_cita, diagnostico, tratamiento, observaciones)
            if id_consulta:
                logger.info(f"Consulta creada exitosamente con ID: {id_consulta}")
            else:
                logger.error("Error al crear consulta: no se obtuvo ID")
            return id_consulta
        except Exception as e:
            logger.exception(f"Excepción al crear consulta: {str(e)}")
            raise

    @staticmethod
    def obtener_por_id(db, id_consulta: int) -> Optional[Dict[str, Any]]:
        """Obtiene una consulta por su ID."""
        return db.obtener_consulta(id_consulta)

    @staticmethod
    def obtener_por_cita(db, id_cita: int) -> List[Dict[str, Any]]:
        """Obtiene todas las consultas de una cita."""
        return db.obtener_consultas_por_cita(id_cita)

    @staticmethod
    def actualizar(db, id_consulta: int, diagnostico: str = None,
                   tratamiento: str = None, observaciones: str = None) -> bool:
        """Actualiza una consulta existente."""
        logger.info(f"Actualizando consulta {id_consulta}")
        try:
            resultado = db.actualizar_consulta(id_consulta, diagnostico, tratamiento, observaciones)
            if resultado:
                logger.info(f"Consulta {id_consulta} actualizada exitosamente")
            else:
                logger.error(f"Error al actualizar consulta {id_consulta}")
            return resultado
        except Exception as e:
            logger.exception(f"Excepción al actualizar consulta {id_consulta}: {str(e)}")
            raise
