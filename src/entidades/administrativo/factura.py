from datetime import datetime
from typing import List, Optional


class Factura:
    """
    Clase Factura
    Propósito: Representar el comprobante de pago por los servicios prestados.

    Principio SOLID:
    - SRP (Responsabilidad Única): Gestiona únicamente la información contable de los servicios.
    """

    METODOS_PAGO_VALIDOS = ("efectivo", "tarjeta", "transferencia", "paypal")

    def __init__(self, id_factura: int, id_consulta: int):
        self.id_factura = id_factura
        self.id_consulta = id_consulta
        self.total: float = 0.0
        self.fecha: Optional[datetime] = None
        self.metodo_pago: Optional[str] = None
        self._detalle_servicios: List[dict] = []

    # ------------------------------
    # Métodos de gestión de la factura
    # ------------------------------

    def calcular_total(self, servicios: List[dict], descuentos: float = 0.0, impuestos: float = 0.0):
        """
        Calcula el total de la factura.
        Parámetros:
            - servicios: lista de diccionarios con {'descripcion': str, 'precio': float}
            - descuentos: monto total de descuentos
            - impuestos: porcentaje de impuestos (ej: 0.16 para 16%)
        """
        subtotal = sum(servicio['precio'] for servicio in servicios)
        subtotal -= descuentos
        if subtotal < 0:
            subtotal = 0
        self.total = subtotal * (1 + impuestos)
        self._detalle_servicios = servicios

    def registrar_pago(self, metodo: str, fecha: Optional[str] = None):
        """Registra el método de pago y la fecha de la factura."""
        if metodo.lower() not in Factura.METODOS_PAGO_VALIDOS:
            raise ValueError(f"Método de pago inválido. Debe ser uno de {Factura.METODOS_PAGO_VALIDOS}.")
        self.metodo_pago = metodo.lower()
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d") if fecha else datetime.now()

    def generar_pdf(self, ruta: Optional[str] = None):
        """
        Placeholder para generar un PDF de la factura.
        `ruta` opcional para guardar el archivo.
        """
        # Aquí se integraría una librería tipo reportlab o fpdf
        print(f"PDF generado para Factura {self.id_factura}. (Simulado)")

    def mostrar_factura(self) -> str:
        """Devuelve un resumen legible de la factura."""
        detalle = "\n".join(
            f"- {s['descripcion']}: {s['precio']:.2f} €" for s in self._detalle_servicios
        )
        resumen = (
            f"Factura ID: {self.id_factura}\n"
            f"Consulta ID: {self.id_consulta}\n"
            f"Fecha: {self.fecha.strftime('%Y-%m-%d') if self.fecha else 'No registrada'}\n"
            f"Servicios:\n{detalle if detalle else 'Sin servicios'}\n"
            f"Total: {self.total:.2f} €\n"
            f"Método de pago: {self.metodo_pago or 'No registrado'}"
        )
        return resumen

    def enviar_por_email(self, email_cliente: str):
        """
        Placeholder para enviar la factura por email.
        Se puede integrar con librerías tipo smtplib o servicios externos.
        """
        print(f"Factura {self.id_factura} enviada a {email_cliente}. (Simulado)")

    # ------------------------------
    # Representación de texto
    # ------------------------------

    def __str__(self):
        return f"Factura {self.id_factura} - Total: {self.total:.2f} € - Método: {self.metodo_pago or 'No registrado'}"
