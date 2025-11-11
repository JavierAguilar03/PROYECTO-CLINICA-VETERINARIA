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

    def calcular_salario(self) -> float:
        """El veterinario recibe un bono del 10% sobre el salario base."""
        return self.salario * 1.10

    def mostrar_info(self) -> str:
        base_info = super().mostrar_info()
        extra = (
            f"\nEspecialidad: {self.especialidad}\n"
            f"Número de Colegiado: {self.num_colegiado}\n"
            f"Horario: {self.horario}"
        )
        return base_info + extra
