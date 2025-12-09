from datetime import datetime


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
