import pytest
import logging
from unittest.mock import MagicMock
from src.entidades.administrativo.consulta import Consulta

# Configurar logger para tests
logger = logging.getLogger('test.consulta')

class TestConsulta:
    """Tests para la clase Consulta y sus métodos de backend."""

    def test_crear_consulta(self):
        """Test crear una nueva consulta."""
        logger.info("Ejecutando test: test_crear_consulta")
        db_mock = MagicMock()
        db_mock.insertar_consulta.return_value = 1
        
        id_consulta = Consulta.crear(
            db_mock,
            id_cita=1,
            diagnostico="Infección leve",
            tratamiento="Antibióticos",
            observaciones="Control en 7 días"
        )
        
        assert id_consulta == 1
        db_mock.insertar_consulta.assert_called_once_with(
            1, "Infección leve", "Antibióticos", "Control en 7 días"
        )
        logger.info("Test test_crear_consulta: PASSED")

    def test_crear_consulta_sin_observaciones(self):
        """Test crear consulta sin observaciones opcionales."""
        db_mock = MagicMock()
        db_mock.insertar_consulta.return_value = 2
        
        id_consulta = Consulta.crear(
            db_mock,
            id_cita=2,
            diagnostico="Revisión general",
            tratamiento="Sin tratamiento"
        )
        
        assert id_consulta == 2
        db_mock.insertar_consulta.assert_called_once_with(
            2, "Revisión general", "Sin tratamiento", None
        )

    def test_obtener_por_id(self):
        """Test obtener consulta por ID."""
        db_mock = MagicMock()
        db_mock.obtener_consulta.return_value = {
            'id_consulta': 1,
            'id_cita': 1,
            'diagnostico': 'Infección',
            'tratamiento': 'Antibióticos'
        }
        
        consulta = Consulta.obtener_por_id(db_mock, 1)
        
        assert consulta is not None
        assert consulta['id_consulta'] == 1
        assert consulta['diagnostico'] == 'Infección'
        db_mock.obtener_consulta.assert_called_once_with(1)

    def test_obtener_por_cita(self):
        """Test obtener consultas por ID de cita (retorna lista)."""
        db_mock = MagicMock()
        db_mock.obtener_consultas_por_cita.return_value = [
            {
                'id_consulta': 1,
                'id_cita': 5,
                'diagnostico': 'Sano',
                'tratamiento': 'Vitaminas'
            }
        ]
        
        consultas = Consulta.obtener_por_cita(db_mock, 5)
        
        assert len(consultas) == 1
        assert consultas[0]['id_cita'] == 5
        assert consultas[0]['id_consulta'] == 1
        db_mock.obtener_consultas_por_cita.assert_called_once_with(5)

    def test_actualizar(self):
        """Test actualizar consulta."""
        db_mock = MagicMock()
        db_mock.actualizar_consulta.return_value = True
        
        resultado = Consulta.actualizar(
            db_mock,
            id_consulta=1,
            diagnostico="Actualizado",
            tratamiento="Nuevo tratamiento"
        )
        
        assert resultado is True
        db_mock.actualizar_consulta.assert_called_once_with(
            1, "Actualizado", "Nuevo tratamiento", None
        )

    def test_actualizar_con_observaciones(self):
        """Test actualizar consulta incluyendo observaciones."""
        db_mock = MagicMock()
        db_mock.actualizar_consulta.return_value = True
        
        resultado = Consulta.actualizar(
            db_mock,
            id_consulta=2,
            diagnostico="Diagnóstico actualizado",
            tratamiento="Tratamiento actualizado",
            observaciones="Observaciones actualizadas"
        )
        
        assert resultado is True
        db_mock.actualizar_consulta.assert_called_once_with(
            2, "Diagnóstico actualizado", "Tratamiento actualizado", "Observaciones actualizadas"
        )

    def test_obtener_por_id_no_existe(self):
        """Test obtener consulta que no existe."""
        db_mock = MagicMock()
        db_mock.obtener_consulta.return_value = None
        
        consulta = Consulta.obtener_por_id(db_mock, 999)
        
        assert consulta is None
        db_mock.obtener_consulta.assert_called_once_with(999)
