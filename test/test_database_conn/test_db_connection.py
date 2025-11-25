"""
Tests para el módulo de conexión a la base de datos.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database_conn.db_conn import DatabaseConnection


class TestDatabaseConnection(unittest.TestCase):
    """Tests para la clase DatabaseConnection."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.db = DatabaseConnection('localhost', 'test_user', 'test_pass', 'test_db')
    
    def test_init(self):
        """Test de inicialización de la clase."""
        self.assertEqual(self.db.host, 'localhost')
        self.assertEqual(self.db.user, 'test_user')
        self.assertEqual(self.db.password, 'test_pass')
        self.assertEqual(self.db.database, 'test_db')
        self.assertIsNone(self.db.connection)
    
    @patch('mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        """Test de conexión exitosa."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        mock_connect.return_value = mock_conn
        
        result = self.db.connect()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.db.connection)
        mock_connect.assert_called_once()
    
    @patch('mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        """Test de fallo en conexión."""
        mock_connect.side_effect = Exception("Connection failed")
        
        result = self.db.connect()
        
        self.assertFalse(result)
    
    def test_disconnect(self):
        """Test de desconexión."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        self.db.connection = mock_conn
        
        self.db.disconnect()
        
        mock_conn.close.assert_called_once()
    
    @patch.object(DatabaseConnection, 'execute_query')
    def test_insertar_dueno(self, mock_execute):
        """Test de inserción de dueño."""
        mock_execute.return_value = True
        mock_cursor = Mock()
        mock_cursor.lastrowid = 123
        self.db.connection = Mock()
        self.db.connection.cursor.return_value = mock_cursor
        
        result = self.db.insertar_dueno('Juan Pérez', '12345678A', '600000000', 
                                       'juan@email.com', '1990-01-01', 'Calle Test')
        
        self.assertEqual(result, 123)
    
    def test_fetch_one_without_connection(self):
        """Test de fetch_one sin conexión."""
        with self.assertRaises(ConnectionError):
            self.db.fetch_one("SELECT * FROM test")


class TestDatabaseQueries(unittest.TestCase):
    """Tests para queries específicas."""
    
    @patch('mysql.connector.connect')
    def setUp(self, mock_connect):
        """Configuración con conexión mock."""
        self.db = DatabaseConnection('localhost', 'test', 'test', 'test')
        mock_conn = MagicMock()
        mock_conn.is_connected.return_value = True
        mock_connect.return_value = mock_conn
        self.db.connection = mock_conn
    
    def test_obtener_todos_duenos(self):
        """Test de obtener todos los dueños."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {'id_dueño': 1, 'nombre': 'Test'}
        ]
        self.db.connection.cursor.return_value = mock_cursor
        
        result = self.db.obtener_todos_duenos()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['nombre'], 'Test')


if __name__ == '__main__':
    unittest.main()
