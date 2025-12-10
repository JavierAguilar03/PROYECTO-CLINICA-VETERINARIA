from typing import Optional, List, Dict, Any
import logging

# Configurar logger
logger = logging.getLogger('entidades.factura')

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
            logger.warning(f"Intento de crear factura con método de pago inválido: {metodo_pago}")
            raise ValueError(f"Método de pago inválido. Debe ser uno de {Factura.METODOS_PAGO_VALIDOS}.")
        logger.info(f"Creando factura para consulta {id_consulta}: total={total}, método={metodo_pago}")
        try:
            id_factura = db.insertar_factura(id_consulta, total, metodo_pago, fecha)
            if id_factura:
                logger.info(f"Factura creada exitosamente con ID: {id_factura}")
            else:
                logger.error("Error al crear factura: no se obtuvo ID")
            return id_factura
        except Exception as e:
            logger.exception(f"Excepción al crear factura: {str(e)}")
            raise

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
            logger.warning(f"Intento de actualizar factura {id_factura} con método de pago inválido: {metodo_pago}")
            raise ValueError(f"Método de pago inválido. Debe ser uno de {Factura.METODOS_PAGO_VALIDOS}.")
        logger.info(f"Actualizando factura {id_factura}")
        try:
            resultado = db.actualizar_factura(id_factura, total, metodo_pago)
            if resultado:
                logger.info(f"Factura {id_factura} actualizada exitosamente")
            else:
                logger.error(f"Error al actualizar factura {id_factura}")
            return resultado
        except Exception as e:
            logger.exception(f"Excepción al actualizar factura {id_factura}: {str(e)}")
            raise
