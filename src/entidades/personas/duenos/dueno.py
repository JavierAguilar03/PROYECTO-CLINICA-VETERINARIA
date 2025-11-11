from datetime import date
from typing import List
from src.entidades.personas.persona import Persona


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
        self.mascotas: List[dict] = [] 

    # ------------------------------
    # Métodos propios del dueño
    # ------------------------------

    def agregar_mascota(self, mascota: dict):
        """Agrega una nueva mascota a la lista del dueño."""
        self.mascotas.append(mascota)

    def obtener_mascotas(self) -> List[dict]:
        """Devuelve la lista de mascotas asociadas al dueño."""
        return self.mascotas

    def eliminar_mascota(self, id_mascota: int):
        """Elimina una mascota según su ID."""
        self.mascotas = [m for m in self.mascotas if m.get("id_mascota") != id_mascota]

    def actualizar_direccion(self, nueva_direccion: str):
        """Actualiza la dirección del dueño."""
        self.direccion = nueva_direccion

    def buscar_mascota_por_nombre(self, nombre: str) -> List[dict]:
        """Busca mascotas que coincidan (total o parcialmente) con el nombre indicado."""
        return [m for m in self.mascotas if nombre.lower() in m.get("nombre", "").lower()]

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
