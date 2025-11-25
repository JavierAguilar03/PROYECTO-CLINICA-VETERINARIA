# src/entidades/personas/empleados/empleado.py
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import List, Optional, Tuple
import logging
from src.entidades.personas.persona import Persona

logger = logging.getLogger('entidades.empleado')


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
            logger.error(f"Intento de asignar salario inválido ({nuevo_salario}) a empleado {self.id_empleado}")
            raise ValueError("El salario debe ser un número positivo.")
        salario_anterior = self.salario
        self.salario = nuevo_salario
        logger.info(f"Salario de empleado {self.id_empleado} actualizado de {salario_anterior} a {nuevo_salario}")

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

    # ------------------------------
    # Métodos de persistencia SQL
    # ------------------------------

    def save(self, db):
        """Guarda el empleado en la base de datos."""
        try:
            fecha_nac_str = self.fecha_nacimiento.strftime('%Y-%m-%d')
            db.insertar_empleado(self.id_empleado, self.nombre, self.dni, self.telefono,
                               self.email, fecha_nac_str, self.salario, self.tipo_empleado,
                               self._credenciales.get('usuario'), 
                               self._credenciales.get('contraseña'))
            logger.info(f"Empleado {self.nombre} (ID: {self.id_empleado}) guardado en base de datos")
        except Exception as e:
            logger.error(f"Error al guardar Empleado {self.id_empleado}: {e}")
            raise

    def update(self, db):
        """Actualiza el empleado en la base de datos."""
        try:
            fecha_nac_str = self.fecha_nacimiento.strftime('%Y-%m-%d')
            db.actualizar_empleado(self.id_empleado, self.nombre, self.dni, self.telefono,
                                 self.email, fecha_nac_str, self.salario, self.tipo_empleado,
                                 self._credenciales.get('usuario'),
                                 self._credenciales.get('contraseña'))
            logger.info(f"Empleado {self.nombre} (ID: {self.id_empleado}) actualizado en base de datos")
        except Exception as e:
            logger.error(f"Error al actualizar Empleado {self.id_empleado}: {e}")
            raise

    def delete(self, db):
        """Elimina el empleado de la base de datos."""
        try:
            db.eliminar_empleado(self.id_empleado)
            logger.info(f"Empleado {self.nombre} (ID: {self.id_empleado}) eliminado de base de datos")
        except Exception as e:
            logger.error(f"Error al eliminar Empleado {self.id_empleado}: {e}")
            raise

    @staticmethod
    def load(db, id_empleado: int):
        """Carga un empleado desde la base de datos."""
        try:
            empleado_data = db.obtener_empleado_por_id(id_empleado)
            if empleado_data:
                logger.info(f"Empleado {id_empleado} cargado desde base de datos")
                # Crear instancia según el tipo de empleado
                from src.entidades.personas.empleados.veterinario import Veterinario
                from src.entidades.personas.empleados.recepcionista import Recepcionista
                from src.entidades.personas.empleados.enfermero import Enfermero
                from src.entidades.personas.empleados.conserje import Conserje
                
                tipo = empleado_data['tipo_empleado']
                if tipo == 'Veterinario':
                    empleado = Veterinario(
                        id_empleado=empleado_data['id_empleado'],
                        nombre=empleado_data['nombre'],
                        dni=empleado_data['dni'],
                        telefono=empleado_data['telefono'],
                        email=empleado_data['email'],
                        fecha_nacimiento=empleado_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                        salario=empleado_data['salario'],
                        especialidad=empleado_data.get('especialidad', ''),
                        num_colegiado=empleado_data.get('num_colegiado', ''),
                        horario=empleado_data.get('horario', '')
                    )
                elif tipo == 'Recepcionista':
                    empleado = Recepcionista(
                        id_empleado=empleado_data['id_empleado'],
                        nombre=empleado_data['nombre'],
                        dni=empleado_data['dni'],
                        telefono=empleado_data['telefono'],
                        email=empleado_data['email'],
                        fecha_nacimiento=empleado_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                        salario=empleado_data['salario'],
                        horario=empleado_data.get('horario', '')
                    )
                elif tipo == 'Enfermero':
                    empleado = Enfermero(
                        id_empleado=empleado_data['id_empleado'],
                        nombre=empleado_data['nombre'],
                        dni=empleado_data['dni'],
                        telefono=empleado_data['telefono'],
                        email=empleado_data['email'],
                        fecha_nacimiento=empleado_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                        salario=empleado_data['salario'],
                        turno=empleado_data.get('turno', ''),
                        area_asignada=empleado_data.get('area_asignada', '')
                    )
                elif tipo == 'Conserje':
                    empleado = Conserje(
                        id_empleado=empleado_data['id_empleado'],
                        nombre=empleado_data['nombre'],
                        dni=empleado_data['dni'],
                        telefono=empleado_data['telefono'],
                        email=empleado_data['email'],
                        fecha_nacimiento=empleado_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                        salario=empleado_data['salario'],
                        turno=empleado_data.get('turno', '')
                    )
                else:
                    # Por defecto crear Empleado genérico (aunque no debería ocurrir)
                    empleado = Empleado(
                        id_empleado=empleado_data['id_empleado'],
                        nombre=empleado_data['nombre'],
                        dni=empleado_data['dni'],
                        telefono=empleado_data['telefono'],
                        email=empleado_data['email'],
                        fecha_nacimiento=empleado_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                        salario=empleado_data['salario'],
                        tipo_empleado=tipo
                    )
                
                # Establecer credenciales si existen
                if empleado_data.get('usuario') and empleado_data.get('contraseña'):
                    empleado.establecer_credenciales(
                        empleado_data['usuario'],
                        empleado_data['contraseña']
                    )
                
                return empleado
            logger.warning(f"Empleado {id_empleado} no encontrado en base de datos")
            return None
        except Exception as e:
            logger.error(f"Error al cargar Empleado {id_empleado}: {e}")
            raise
