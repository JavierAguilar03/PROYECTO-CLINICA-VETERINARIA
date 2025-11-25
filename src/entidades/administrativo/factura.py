from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import logging

if TYPE_CHECKING:
    from src.entidades.administrativo.consulta import Consulta
    from src.entidades.administrativo.cita import Cita

# Configurar logger
logger = logging.getLogger('entidades.factura')


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
        logger.debug(f"Calculando total para Factura {self.id_factura} con {len(servicios)} servicios")
        subtotal = sum(servicio['precio'] for servicio in servicios)
        subtotal -= descuentos
        if subtotal < 0:
            logger.warning(f"Subtotal negativo detectado, ajustando a 0")
            subtotal = 0
        self.total = subtotal * (1 + impuestos)
        self._detalle_servicios = servicios
        logger.info(f"Total calculado para Factura {self.id_factura}: {self.total:.2f} €")

    def registrar_pago(self, metodo: str, fecha: Optional[str] = None):
        """Registra el método de pago y la fecha de la factura."""
        if metodo.lower() not in Factura.METODOS_PAGO_VALIDOS:
            raise ValueError(f"Método de pago inválido. Debe ser uno de {Factura.METODOS_PAGO_VALIDOS}.")
        self.metodo_pago = metodo.lower()
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d") if fecha else datetime.now()

    def generar_pdf(self, ruta: Optional[str] = None):
        """
        Genera un PDF de la factura usando reportlab.
        `ruta` opcional para guardar el archivo. Si no se especifica, se guarda en facturas/
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import inch
            
            # Definir ruta por defecto
            if not ruta:
                os.makedirs("facturas", exist_ok=True)
                ruta = f"facturas/factura_{self.id_factura}.pdf"
            
            # Crear el PDF
            c = canvas.Canvas(ruta, pagesize=letter)
            width, height = letter
            
            # Título
            c.setFont("Helvetica-Bold", 20)
            c.drawString(1 * inch, height - 1 * inch, "FACTURA")
            
            # Información de la factura
            c.setFont("Helvetica", 12)
            y_position = height - 1.5 * inch
            c.drawString(1 * inch, y_position, f"Factura ID: {self.id_factura}")
            y_position -= 0.3 * inch
            c.drawString(1 * inch, y_position, f"Consulta ID: {self.id_consulta}")
            y_position -= 0.3 * inch
            c.drawString(1 * inch, y_position, f"Fecha: {self.fecha.strftime('%Y-%m-%d') if self.fecha else 'No registrada'}")
            y_position -= 0.3 * inch
            c.drawString(1 * inch, y_position, f"Método de pago: {self.metodo_pago or 'No registrado'}")
            
            # Línea separadora
            y_position -= 0.5 * inch
            c.line(1 * inch, y_position, width - 1 * inch, y_position)
            
            # Servicios
            y_position -= 0.4 * inch
            c.setFont("Helvetica-Bold", 14)
            c.drawString(1 * inch, y_position, "Servicios:")
            
            c.setFont("Helvetica", 11)
            y_position -= 0.3 * inch
            for servicio in self._detalle_servicios:
                if y_position < 2 * inch:  # Nueva página si no hay espacio
                    c.showPage()
                    y_position = height - 1 * inch
                c.drawString(1.2 * inch, y_position, f"• {servicio['descripcion']}")
                c.drawString(width - 2.5 * inch, y_position, f"{servicio['precio']:.2f} €")
                y_position -= 0.25 * inch
            
            # Total
            y_position -= 0.3 * inch
            c.line(1 * inch, y_position, width - 1 * inch, y_position)
            y_position -= 0.4 * inch
            c.setFont("Helvetica-Bold", 14)
            c.drawString(1 * inch, y_position, "TOTAL:")
            c.drawString(width - 2.5 * inch, y_position, f"{self.total:.2f} €")
            
            # Finalizar
            c.save()
            print(f"PDF generado exitosamente: {ruta}")
            return ruta
            
        except ImportError:
            print("Error: reportlab no está instalado. Ejecute: pip install reportlab")
            return None
        except Exception as e:
            print(f"Error al generar PDF: {str(e)}")
            return None

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

    def enviar_por_email(self, email_cliente: str, smtp_server: str = "smtp.gmail.com",
                         smtp_port: int = 587, email_remitente: str = None,
                         password_remitente: str = None, adjuntar_pdf: bool = True):
        """
        Envía la factura por email usando smtplib.
        
        Parámetros:
            - email_cliente: email del destinatario
            - smtp_server: servidor SMTP (por defecto Gmail)
            - smtp_port: puerto SMTP
            - email_remitente: email del remitente (debe configurarse)
            - password_remitente: contraseña del remitente (debe configurarse)
            - adjuntar_pdf: si True, genera y adjunta el PDF
        
        Nota: Para Gmail, usar contraseña de aplicación, no la contraseña normal.
        """
        if not email_remitente or not password_remitente:
            print("Error: Debe proporcionar credenciales de email (email_remitente y password_remitente)")
            print("Para Gmail, use una contraseña de aplicación: https://support.google.com/accounts/answer/185833")
            return False
        
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = email_remitente
            msg['To'] = email_cliente
            msg['Subject'] = f"Factura #{self.id_factura} - Clínica Veterinaria"
            
            # Cuerpo del mensaje
            cuerpo = f"""
            Estimado cliente,
            
            Adjuntamos la factura #{self.id_factura} correspondiente a la consulta #{self.id_consulta}.
            
            Resumen:
            {self.mostrar_factura()}
            
            Gracias por confiar en nosotros.
            
            Saludos cordiales,
            Clínica Veterinaria
            """
            msg.attach(MIMEText(cuerpo, 'plain'))
            
            # Adjuntar PDF si se solicita
            if adjuntar_pdf:
                ruta_pdf = self.generar_pdf()
                if ruta_pdf and os.path.exists(ruta_pdf):
                    with open(ruta_pdf, 'rb') as f:
                        pdf_adjunto = MIMEApplication(f.read(), _subtype="pdf")
                        pdf_adjunto.add_header('Content-Disposition', 'attachment',
                                             filename=f'factura_{self.id_factura}.pdf')
                        msg.attach(pdf_adjunto)
            
            # Enviar email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_remitente, password_remitente)
                server.send_message(msg)
            
            print(f"Factura {self.id_factura} enviada exitosamente a {email_cliente}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Error de autenticación. Verifique las credenciales.")
            print("Para Gmail, use una contraseña de aplicación.")
            return False
        except Exception as e:
            print(f"Error al enviar email: {str(e)}")
            return False

    # ------------------------------
    # Métodos de persistencia SQL
    # ------------------------------

    def save(self, db):
        """Guarda la factura en la base de datos."""
        try:
            fecha_str = self.fecha.strftime('%Y-%m-%d') if self.fecha else None
            db.insertar_factura(self.id_factura, self.id_consulta, fecha_str, 
                              self.total, self.metodo_pago)
            logger.info(f"Factura {self.id_factura} guardada en base de datos")
        except Exception as e:
            logger.error(f"Error al guardar Factura {self.id_factura}: {e}")
            raise

    def update(self, db):
        """Actualiza la factura en la base de datos."""
        try:
            fecha_str = self.fecha.strftime('%Y-%m-%d') if self.fecha else None
            db.actualizar_factura(self.id_factura, fecha_str, self.total, self.metodo_pago)
            logger.info(f"Factura {self.id_factura} actualizada en base de datos")
        except Exception as e:
            logger.error(f"Error al actualizar Factura {self.id_factura}: {e}")
            raise

    def delete(self, db):
        """Elimina la factura de la base de datos."""
        try:
            db.eliminar_factura(self.id_factura)
            logger.info(f"Factura {self.id_factura} eliminada de base de datos")
        except Exception as e:
            logger.error(f"Error al eliminar Factura {self.id_factura}: {e}")
            raise

    @staticmethod
    def load(db, id_factura: int):
        """Carga una factura desde la base de datos."""
        try:
            factura_data = db.obtener_factura_por_id(id_factura)
            if factura_data:
                logger.info(f"Factura {id_factura} cargada desde base de datos")
                factura = Factura(
                    id_factura=factura_data['id_factura'],
                    id_consulta=factura_data['id_consulta']
                )
                factura.total = factura_data['total']
                factura.fecha = factura_data['fecha']
                factura.metodo_pago = factura_data['metodo_pago']
                return factura
            logger.warning(f"Factura {id_factura} no encontrada en base de datos")
            return None
        except Exception as e:
            logger.error(f"Error al cargar Factura {id_factura}: {e}")
            raise

    # ------------------------------
    # Representación de texto
    # ------------------------------

    def __str__(self):
        return f"Factura {self.id_factura} - Total: {self.total:.2f} € - Método: {self.metodo_pago or 'No registrado'}"
