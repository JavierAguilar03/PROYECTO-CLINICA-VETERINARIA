import pytest
import logging
from unittest.mock import MagicMock
from src.entidades.personas.empleados.empleado import Empleado

# Configurar logger para tests
logger = logging.getLogger('test.empleado')

class TestEmpleado:
    """Tests para la clase Empleado y sus métodos de backend."""

    def test_crear_empleado(self):
        """Test crear un nuevo empleado."""
        logger.info("Ejecutando test: test_crear_empleado")
        db_mock = MagicMock()
        db_mock.insertar_empleado.return_value = 1
        
        id_empleado = Empleado.crear(
            db_mock,
            nombre="Dr. Carlos Ruiz",
            dni="11223344C",
            telefono="600111222",
            email="carlos@veterinaria.com",
            fecha_nacimiento="1980-04-10",
            salario=2500.0,
            tipo_empleado="Veterinario"
        )
        
        assert id_empleado == 1
        db_mock.insertar_empleado.assert_called_once_with(
            "Dr. Carlos Ruiz", "11223344C", "600111222", "carlos@veterinaria.com",
            "1980-04-10", 2500.0, "Veterinario", None, None
        )
        logger.info("Test test_crear_empleado: PASSED")

    def test_crear_empleado_con_credenciales(self):
        """Test crear empleado con usuario y contraseña."""
        db_mock = MagicMock()
        db_mock.insertar_empleado.return_value = 2
        
        id_empleado = Empleado.crear(
            db_mock,
            nombre="Ana Martínez",
            dni="55667788D",
            telefono="600333444",
            email="ana@veterinaria.com",
            fecha_nacimiento="1992-08-25",
            salario=1800.0,
            tipo_empleado="Recepcionista",
            usuario="ana_m",
            contraseña="secure123"
        )
        
        assert id_empleado == 2
        db_mock.insertar_empleado.assert_called_once_with(
            "Ana Martínez", "55667788D", "600333444", "ana@veterinaria.com",
            "1992-08-25", 1800.0, "Recepcionista", "ana_m", "secure123"
        )

    def test_obtener_por_id(self):
        """Test obtener empleado por ID."""
        db_mock = MagicMock()
        db_mock.obtener_empleado.return_value = {
            'id_empleado': 1,
            'nombre': 'Dr. Carlos Ruiz',
            'tipo_empleado': 'Veterinario',
            'salario': 2500.0
        }
        
        empleado = Empleado.obtener_por_id(db_mock, 1)
        
        assert empleado is not None
        assert empleado['id_empleado'] == 1
        assert empleado['tipo_empleado'] == 'Veterinario'
        db_mock.obtener_empleado.assert_called_once_with(1)

    def test_obtener_todos_sin_filtro(self):
        """Test obtener todos los empleados sin filtro."""
        db_mock = MagicMock()
        db_mock.obtener_todos_empleados.return_value = [
            {'id_empleado': 1, 'tipo_empleado': 'Veterinario'},
            {'id_empleado': 2, 'tipo_empleado': 'Recepcionista'},
            {'id_empleado': 3, 'tipo_empleado': 'Enfermero'}
        ]
        
        empleados = Empleado.obtener_todos(db_mock)
        
        assert len(empleados) == 3
        db_mock.obtener_todos_empleados.assert_called_once()

    def test_obtener_todos_filtrado_por_tipo(self):
        """Test obtener empleados filtrados por tipo."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_empleado': 1, 'tipo_empleado': 'Veterinario'},
            {'id_empleado': 4, 'tipo_empleado': 'Veterinario'}
        ]
        
        empleados = Empleado.obtener_todos(db_mock, tipo='Veterinario')
        
        assert len(empleados) == 2
        assert all(e['tipo_empleado'] == 'Veterinario' for e in empleados)
        db_mock.fetch_all.assert_called_once()

    def test_obtener_recepcionistas(self):
        """Test obtener solo recepcionistas."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_empleado': 2, 'tipo_empleado': 'Recepcionista'}
        ]
        
        recepcionistas = Empleado.obtener_todos(db_mock, tipo='Recepcionista')
        
        assert len(recepcionistas) == 1
        assert recepcionistas[0]['tipo_empleado'] == 'Recepcionista'

    def test_obtener_enfermeros(self):
        """Test obtener solo enfermeros."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_empleado': 3, 'tipo_empleado': 'Enfermero'},
            {'id_empleado': 5, 'tipo_empleado': 'Enfermero'}
        ]
        
        enfermeros = Empleado.obtener_todos(db_mock, tipo='Enfermero')
        
        assert len(enfermeros) == 2

    def test_actualizar_empleado(self):
        """Test actualizar empleado."""
        db_mock = MagicMock()
        db_mock.actualizar_empleado.return_value = True
        
        resultado = Empleado.actualizar(
            db_mock,
            id_empleado=1,
            telefono="600555666",
            email="nuevo@email.com"
        )
        
        assert resultado is True
        db_mock.actualizar_empleado.assert_called_once_with(
            1, "600555666", "nuevo@email.com", None, None, None
        )

    def test_actualizar_salario(self):
        """Test actualizar salario de empleado."""
        db_mock = MagicMock()
        db_mock.actualizar_empleado.return_value = True
        
        resultado = Empleado.actualizar(
            db_mock,
            id_empleado=2,
            salario=2000.0
        )
        
        assert resultado is True
        db_mock.actualizar_empleado.assert_called_once_with(
            2, None, None, 2000.0, None, None
        )

    def test_actualizar_credenciales(self):
        """Test actualizar usuario y contraseña."""
        db_mock = MagicMock()
        db_mock.actualizar_empleado.return_value = True
        
        resultado = Empleado.actualizar(
            db_mock,
            id_empleado=3,
            usuario="nuevo_usuario",
            contraseña="nueva_password"
        )
        
        assert resultado is True
        db_mock.actualizar_empleado.assert_called_once_with(
            3, None, None, None, "nuevo_usuario", "nueva_password"
        )

    def test_eliminar(self):
        """Test eliminar empleado."""
        db_mock = MagicMock()
        db_mock.eliminar_empleado.return_value = True
        
        resultado = Empleado.eliminar(db_mock, 1)
        
        assert resultado is True
        db_mock.eliminar_empleado.assert_called_once_with(1)

    def test_obtener_por_id_no_existe(self):
        """Test obtener empleado que no existe."""
        db_mock = MagicMock()
        db_mock.obtener_empleado.return_value = None
        
        empleado = Empleado.obtener_por_id(db_mock, 999)
        
        assert empleado is None
