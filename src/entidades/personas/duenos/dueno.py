from datetime import date
from typing import List, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from src.entidades.mascotas.mascota import Mascota

from src.entidades.personas.persona import Persona

logger = logging.getLogger('entidades.dueno')


class Dueño(Persona):
    """
    Clase Dueño
    Propósito: Representar al cliente que posee una o más mascotas.

    Principio SOLID aplicado:
    - SRP: Solo gestiona datos y relaciones del dueño.
    """

    def __init__(self, id_dueño: int, nombre: str, dni: str, telefono: str, email: str,
                 fecha_nacimiento: str, direccion: str):
        super().__init__(nombre, dni, telefono, email, fecha_nacimiento)
        self.id_dueño = id_dueño
        self.direccion = direccion
        self.mascotas: List['Mascota'] = []

    # ------------------------------
    # Métodos propios del dueño
    # ------------------------------

    def agregar_mascota(self, mascota: 'Mascota'):
        """Agrega una nueva mascota a la lista del dueño."""
        if mascota not in self.mascotas:
            self.mascotas.append(mascota)
            logger.info(f"Mascota {mascota.nombre} (ID: {mascota.id_mascota}) agregada a dueño {self.nombre} (ID: {self.id_dueño})")
        else:
            logger.warning(f"Mascota {mascota.id_mascota} ya está asociada al dueño {self.id_dueño}")

    def obtener_mascotas(self) -> List['Mascota']:
        """Devuelve la lista de mascotas asociadas al dueño."""
        return self.mascotas

    def eliminar_mascota(self, id_mascota: int):
        """Elimina una mascota según su ID."""
        cantidad_antes = len(self.mascotas)
        self.mascotas = [m for m in self.mascotas if m.id_mascota != id_mascota]
        if len(self.mascotas) < cantidad_antes:
            logger.info(f"Mascota ID {id_mascota} eliminada de dueño {self.nombre} (ID: {self.id_dueño})")
        else:
            logger.warning(f"Mascota ID {id_mascota} no encontrada en lista de dueño {self.id_dueño}")

    def actualizar_direccion(self, nueva_direccion: str):
        """Actualiza la dirección del dueño."""
        direccion_anterior = self.direccion
        self.direccion = nueva_direccion
        logger.info(f"Dirección de dueño {self.nombre} (ID: {self.id_dueño}) actualizada: '{direccion_anterior}' -> '{nueva_direccion}'")

    def buscar_mascota_por_nombre(self, nombre: str) -> List['Mascota']:
        """Busca mascotas que coincidan (total o parcialmente) con el nombre indicado."""
        return [m for m in self.mascotas if nombre.lower() in m.nombre.lower()]

    def buscar_mascota_por_id(self, id_mascota: int) -> 'Mascota':
        """Busca una mascota específica por su ID."""
        for mascota in self.mascotas:
            if mascota.id_mascota == id_mascota:
                return mascota
        return None

    # ------------------------------
    # Implementaciones de métodos abstractos
    # ------------------------------

    def mostrar_info(self) -> str:
        """Devuelve un resumen de los datos personales y sus mascotas."""
        info = (
            f"Dueño: {self.nombre} (ID: {self.id_dueño})\n"
            f"DNI: {self.dni}\n"
            f"Teléfono: {self.telefono}\n"
            f"Email: {self.email}\n"
            f"Dirección: {self.direccion}\n"
            f"Edad: {self.calcular_edad()} años\n"
            f"Mascotas registradas: {len(self.mascotas)}"
        )
        return info

    def actualizar_datos(self, contacto=None, email=None, telefono=None):
        """Actualiza datos personales básicos del dueño."""
        if contacto:
            self.nombre = contacto
        if email:
            self.email = email
        if telefono:
            self.telefono = telefono

    def calcular_edad(self) -> int:
        """Calcula la edad actual del dueño."""
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad

    # ------------------------------
    # Métodos de persistencia SQL
    # ------------------------------

    def save(self, db):
        """Guarda el dueño en la base de datos."""
        try:
            fecha_nac_str = self.fecha_nacimiento.strftime('%Y-%m-%d')
            db.insertar_dueno(self.id_dueño, self.nombre, self.dni, self.telefono,
                            self.email, fecha_nac_str, self.direccion)
            logger.info(f"Dueño {self.nombre} (ID: {self.id_dueño}) guardado en base de datos")
        except Exception as e:
            logger.error(f"Error al guardar Dueño {self.id_dueño}: {e}")
            raise

    def update(self, db):
        """Actualiza el dueño en la base de datos."""
        try:
            fecha_nac_str = self.fecha_nacimiento.strftime('%Y-%m-%d')
            db.actualizar_dueno(self.id_dueño, self.nombre, self.dni, self.telefono,
                              self.email, fecha_nac_str, self.direccion)
            logger.info(f"Dueño {self.nombre} (ID: {self.id_dueño}) actualizado en base de datos")
        except Exception as e:
            logger.error(f"Error al actualizar Dueño {self.id_dueño}: {e}")
            raise

    def delete(self, db):
        """Elimina el dueño de la base de datos."""
        try:
            db.eliminar_dueno(self.id_dueño)
            logger.info(f"Dueño {self.nombre} (ID: {self.id_dueño}) eliminado de base de datos")
        except Exception as e:
            logger.error(f"Error al eliminar Dueño {self.id_dueño}: {e}")
            raise

    @staticmethod
    def load(db, id_dueno: int):
        """Carga un dueño desde la base de datos."""
        try:
            dueno_data = db.obtener_dueno_por_id(id_dueno)
            if dueno_data:
                logger.info(f"Dueño {id_dueno} cargado desde base de datos")
                return Dueño(
                    id_dueño=dueno_data['id_dueno'],
                    nombre=dueno_data['nombre'],
                    dni=dueno_data['dni'],
                    telefono=dueno_data['telefono'],
                    email=dueno_data['email'],
                    fecha_nacimiento=dueno_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                    direccion=dueno_data['direccion']
                )
            logger.warning(f"Dueño {id_dueno} no encontrado en base de datos")
            return None
        except Exception as e:
            logger.error(f"Error al cargar Dueño {id_dueno}: {e}")
            raise
