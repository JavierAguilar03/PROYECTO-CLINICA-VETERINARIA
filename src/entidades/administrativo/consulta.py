from datetime import datetime
from typing import Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from src.entidades.administrativo.factura import Factura
    from src.entidades.administrativo.cita import Cita

logger = logging.getLogger('entidades.consulta')


class Consulta:
    """
    Clase Consulta
    Propósito: Registrar la información médica derivada de una cita.

    Principio SOLID:
    - OCP (Abierto/Cerrado): Permite crear nuevos tipos de consultas sin modificar esta clase base.
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
        self.fecha_registro = datetime.now()

    # ------------------------------
    # Métodos principales
    # ------------------------------

    def registrar_diagnostico(self, diagnostico: str):
        """Registra o actualiza el diagnóstico médico."""
        if not diagnostico.strip():
            logger.error(f"Intento de registrar diagnóstico vacío en Consulta {self.id_consulta}")
            raise ValueError("El diagnóstico no puede estar vacío.")
        self.diagnostico = diagnostico
        logger.info(f"Diagnóstico registrado en Consulta {self.id_consulta}")

    def mostrar_detalle(self) -> str:
        """Muestra la información completa de la consulta."""
        detalle = (
            f"Consulta ID: {self.id_consulta}\n"
            f"Cita asociada: {self.id_cita}\n"
            f"Fecha de registro: {self.fecha_registro.strftime('%Y-%m-%d %H:%M')}\n"
            f"Diagnóstico: {self.diagnostico}\n"
            f"Tratamiento: {self.tratamiento}\n"
            f"Observaciones: {self.observaciones or 'Sin observaciones'}\n"
            f"Factura asociada: {self.id_factura if self.id_factura else 'No vinculada'}"
        )
        return detalle

    def actualizar_tratamiento(self, nuevo_tratamiento: str):
        """Actualiza el tratamiento prescrito."""
        if not nuevo_tratamiento.strip():
            raise ValueError("El tratamiento no puede estar vacío.")
        self.tratamiento = nuevo_tratamiento

    def agregar_observacion(self, texto: str):
        """Agrega una observación adicional al registro."""
        if not texto.strip():
            raise ValueError("La observación no puede estar vacía.")
        self.observaciones += (f"\n{texto}" if self.observaciones else texto)

    def vincular_factura(self, id_factura: int):
        """Asocia la consulta con una factura."""
        if self.id_factura is not None:
            logger.warning(f"Intento de vincular factura {id_factura} a Consulta {self.id_consulta} que ya tiene factura {self.id_factura}")
            raise ValueError("Esta consulta ya está vinculada a una factura.")
        self.id_factura = id_factura
        logger.info(f"Factura {id_factura} vinculada a Consulta {self.id_consulta}")

    # ------------------------------
    # Métodos de persistencia SQL
    # ------------------------------

    def save(self, db):
        """Guarda la consulta en la base de datos."""
        try:
            db.insertar_consulta(self.id_consulta, self.id_cita, self.id_veterinario,
                               self.diagnostico, self.tratamiento, self.observaciones)
            logger.info(f"Consulta {self.id_consulta} guardada en base de datos")
        except Exception as e:
            logger.error(f"Error al guardar Consulta {self.id_consulta}: {e}")
            raise

    def update(self, db):
        """Actualiza la consulta en la base de datos."""
        try:
            db.actualizar_consulta(self.id_consulta, self.diagnostico, 
                                 self.tratamiento, self.observaciones)
            logger.info(f"Consulta {self.id_consulta} actualizada en base de datos")
        except Exception as e:
            logger.error(f"Error al actualizar Consulta {self.id_consulta}: {e}")
            raise

    def delete(self, db):
        """Elimina la consulta de la base de datos."""
        try:
            db.eliminar_consulta(self.id_consulta)
            logger.info(f"Consulta {self.id_consulta} eliminada de base de datos")
        except Exception as e:
            logger.error(f"Error al eliminar Consulta {self.id_consulta}: {e}")
            raise

    @staticmethod
    def load(db, id_consulta: int):
        """Carga una consulta desde la base de datos."""
        try:
            consulta_data = db.obtener_consulta_por_id(id_consulta)
            if consulta_data:
                logger.info(f"Consulta {id_consulta} cargada desde base de datos")
                return Consulta(
                    id_consulta=consulta_data['id_consulta'],
                    id_cita=consulta_data['id_cita'],
                    id_veterinario=consulta_data['id_veterinario'],
                    diagnostico=consulta_data['diagnostico'],
                    tratamiento=consulta_data['tratamiento'],
                    observaciones=consulta_data['observaciones']
                )
            logger.warning(f"Consulta {id_consulta} no encontrada en base de datos")
            return None
        except Exception as e:
            logger.error(f"Error al cargar Consulta {id_consulta}: {e}")
            raise

    # ------------------------------
    # Representación legible
    # ------------------------------

    def __str__(self):
        return f"Consulta {self.id_consulta} - Diagnóstico: {self.diagnostico} (Cita {self.id_cita})"
