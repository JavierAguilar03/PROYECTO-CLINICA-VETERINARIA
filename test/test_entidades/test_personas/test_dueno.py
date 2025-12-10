import pytest
import logging
from unittest.mock import MagicMock
from src.entidades.personas.duenos.dueno import Dueno

# Configurar logger para tests
logger = logging.getLogger('test.dueno')

class TestDueno:
    """Tests para la clase Dueno y sus métodos de backend."""

    def test_crear_dueno(self):
        """Test crear un nuevo dueño."""
        logger.info("Ejecutando test: test_crear_dueno")
        db_mock = MagicMock()
        db_mock.insertar_dueno.return_value = 1
        
        id_dueno = Dueno.crear(
            db_mock,
            nombre="Juan Pérez",
            dni="12345678A",
            telefono="600123456",
            email="juan@email.com",
            fecha_nacimiento="1985-03-20",
            direccion="Calle Mayor 1"
        )
        
        assert id_dueno == 1
        db_mock.insertar_dueno.assert_called_once_with(
            "Juan Pérez", "12345678A", "600123456", "juan@email.com",
            "1985-03-20", "Calle Mayor 1"
        )
        logger.info("Test test_crear_dueno: PASSED")

    def test_obtener_por_id(self):
        """Test obtener dueño por ID."""
        db_mock = MagicMock()
        db_mock.obtener_dueno.return_value = {
            'id_dueno': 1,
            'nombre': 'Juan Pérez',
            'dni': '12345678A',
            'email': 'juan@email.com'
        }
        
        dueno = Dueno.obtener_por_id(db_mock, 1)
        
        assert dueno is not None
        assert dueno['id_dueno'] == 1
        assert dueno['nombre'] == 'Juan Pérez'
        db_mock.obtener_dueno.assert_called_once_with(1)

    def test_obtener_todos(self):
        """Test obtener todos los dueños."""
        db_mock = MagicMock()
        db_mock.obtener_todos_duenos.return_value = [
            {'id_dueno': 1, 'nombre': 'Juan Pérez'},
            {'id_dueno': 2, 'nombre': 'María García'},
            {'id_dueno': 3, 'nombre': 'Carlos López'}
        ]
        
        duenos = Dueno.obtener_todos(db_mock)
        
        assert len(duenos) == 3
        db_mock.obtener_todos_duenos.assert_called_once()

    def test_buscar_con_query(self):
        """Test buscar dueño con query personalizada."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_dueno': 1, 'nombre': 'Juan Pérez', 'dni': '12345678A'}
        ]
        
        query = "SELECT * FROM duenos WHERE dni = %s"
        params = ("12345678A",)
        duenos = Dueno.buscar(db_mock, query, params)
        
        assert len(duenos) == 1
        assert duenos[0]['dni'] == '12345678A'
        db_mock.fetch_all.assert_called_once_with(query, params)

    def test_buscar_sin_params(self):
        """Test buscar sin parámetros."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_dueno': 1, 'nombre': 'Juan Pérez'},
            {'id_dueno': 2, 'nombre': 'María García'}
        ]
        
        query = "SELECT * FROM duenos"
        duenos = Dueno.buscar(db_mock, query)
        
        assert len(duenos) == 2
        db_mock.fetch_all.assert_called_once_with(query, None)

    def test_actualizar_telefono_y_email(self):
        """Test actualizar teléfono y email del dueño."""
        db_mock = MagicMock()
        db_mock.actualizar_dueno.return_value = True
        
        resultado = Dueno.actualizar(
            db_mock,
            id_dueno=1,
            telefono="600999888",
            email="nuevo@email.com"
        )
        
        assert resultado is True
        db_mock.actualizar_dueno.assert_called_once_with(
            1, None, "600999888", "nuevo@email.com", None
        )

    def test_actualizar_direccion(self):
        """Test actualizar dirección del dueño."""
        db_mock = MagicMock()
        db_mock.actualizar_dueno.return_value = True
        
        resultado = Dueno.actualizar(
            db_mock,
            id_dueno=2,
            direccion="Nueva Dirección 123"
        )
        
        assert resultado is True
        db_mock.actualizar_dueno.assert_called_once_with(
            2, None, None, None, "Nueva Dirección 123"
        )

    def test_actualizar_nombre(self):
        """Test actualizar nombre del dueño."""
        db_mock = MagicMock()
        db_mock.actualizar_dueno.return_value = True
        
        resultado = Dueno.actualizar(
            db_mock,
            id_dueno=3,
            nombre="Nombre Actualizado"
        )
        
        assert resultado is True
        db_mock.actualizar_dueno.assert_called_once_with(
            3, "Nombre Actualizado", None, None, None
        )

    def test_eliminar(self):
        """Test eliminar dueño."""
        db_mock = MagicMock()
        db_mock.eliminar_dueno.return_value = True
        
        resultado = Dueno.eliminar(db_mock, 1)
        
        assert resultado is True
        db_mock.eliminar_dueno.assert_called_once_with(1)

    def test_obtener_por_id_no_existe(self):
        """Test obtener dueño que no existe."""
        db_mock = MagicMock()
        db_mock.obtener_dueno.return_value = None
        
        dueno = Dueno.obtener_por_id(db_mock, 999)
        
        assert dueno is None
