from typing import Optional, List, Dict, Any


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

    # ------------------------------
    # Métodos estáticos de acceso a datos
    # ------------------------------

    @staticmethod
    def crear(db, id_consulta: int, total: float, metodo_pago: str = None,
              fecha: str = None) -> Optional[int]:
        """Crea una nueva factura en la base de datos y retorna su ID."""
        if metodo_pago and metodo_pago.lower() not in Factura.METODOS_PAGO_VALIDOS:
            raise ValueError(f"Método de pago inválido. Debe ser uno de {Factura.METODOS_PAGO_VALIDOS}.")
        return db.insertar_factura(id_consulta, total, metodo_pago, fecha)

    @staticmethod
    def obtener_por_id(db, id_factura: int) -> Optional[Dict[str, Any]]:
        """Obtiene una factura por su ID."""
        return db.obtener_factura(id_factura)

    @staticmethod
    def obtener_por_consulta(db, id_consulta: int) -> List[Dict[str, Any]]:
        """Obtiene todas las facturas de una consulta."""
        return db.obtener_facturas_por_consulta(id_consulta)

    @staticmethod
    def obtener_todas(db) -> List[Dict[str, Any]]:
        """Obtiene todas las facturas."""
        return db.fetch_all("SELECT * FROM facturas ORDER BY id_factura DESC")

    @staticmethod
    def actualizar(db, id_factura: int, total: float = None, metodo_pago: str = None) -> bool:
        """Actualiza una factura existente."""
        if metodo_pago and metodo_pago.lower() not in Factura.METODOS_PAGO_VALIDOS:
            raise ValueError(f"Método de pago inválido. Debe ser uno de {Factura.METODOS_PAGO_VALIDOS}.")
        return db.actualizar_factura(id_factura, total, metodo_pago)
