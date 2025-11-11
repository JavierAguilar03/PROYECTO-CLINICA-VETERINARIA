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

    def calcular_salario(self) -> float:
        """El recepcionista recibe un bono fijo de 100€."""
        return self.salario + 100

    def mostrar_info(self) -> str:
        base_info = super().mostrar_info()
        extra = f"\nHorario: {self.horario}"
        return base_info + extra
