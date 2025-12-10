
import unittest
from unittest.mock import patch, MagicMock
from src.database_conn.db_conn import DatabaseConnection


class TestDatabaseConnection(unittest.TestCase):

    # ========== Tests de Conexión ==========
    
    @patch("mysql.connector.connect")
    def test_connect_successful(self, mock_connect):
        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection

        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        connected = db.connect()
        self.assertTrue(connected)

    @patch("mysql.connector.connect")
    def test_connect_failure(self, mock_connect):
        from mysql.connector import Error
        mock_connect.side_effect = Error("Connection error")
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        connected = db.connect()
        self.assertFalse(connected)

    def test_disconnect(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        db.disconnect()
        db.connection.close.assert_called_once()

    # ========== Tests de Operaciones Básicas ==========

    def test_execute_query_success(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        cursor = MagicMock()
        db.connection.cursor.return_value = cursor

        success = db.execute_query("INSERT INTO test VALUES (%s)", ("value",))
        self.assertTrue(success)
        cursor.execute.assert_called_once()
        db.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        from mysql.connector import Error
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        cursor = MagicMock()
        cursor.execute.side_effect = Error("Query error")
        db.connection.cursor.return_value = cursor

        success = db.execute_query("INVALID SQL")
        self.assertFalse(success)
        db.connection.rollback.assert_called_once()

    def test_execute_query_not_connected(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = None
        with self.assertRaises(ConnectionError):
            db.execute_query("SELECT 1")

    def test_execute_insert_success(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        cursor = MagicMock()
        cursor.lastrowid = 42
        db.connection.cursor.return_value = cursor

        last_id = db.execute_insert("INSERT INTO test VALUES (%s)", ("value",))
        self.assertEqual(last_id, 42)
        cursor.execute.assert_called_once()
        db.connection.commit.assert_called_once()

    def test_execute_insert_failure(self):
        from mysql.connector import Error
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        cursor = MagicMock()
        cursor.execute.side_effect = Error("Insert error")
        db.connection.cursor.return_value = cursor

        last_id = db.execute_insert("INSERT INTO test VALUES (%s)", ("value",))
        self.assertIsNone(last_id)
        db.connection.rollback.assert_called_once()

    def test_fetch_one_returns_result(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        cursor = MagicMock()
        cursor.fetchone.return_value = {"usuario": "admin"}
        db.connection.cursor.return_value = cursor

        result = db.fetch_one("SELECT * FROM empleados WHERE id=%s", (1,))
        self.assertEqual(result, {"usuario": "admin"})

    def test_fetch_one_raises_if_not_connected(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = None
        with self.assertRaises(ConnectionError):
            db.fetch_one("SELECT 1")

    def test_fetch_all_returns_list(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        cursor = MagicMock()
        cursor.fetchall.return_value = [{"id": 1}, {"id": 2}]
        db.connection.cursor.return_value = cursor

        results = db.fetch_all("SELECT * FROM test")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], 1)

    def test_fetch_all_not_connected(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = None
        with self.assertRaises(ConnectionError):
            db.fetch_all("SELECT 1")

    def test_validate_user_found(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        db.fetch_one = MagicMock(return_value={"usuario": "admin"})
        valid = db.validate_user("admin", "1234")
        self.assertTrue(valid)

    def test_validate_user_not_found(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        db.fetch_one = MagicMock(return_value=None)
        valid = db.validate_user("admin", "wrong")
        self.assertFalse(valid)

    # ========== Tests para Métodos de DUEÑOS ==========

    def test_insertar_dueno(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_insert = MagicMock(return_value=1)
        id_dueno = db.insertar_dueno("Juan", "12345678A", "666777888", 
                                     "juan@mail.com", "1990-01-01", "Calle Test 1")
        self.assertEqual(id_dueno, 1)
        db.execute_insert.assert_called_once()

    def test_obtener_dueno(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_one = MagicMock(return_value={"id_dueno": 1, "nombre": "Juan"})
        dueno = db.obtener_dueno(1)
        self.assertEqual(dueno["nombre"], "Juan")

    def test_obtener_todos_duenos(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_all = MagicMock(return_value=[{"id_dueno": 1}, {"id_dueno": 2}])
        duenos = db.obtener_todos_duenos()
        self.assertEqual(len(duenos), 2)

    def test_actualizar_dueno(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.actualizar_dueno(1, nombre="Pedro", telefono="111222333")
        self.assertTrue(success)
        db.execute_query.assert_called_once()

    def test_actualizar_dueno_sin_cambios(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        success = db.actualizar_dueno(1)
        self.assertFalse(success)

    def test_eliminar_dueno(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.eliminar_dueno(1)
        self.assertTrue(success)

    # ========== Tests para Métodos de MASCOTAS ==========

    def test_insertar_mascota(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_insert = MagicMock(return_value=10)
        id_mascota = db.insertar_mascota("Rex", "Perro", "Labrador", 
                                        "2020-05-15", 25.5, "Macho", 1)
        self.assertEqual(id_mascota, 10)

    def test_obtener_mascota(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_one = MagicMock(return_value={"id_mascota": 10, "nombre": "Rex"})
        mascota = db.obtener_mascota(10)
        self.assertEqual(mascota["nombre"], "Rex")

    def test_obtener_mascotas_por_dueno(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_all = MagicMock(return_value=[{"id_mascota": 10}, {"id_mascota": 11}])
        mascotas = db.obtener_mascotas_por_dueno(1)
        self.assertEqual(len(mascotas), 2)

    def test_actualizar_mascota(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.actualizar_mascota(10, peso=30.0, nombre="Rex Jr")
        self.assertTrue(success)

    def test_actualizar_mascota_sin_cambios(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        success = db.actualizar_mascota(10)
        self.assertFalse(success)

    def test_eliminar_mascota(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.eliminar_mascota(10)
        self.assertTrue(success)

    # ========== Tests para Métodos de CITAS ==========

    def test_insertar_cita(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_insert = MagicMock(return_value=20)
        id_cita = db.insertar_cita("2024-06-01", "10:00", "Revisión", 10, 5, "pendiente")
        self.assertEqual(id_cita, 20)

    def test_obtener_cita(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_one = MagicMock(return_value={"id_cita": 20, "motivo": "Revisión"})
        cita = db.obtener_cita(20)
        self.assertEqual(cita["motivo"], "Revisión")

    def test_obtener_citas_por_mascota(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_all = MagicMock(return_value=[{"id_cita": 20}, {"id_cita": 21}])
        citas = db.obtener_citas_por_mascota(10)
        self.assertEqual(len(citas), 2)

    def test_obtener_citas_por_estado(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_all = MagicMock(return_value=[{"id_cita": 20, "estado": "completada"}])
        citas = db.obtener_citas_por_estado("completada")
        self.assertEqual(len(citas), 1)

    def test_actualizar_cita(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.actualizar_cita(20, estado="completada")
        self.assertTrue(success)

    def test_actualizar_cita_sin_cambios(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        success = db.actualizar_cita(20)
        self.assertFalse(success)

    def test_eliminar_cita(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.eliminar_cita(20)
        self.assertTrue(success)

    # ========== Tests para Métodos de CONSULTAS ==========

    def test_insertar_consulta(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_insert = MagicMock(return_value=30)
        id_consulta = db.insertar_consulta(20, "Diagnóstico", "Tratamiento", "Observaciones")
        self.assertEqual(id_consulta, 30)

    def test_insertar_consulta_sin_observaciones(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_insert = MagicMock(return_value=31)
        id_consulta = db.insertar_consulta(20, "Diagnóstico", "Tratamiento")
        self.assertEqual(id_consulta, 31)

    def test_obtener_consulta(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_one = MagicMock(return_value={"id_consulta": 30, "diagnostico": "Diagnóstico"})
        consulta = db.obtener_consulta(30)
        self.assertEqual(consulta["diagnostico"], "Diagnóstico")

    def test_obtener_consultas_por_cita(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_all = MagicMock(return_value=[{"id_consulta": 30}])
        consultas = db.obtener_consultas_por_cita(20)
        self.assertEqual(len(consultas), 1)

    def test_actualizar_consulta(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.actualizar_consulta(30, diagnostico="Nuevo diagnóstico")
        self.assertTrue(success)

    def test_actualizar_consulta_sin_cambios(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        success = db.actualizar_consulta(30)
        self.assertFalse(success)

    # ========== Tests para Métodos de FACTURAS ==========

    def test_insertar_factura(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_insert = MagicMock(return_value=40)
        id_factura = db.insertar_factura(30, 150.50, "Tarjeta", "2024-06-01")
        self.assertEqual(id_factura, 40)

    def test_obtener_factura(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_one = MagicMock(return_value={"id_factura": 40, "total": 150.50})
        factura = db.obtener_factura(40)
        self.assertEqual(factura["total"], 150.50)

    def test_obtener_facturas_por_consulta(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_all = MagicMock(return_value=[{"id_factura": 40}])
        facturas = db.obtener_facturas_por_consulta(30)
        self.assertEqual(len(facturas), 1)

    def test_actualizar_factura(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.actualizar_factura(40, total=200.0, metodo_pago="Efectivo")
        self.assertTrue(success)

    def test_actualizar_factura_sin_cambios(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        success = db.actualizar_factura(40)
        self.assertFalse(success)

    # ========== Tests para Métodos de EMPLEADOS ==========

    def test_insertar_empleado(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_insert = MagicMock(return_value=50)
        id_empleado = db.insertar_empleado("Ana", "87654321B", "555666777", 
                                           "ana@mail.com", "1985-03-20", 2500.0, 
                                           "Veterinario", "ana_user", "pass123")
        self.assertEqual(id_empleado, 50)

    def test_obtener_empleado(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_one = MagicMock(return_value={"id_empleado": 50, "nombre": "Ana"})
        empleado = db.obtener_empleado(50)
        self.assertEqual(empleado["nombre"], "Ana")

    def test_obtener_todos_empleados(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.fetch_all = MagicMock(return_value=[{"id_empleado": 50}, {"id_empleado": 51}])
        empleados = db.obtener_todos_empleados()
        self.assertEqual(len(empleados), 2)

    def test_actualizar_empleado(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.actualizar_empleado(50, salario=3000.0, email="ana_nueva@mail.com")
        self.assertTrue(success)

    def test_actualizar_empleado_sin_cambios(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        success = db.actualizar_empleado(50)
        self.assertFalse(success)

    def test_eliminar_empleado(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.execute_query = MagicMock(return_value=True)
        success = db.eliminar_empleado(50)
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main(verbosity=2)
