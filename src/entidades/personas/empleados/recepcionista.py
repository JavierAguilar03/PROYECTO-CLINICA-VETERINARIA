from src.entidades.personas.empleados.empleado import Empleado


class Recepcionista(Empleado):
    """
    Subclase concreta de Empleado.
    Representa al personal de recepcion de la clínica.
    """

    def __init__(self, id_empleado, nombre, dni, telefono, email,
                 fecha_nacimiento, salario, horario):
        super().__init__(id_empleado, nombre, dni, telefono, email, fecha_nacimiento, salario, "Recepcionista")
        self.horario = horario
