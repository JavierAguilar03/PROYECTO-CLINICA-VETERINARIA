from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

# Configurar logger
logger = logging.getLogger('entidades.cita')

class Cita:
    """
    Clase Cita
    Propósito: Representar una cita entre una mascota y un veterinario o empleado.
    """

    ESTADOS_VALIDOS = ("pendiente", "completada", "cancelada")

    def __init__(self, id_cita: int, fecha: str, hora: str, motivo: str,
                 id_mascota: int, id_empleado: int, estado: str = "pendiente"):
        self.id_cita = id_cita
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        self.hora = datetime.strptime(hora, "%H:%M").time()
        self.motivo = motivo
        self.id_mascota = id_mascota
        self.id_empleado = id_empleado

        if estado not in Cita.ESTADOS_VALIDOS:
            raise ValueError(f"Estado '{estado}' inválido. Debe ser uno de {Cita.ESTADOS_VALIDOS}.")
        self.estado = estado

    # ------------------------------
    # Métodos de negocio
    # ------------------------------

    def marcar_como_completada(self):
        """Marca la cita como completada."""
        if self.estado == "cancelada":
            raise ValueError("No se puede completar una cita cancelada.")
        self.estado = "completada"

    def cancelar(self):
        """Marca la cita como cancelada."""
        if self.estado == "completada":
            raise ValueError("No se puede cancelar una cita completada.")
        self.estado = "cancelada"

    # ------------------------------
    # Métodos estáticos de acceso a datos
    # ------------------------------

    @staticmethod
    def crear(db, fecha: str, hora: str, motivo: str, id_mascota: int,
              id_empleado: int, estado: str = "pendiente") -> Optional[int]:
        """Crea una nueva cita en la base de datos y retorna su ID."""
        logger.info(f"Creando cita: mascota={id_mascota}, empleado={id_empleado}, fecha={fecha}, estado={estado}")
        try:
            id_cita = db.insertar_cita(fecha, hora, motivo, id_mascota, id_empleado, estado)
            if id_cita:
                logger.info(f"Cita creada exitosamente con ID: {id_cita}")
            else:
                logger.error("Error al crear cita: no se obtuvo ID")
            return id_cita
        except Exception as e:
            logger.exception(f"Excepción al crear cita: {str(e)}")
            raise

    @staticmethod
    def obtener_por_id(db, id_cita: int) -> Optional[Dict[str, Any]]:
        """Obtiene una cita por su ID."""
        return db.obtener_cita(id_cita)

    @staticmethod
    def obtener_por_mascota(db, id_mascota: int) -> List[Dict[str, Any]]:
        """Obtiene todas las citas de una mascota."""
        return db.obtener_citas_por_mascota(id_mascota)

    @staticmethod
    def obtener_por_estado(db, estado: str) -> List[Dict[str, Any]]:
        """Obtiene todas las citas con un estado específico."""
        return db.obtener_citas_por_estado(estado)

    @staticmethod
    def obtener_todas_filtradas(db, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Ejecuta una consulta personalizada para obtener citas filtradas."""
        return db.fetch_all(query, params)

    @staticmethod
    def actualizar_estado(db, id_cita: int, estado: str) -> bool:
        """Actualiza el estado de una cita."""
        if estado not in Cita.ESTADOS_VALIDOS:
            logger.warning(f"Intento de actualizar cita {id_cita} con estado inválido: {estado}")
            raise ValueError(f"Estado '{estado}' inválido. Debe ser uno de {Cita.ESTADOS_VALIDOS}.")
        logger.info(f"Actualizando estado de cita {id_cita} a '{estado}'")
        try:
            resultado = db.actualizar_cita(id_cita, estado=estado)
            if resultado:
                logger.info(f"Cita {id_cita} actualizada exitosamente")
            else:
                logger.error(f"Error al actualizar cita {id_cita}")
            return resultado
        except Exception as e:
            logger.exception(f"Excepción al actualizar cita {id_cita}: {str(e)}")
            raise

    @staticmethod
    def eliminar(db, id_cita: int) -> bool:
        """Elimina una cita de la base de datos."""
        return db.eliminar_cita(id_cita)
