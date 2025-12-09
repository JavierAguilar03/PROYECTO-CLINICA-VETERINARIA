from datetime import datetime
from typing import TYPE_CHECKING, Optional, List, Dict, Any

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

    # ------------------------------
    # Métodos estáticos de acceso a datos
    # ------------------------------

    @staticmethod
    def crear(db, nombre: str, especie: str, raza: str, fecha_nacimiento: str,
              peso: float, sexo: str, id_dueno: int) -> Optional[int]:
        """Crea una nueva mascota en la base de datos y retorna su ID."""
        return db.insertar_mascota(nombre, especie, raza, fecha_nacimiento, peso, sexo, id_dueno)

    @staticmethod
    def obtener_por_id(db, id_mascota: int) -> Optional[Dict[str, Any]]:
        """Obtiene una mascota por su ID."""
        return db.obtener_mascota(id_mascota)

    @staticmethod
    def obtener_por_dueno(db, id_dueno: int) -> List[Dict[str, Any]]:
        """Obtiene todas las mascotas de un dueño."""
        return db.obtener_mascotas_por_dueno(id_dueno)

    @staticmethod
    def obtener_todas(db) -> List[Dict[str, Any]]:
        """Obtiene todas las mascotas."""
        return db.fetch_all("SELECT m.*, d.nombre as dueno_nombre FROM mascotas m LEFT JOIN duenos d ON m.id_dueno = d.id_dueno")

    @staticmethod
    def actualizar(db, id_mascota: int, peso: float = None, nombre: str = None) -> bool:
        """Actualiza una mascota existente."""
        return db.actualizar_mascota(id_mascota, peso, nombre)

    @staticmethod
    def eliminar(db, id_mascota: int) -> bool:
        """Elimina una mascota de la base de datos."""
        return db.eliminar_mascota(id_mascota)
