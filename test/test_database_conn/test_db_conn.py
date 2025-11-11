
import unittest
from unittest.mock import patch, MagicMock
from src.database_conn.db_conn import DatabaseConnection


class TestDatabaseConnection(unittest.TestCase):

    @patch("mysql.connector.connect")
    def test_connect_successful(self, mock_connect):
        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection

        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        connected = db.connect()
        self.assertTrue(connected)

    @patch("mysql.connector.connect", side_effect=Exception("Connection error"))
    def test_connect_failure(self, mock_connect):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        connected = db.connect()
        self.assertFalse(connected)

    def test_disconnect(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        db.disconnect()
        db.connection.close.assert_called_once()

    def test_execute_query_success(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        cursor = MagicMock()
        db.connection.cursor.return_value = cursor

        success = db.execute_query("INSERT INTO test VALUES (%s)", ("value",))
        self.assertTrue(success)
        cursor.execute.assert_called_once()

    def test_execute_query_failure(self):
        db = DatabaseConnection("localhost", "user", "pass", "clinicadb")
        db.connection = MagicMock()
        db.connection.is_connected.return_value = True
        cursor = MagicMock()
        cursor.execute.side_effect = Exception("Query error")
        db.connection.cursor.return_value = cursor

        success = db.execute_query("INVALID SQL")
        self.assertFalse(success)

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
