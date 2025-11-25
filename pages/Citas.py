import streamlit as st
import sys
import os
from datetime import datetime, date

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Citas - Clínica Veterinaria", page_icon="📅", layout="wide")

# Verificar autenticación
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

def init_db():
    """Inicializa la conexión a la base de datos."""
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    
    db = DatabaseConnection(host, user, password, database)
    return db

st.title("📅 Gestión de Citas")
st.markdown("---")

# Tabs para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["📋 Ver Citas", "➕ Nueva Cita", "🔍 Buscar"])

# TAB 1: Ver Citas
with tab1:
    st.subheader("Lista de Citas")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        filter_estado = st.selectbox(
            "Filtrar por estado:",
            ["Todas", "pendiente", "completada", "cancelada"]
        )
    
    try:
        db = init_db()
        if db.connect():
            if filter_estado == "Todas":
                query = """
                    SELECT c.*, m.nombre as mascota_nombre, e.nombre as empleado_nombre
                    FROM citas c
                    LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                    LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                    ORDER BY c.fecha DESC, c.hora DESC
                """
                citas = db.fetch_all(query)
            else:
                citas = db.obtener_citas_por_estado(filter_estado)
            
            db.disconnect()
            
            if citas:
                st.info(f"📊 Total de citas: {len(citas)}")
                
                for cita in citas:
                    with st.expander(f"🗓️ Cita #{cita['id_cita']} - {cita['fecha']} {cita['hora']} - {cita['estado'].upper()}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Mascota**: {cita.get('mascota_nombre', 'N/A')} (ID: {cita['id_mascota']})")
                            st.write(f"**Empleado**: {cita.get('empleado_nombre', 'N/A')} (ID: {cita['id_empleado']})")
                            st.write(f"**Motivo**: {cita['motivo']}")
                        
                        with col2:
                            st.write(f"**Estado**: {cita['estado']}")
                            st.write(f"**Fecha**: {cita['fecha']}")
                            st.write(f"**Hora**: {cita['hora']}")
                        
                        # Acciones (solo para empleados)
                        if st.session_state.user_type == "empleado":
                            col_btn1, col_btn2, col_btn3 = st.columns(3)
                            with col_btn1:
                                if st.button("✅ Completar", key=f"complete_{cita['id_cita']}"):
                                    db2 = init_db()
                                    if db2.connect():
                                        db2.actualizar_cita(cita['id_cita'], estado="completada")
                                        db2.disconnect()
                                        st.success("Cita completada")
                                        st.rerun()
                            
                            with col_btn2:
                                if st.button("❌ Cancelar", key=f"cancel_{cita['id_cita']}"):
                                    db2 = init_db()
                                    if db2.connect():
                                        db2.actualizar_cita(cita['id_cita'], estado="cancelada")
                                        db2.disconnect()
                                        st.success("Cita cancelada")
                                        st.rerun()
            else:
                st.warning("No hay citas registradas")
    
    except Exception as e:
        st.error(f"Error al cargar citas: {str(e)}")

# TAB 2: Nueva Cita
with tab2:
    st.subheader("Registrar Nueva Cita")
    
    with st.form("nueva_cita"):
        col1, col2 = st.columns(2)
        
        with col1:
            fecha = st.date_input("Fecha de la cita", min_value=date.today())
            hora = st.time_input("Hora de la cita")
            
            # Obtener mascotas
            try:
                db = init_db()
                if db.connect():
                    if st.session_state.user_type == "dueño":
                        # Solo mascotas del dueño
                        mascotas = db.obtener_mascotas_por_dueno(st.session_state.user_data['id_dueño'])
                    else:
                        # Todas las mascotas para empleados
                        mascotas = db.fetch_all("SELECT * FROM mascotas")
                    db.disconnect()
                    
                    if mascotas:
                        mascota_options = {f"{m['nombre']} (ID: {m['id_mascota']})": m['id_mascota'] for m in mascotas}
                        mascota_selected = st.selectbox("Mascota", list(mascota_options.keys()))
                        id_mascota = mascota_options[mascota_selected]
                    else:
                        st.warning("No hay mascotas registradas")
                        id_mascota = None
            except Exception as e:
                st.error(f"Error: {str(e)}")
                id_mascota = None
        
        with col2:
            motivo = st.text_area("Motivo de la cita", height=100)
            
            # Obtener empleados (solo para empleados)
            if st.session_state.user_type == "empleado":
                try:
                    db = init_db()
                    if db.connect():
                        empleados = db.obtener_todos_empleados()
                        db.disconnect()
                        
                        if empleados:
                            empleado_options = {f"{e['nombre']} - {e['tipo_empleado']}": e['id_empleado'] for e in empleados}
                            empleado_selected = st.selectbox("Empleado asignado", list(empleado_options.keys()))
                            id_empleado = empleado_options[empleado_selected]
                        else:
                            id_empleado = None
                except:
                    id_empleado = None
            else:
                # Para dueños, asignar empleado por defecto o dejar vacío
                id_empleado = st.number_input("ID Empleado (opcional)", min_value=1, value=1)
        
        submitted = st.form_submit_button("📅 Registrar Cita", use_container_width=True)
        
        if submitted:
            if id_mascota and motivo and id_empleado:
                try:
                    db = init_db()
                    if db.connect():
                        fecha_str = fecha.strftime("%Y-%m-%d")
                        hora_str = hora.strftime("%H:%M")
                        
                        id_cita = db.insertar_cita(fecha_str, hora_str, motivo, id_mascota, id_empleado)
                        db.disconnect()
                        
                        if id_cita:
                            st.success(f"✅ Cita registrada exitosamente (ID: {id_cita})")
                        else:
                            st.error("Error al registrar la cita")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Por favor complete todos los campos")

# TAB 3: Buscar
with tab3:
    st.subheader("Buscar Citas")
    
    buscar_por = st.radio("Buscar por:", ["ID Cita", "ID Mascota"], horizontal=True)
    
    if buscar_por == "ID Cita":
        id_buscar = st.number_input("ID de la cita", min_value=1, step=1)
        if st.button("🔍 Buscar"):
            try:
                db = init_db()
                if db.connect():
                    cita = db.obtener_cita(id_buscar)
                    db.disconnect()
                    
                    if cita:
                        st.success("Cita encontrada")
                        st.json(cita)
                    else:
                        st.warning("No se encontró la cita")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    else:  # ID Mascota
        id_mascota_buscar = st.number_input("ID de la mascota", min_value=1, step=1)
        if st.button("🔍 Buscar Citas"):
            try:
                db = init_db()
                if db.connect():
                    citas = db.obtener_citas_por_mascota(id_mascota_buscar)
                    db.disconnect()
                    
                    if citas:
                        st.success(f"Se encontraron {len(citas)} citas")
                        for cita in citas:
                            st.write(f"**Cita #{cita['id_cita']}** - {cita['fecha']} {cita['hora']} - {cita['estado']}")
                    else:
                        st.warning("No se encontraron citas para esta mascota")
            except Exception as e:
                st.error(f"Error: {str(e)}")
