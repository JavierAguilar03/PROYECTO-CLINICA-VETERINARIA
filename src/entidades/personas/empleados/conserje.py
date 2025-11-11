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

    def calcular_salario(self) -> float:
        """
        Regla ejemplo:
        - Turno nocturno gana un 20% extra.
        """
        if self.turno.lower() == "nocturno":
            return self.salario * 1.20
        return self.salario

    def mostrar_info(self) -> str:
        base_info = super().mostrar_info()
        extra = f"\nTurno: {self.turno}"
        return base_info + extra
