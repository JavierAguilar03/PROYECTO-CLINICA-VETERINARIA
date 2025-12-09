from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entidades.personas.duenos.dueno import Dueno


class Mascota:
    """
    Clase Mascota
    Propósito: Representar a los animales registrados en la clínica.
    """

    def __init__(self, id_mascota: int, nombre: str, especie: str, raza: str,
                 fecha_nacimiento: str, peso: float, sexo: str, dueno: 'Dueno'):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        self.peso = peso
        self.sexo = sexo
        self.dueno = dueno
