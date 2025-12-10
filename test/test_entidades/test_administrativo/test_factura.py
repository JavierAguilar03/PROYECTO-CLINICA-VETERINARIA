import pytest
from unittest.mock import MagicMock
from src.entidades.administrativo.factura import Factura


class TestFactura:
    """Tests para la clase Factura y sus métodos de backend."""

    def test_crear_factura(self):
        """Test crear una nueva factura."""
        db_mock = MagicMock()
        db_mock.insertar_factura.return_value = 1
        
        id_factura = Factura.crear(
            db_mock,
            id_consulta=1,
            total=150.50,
            metodo_pago="tarjeta",
            fecha="2025-12-10"
        )
        
        assert id_factura == 1
        db_mock.insertar_factura.assert_called_once_with(
            1, 150.50, "tarjeta", "2025-12-10"
        )

    def test_crear_factura_metodo_invalido(self):
        """Test crear factura con método de pago inválido."""
        db_mock = MagicMock()
        
        with pytest.raises(ValueError, match="Método de pago inválido"):
            Factura.crear(
                db_mock,
                id_consulta=1,
                total=100.0,
                metodo_pago="criptomoneda"
            )

    def test_crear_factura_sin_metodo_pago(self):
        """Test crear factura sin especificar método de pago."""
        db_mock = MagicMock()
        db_mock.insertar_factura.return_value = 2
        
        id_factura = Factura.crear(
            db_mock,
            id_consulta=2,
            total=75.0
        )
        
        assert id_factura == 2
        db_mock.insertar_factura.assert_called_once_with(2, 75.0, None, None)

    def test_obtener_por_id(self):
        """Test obtener factura por ID."""
        db_mock = MagicMock()
        db_mock.obtener_factura.return_value = {
            'id_factura': 1,
            'id_consulta': 1,
            'total': 150.50,
            'metodo_pago': 'tarjeta'
        }
        
        factura = Factura.obtener_por_id(db_mock, 1)
        
        assert factura is not None
        assert factura['id_factura'] == 1
        assert factura['total'] == 150.50
        db_mock.obtener_factura.assert_called_once_with(1)

    def test_obtener_por_consulta(self):
        """Test obtener facturas por consulta."""
        db_mock = MagicMock()
        db_mock.obtener_facturas_por_consulta.return_value = [
            {'id_factura': 1, 'id_consulta': 5, 'total': 100.0},
            {'id_factura': 2, 'id_consulta': 5, 'total': 50.0}
        ]
        
        facturas = Factura.obtener_por_consulta(db_mock, 5)
        
        assert len(facturas) == 2
        assert facturas[0]['id_consulta'] == 5
        db_mock.obtener_facturas_por_consulta.assert_called_once_with(5)

    def test_obtener_todas(self):
        """Test obtener todas las facturas."""
        db_mock = MagicMock()
        db_mock.fetch_all.return_value = [
            {'id_factura': 1, 'total': 100.0},
            {'id_factura': 2, 'total': 200.0},
            {'id_factura': 3, 'total': 150.0}
        ]
        
        facturas = Factura.obtener_todas(db_mock)
        
        assert len(facturas) == 3
        db_mock.fetch_all.assert_called_once()

    def test_actualizar(self):
        """Test actualizar factura."""
        db_mock = MagicMock()
        db_mock.actualizar_factura.return_value = True
        
        resultado = Factura.actualizar(
            db_mock,
            id_factura=1,
            total=200.0,
            metodo_pago="efectivo"
        )
        
        assert resultado is True
        db_mock.actualizar_factura.assert_called_once_with(1, 200.0, "efectivo")

    def test_actualizar_metodo_invalido(self):
        """Test actualizar con método de pago inválido."""
        db_mock = MagicMock()
        
        with pytest.raises(ValueError, match="Método de pago inválido"):
            Factura.actualizar(
                db_mock,
                id_factura=1,
                metodo_pago="bitcoin"
            )

    def test_metodos_pago_validos(self):
        """Test verificar métodos de pago válidos."""
        assert "efectivo" in Factura.METODOS_PAGO_VALIDOS
        assert "tarjeta" in Factura.METODOS_PAGO_VALIDOS
        assert "transferencia" in Factura.METODOS_PAGO_VALIDOS
        assert "paypal" in Factura.METODOS_PAGO_VALIDOS
