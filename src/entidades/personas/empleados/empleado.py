from src.entidades.personas.persona import Persona


class Empleado(Persona):
    """
    Clase Empleado
    Propósito: Representar a los trabajadores de la clínica.
    """

    def __init__(
        self,
        id_empleado: int,
        nombre: str,
        dni: str,
        telefono: str,
        email: str,
        fecha_nacimiento: str,
        salario: float,
        tipo_empleado: str,
    ):
        super().__init__(nombre, dni, telefono, email, fecha_nacimiento)
        self.id_empleado = id_empleado
        self.salario = salario
        self.tipo_empleado = tipo_empleado
