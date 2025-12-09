from src.entidades.personas.empleados.empleado import Empleado


class Veterinario(Empleado):
    """
    Subclase concreta de Empleado.
    Representa al veterinario de la clínica.
    """

    def __init__(self, id_empleado, nombre, dni, telefono, email,
                 fecha_nacimiento, salario, especialidad, num_colegiado, horario):
        super().__init__(id_empleado, nombre, dni, telefono, email, fecha_nacimiento, salario, "Veterinario")
        self.especialidad = especialidad
        self.num_colegiado = num_colegiado
        self.horario = horario
