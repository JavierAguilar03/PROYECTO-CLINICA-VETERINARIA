from datetime import datetime, date
from typing import List, Optional
from src.entidades.personas.duenos.dueno import Dueño


class Mascota:
    """
    Clase Mascota
    Propósito: Representar a los animales registrados en la clínica.

    Principio SOLID:
    - SRP (Responsabilidad Única): Gestiona exclusivamente la información de la mascota.
    """

    def __init__(self, id_mascota: int, nombre: str, especie: str, raza: str,
                 fecha_nacimiento: str, peso: float, sexo: str, dueño: Dueño):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        # Se espera formato YYYY-MM-DD
        self.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        self.peso = peso
        self.sexo = sexo
        self.dueño = dueño
        self.historial_consultas: List[int] = []  # lista de IDs de consultas

    # ------------------------------
    # Métodos principales
    # ------------------------------

    def mostrar_historial(self) -> str:
        """Muestra el historial de consultas de la mascota."""
        if not self.historial_consultas:
            return f"La mascota {self.nombre} no tiene consultas registradas."
        historial = ", ".join(str(id_c) for id_c in self.historial_consultas)
        return f"Historial de consultas de {self.nombre}: {historial}"

    def actualizar_peso(self, nuevo_peso: float):
        """Actualiza el peso actual de la mascota."""
        if nuevo_peso <= 0:
            raise ValueError("El peso debe ser un número positivo.")
        self.peso = nuevo_peso

    def calcular_edad(self) -> int:
        """Calcula la edad actual de la mascota en años."""
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad

    def registrar_consulta(self, id_consulta: int):
        """Agrega una nueva consulta al historial de la mascota."""
        if id_consulta not in self.historial_consultas:
            self.historial_consultas.append(id_consulta)

    def mostrar_ultima_consulta(self) -> Optional[int]:
        """Devuelve el ID de la última consulta registrada."""
        if not self.historial_consultas:
            return None
        return self.historial_consultas[-1]

    # ------------------------------
    # Representación en texto
    # ------------------------------

    def __str__(self):
        return (
            f"Mascota: {self.nombre} (ID: {self.id_mascota})\n"
            f"Especie: {self.especie} - Raza: {self.raza}\n"
            f"Edad: {self.calcular_edad()} años - Peso: {self.peso} kg\n"
            f"Sexo: {self.sexo}\n"
            f"Dueño: {self.dueño.nombre} (ID: {self.dueño.id_dueño})"
        )
