from datetime import datetime
from typing import Optional


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
            raise ValueError("El diagnóstico no puede estar vacío.")
        self.diagnostico = diagnostico

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
            raise ValueError("Esta consulta ya está vinculada a una factura.")
        self.id_factura = id_factura

    # ------------------------------
    # Representación legible
    # ------------------------------

    def __str__(self):
        return f"Consulta {self.id_consulta} - Diagnóstico: {self.diagnostico} (Cita {self.id_cita})"
