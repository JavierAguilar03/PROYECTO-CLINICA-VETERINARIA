from datetime import datetime, timedelta


class Cita:
    """
    Clase Cita
    Propósito: Representar una cita entre una mascota y un veterinario o empleado.

    Principio SOLID:
    - SRP (Responsabilidad Única): Gestiona únicamente la información y estado de la cita.
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

        self._hora_fin = None  # Se calculará si se usa obtener_duracion()

    # ------------------------------
    # Métodos de gestión
    # ------------------------------

    def reprogramar(self, nueva_fecha: str, nueva_hora: str):
        """Cambia la fecha y hora de la cita (solo si está pendiente)."""
        if self.estado != "pendiente":
            raise ValueError("Solo se pueden reprogramar citas pendientes.")
        self.fecha = datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
        self.hora = datetime.strptime(nueva_hora, "%H:%M").time()

    def cancelar(self):
        """Marca la cita como cancelada."""
        if self.estado == "completada":
            raise ValueError("No se puede cancelar una cita completada.")
        self.estado = "cancelada"

    def marcar_como_completada(self, hora_fin: str):
        """Marca la cita como completada y registra la hora de finalización."""
        if self.estado == "cancelada":
            raise ValueError("No se puede completar una cita cancelada.")
        self.estado = "completada"
        self._hora_fin = datetime.strptime(hora_fin, "%H:%M").time()

    def obtener_duracion(self) -> timedelta:
        """Devuelve la duración estimada de la cita si tiene hora de fin registrada."""
        if not self._hora_fin:
            raise ValueError("La cita no tiene hora de finalización registrada.")
        hora_inicio_dt = datetime.combine(self.fecha, self.hora)
        hora_fin_dt = datetime.combine(self.fecha, self._hora_fin)
        return hora_fin_dt - hora_inicio_dt

    def mostrar_resumen(self) -> str:
        """Devuelve un resumen legible de la cita."""
        resumen = (
            f"Cita ID: {self.id_cita}\n"
            f"Fecha: {self.fecha.strftime('%Y-%m-%d')} a las {self.hora.strftime('%H:%M')}\n"
            f"Motivo: {self.motivo}\n"
            f"Mascota ID: {self.id_mascota}\n"
            f"Empleado ID: {self.id_empleado}\n"
            f"Estado: {self.estado.capitalize()}"
        )
        if self._hora_fin:
            resumen += f"\nDuración: {self.obtener_duracion()}"
        return resumen

    # ------------------------------
    # Representación de texto
    # ------------------------------

    def __str__(self):
        return f"Cita {self.id_cita} - {self.fecha} {self.hora.strftime('%H:%M')} ({self.estado})"
