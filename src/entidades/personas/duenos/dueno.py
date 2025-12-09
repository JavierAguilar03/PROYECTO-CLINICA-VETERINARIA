from src.entidades.personas.persona import Persona


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
