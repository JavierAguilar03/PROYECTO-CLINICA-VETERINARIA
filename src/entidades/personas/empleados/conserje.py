from src.entidades.personas.empleados.empleado import Empleado


class Conserje(Empleado):
    """
    Subclase concreta de Empleado.
    Representa al conserje de la clínica.
    """

    def __init__(self, id_empleado, nombre, dni, telefono, email,
                 fecha_nacimiento, salario, turno):
        super().__init__(id_empleado, nombre, dni, telefono, email, fecha_nacimiento, salario, "Conserje")
        self.turno = turno
