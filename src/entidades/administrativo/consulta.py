from typing import Optional


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
