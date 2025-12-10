import pytest
from unittest.mock import MagicMock
from src.entidades.mascotas.mascota import Mascota


class TestMascota:
    """Tests para la clase Mascota y sus métodos de backend."""

    def test_crear_mascota(self):
        """Test crear una nueva mascota."""
        db_mock = MagicMock()
        db_mock.insertar_mascota.return_value = 1
        
        id_mascota = Mascota.crear(
            db_mock,
            nombre="Max",
            especie="Perro",
            raza="Labrador",
            fecha_nacimiento="2020-05-15",
            peso=25.5,
            sexo="Macho",
            id_dueno=1
        )
        
        assert id_mascota == 1
        db_mock.insertar_mascota.assert_called_once_with(
            "Max", "Perro", "Labrador", "2020-05-15", 25.5, "Macho", 1
        )

    def test_obtener_por_id(self):
        """Test obtener mascota por ID."""
        db_mock = MagicMock()
        db_mock.obtener_mascota.return_value = {
            'id_mascota': 1,
            'nombre': 'Max',
            'especie': 'Perro',
            'raza': 'Labrador'
        }
        
        mascota = Mascota.obtener_por_id(db_mock, 1)
        
        assert mascota is not None
        assert mascota['id_mascota'] == 1
        assert mascota['nombre'] == 'Max'
        db_mock.obtener_mascota.assert_called_once_with(1)

    def test_obtener_por_dueno(self):
        """Test obtener mascotas por dueño."""
        db_mock = MagicMock()
        db_mock.obtener_mascotas_por_dueno.return_value = [
            {'id_mascota': 1, 'nombre': 'Max', 'id_dueno': 1},
            {'id_mascota': 2, 'nombre': 'Luna', 'id_dueno': 1}
        ]
        
        mascotas = Mascota.obtener_por_dueno(db_mock, 1)
        
        assert len(mascotas) == 2
        assert mascotas[0]['nombre'] == 'Max'
        assert mascotas[1]['nombre'] == 'Luna'
        db_mock.obtener_mascotas_por_dueno.assert_called_once_with(1)

    def test_obtener_todas(self):
        """Test obtener todas las mascotas."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_mascota': 1, 'nombre': 'Max'},
            {'id_mascota': 2, 'nombre': 'Luna'},
            {'id_mascota': 3, 'nombre': 'Rocky'}
        ]
        
        mascotas = Mascota.obtener_todas(db_mock)
        
        assert len(mascotas) == 3
        db_mock.fetch_all.assert_called_once()

    def test_actualizar(self):
        """Test actualizar mascota."""
        db_mock = MagicMock()
        db_mock.actualizar_mascota.return_value = True
        
        resultado = Mascota.actualizar(
            db_mock,
            id_mascota=1,
            peso=26.0,
            nombre="Max Jr"
        )
        
        assert resultado is True
        db_mock.actualizar_mascota.assert_called_once_with(1, 26.0, "Max Jr")

    def test_actualizar_multiple_campos(self):
        """Test actualizar múltiples campos de mascota."""
        db_mock = MagicMock()
        db_mock.actualizar_mascota.return_value = True
        
        resultado = Mascota.actualizar(
            db_mock,
            id_mascota=2,
            nombre="Max Jr",
            peso=27.5
        )
        
        assert resultado is True
        db_mock.actualizar_mascota.assert_called_once_with(2, 27.5, "Max Jr")

    def test_eliminar(self):
        """Test eliminar mascota."""
        db_mock = MagicMock()
        db_mock.eliminar_mascota.return_value = True
        
        resultado = Mascota.eliminar(db_mock, 1)
        
        assert resultado is True
        db_mock.eliminar_mascota.assert_called_once_with(1)

    def test_obtener_por_id_no_existe(self):
        """Test obtener mascota que no existe."""
        db_mock = MagicMock()
        db_mock.obtener_mascota.return_value = None
        
        mascota = Mascota.obtener_por_id(db_mock, 999)
        
        assert mascota is None

    def test_obtener_por_dueno_sin_mascotas(self):
        """Test obtener mascotas de dueño sin mascotas."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = []
        
        mascotas = Mascota.obtener_por_dueno(db_mock, 99)
        
        assert len(mascotas) == 0
