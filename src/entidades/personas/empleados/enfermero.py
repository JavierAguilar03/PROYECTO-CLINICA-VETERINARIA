from src.entidades.personas.empleados.empleado import Empleado


class Enfermero(Empleado):
    """
    Subclase concreta de Empleado.
    Representa a un enfermero de la clínica.
    """

    def __init__(self, id_empleado, nombre, dni, telefono, email,
                 fecha_nacimiento, salario, turno, area_asignada):
        super().__init__(id_empleado, nombre, dni, telefono, email, fecha_nacimiento, salario, "Enfermero")
        self.turno = turno
        self.area_asignada = area_asignada
