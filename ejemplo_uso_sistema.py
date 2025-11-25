"""
Ejemplo de uso del sistema de clínica veterinaria
Este script demuestra cómo usar las entidades con persistencia SQL y logging
"""

from src.database_conn.db_conn import DatabaseConnection
from src.entidades.administrativo.cita import Cita
from src.entidades.administrativo.consulta import Consulta
from src.entidades.administrativo.factura import Factura
from src.entidades.mascotas.mascota import Mascota
from src.entidades.personas.duenos.dueno import Dueño
from src.logging.log_config import setup_logging
import os


def main():
    """Función principal de ejemplo"""
    
    # 1. Configurar logging
    print("=" * 60)
    print("1. CONFIGURANDO SISTEMA DE LOGGING")
    print("=" * 60)
    setup_logging()
    print("✓ Logging configurado. Ver logs en: logs/app.log\n")
    
    # 2. Conectar a la base de datos
    print("=" * 60)
    print("2. CONECTANDO A BASE DE DATOS")
    print("=" * 60)
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    
    db = DatabaseConnection(host, user, password, database)
    print(f"✓ Conectado a: {database}@{host}\n")
    
    # 3. Cargar un dueño existente
    print("=" * 60)
    print("3. CARGANDO DUEÑO DESDE BASE DE DATOS")
    print("=" * 60)
    dueno = Dueño.load(db, 1)
    if dueno:
        print(f"✓ Dueño cargado: {dueno.nombre}")
        print(f"  - ID: {dueno.id_dueño}")
        print(f"  - Email: {dueno.email}")
        print(f"  - Mascotas: {len(dueno.mascotas)}\n")
    else:
        print("⚠ No se encontró dueño con ID 1")
        print("  Ejecuta database_setup.sql primero\n")
        return
    
    # 4. Cargar una mascota existente
    print("=" * 60)
    print("4. CARGANDO MASCOTA DESDE BASE DE DATOS")
    print("=" * 60)
    mascota = Mascota.load(db, 1, dueno)
    if mascota:
        print(f"✓ Mascota cargada: {mascota.nombre}")
        print(f"  - Especie: {mascota.especie}")
        print(f"  - Edad: {mascota.calcular_edad()} años")
        print(f"  - Peso: {mascota.peso} kg\n")
        
        # Actualizar peso de la mascota
        print("  Actualizando peso de la mascota...")
        mascota.actualizar_peso(mascota.peso + 0.5)
        mascota.update(db)
        print(f"  ✓ Peso actualizado a: {mascota.peso} kg\n")
    
    # 5. Cargar una cita existente
    print("=" * 60)
    print("5. CARGANDO CITA DESDE BASE DE DATOS")
    print("=" * 60)
    cita = Cita.load(db, 1)
    if cita:
        print(f"✓ Cita cargada: ID {cita.id_cita}")
        print(f"  - Fecha: {cita.fecha}")
        print(f"  - Hora: {cita.hora}")
        print(f"  - Motivo: {cita.motivo}")
        print(f"  - Estado: {cita.estado}\n")
        
        # Si está pendiente, se puede reprogramar
        if cita.estado == "pendiente":
            print("  La cita está pendiente, se puede reprogramar")
            # cita.reprogramar('2024-02-01', '14:30')
            # cita.update(db)
            # print("  ✓ Cita reprogramada\n")
    
    # 6. Cargar una consulta existente
    print("=" * 60)
    print("6. CARGANDO CONSULTA DESDE BASE DE DATOS")
    print("=" * 60)
    consulta = Consulta.load(db, 1)
    if consulta:
        print(f"✓ Consulta cargada: ID {consulta.id_consulta}")
        print(f"  - Diagnóstico: {consulta.diagnostico}")
        print(f"  - Tratamiento: {consulta.tratamiento}")
        print(f"  - Factura vinculada: {consulta.id_factura or 'No'}\n")
        
        # Añadir observaciones
        print("  Añadiendo observación a la consulta...")
        consulta.agregar_observacion("Mascota responde bien al tratamiento")
        consulta.update(db)
        print("  ✓ Observación añadida\n")
    
    # 7. Cargar una factura existente
    print("=" * 60)
    print("7. CARGANDO FACTURA DESDE BASE DE DATOS")
    print("=" * 60)
    factura = Factura.load(db, 1)
    if factura:
        print(f"✓ Factura cargada: ID {factura.id_factura}")
        print(f"  - Total: {factura.total:.2f} €")
        print(f"  - Método de pago: {factura.metodo_pago or 'No registrado'}")
        print(f"  - Fecha: {factura.fecha or 'No registrada'}\n")
        
        # Ejemplo de generar PDF (comentado para no generar archivos)
        print("  Ejemplo de generación de PDF:")
        print("  >>> factura.generar_pdf()")
        print("  >>> # Genera: facturas/factura_1.pdf\n")
        
        # Ejemplo de enviar por email (comentado, requiere credenciales)
        print("  Ejemplo de envío por email:")
        print("  >>> factura.enviar_por_email(")
        print("  ...     email_cliente='cliente@email.com',")
        print("  ...     email_remitente='clinica@veterinaria.com',")
        print("  ...     password_remitente='contraseña_app'")
        print("  ... )\n")
    
    # 8. Ejemplo de crear una nueva cita
    print("=" * 60)
    print("8. EJEMPLO: CREAR NUEVA CITA")
    print("=" * 60)
    print("  >>> nueva_cita = Cita(")
    print("  ...     id_cita=999,")
    print("  ...     fecha='2024-02-15',")
    print("  ...     hora='10:00',")
    print("  ...     motivo='Revisión anual',")
    print("  ...     id_mascota=1,")
    print("  ...     id_empleado=1")
    print("  ... )")
    print("  >>> nueva_cita.save(db)  # Guarda en base de datos")
    print("  >>> # Logging: INFO - Cita 999 guardada en base de datos\n")
    
    # 9. Resumen de logging
    print("=" * 60)
    print("9. SISTEMA DE LOGGING")
    print("=" * 60)
    print("  Todas las operaciones se registran en:")
    print("  - Consola: Mensajes WARNING y superiores")
    print("  - Archivo: logs/app.log (todos los niveles)")
    print("\n  Niveles de logging:")
    print("  - DEBUG: Detalles de cálculos y operaciones")
    print("  - INFO: Operaciones exitosas (save, update, delete)")
    print("  - WARNING: Operaciones inusuales (cita ya existe)")
    print("  - ERROR: Errores controlados (validaciones fallidas)")
    print("\n  Ejemplo de log:")
    print("  2024-01-15 10:30:45 - entidades.mascota - INFO - Peso de mascota Max (ID: 1) actualizado: 12.5kg -> 13.0kg\n")
    
    # 10. Cerrar conexión
    print("=" * 60)
    print("10. CERRANDO CONEXIÓN")
    print("=" * 60)
    db.cerrar_conexion()
    print("✓ Conexión cerrada correctamente\n")
    
    print("=" * 60)
    print("DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)
    print("Revisa el archivo logs/app.log para ver todos los logs generados")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de haber ejecutado database_setup.sql primero")
        import traceback
        traceback.print_exc()
