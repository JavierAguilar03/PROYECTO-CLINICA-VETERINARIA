import streamlit as st
import sys
import os
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Consultas", page_icon="🏥", layout="wide")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Control de acceso por rol
if st.session_state.user_type != "empleado":
    st.error("🚫 Acceso restringido. Solo empleados.")
    st.stop()

user_role = st.session_state.user_data.get('tipo_empleado', '').lower()

# Solo veterinarios, enfermeros y recepcionistas tienen acceso a consultas
if user_role not in ['veterinario', 'enfermero', 'recepcionista']:
    st.error("🚫 Acceso restringido. Los conserjes solo pueden acceder a la sección de Empleados.")
    st.stop()

def init_db():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    return DatabaseConnection(host, user, password, database)

st.title("🏥 Gestión de Consultas")
st.markdown("---")

tab1, tab2 = st.tabs(["📋 Ver Consultas", "➕ Nueva Consulta"])

with tab1:
    st.subheader("Lista de Consultas")
    try:
        db = init_db()
        if db.connect():
            # Filtrar según rol
            if user_role == 'veterinario':
                # Veterinarios solo ven consultas de sus citas
                id_empleado = st.session_state.user_data['id_empleado']
                query = """
                    SELECT co.* FROM consultas co
                    INNER JOIN citas ci ON co.id_cita = ci.id_cita
                    WHERE ci.id_empleado = %s
                    ORDER BY co.id_consulta DESC
                """
                consultas = db.fetch_all(query, (id_empleado,))
            elif user_role in ['enfermero', 'recepcionista']:
                # Enfermeros y recepcionistas ven todas las consultas
                consultas = db.fetch_all("SELECT * FROM consultas ORDER BY id_consulta DESC")
            else:
                consultas = []
            db.disconnect()
            
            if consultas:
                for consulta in consultas:
                    # Obtener factura asociada
                    db2 = init_db()
                    factura = None
                    if db2.connect():
                        facturas = db2.obtener_facturas_por_consulta(consulta['id_consulta'])
                        if facturas:
                            factura = facturas[0]
                        db2.disconnect()
                    
                    with st.expander(f"📋 Consulta #{consulta['id_consulta']} - Cita #{consulta['id_cita']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Diagnóstico**: {consulta.get('diagnostico', 'N/A')}")
                            st.write(f"**Tratamiento**: {consulta.get('tratamiento', 'N/A')}")
                            st.write(f"**Observaciones**: {consulta.get('observaciones', 'N/A')}")
                        with col2:
                            if factura:
                                st.write(f"**💰 Factura ID**: {factura['id_factura']}")
                                st.write(f"**💵 Total**: {factura['total']}€")
                                st.write(f"**💳 Método**: {factura.get('metodo_pago', 'N/A')}")
                                st.write(f"**📅 Fecha**: {factura.get('fecha', 'N/A')}")
                            else:
                                st.warning("⚠️ Sin factura asociada")
            else:
                st.warning("No hay consultas registradas")
    except Exception as e:
        st.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Registrar Nueva Consulta")
    
    # Solo veterinarios pueden registrar consultas
    if user_role != 'veterinario':
        st.warning("⚠️ Solo veterinarios pueden registrar consultas médicas.")
    else:
        # Verificar si hay una cita para completar
        if 'cita_a_completar' in st.session_state:
            cita_info = st.session_state.cita_a_completar
            st.info(f"""📋 **Completando Cita #{cita_info['id_cita']}**
            
            - **Mascota:** {cita_info['mascota']}
            - **Empleado:** {cita_info['empleado']}
            - **Motivo:** {cita_info['motivo']}
            - **Fecha:** {cita_info['fecha']} {cita_info['hora']}
            """)
            
            with st.form("nueva_consulta_desde_cita"):
                id_cita = cita_info['id_cita']
                st.write(f"**ID de la Cita:** {id_cita}")
                
                diagnostico = st.text_area("Diagnóstico*", height=120, placeholder="Describa el diagnóstico de la consulta...")
                tratamiento = st.text_area("Tratamiento*", height=120, placeholder="Describa el tratamiento recomendado...")
                observaciones = st.text_area("Observaciones", height=80, placeholder="Observaciones adicionales (opcional)")
                
                st.markdown("---")
                st.subheader("💰 Información de Factura")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    total_factura = st.number_input("Total a Cobrar (€)*", min_value=0.0, step=5.0, value=50.0)
                with col_f2:
                    metodo_pago = st.selectbox("Método de Pago*", ["efectivo", "tarjeta", "transferencia", "paypal"])
                
                if st.form_submit_button("🏥 Completar Cita y Registrar Consulta", use_container_width=True):
                    if diagnostico and tratamiento and total_factura > 0:
                        try:
                            db = init_db()
                            if db.connect():
                                # 1. Actualizar estado de la cita a completada
                                db.actualizar_cita(id_cita, estado="completada")
                                
                                # 2. Registrar la consulta
                                id_consulta = db.insertar_consulta(id_cita, diagnostico, tratamiento, observaciones)
                                
                                if id_consulta:
                                    # 3. Generar factura automáticamente
                                    fecha_hoy = date.today().strftime("%Y-%m-%d")
                                    id_factura = db.insertar_factura(id_consulta, total_factura, metodo_pago, fecha_hoy)
                                    
                                    db.disconnect()
                                    
                                    if id_factura:
                                        st.success(f"""✅ **CONSULTA Y FACTURA REGISTRADAS EXITOSAMENTE**
                                        
                                        - **Consulta ID:** {id_consulta}
                                        - **Factura ID:** {id_factura}
                                        - **Total:** {total_factura}€
                                        - **Método de Pago:** {metodo_pago}
                                        """)
                                        st.balloons()
                                        
                                        # Limpiar session_state
                                        del st.session_state.cita_a_completar
                                        st.rerun()
                                    else:
                                        st.error("⚠️ Consulta registrada pero error al generar factura")
                                else:
                                    st.error("Error al registrar la consulta")
                                    db.disconnect()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("⚠️ Complete los campos obligatorios y asegúrese de que el total sea mayor a 0")
        else:
            # Formulario normal para crear consulta manualmente
            with st.form("nueva_consulta"):
                id_cita = st.number_input("ID de la Cita*", min_value=1, step=1)
                diagnostico = st.text_area("Diagnóstico*", height=100)
                tratamiento = st.text_area("Tratamiento*", height=100)
                observaciones = st.text_area("Observaciones", height=80)
                
                st.markdown("---")
                st.subheader("💰 Información de Factura")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    total_factura = st.number_input("Total a Cobrar (€)*", min_value=0.0, step=5.0, value=50.0)
                with col_f2:
                    metodo_pago = st.selectbox("Método de Pago*", ["efectivo", "tarjeta", "transferencia", "paypal"])
                
                if st.form_submit_button("🏥 Registrar Consulta y Factura", use_container_width=True):
                    if id_cita and diagnostico and tratamiento and total_factura > 0:
                        try:
                            db = init_db()
                            if db.connect():
                                # Verificar que la cita exista y esté completada
                                cita = db.obtener_cita(id_cita)
                                if not cita:
                                    st.error("⚠️ La cita especificada no existe")
                                elif cita['estado'].lower() != 'completada':
                                    st.warning("⚠️ La cita debe estar marcada como completada primero")
                                else:
                                    # Registrar la consulta
                                    id_consulta = db.insertar_consulta(id_cita, diagnostico, tratamiento, observaciones)
                                    
                                    if id_consulta:
                                        # Generar factura automáticamente
                                        fecha_hoy = date.today().strftime("%Y-%m-%d")
                                        id_factura = db.insertar_factura(id_consulta, total_factura, metodo_pago, fecha_hoy)
                                        
                                        if id_factura:
                                            st.success(f"""✅ **CONSULTA Y FACTURA REGISTRADAS**
                                            
                                            - **Consulta ID:** {id_consulta}
                                            - **Factura ID:** {id_factura}
                                            - **Total:** {total_factura}€
                                            """)
                                        else:
                                            st.error("⚠️ Consulta registrada pero error al generar factura")
                                    else:
                                        st.error("Error al registrar la consulta")
                                db.disconnect()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("⚠️ Complete los campos obligatorios y asegúrese de que el total sea mayor a 0")
