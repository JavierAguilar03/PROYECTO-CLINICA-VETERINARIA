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

    def calcular_salario(self) -> float:
        """
        Regla ejemplo:
        - Turno nocturno gana un 15% extra.
        - Turno diurno mantiene salario base.
        """
        if self.turno.lower() == "nocturno":
            return self.salario * 1.15
        return self.salario

    def mostrar_info(self) -> str:
        base_info = super().mostrar_info()
        extra = (
            f"\nTurno: {self.turno}\n"
            f"Área asignada: {self.area_asignada}"
        )
        return base_info + extra
