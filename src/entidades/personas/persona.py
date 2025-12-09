from datetime import datetime


class Persona:
    """
    Clase Persona
    Propósito: Representar de manera general a toda persona registrada en el sistema.
    """

    def __init__(self, nombre: str, dni: str, telefono: str, email: str, fecha_nacimiento: str):
        self.nombre = nombre
        self.dni = dni
        self.telefono = telefono
        self.email = email
        self.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
