import pytest
from unittest.mock import MagicMock, patch
from src.entidades.administrativo.cita import Cita


class TestCita:
    """Tests para la clase Cita y sus métodos de backend."""

    def test_crear_cita(self):
        """Test crear una nueva cita."""
        db_mock = MagicMock()
        db_mock.insertar_cita.return_value = 1
        
        id_cita = Cita.crear(
            db_mock,
            fecha="2025-12-15",
            hora="10:30",
            motivo="Vacunación",
            id_mascota=1,
            id_empleado=1,
            estado="pendiente"
        )
        
        assert id_cita == 1
        db_mock.insertar_cita.assert_called_once_with(
            "2025-12-15", "10:30", "Vacunación", 1, 1, "pendiente"
        )

    def test_crear_cita_estado_invalido(self):
        """Test crear cita con estado inválido no lanza excepción (validación en DB)."""
        db_mock = MagicMock()
        db_mock.insertar_cita.return_value = 2
        
        # La validación de estado no ocurre en crear(), solo en el constructor de instancia
        id_cita = Cita.crear(
            db_mock,
            fecha="2025-12-15",
            hora="10:30",
            motivo="Consulta",
            id_mascota=1,
            id_empleado=1,
            estado="otro_estado"
        )
        
        assert id_cita == 2

    def test_obtener_por_id(self):
        """Test obtener cita por ID."""
        db_mock = MagicMock()
        db_mock.obtener_cita.return_value = {
            'id_cita': 1,
            'fecha': '2025-12-15',
            'hora': '10:30',
            'motivo': 'Vacunación',
            'estado': 'pendiente'
        }
        
        cita = Cita.obtener_por_id(db_mock, 1)
        
        assert cita is not None
        assert cita['id_cita'] == 1
        assert cita['estado'] == 'pendiente'
        db_mock.obtener_cita.assert_called_once_with(1)

    def test_obtener_por_mascota(self):
        """Test obtener citas por mascota."""
        db_mock = MagicMock()
        db_mock.obtener_citas_por_mascota.return_value = [
            {'id_cita': 1, 'id_mascota': 1, 'fecha': '2025-12-15'},
            {'id_cita': 2, 'id_mascota': 1, 'fecha': '2025-12-20'}
        ]
        
        citas = Cita.obtener_por_mascota(db_mock, 1)
        
        assert len(citas) == 2
        assert citas[0]['id_cita'] == 1
        assert citas[1]['id_cita'] == 2
        db_mock.obtener_citas_por_mascota.assert_called_once_with(1)

    def test_obtener_por_estado(self):
        """Test obtener citas por estado."""
        db_mock = MagicMock()
        db_mock.obtener_citas_por_estado.return_value = [
            {'id_cita': 1, 'estado': 'pendiente'},
            {'id_cita': 2, 'estado': 'pendiente'}
        ]
        
        citas = Cita.obtener_por_estado(db_mock, 'pendiente')
        
        assert len(citas) == 2
        assert all(c['estado'] == 'pendiente' for c in citas)
        db_mock.obtener_citas_por_estado.assert_called_once_with('pendiente')

    def test_obtener_todas_filtradas_sin_filtros(self):
        """Test obtener todas las citas sin filtros."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_cita': 1, 'estado': 'pendiente'},
            {'id_cita': 2, 'estado': 'completada'}
        ]
        
        query = "SELECT * FROM citas"
        citas = Cita.obtener_todas_filtradas(db_mock, query)
        
        assert len(citas) == 2
        db_mock.fetch_all.assert_called_once_with(query, None)

    def test_obtener_todas_filtradas_con_estado(self):
        """Test obtener citas filtradas por estado."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_cita': 1, 'estado': 'completada'}
        ]
        
        query = "SELECT * FROM citas WHERE estado = %s"
        params = ('completada',)
        citas = Cita.obtener_todas_filtradas(db_mock, query, params)
        
        assert len(citas) == 1
        assert citas[0]['estado'] == 'completada'
        db_mock.fetch_all.assert_called_once_with(query, params)

    def test_actualizar_estado(self):
        """Test actualizar estado de cita."""
        db_mock = MagicMock()
        db_mock.actualizar_cita.return_value = True
        
        resultado = Cita.actualizar_estado(db_mock, 1, estado='completada')
        
        assert resultado is True
        db_mock.actualizar_cita.assert_called_once_with(1, estado='completada')

    def test_actualizar_estado_invalido(self):
        """Test actualizar con estado inválido lanza excepción."""
        db_mock = MagicMock()
        
        with pytest.raises(ValueError, match="Estado .* inválido"):
            Cita.actualizar_estado(db_mock, 1, estado='estado_invalido')

    def test_eliminar(self):
        """Test eliminar cita."""
        db_mock = MagicMock()
        db_mock.eliminar_cita.return_value = True
        
        resultado = Cita.eliminar(db_mock, 1)
        
        assert resultado is True
        db_mock.eliminar_cita.assert_called_once_with(1)
