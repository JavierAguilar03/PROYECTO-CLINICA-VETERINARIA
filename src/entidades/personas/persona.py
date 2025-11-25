from abc import ABC, abstractmethod
from datetime import date, datetime
import logging

logger = logging.getLogger('entidades.persona')


class Persona(ABC):
    """
    Clase Abstracta Persona
    Propósito: Representar de manera general a toda persona registrada en el sistema
    (dueños y empleados).

    Principios SOLID aplicados:
    - SRP (Responsabilidad Única): Gestiona únicamente información personal.
    - OCP (Abierto/Cerrado): Permite crear nuevos tipos de personas sin modificar la clase base.
    """

    def __init__(self, nombre: str, dni: str, telefono: str, email: str, fecha_nacimiento: str):
        self.nombre = nombre
        self.dni = dni
        self.telefono = telefono
        self.email = email
        self.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()

    @abstractmethod
    def mostrar_info(self) -> str:
        """Devuelve un resumen de los datos personales."""
        pass

    @abstractmethod
    def actualizar_datos(self, contacto: str = None, email: str = None, telefono: str = None):
        """Actualiza los datos de contacto de la persona."""
        pass

    @abstractmethod
    def calcular_edad(self) -> int:
        """Calcula la edad actual de la persona en años."""
        pass
