from typing import Optional


class Factura:
    """
    Clase Factura
    Propósito: Representar el comprobante de pago por los servicios prestados.
    """

    METODOS_PAGO_VALIDOS = ("efectivo", "tarjeta", "transferencia", "paypal")

    def __init__(self, id_factura: int, id_consulta: int):
        self.id_factura = id_factura
        self.id_consulta = id_consulta
        self.total: float = 0.0
        self.fecha: Optional[str] = None
        self.metodo_pago: Optional[str] = None
