import mysql.connector 
from mysql.connector import Error
import sys
import os
from typing import Optional, Any
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

# Configurar logger
logger = logging.getLogger('db_conn')



class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = "root"
        self.password = "1234"
        self.database = "clinica_veterinaria"
        self.connection: Optional[mysql.connector.connection.MySQLConnection] = None

    def connect(self) -> bool:
        try:
            logger.info(f"Intentando conectar a la base de datos {self.database} en {self.host}")
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            is_connected = self.connection.is_connected()
            if is_connected:
                logger.info("Conexión a la base de datos establecida exitosamente")
            else:
                logger.warning("No se pudo establecer la conexión a la base de datos")
            return is_connected
        except Error as e:
            logger.error(f"Error al conectar a la base de datos: {str(e)}")
            return False

    def disconnect(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión a la base de datos cerrada")

    def execute_query(self, query: str, params: Optional[tuple] = None) -> bool:
        if not self.connection or not self.connection.is_connected():
            logger.error("Intento de ejecutar query sin conexión activa")
            raise ConnectionError("Database not connected")
        cursor = self.connection.cursor()
        try:
            logger.debug(f"Ejecutando query: {query} con params: {params}")
            cursor.execute(query, params)
            self.connection.commit()
            logger.info("Query ejecutada exitosamente")
            return True
        except Error as e:
            logger.error(f"Error al ejecutar query: {str(e)}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("Database not connected")
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query: str, params: Optional[tuple] = None) -> list:
        """Fetch all results from a query."""
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("Database not connected")
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def validate_user(self, username: str, password: str) -> bool:
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("Database not connected")
        query = """
            SELECT * FROM empleados
            WHERE usuario = %s AND contraseña = %s
        """
        result = self.fetch_one(query, (username, password))
        return result is not None

    # ------------------------------
    # Métodos específicos para DUEÑOS
    # ------------------------------
    
    def insertar_dueno(self, nombre: str, dni: str, telefono: str, email: str, 
                       fecha_nacimiento: str, direccion: str) -> Optional[int]:
        """Inserta un nuevo dueño y retorna su ID."""
        query = """
            INSERT INTO duenos (nombre, dni, telefono, email, fecha_nacimiento, direccion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        if self.execute_query(query, (nombre, dni, telefono, email, fecha_nacimiento, direccion)):
            return self.connection.cursor().lastrowid
        return None

    def obtener_dueno(self, id_dueno: int) -> Optional[Any]:
        """Obtiene un dueño por su ID."""
        query = "SELECT * FROM duenos WHERE id_dueno = %s"
        return self.fetch_one(query, (id_dueno,))

    def obtener_todos_duenos(self) -> list:
        """Obtiene todos los dueños registrados."""
        query = "SELECT * FROM duenos"
        return self.fetch_all(query)

    def actualizar_dueno(self, id_dueno: int, nombre: str = None, telefono: str = None, 
                         email: str = None, direccion: str = None) -> bool:
        """Actualiza datos de un dueño."""
        updates = []
        params = []
        if nombre:
            updates.append("nombre = %s")
            params.append(nombre)
        if telefono:
            updates.append("telefono = %s")
            params.append(telefono)
        if email:
            updates.append("email = %s")
            params.append(email)
        if direccion:
            updates.append("direccion = %s")
            params.append(direccion)
        
        if not updates:
            return False
        
        params.append(id_dueno)
        query = f"UPDATE duenos SET {', '.join(updates)} WHERE id_dueno = %s"
        return self.execute_query(query, tuple(params))

    def eliminar_dueno(self, id_dueno: int) -> bool:
        """Elimina un dueño por su ID."""
        query = "DELETE FROM duenos WHERE id_dueno = %s"
        return self.execute_query(query, (id_dueno,))

    # ------------------------------
    # Métodos específicos para MASCOTAS
    # ------------------------------

    def insertar_mascota(self, nombre: str, especie: str, raza: str, fecha_nacimiento: str,
                        peso: float, sexo: str, id_dueno: int) -> Optional[int]:
        """Inserta una nueva mascota y retorna su ID."""
        query = """
            INSERT INTO mascotas (nombre, especie, raza, fecha_nacimiento, peso, sexo, id_dueno)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        if self.execute_query(query, (nombre, especie, raza, fecha_nacimiento, peso, sexo, id_dueno)):
            return self.connection.cursor().lastrowid
        return None

    def obtener_mascota(self, id_mascota: int) -> Optional[Any]:
        """Obtiene una mascota por su ID."""
        query = "SELECT * FROM mascotas WHERE id_mascota = %s"
        return self.fetch_one(query, (id_mascota,))

    def obtener_mascotas_por_dueno(self, id_dueno: int) -> list:
        """Obtiene todas las mascotas de un dueño."""
        query = "SELECT * FROM mascotas WHERE id_dueno = %s"
        return self.fetch_all(query, (id_dueno,))

    def actualizar_mascota(self, id_mascota: int, peso: float = None, nombre: str = None) -> bool:
        """Actualiza datos de una mascota."""
        updates = []
        params = []
        if peso:
            updates.append("peso = %s")
            params.append(peso)
        if nombre:
            updates.append("nombre = %s")
            params.append(nombre)
        
        if not updates:
            return False
        
        params.append(id_mascota)
        query = f"UPDATE mascotas SET {', '.join(updates)} WHERE id_mascota = %s"
        return self.execute_query(query, tuple(params))

    def eliminar_mascota(self, id_mascota: int) -> bool:
        """Elimina una mascota por su ID."""
        query = "DELETE FROM mascotas WHERE id_mascota = %s"
        return self.execute_query(query, (id_mascota,))

    # ------------------------------
    # Métodos específicos para CITAS
    # ------------------------------

    def insertar_cita(self, fecha: str, hora: str, motivo: str, id_mascota: int,
                     id_empleado: int, estado: str = "pendiente") -> Optional[int]:
        """Inserta una nueva cita y retorna su ID."""
        query = """
            INSERT INTO citas (fecha, hora, motivo, id_mascota, id_empleado, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        if self.execute_query(query, (fecha, hora, motivo, id_mascota, id_empleado, estado)):
            return self.connection.cursor().lastrowid
        return None

    def obtener_cita(self, id_cita: int) -> Optional[Any]:
        """Obtiene una cita por su ID."""
        query = "SELECT * FROM citas WHERE id_cita = %s"
        return self.fetch_one(query, (id_cita,))

    def obtener_citas_por_mascota(self, id_mascota: int) -> list:
        """Obtiene todas las citas de una mascota."""
        query = "SELECT * FROM citas WHERE id_mascota = %s"
        return self.fetch_all(query, (id_mascota,))

    def obtener_citas_por_estado(self, estado: str) -> list:
        """Obtiene todas las citas con un estado específico."""
        query = "SELECT * FROM citas WHERE estado = %s"
        return self.fetch_all(query, (estado,))

    def actualizar_cita(self, id_cita: int, fecha: str = None, hora: str = None,
                       estado: str = None) -> bool:
        """Actualiza datos de una cita."""
        updates = []
        params = []
        if fecha:
            updates.append("fecha = %s")
            params.append(fecha)
        if hora:
            updates.append("hora = %s")
            params.append(hora)
        if estado:
            updates.append("estado = %s")
            params.append(estado)
        
        if not updates:
            return False
        
        params.append(id_cita)
        query = f"UPDATE citas SET {', '.join(updates)} WHERE id_cita = %s"
        return self.execute_query(query, tuple(params))

    def eliminar_cita(self, id_cita: int) -> bool:
        """Elimina una cita por su ID."""
        query = "DELETE FROM citas WHERE id_cita = %s"
        return self.execute_query(query, (id_cita,))

    # ------------------------------
    # Métodos específicos para CONSULTAS
    # ------------------------------

    def insertar_consulta(self, id_cita: int, diagnostico: str = None,
                         tratamiento: str = None, observaciones: str = None) -> Optional[int]:
        """Inserta una nueva consulta y retorna su ID."""
        query = """
            INSERT INTO consultas (id_cita, diagnostico, tratamiento, observaciones)
            VALUES (%s, %s, %s, %s)
        """
        if self.execute_query(query, (id_cita, diagnostico, tratamiento, observaciones)):
            return self.connection.cursor().lastrowid
        return None

    def obtener_consulta(self, id_consulta: int) -> Optional[Any]:
        """Obtiene una consulta por su ID."""
        query = "SELECT * FROM consultas WHERE id_consulta = %s"
        return self.fetch_one(query, (id_consulta,))

    def obtener_consultas_por_cita(self, id_cita: int) -> list:
        """Obtiene todas las consultas de una cita."""
        query = "SELECT * FROM consultas WHERE id_cita = %s"
        return self.fetch_all(query, (id_cita,))

    def actualizar_consulta(self, id_consulta: int, diagnostico: str = None,
                           tratamiento: str = None, observaciones: str = None) -> bool:
        """Actualiza datos de una consulta."""
        updates = []
        params = []
        if diagnostico:
            updates.append("diagnostico = %s")
            params.append(diagnostico)
        if tratamiento:
            updates.append("tratamiento = %s")
            params.append(tratamiento)
        if observaciones:
            updates.append("observaciones = %s")
            params.append(observaciones)
        
        if not updates:
            return False
        
        params.append(id_consulta)
        query = f"UPDATE consultas SET {', '.join(updates)} WHERE id_consulta = %s"
        return self.execute_query(query, tuple(params))

    # ------------------------------
    # Métodos específicos para FACTURAS
    # ------------------------------

    def insertar_factura(self, id_consulta: int, total: float, metodo_pago: str = None,
                        fecha: str = None) -> Optional[int]:
        """Inserta una nueva factura y retorna su ID."""
        query = """
            INSERT INTO facturas (id_consulta, total, metodo_pago, fecha)
            VALUES (%s, %s, %s, %s)
        """
        if self.execute_query(query, (id_consulta, total, metodo_pago, fecha)):
            return self.connection.cursor().lastrowid
        return None

    def obtener_factura(self, id_factura: int) -> Optional[Any]:
        """Obtiene una factura por su ID."""
        query = "SELECT * FROM facturas WHERE id_factura = %s"
        return self.fetch_one(query, (id_factura,))

    def obtener_facturas_por_consulta(self, id_consulta: int) -> list:
        """Obtiene todas las facturas de una consulta."""
        query = "SELECT * FROM facturas WHERE id_consulta = %s"
        return self.fetch_all(query, (id_consulta,))

    def actualizar_factura(self, id_factura: int, total: float = None,
                          metodo_pago: str = None) -> bool:
        """Actualiza datos de una factura."""
        updates = []
        params = []
        if total:
            updates.append("total = %s")
            params.append(total)
        if metodo_pago:
            updates.append("metodo_pago = %s")
            params.append(metodo_pago)
        
        if not updates:
            return False
        
        params.append(id_factura)
        query = f"UPDATE facturas SET {', '.join(updates)} WHERE id_factura = %s"
        return self.execute_query(query, tuple(params))

    # ------------------------------
    # Métodos específicos para EMPLEADOS
    # ------------------------------

    def insertar_empleado(self, nombre: str, dni: str, telefono: str, email: str,
                         fecha_nacimiento: str, salario: float, tipo_empleado: str,
                         usuario: str = None, contraseña: str = None) -> Optional[int]:
        """Inserta un nuevo empleado y retorna su ID."""
        query = """
            INSERT INTO empleados (nombre, dni, telefono, email, fecha_nacimiento, 
                                  salario, tipo_empleado, usuario, contraseña)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        if self.execute_query(query, (nombre, dni, telefono, email, fecha_nacimiento,
                                     salario, tipo_empleado, usuario, contraseña)):
            return self.connection.cursor().lastrowid
        return None

    def obtener_empleado(self, id_empleado: int) -> Optional[Any]:
        """Obtiene un empleado por su ID."""
        query = "SELECT * FROM empleados WHERE id_empleado = %s"
        return self.fetch_one(query, (id_empleado,))

    def obtener_todos_empleados(self) -> list:
        """Obtiene todos los empleados registrados."""
        query = "SELECT * FROM empleados"
        return self.fetch_all(query)

    def actualizar_empleado(self, id_empleado: int, telefono: str = None, email: str = None,
                           salario: float = None, usuario: str = None, contraseña: str = None) -> bool:
        """Actualiza datos de un empleado."""
        updates = []
        params = []
        if telefono:
            updates.append("telefono = %s")
            params.append(telefono)
        if email:
            updates.append("email = %s")
            params.append(email)
        if salario:
            updates.append("salario = %s")
            params.append(salario)
        if usuario:
            updates.append("usuario = %s")
            params.append(usuario)
        if contraseña:
            updates.append("contraseña = %s")
            params.append(contraseña)
        
        if not updates:
            return False
        
        params.append(id_empleado)
        query = f"UPDATE empleados SET {', '.join(updates)} WHERE id_empleado = %s"
        return self.execute_query(query, tuple(params))

    def eliminar_empleado(self, id_empleado: int) -> bool:
        """Elimina un empleado por su ID."""
        query = "DELETE FROM empleados WHERE id_empleado = %s"
        return self.execute_query(query, (id_empleado,))
