from datetime import datetime, date
from typing import List, Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from src.entidades.personas.duenos.dueno import Dueno
    from src.entidades.administrativo.consulta import Consulta

logger = logging.getLogger('entidades.mascota')


class Mascota:
    """
    Clase Mascota
    Propósito: Representar a los animales registrados en la clínica.

    Principio SOLID:
    - SRP (Responsabilidad Única): Gestiona exclusivamente la información de la mascota.
    """

    def __init__(self, id_mascota: int, nombre: str, especie: str, raza: str,
                 fecha_nacimiento: str, peso: float, sexo: str, dueno: 'Dueno'):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        # Se espera formato YYYY-MM-DD
        self.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        self.peso = peso
        self.sexo = sexo
        self.dueno = dueno
        self.historial_consultas: List[int] = []  # lista de IDs de consultas
        self._consultas_cache: List['Consulta'] = []  # cache opcional para objetos Consulta

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
            logger.error(f"Intento de actualizar peso de mascota {self.id_mascota} con valor inválido: {nuevo_peso}")
            raise ValueError("El peso debe ser un número positivo.")
        peso_anterior = self.peso
        self.peso = nuevo_peso
        logger.info(f"Peso de mascota {self.nombre} (ID: {self.id_mascota}) actualizado: {peso_anterior}kg -> {nuevo_peso}kg")

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
            logger.info(f"Consulta {id_consulta} registrada en historial de mascota {self.nombre} (ID: {self.id_mascota})")
        else:
            logger.warning(f"Consulta {id_consulta} ya existe en historial de mascota {self.id_mascota}")

    def mostrar_ultima_consulta(self) -> Optional[int]:
        """Devuelve el ID de la última consulta registrada."""
        if not self.historial_consultas:
            return None
        return self.historial_consultas[-1]

    def agregar_consulta_objeto(self, consulta: 'Consulta'):
        """Agrega un objeto Consulta al cache interno de la mascota."""
        if consulta.id_consulta not in self.historial_consultas:
            self.historial_consultas.append(consulta.id_consulta)
        if consulta not in self._consultas_cache:
            self._consultas_cache.append(consulta)

    def obtener_consultas_objetos(self) -> List['Consulta']:
        """Devuelve la lista de objetos Consulta cacheados."""
        return self._consultas_cache

    def limpiar_cache_consultas(self):
        """Limpia el cache de consultas (útil si se necesita recargar desde BD)."""
        self._consultas_cache = []

    # ------------------------------
    # Métodos de persistencia SQL
    # ------------------------------

    def save(self, db):
        """Guarda la mascota en la base de datos."""
        try:
            fecha_nac_str = self.fecha_nacimiento.strftime('%Y-%m-%d')
            db.insertar_mascota(self.id_mascota, self.nombre, self.especie, self.raza,
                              fecha_nac_str, self.peso, self.sexo, self.dueno.id_dueno)
            logger.info(f"Mascota {self.nombre} (ID: {self.id_mascota}) guardada en base de datos")
        except Exception as e:
            logger.error(f"Error al guardar Mascota {self.id_mascota}: {e}")
            raise

    def update(self, db):
        """Actualiza la mascota en la base de datos."""
        try:
            fecha_nac_str = self.fecha_nacimiento.strftime('%Y-%m-%d')
            db.actualizar_mascota(self.id_mascota, self.nombre, self.especie, self.raza,
                                fecha_nac_str, self.peso, self.sexo, self.dueno.id_dueno)
            logger.info(f"Mascota {self.nombre} (ID: {self.id_mascota}) actualizada en base de datos")
        except Exception as e:
            logger.error(f"Error al actualizar Mascota {self.id_mascota}: {e}")
            raise

    def delete(self, db):
        """Elimina la mascota de la base de datos."""
        try:
            db.eliminar_mascota(self.id_mascota)
            logger.info(f"Mascota {self.nombre} (ID: {self.id_mascota}) eliminada de base de datos")
        except Exception as e:
            logger.error(f"Error al eliminar Mascota {self.id_mascota}: {e}")
            raise

    @staticmethod
    def load(db, id_mascota: int, dueno):
        """Carga una mascota desde la base de datos."""
        try:
            mascota_data = db.obtener_mascota_por_id(id_mascota)
            if mascota_data:
                logger.info(f"Mascota {id_mascota} cargada desde base de datos")
                return Mascota(
                    id_mascota=mascota_data['id_mascota'],
                    nombre=mascota_data['nombre'],
                    especie=mascota_data['especie'],
                    raza=mascota_data['raza'],
                    fecha_nacimiento=mascota_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                    peso=mascota_data['peso'],
                    sexo=mascota_data['sexo'],
                    dueno=dueno
                )
            logger.warning(f"Mascota {id_mascota} no encontrada en base de datos")
            return None
        except Exception as e:
            logger.error(f"Error al cargar Mascota {id_mascota}: {e}")
            raise

    # ------------------------------
    # Representación en texto
    # ------------------------------

    def __str__(self):
        return (
            f"Mascota: {self.nombre} (ID: {self.id_mascota})\n"
            f"Especie: {self.especie} - Raza: {self.raza}\n"
            f"Edad: {self.calcular_edad()} años - Peso: {self.peso} kg\n"
            f"Sexo: {self.sexo}\n"
            f"Dueño: {self.dueno.nombre} (ID: {self.dueno.id_dueno})"
        )
