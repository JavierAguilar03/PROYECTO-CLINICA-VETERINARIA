"""
Tests para las entidades del sistema.
"""
import unittest
from datetime import datetime, date
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.entidades.administrativo.cita import Cita
from src.entidades.administrativo.consulta import Consulta
from src.entidades.administrativo.factura import Factura


class TestCita(unittest.TestCase):
    """Tests para la clase Cita."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.cita = Cita(1, "2025-01-15", "10:30", "Revisión general", 1, 1)
    
    def test_init(self):
        """Test de inicialización."""
        self.assertEqual(self.cita.id_cita, 1)
        self.assertEqual(self.cita.motivo, "Revisión general")
        self.assertEqual(self.cita.estado, "pendiente")
    
    def test_cancelar(self):
        """Test de cancelación de cita."""
        self.cita.cancelar()
        self.assertEqual(self.cita.estado, "cancelada")
    
    def test_cancelar_completada_error(self):
        """Test que no se puede cancelar una cita completada."""
        self.cita.marcar_como_completada("11:00")
        with self.assertRaises(ValueError):
            self.cita.cancelar()
    
    def test_reprogramar(self):
        """Test de reprogramación de cita."""
        self.cita.reprogramar("2025-01-20", "14:00")
        self.assertEqual(self.cita.fecha, datetime.strptime("2025-01-20", "%Y-%m-%d").date())
    
    def test_estado_invalido(self):
        """Test con estado inválido."""
        with self.assertRaises(ValueError):
            Cita(2, "2025-01-15", "10:30", "Test", 1, 1, "invalido")


class TestConsulta(unittest.TestCase):
    """Tests para la clase Consulta."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.consulta = Consulta(1, 1, "Gastroenteritis", "Dieta blanda")
    
    def test_init(self):
        """Test de inicialización."""
        self.assertEqual(self.consulta.id_consulta, 1)
        self.assertEqual(self.consulta.diagnostico, "Gastroenteritis")
        self.assertIsNone(self.consulta.id_factura)
    
    def test_registrar_diagnostico(self):
        """Test de registro de diagnóstico."""
        self.consulta.registrar_diagnostico("Nuevo diagnóstico")
        self.assertEqual(self.consulta.diagnostico, "Nuevo diagnóstico")
    
    def test_diagnostico_vacio_error(self):
        """Test que no se puede registrar diagnóstico vacío."""
        with self.assertRaises(ValueError):
            self.consulta.registrar_diagnostico("")
    
    def test_agregar_observacion(self):
        """Test de agregar observación."""
        self.consulta.agregar_observacion("Paciente mejoró")
        self.assertIn("Paciente mejoró", self.consulta.observaciones)
    
    def test_vincular_factura(self):
        """Test de vinculación con factura."""
        self.consulta.vincular_factura(123)
        self.assertEqual(self.consulta.id_factura, 123)
    
    def test_vincular_factura_duplicada_error(self):
        """Test que no se puede vincular dos veces."""
        self.consulta.vincular_factura(123)
        with self.assertRaises(ValueError):
            self.consulta.vincular_factura(456)


class TestFactura(unittest.TestCase):
    """Tests para la clase Factura."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.factura = Factura(1, 1)
    
    def test_init(self):
        """Test de inicialización."""
        self.assertEqual(self.factura.id_factura, 1)
        self.assertEqual(self.factura.total, 0.0)
        self.assertIsNone(self.factura.metodo_pago)
    
    def test_calcular_total(self):
        """Test de cálculo de total."""
        servicios = [
            {'descripcion': 'Consulta', 'precio': 50.0},
            {'descripcion': 'Vacuna', 'precio': 30.0}
        ]
        self.factura.calcular_total(servicios, descuentos=10.0, impuestos=0.16)
        self.assertAlmostEqual(self.factura.total, 81.2, places=2)
    
    def test_registrar_pago(self):
        """Test de registro de pago."""
        self.factura.registrar_pago("efectivo")
        self.assertEqual(self.factura.metodo_pago, "efectivo")
        self.assertIsNotNone(self.factura.fecha)
    
    def test_metodo_pago_invalido(self):
        """Test con método de pago inválido."""
        with self.assertRaises(ValueError):
            self.factura.registrar_pago("criptomonedas")
    
    def test_mostrar_factura(self):
        """Test de mostrar factura."""
        servicios = [{'descripcion': 'Test', 'precio': 100.0}]
        self.factura.calcular_total(servicios)
        self.factura.registrar_pago("tarjeta")
        
        resumen = self.factura.mostrar_factura()
        self.assertIn("Factura ID: 1", resumen)
        self.assertIn("100.00", resumen)


if __name__ == '__main__':
    unittest.main()
