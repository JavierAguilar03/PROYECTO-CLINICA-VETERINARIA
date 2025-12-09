from src.entidades.personas.persona import Persona
from typing import Optional, List, Dict, Any


class Empleado(Persona):
    """
    Clase Empleado
    Propósito: Representar a los trabajadores de la clínica.
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

    # ------------------------------
    # Métodos estáticos de acceso a datos
    # ------------------------------

    @staticmethod
    def crear(db, nombre: str, dni: str, telefono: str, email: str,
              fecha_nacimiento: str, salario: float, tipo_empleado: str,
              usuario: str = None, contraseña: str = None) -> Optional[int]:
        """Crea un nuevo empleado en la base de datos y retorna su ID."""
        return db.insertar_empleado(nombre, dni, telefono, email, fecha_nacimiento,
                                    salario, tipo_empleado, usuario, contraseña)

    @staticmethod
    def obtener_por_id(db, id_empleado: int) -> Optional[Dict[str, Any]]:
        """Obtiene un empleado por su ID."""
        return db.obtener_empleado(id_empleado)

    @staticmethod
    def obtener_todos(db) -> List[Dict[str, Any]]:
        """Obtiene todos los empleados."""
        return db.obtener_todos_empleados()

    @staticmethod
    def actualizar(db, id_empleado: int, telefono: str = None, email: str = None,
                   salario: float = None, usuario: str = None, contraseña: str = None) -> bool:
        """Actualiza un empleado existente."""
        return db.actualizar_empleado(id_empleado, telefono, email, salario, usuario, contraseña)

    @staticmethod
    def eliminar(db, id_empleado: int) -> bool:
        """Elimina un empleado de la base de datos."""
        return db.eliminar_empleado(id_empleado)
