# src/entidades/personas/empleados/empleado.py
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import List, Optional, Tuple
from src.entidades.personas.persona import Persona


class Empleado(Persona, ABC):
    """
    Clase Abstracta Empleado
    Propósito: Representar a los trabajadores de la clínica.

    Mantiene como abstracto `calcular_salario()` para que cada subclase
    implemente su propia regla salarial. Provee implementaciones base
    para los métodos de Persona que son comunes.
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
        self.registro_horario: List[Tuple[datetime.time, datetime.time]] = []  # tuplas (entrada, salida)
        self._credenciales = {"usuario": None, "contraseña": None}

    # ------------------------------
    # Métodos abstractos (subclases deben implementar)
    # ------------------------------

    @abstractmethod
    def calcular_salario(self) -> float:
        """Calcula el salario final del empleado según reglas de la subclase."""
        raise NotImplementedError

    # ------------------------------
    # Métodos concretos reutilizables
    # ------------------------------
    def registrar_horario(self, entrada: str, salida: str):
        """
        Registra el horario de trabajo del empleado.
        Formato de hora: "HH:MM".
        """
        try:
            hora_entrada = datetime.strptime(entrada, "%H:%M").time()
            hora_salida = datetime.strptime(salida, "%H:%M").time()
            self.registro_horario.append((hora_entrada, hora_salida))
        except ValueError:
            raise ValueError("Formato de hora incorrecto. Use 'HH:MM'.")

    def actualizar_salario(self, nuevo_salario: float):
        """Actualiza el salario del empleado (valida que sea positivo)."""
        if nuevo_salario <= 0:
            raise ValueError("El salario debe ser un número positivo.")
        self.salario = nuevo_salario

    def establecer_credenciales(self, usuario: str, contraseña: str):
        """Asigna credenciales de acceso al empleado."""
        self._credenciales["usuario"] = usuario
        self._credenciales["contraseña"] = contraseña

    def validar_credenciales(self, usuario: str, contraseña: str) -> bool:
        """Verifica si las credenciales ingresadas son correctas."""
        return (
            usuario == self._credenciales["usuario"]
            and contraseña == self._credenciales["contraseña"]
        )

    # ------------------------------
    # Métodos heredados de Persona implementados aquí
    # ------------------------------

    def mostrar_info(self) -> str:
        """
        Implementación base de mostrar_info con datos comunes.
        Las subclases pueden sobrescribir y extender esta salida.
        """
        info = (
            f"{self.tipo_empleado}: {self.nombre} (ID: {self.id_empleado})\n"
            f"DNI: {self.dni}\n"
            f"Teléfono: {self.telefono}\n"
            f"Email: {self.email}\n"
            f"Edad: {self.calcular_edad()} años\n"
            f"Salario base: {self.salario} €"
        )
        return info
    
    def calcular_edad(self) -> int:
        """Calcula la edad actual del empleado en años."""
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad

    def actualizar_datos(self, contacto: Optional[str] = None, email: Optional[str] = None, telefono: Optional[str] = None):
        """Actualiza datos personales básicos del empleado."""
        if contacto:
            self.nombre = contacto
        if email:
            self.email = email
        if telefono:
            self.telefono = telefono
